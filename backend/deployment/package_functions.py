"""
Lambda function packager.

Packages individual Lambda functions with their code, shared modules,
and function-specific dependencies.
"""

import os
import shutil
import zipfile
from pathlib import Path
from typing import List, Optional
from dataclasses import dataclass


@dataclass
class FunctionArtifact:
    """Lambda function artifact information."""
    function_name: str
    zip_path: str
    uncompressed_size_mb: float
    compressed_size_mb: float
    includes_shared: bool
    needs_layer: bool


class LambdaFunctionPackager:
    """Packages Lambda functions for deployment."""
    
    # AWS Lambda deployment package size limits
    MAX_DIRECT_UPLOAD_SIZE_MB = 50
    MAX_UNCOMPRESSED_SIZE_MB = 250
    
    # Files/directories to exclude from packages
    EXCLUDE_PATTERNS = [
        "__pycache__",
        "*.pyc",
        "*.pyo",
        "*.pyd",
        ".pytest_cache",
        ".mypy_cache",
        ".hypothesis",
        "tests",
        "test_*.py",
        "*_test.py",
        ".git",
        ".gitignore",
        ".DS_Store",
        "*.md",
        "requirements-dev.txt",
    ]
    
    # Development dependencies to exclude
    DEV_DEPENDENCIES = [
        "pytest",
        "mypy",
        "black",
        "hypothesis",
        "flake8",
        "isort",
        "coverage",
    ]
    
    def __init__(self, workspace_dir: str = "backend"):
        """
        Initialize function packager.
        
        Args:
            workspace_dir: Root directory of the backend workspace
        """
        self.workspace_dir = Path(workspace_dir)
        self.lambda_functions_dir = self.workspace_dir / "lambda_functions"
        self.shared_dir = self.workspace_dir / "shared"
        self.dist_dir = self.workspace_dir / "dist"
        self.build_dir = self.workspace_dir / "function_build"
    
    def package_function(
        self,
        function_name: str,
        include_shared: bool = True
    ) -> FunctionArtifact:
        """
        Package a single Lambda function.
        
        Args:
            function_name: Name of the function file (without .py extension)
            include_shared: Whether to include shared modules
        
        Returns:
            FunctionArtifact with package information
        
        Raises:
            FileNotFoundError: If function file doesn't exist
            RuntimeError: If packaging fails
        """
        print(f"📦 Packaging function: {function_name}")
        
        # Validate function exists
        function_file = self.lambda_functions_dir / f"{function_name}.py"
        if not function_file.exists():
            raise FileNotFoundError(f"Function file not found: {function_file}")
        
        # Clean and create build directory
        self._prepare_build_directory()
        
        # Copy function code
        self._copy_function_code(function_name)
        
        # Copy shared modules if requested
        if include_shared:
            self._copy_shared_modules()
        
        # Create zip artifact
        zip_path = self._create_zip_artifact(function_name)
        
        # Calculate sizes
        artifact = self._calculate_sizes(function_name, zip_path, include_shared)
        
        # Clean up build directory
        shutil.rmtree(self.build_dir)
        
        print(f"  ✓ Packaged: {artifact.zip_path}")
        print(f"    Size: {artifact.compressed_size_mb:.2f} MB (compressed)")
        print(f"    Needs layer: {artifact.needs_layer}")
        
        return artifact
    
    def package_all_functions(
        self,
        include_shared: bool = True
    ) -> List[FunctionArtifact]:
        """
        Package all Lambda functions.
        
        Args:
            include_shared: Whether to include shared modules
        
        Returns:
            List of FunctionArtifacts
        """
        print("📦 Packaging all Lambda functions...\n")
        
        # Get all Python files in lambda_functions directory
        function_files = [
            f.stem for f in self.lambda_functions_dir.glob("*.py")
            if f.stem != "__init__"
        ]
        
        artifacts = []
        for function_name in function_files:
            try:
                artifact = self.package_function(function_name, include_shared)
                artifacts.append(artifact)
            except Exception as e:
                print(f"  ✗ Failed to package {function_name}: {e}")
        
        print(f"\n✓ Packaged {len(artifacts)} functions")
        return artifacts
    
    def _prepare_build_directory(self):
        """Prepare build directory."""
        if self.build_dir.exists():
            shutil.rmtree(self.build_dir)
        self.build_dir.mkdir(parents=True, exist_ok=True)
        
        # Create dist directory
        self.dist_dir.mkdir(parents=True, exist_ok=True)
    
    def _copy_function_code(self, function_name: str):
        """
        Copy function code to build directory.
        
        Args:
            function_name: Name of the function
        """
        function_file = self.lambda_functions_dir / f"{function_name}.py"
        dest_file = self.build_dir / f"{function_name}.py"
        shutil.copy2(function_file, dest_file)
        
        # Also copy __init__.py if it exists
        init_file = self.lambda_functions_dir / "__init__.py"
        if init_file.exists():
            shutil.copy2(init_file, self.build_dir / "__init__.py")
    
    def _copy_shared_modules(self):
        """Copy shared modules to build directory."""
        if not self.shared_dir.exists():
            return
        
        dest_shared_dir = self.build_dir / "shared"
        
        # Copy entire shared directory
        shutil.copytree(
            self.shared_dir,
            dest_shared_dir,
            ignore=self._get_ignore_function()
        )
    
    def _get_ignore_function(self):
        """
        Get ignore function for shutil.copytree.
        
        Returns:
            Ignore function that excludes unwanted files
        """
        def ignore_function(directory, files):
            ignored = []
            for file in files:
                # Check if file matches any exclude pattern
                if any(self._matches_pattern(file, pattern) for pattern in self.EXCLUDE_PATTERNS):
                    ignored.append(file)
                # Check if it's a dev dependency directory
                elif any(dev_dep in file.lower() for dev_dep in self.DEV_DEPENDENCIES):
                    ignored.append(file)
            return ignored
        
        return ignore_function
    
    def _matches_pattern(self, filename: str, pattern: str) -> bool:
        """
        Check if filename matches pattern.
        
        Args:
            filename: File name to check
            pattern: Pattern to match (supports * wildcard)
        
        Returns:
            True if matches, False otherwise
        """
        if pattern == filename:
            return True
        
        if "*" in pattern:
            if pattern.startswith("*"):
                return filename.endswith(pattern[1:])
            elif pattern.endswith("*"):
                return filename.startswith(pattern[:-1])
        
        return False
    
    def _create_zip_artifact(self, function_name: str) -> Path:
        """
        Create zip artifact from build directory.
        
        Args:
            function_name: Name of the function
        
        Returns:
            Path to created zip file
        """
        zip_path = self.dist_dir / f"{function_name}.zip"
        
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Walk through build directory and add all files
            for root, dirs, files in os.walk(self.build_dir):
                for file in files:
                    file_path = Path(root) / file
                    # Calculate archive name (relative to build_dir)
                    arcname = file_path.relative_to(self.build_dir)
                    zipf.write(file_path, arcname)
        
        return zip_path
    
    def _calculate_sizes(
        self,
        function_name: str,
        zip_path: Path,
        includes_shared: bool
    ) -> FunctionArtifact:
        """
        Calculate artifact sizes and determine if layer is needed.
        
        Args:
            function_name: Name of the function
            zip_path: Path to zip file
            includes_shared: Whether shared modules are included
        
        Returns:
            FunctionArtifact with size information
        """
        # Compressed size (zip file)
        compressed_size_bytes = zip_path.stat().st_size
        compressed_size_mb = compressed_size_bytes / (1024 * 1024)
        
        # Uncompressed size (all files in build directory)
        uncompressed_size_bytes = 0
        for root, dirs, files in os.walk(self.build_dir):
            for file in files:
                file_path = Path(root) / file
                uncompressed_size_bytes += file_path.stat().st_size
        uncompressed_size_mb = uncompressed_size_bytes / (1024 * 1024)
        
        # Determine if layer is needed
        needs_layer = uncompressed_size_mb > self.MAX_DIRECT_UPLOAD_SIZE_MB
        
        return FunctionArtifact(
            function_name=function_name,
            zip_path=str(zip_path),
            uncompressed_size_mb=uncompressed_size_mb,
            compressed_size_mb=compressed_size_mb,
            includes_shared=includes_shared,
            needs_layer=needs_layer
        )


def main():
    """Main entry point for function packager."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Package Lambda functions")
    parser.add_argument(
        "--function",
        help="Specific function to package (default: all functions)"
    )
    parser.add_argument(
        "--no-shared",
        action="store_true",
        help="Don't include shared modules"
    )
    parser.add_argument(
        "--workspace",
        default="backend",
        help="Backend workspace directory (default: backend)"
    )
    
    args = parser.parse_args()
    
    try:
        packager = LambdaFunctionPackager(workspace_dir=args.workspace)
        include_shared = not args.no_shared
        
        if args.function:
            artifact = packager.package_function(args.function, include_shared)
            print(f"\n✓ Function packaged: {artifact.zip_path}")
        else:
            artifacts = packager.package_all_functions(include_shared)
            print(f"\n✓ All functions packaged successfully")
            print(f"  Total artifacts: {len(artifacts)}")
            total_size = sum(a.compressed_size_mb for a in artifacts)
            print(f"  Total size: {total_size:.2f} MB")
    except Exception as e:
        print(f"\n✗ Packaging failed: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
