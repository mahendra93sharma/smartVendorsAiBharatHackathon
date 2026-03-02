"""
Lambda layer builder for shared dependencies.

Packages shared Python dependencies into a Lambda layer that can be
attached to multiple Lambda functions.
"""

import os
import shutil
import subprocess
import zipfile
from pathlib import Path
from typing import Optional
from dataclasses import dataclass


@dataclass
class LayerArtifact:
    """Lambda layer artifact information."""
    zip_path: str
    uncompressed_size_mb: float
    compressed_size_mb: float
    package_count: int


class LambdaLayerBuilder:
    """Builds Lambda layers from requirements files."""
    
    # AWS Lambda layer size limits
    MAX_UNCOMPRESSED_SIZE_MB = 250
    MAX_COMPRESSED_SIZE_MB = 50
    
    def __init__(self, workspace_dir: str = "backend"):
        """
        Initialize layer builder.
        
        Args:
            workspace_dir: Root directory of the backend workspace
        """
        self.workspace_dir = Path(workspace_dir)
        self.dist_dir = self.workspace_dir / "dist"
        self.layer_dir = self.workspace_dir / "layer_build"
    
    def build_layer(
        self,
        requirements_file: str = "layer_requirements.txt",
        output_name: str = "lambda_layer"
    ) -> LayerArtifact:
        """
        Build Lambda layer from requirements file.
        
        Args:
            requirements_file: Path to requirements file (relative to workspace)
            output_name: Name for the output zip file
        
        Returns:
            LayerArtifact with build information
        
        Raises:
            RuntimeError: If build fails or size limits are exceeded
        """
        print(f"🔨 Building Lambda layer from {requirements_file}...")
        
        # Clean and create directories
        self._prepare_directories()
        
        # Install dependencies
        requirements_path = self.workspace_dir / requirements_file
        if not requirements_path.exists():
            raise FileNotFoundError(f"Requirements file not found: {requirements_path}")
        
        self._install_dependencies(requirements_path)
        
        # Create zip artifact
        zip_path = self._create_zip_artifact(output_name)
        
        # Calculate sizes
        artifact = self._calculate_sizes(zip_path)
        
        # Validate sizes
        self._validate_sizes(artifact)
        
        # Clean up build directory
        shutil.rmtree(self.layer_dir)
        
        print(f"✓ Layer built successfully: {artifact.zip_path}")
        print(f"  Uncompressed: {artifact.uncompressed_size_mb:.2f} MB")
        print(f"  Compressed: {artifact.compressed_size_mb:.2f} MB")
        print(f"  Packages: {artifact.package_count}")
        
        return artifact
    
    def _prepare_directories(self):
        """Prepare build and output directories."""
        # Clean layer build directory
        if self.layer_dir.exists():
            shutil.rmtree(self.layer_dir)
        
        # Create layer directory with proper structure
        # Lambda layers must have python/ subdirectory
        python_dir = self.layer_dir / "python"
        python_dir.mkdir(parents=True, exist_ok=True)
        
        # Create dist directory
        self.dist_dir.mkdir(parents=True, exist_ok=True)
    
    def _install_dependencies(self, requirements_path: Path):
        """
        Install dependencies to layer directory.
        
        Args:
            requirements_path: Path to requirements.txt file
        """
        print(f"  Installing dependencies from {requirements_path.name}...")
        
        python_dir = self.layer_dir / "python"
        
        # Install packages using pip
        result = subprocess.run(
            [
                "pip", "install",
                "-r", str(requirements_path),
                "-t", str(python_dir),
                "--upgrade",
                "--no-cache-dir"
            ],
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            raise RuntimeError(f"Failed to install dependencies:\n{result.stderr}")
        
        # Count installed packages
        site_packages = python_dir
        package_count = len([
            d for d in site_packages.iterdir()
            if d.is_dir() and not d.name.startswith('.')
        ])
        
        print(f"  Installed {package_count} packages")
    
    def _create_zip_artifact(self, output_name: str) -> Path:
        """
        Create zip artifact from layer directory.
        
        Args:
            output_name: Name for the output zip file
        
        Returns:
            Path to created zip file
        """
        print(f"  Creating zip artifact...")
        
        zip_path = self.dist_dir / f"{output_name}.zip"
        
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Walk through layer directory and add all files
            for root, dirs, files in os.walk(self.layer_dir):
                for file in files:
                    file_path = Path(root) / file
                    # Calculate archive name (relative to layer_dir)
                    arcname = file_path.relative_to(self.layer_dir)
                    zipf.write(file_path, arcname)
        
        return zip_path
    
    def _calculate_sizes(self, zip_path: Path) -> LayerArtifact:
        """
        Calculate artifact sizes.
        
        Args:
            zip_path: Path to zip file
        
        Returns:
            LayerArtifact with size information
        """
        # Compressed size (zip file)
        compressed_size_bytes = zip_path.stat().st_size
        compressed_size_mb = compressed_size_bytes / (1024 * 1024)
        
        # Uncompressed size (all files in layer directory)
        uncompressed_size_bytes = 0
        for root, dirs, files in os.walk(self.layer_dir):
            for file in files:
                file_path = Path(root) / file
                uncompressed_size_bytes += file_path.stat().st_size
        uncompressed_size_mb = uncompressed_size_bytes / (1024 * 1024)
        
        # Count packages
        python_dir = self.layer_dir / "python"
        package_count = len([
            d for d in python_dir.iterdir()
            if d.is_dir() and not d.name.startswith('.')
        ])
        
        return LayerArtifact(
            zip_path=str(zip_path),
            uncompressed_size_mb=uncompressed_size_mb,
            compressed_size_mb=compressed_size_mb,
            package_count=package_count
        )
    
    def _validate_sizes(self, artifact: LayerArtifact):
        """
        Validate artifact sizes against AWS limits.
        
        Args:
            artifact: LayerArtifact to validate
        
        Raises:
            RuntimeError: If size limits are exceeded
        """
        if artifact.uncompressed_size_mb > self.MAX_UNCOMPRESSED_SIZE_MB:
            raise RuntimeError(
                f"Layer uncompressed size ({artifact.uncompressed_size_mb:.2f} MB) "
                f"exceeds AWS limit ({self.MAX_UNCOMPRESSED_SIZE_MB} MB)"
            )
        
        if artifact.compressed_size_mb > self.MAX_COMPRESSED_SIZE_MB:
            raise RuntimeError(
                f"Layer compressed size ({artifact.compressed_size_mb:.2f} MB) "
                f"exceeds AWS limit ({self.MAX_COMPRESSED_SIZE_MB} MB)"
            )


def main():
    """Main entry point for layer builder."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Build Lambda layer from requirements")
    parser.add_argument(
        "--requirements",
        default="layer_requirements.txt",
        help="Requirements file (default: layer_requirements.txt)"
    )
    parser.add_argument(
        "--output",
        default="lambda_layer",
        help="Output zip file name (default: lambda_layer)"
    )
    parser.add_argument(
        "--workspace",
        default="backend",
        help="Backend workspace directory (default: backend)"
    )
    
    args = parser.parse_args()
    
    try:
        builder = LambdaLayerBuilder(workspace_dir=args.workspace)
        artifact = builder.build_layer(
            requirements_file=args.requirements,
            output_name=args.output
        )
        print(f"\n✓ Layer artifact created: {artifact.zip_path}")
    except Exception as e:
        print(f"\n✗ Layer build failed: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
