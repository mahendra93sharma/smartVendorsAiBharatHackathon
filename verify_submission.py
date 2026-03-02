#!/usr/bin/env python3
"""
Smart Vendors - Submission Verification Script
Verifies all hackathon deliverables are ready for submission
"""

import os
import sys
import requests
from pathlib import Path
from typing import Dict, List, Tuple


class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'


def print_header(text: str) -> None:
    """Print section header"""
    print(f"\n{Colors.BLUE}{'=' * 60}{Colors.END}")
    print(f"{Colors.BLUE}{text}{Colors.END}")
    print(f"{Colors.BLUE}{'=' * 60}{Colors.END}\n")


def print_check(passed: bool, message: str) -> None:
    """Print check result"""
    if passed:
        print(f"{Colors.GREEN}✅ {message}{Colors.END}")
    else:
        print(f"{Colors.RED}❌ {message}{Colors.END}")


def print_warning(message: str) -> None:
    """Print warning message"""
    print(f"{Colors.YELLOW}⚠️  {message}{Colors.END}")


def check_file_exists(filepath: str) -> bool:
    """Check if file exists"""
    return Path(filepath).exists()


def check_url_accessible(url: str, timeout: int = 10) -> Tuple[bool, str]:
    """Check if URL is accessible"""
    try:
        response = requests.get(url, timeout=timeout, allow_redirects=True)
        if response.status_code == 200:
            return True, f"Status: {response.status_code}"
        else:
            return False, f"Status: {response.status_code}"
    except requests.exceptions.Timeout:
        return False, "Timeout"
    except requests.exceptions.ConnectionError:
        return False, "Connection error"
    except Exception as e:
        return False, str(e)


def verify_github_repo() -> Dict[str, bool]:
    """Verify GitHub repository requirements"""
    print_header("1. GitHub Repository Verification")
    
    results = {}
    
    # Check required files
    required_files = [
        "README.md",
        "LICENSE",
        ".gitignore",
        ".env.example",
        "CONTRIBUTING.md",
        "docker-compose.yml",
        "setup.sh",
    ]
    
    for file in required_files:
        exists = check_file_exists(file)
        results[f"file_{file}"] = exists
        print_check(exists, f"File exists: {file}")
    
    # Check documentation
    docs_files = [
        "docs/API.md",
        "docs/ARCHITECTURE.md",
        "docs/DEPLOYMENT.md",
    ]
    
    for file in docs_files:
        exists = check_file_exists(file)
        results[f"doc_{file}"] = exists
        print_check(exists, f"Documentation exists: {file}")
    
    # Check backend structure
    backend_dirs = [
        "backend/lambda_functions",
        "backend/shared",
        "backend/tests",
    ]
    
    for dir_path in backend_dirs:
        exists = Path(dir_path).is_dir()
        results[f"backend_{dir_path}"] = exists
        print_check(exists, f"Backend directory exists: {dir_path}")
    
    # Check frontend structure
    frontend_dirs = [
        "frontend/src",
        "frontend/public",
    ]
    
    for dir_path in frontend_dirs:
        exists = Path(dir_path).is_dir()
        results[f"frontend_{dir_path}"] = exists
        print_check(exists, f"Frontend directory exists: {dir_path}")
    
    return results


def verify_prototype_url() -> Dict[str, bool]:
    """Verify prototype URL accessibility"""
    print_header("2. Prototype URL Verification")
    
    results = {}
    
    # Check if URL is configured
    env_file = Path(".env")
    if env_file.exists():
        with open(env_file) as f:
            content = f.read()
            if "PROTOTYPE_URL" in content:
                print_check(True, "Prototype URL configured in .env")
                results["url_configured"] = True
                
                # Extract URL (simple parsing)
                for line in content.split('\n'):
                    if line.startswith("PROTOTYPE_URL="):
                        url = line.split('=')[1].strip()
                        print(f"   URL: {url}")
                        
                        # Test accessibility
                        accessible, status = check_url_accessible(url)
                        results["url_accessible"] = accessible
                        print_check(accessible, f"Prototype accessible: {status}")
            else:
                print_warning("PROTOTYPE_URL not found in .env")
                results["url_configured"] = False
    else:
        print_warning(".env file not found")
        print("   Please create .env with PROTOTYPE_URL=your-url")
        results["url_configured"] = False
    
    return results


def verify_demo_video() -> Dict[str, bool]:
    """Verify demo video"""
    print_header("3. Demo Video Verification")
    
    results = {}
    
    # Check if video URL is configured
    env_file = Path(".env")
    if env_file.exists():
        with open(env_file) as f:
            content = f.read()
            if "VIDEO_URL" in content:
                print_check(True, "Video URL configured in .env")
                results["video_configured"] = True
                
                # Extract URL
                for line in content.split('\n'):
                    if line.startswith("VIDEO_URL="):
                        url = line.split('=')[1].strip()
                        print(f"   URL: {url}")
                        
                        # Test accessibility
                        accessible, status = check_url_accessible(url)
                        results["video_accessible"] = accessible
                        print_check(accessible, f"Video accessible: {status}")
            else:
                print_warning("VIDEO_URL not found in .env")
                results["video_configured"] = False
    else:
        print_warning(".env file not found")
        results["video_configured"] = False
    
    return results


def verify_project_summary() -> Dict[str, bool]:
    """Verify project summary document"""
    print_header("4. Project Summary Verification")
    
    results = {}
    
    # Check for PDF file
    pdf_files = list(Path(".").glob("*summary*.pdf")) + list(Path("docs").glob("*summary*.pdf"))
    
    if pdf_files:
        print_check(True, f"Project summary found: {pdf_files[0]}")
        results["summary_exists"] = True
        
        # Check file size
        file_size = pdf_files[0].stat().st_size
        size_mb = file_size / (1024 * 1024)
        
        if size_mb < 10:
            print_check(True, f"File size OK: {size_mb:.2f} MB")
            results["summary_size_ok"] = True
        else:
            print_check(False, f"File size too large: {size_mb:.2f} MB (max 10 MB)")
            results["summary_size_ok"] = False
    else:
        print_check(False, "Project summary PDF not found")
        results["summary_exists"] = False
    
    return results


def verify_aws_services() -> Dict[str, bool]:
    """Verify AWS services documentation"""
    print_header("5. AWS Services Documentation")
    
    results = {}
    
    # Check README for AWS services
    readme_path = Path("README.md")
    if readme_path.exists():
        with open(readme_path) as f:
            content = f.read().lower()
            
            aws_services = [
                "bedrock",
                "lambda",
                "dynamodb",
                "s3",
                "sagemaker",
                "transcribe",
                "api gateway",
            ]
            
            for service in aws_services:
                mentioned = service in content
                results[f"aws_{service}"] = mentioned
                print_check(mentioned, f"AWS {service.title()} mentioned in README")
    else:
        print_warning("README.md not found")
    
    return results


def verify_tests() -> Dict[str, bool]:
    """Verify tests exist"""
    print_header("6. Tests Verification")
    
    results = {}
    
    # Check backend tests
    backend_tests = list(Path("backend/tests").glob("test_*.py"))
    if backend_tests:
        print_check(True, f"Backend tests found: {len(backend_tests)} files")
        results["backend_tests"] = True
    else:
        print_check(False, "No backend tests found")
        results["backend_tests"] = False
    
    # Check frontend tests
    frontend_tests = list(Path("frontend/src").rglob("*.test.ts*"))
    if frontend_tests:
        print_check(True, f"Frontend tests found: {len(frontend_tests)} files")
        results["frontend_tests"] = True
    else:
        print_warning("No frontend tests found")
        results["frontend_tests"] = False
    
    return results


def generate_summary(all_results: Dict[str, Dict[str, bool]]) -> None:
    """Generate verification summary"""
    print_header("Verification Summary")
    
    total_checks = 0
    passed_checks = 0
    
    for category, results in all_results.items():
        for check, passed in results.items():
            total_checks += 1
            if passed:
                passed_checks += 1
    
    percentage = (passed_checks / total_checks * 100) if total_checks > 0 else 0
    
    print(f"Total Checks: {total_checks}")
    print(f"Passed: {passed_checks}")
    print(f"Failed: {total_checks - passed_checks}")
    print(f"Success Rate: {percentage:.1f}%")
    
    if percentage == 100:
        print(f"\n{Colors.GREEN}🎉 All checks passed! Ready for submission!{Colors.END}")
        return 0
    elif percentage >= 80:
        print(f"\n{Colors.YELLOW}⚠️  Most checks passed. Review failed items before submission.{Colors.END}")
        return 1
    else:
        print(f"\n{Colors.RED}❌ Many checks failed. Please address issues before submission.{Colors.END}")
        return 2


def main() -> int:
    """Main verification function"""
    print(f"\n{Colors.BLUE}{'=' * 60}{Colors.END}")
    print(f"{Colors.BLUE}Smart Vendors - Submission Verification{Colors.END}")
    print(f"{Colors.BLUE}{'=' * 60}{Colors.END}")
    
    all_results = {}
    
    # Run all verifications
    all_results["github"] = verify_github_repo()
    all_results["prototype"] = verify_prototype_url()
    all_results["video"] = verify_demo_video()
    all_results["summary"] = verify_project_summary()
    all_results["aws"] = verify_aws_services()
    all_results["tests"] = verify_tests()
    
    # Generate summary
    return generate_summary(all_results)


if __name__ == "__main__":
    sys.exit(main())
