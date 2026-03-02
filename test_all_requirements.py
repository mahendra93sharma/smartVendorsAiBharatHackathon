#!/usr/bin/env python3
"""
Comprehensive Requirements Testing Script
Tests all hackathon requirements are met
"""

import subprocess
import sys
import time
import requests
from pathlib import Path


class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'


def print_header(text):
    print(f"\n{Colors.BLUE}{'=' * 70}{Colors.END}")
    print(f"{Colors.BLUE}{text}{Colors.END}")
    print(f"{Colors.BLUE}{'=' * 70}{Colors.END}\n")


def print_test(passed, message):
    if passed:
        print(f"{Colors.GREEN}✅ PASS: {message}{Colors.END}")
        return 1
    else:
        print(f"{Colors.RED}❌ FAIL: {message}{Colors.END}")
        return 0


def print_info(message):
    print(f"{Colors.YELLOW}ℹ️  INFO: {message}{Colors.END}")


def run_command(cmd, cwd=None):
    """Run shell command and return output"""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=30
        )
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return False, "", "Command timed out"
    except Exception as e:
        return False, "", str(e)


def test_frontend_structure():
    """Test frontend project structure"""
    print_header("1. Frontend Structure Tests")
    passed = 0
    total = 0
    
    # Check key directories
    dirs = [
        "frontend/src",
        "frontend/src/pages",
        "frontend/src/components",
        "frontend/src/services",
        "frontend/src/contexts",
        "frontend/public",
    ]
    
    for dir_path in dirs:
        total += 1
        exists = Path(dir_path).is_dir()
        passed += print_test(exists, f"Directory exists: {dir_path}")
    
    # Check key files
    files = [
        "frontend/package.json",
        "frontend/tsconfig.json",
        "frontend/.eslintrc.cjs",
        "frontend/.prettierrc",
        "frontend/vite.config.ts",
        "frontend/tailwind.config.js",
    ]
    
    for file_path in files:
        total += 1
        exists = Path(file_path).is_file()
        passed += print_test(exists, f"File exists: {file_path}")
    
    return passed, total


def test_frontend_pages():
    """Test all required frontend pages exist"""
    print_header("2. Frontend Pages Tests")
    passed = 0
    total = 0
    
    pages = [
        "frontend/src/pages/Home.tsx",
        "frontend/src/pages/VoiceTransaction.tsx",
        "frontend/src/pages/PriceIntelligence.tsx",
        "frontend/src/pages/FreshnessScanner.tsx",
        "frontend/src/pages/Marketplace.tsx",
        "frontend/src/pages/TrustScore.tsx",
    ]
    
    for page in pages:
        total += 1
        exists = Path(page).is_file()
        passed += print_test(exists, f"Page exists: {Path(page).name}")
    
    return passed, total


def test_frontend_features():
    """Test frontend feature implementations"""
    print_header("3. Frontend Features Tests")
    passed = 0
    total = 0
    
    # Check demo mode context
    total += 1
    demo_context = Path("frontend/src/contexts/DemoModeContext.tsx")
    if demo_context.exists():
        content = demo_context.read_text()
        has_demo = "isDemoMode" in content and "toggleDemoMode" in content
        passed += print_test(has_demo, "Demo mode context implemented")
    else:
        print_test(False, "Demo mode context missing")
    
    # Check demo data
    total += 1
    demo_data = Path("frontend/src/data/demoData.ts")
    if demo_data.exists():
        content = demo_data.read_text()
        has_samples = "DEMO_AUDIO_SAMPLES" in content and "DEMO_MARKET_PRICES" in content
        passed += print_test(has_samples, "Demo data implemented")
    else:
        print_test(False, "Demo data missing")
    
    # Check API service
    total += 1
    api_service = Path("frontend/src/services/api.ts")
    exists = api_service.exists()
    passed += print_test(exists, "API service implemented")
    
    return passed, total


def test_frontend_build():
    """Test frontend builds successfully"""
    print_header("4. Frontend Build Tests")
    passed = 0
    total = 1
    
    print_info("Building frontend (this may take a minute)...")
    success, stdout, stderr = run_command("npm run build", cwd="frontend")
    
    if success and Path("frontend/dist").exists():
        passed += print_test(True, "Frontend builds successfully")
        
        # Check build output
        dist_files = list(Path("frontend/dist").rglob("*"))
        has_index = any("index.html" in str(f) for f in dist_files)
        has_assets = any("assets" in str(f) for f in dist_files)
        
        total += 2
        passed += print_test(has_index, "Build contains index.html")
        passed += print_test(has_assets, "Build contains assets")
    else:
        print_test(False, "Frontend build failed")
        if stderr:
            print(f"  Error: {stderr[:200]}")
    
    return passed, total


def test_frontend_linting():
    """Test frontend code quality"""
    print_header("5. Frontend Code Quality Tests")
    passed = 0
    total = 0
    
    # ESLint
    total += 1
    print_info("Running ESLint...")
    success, stdout, stderr = run_command("npm run lint", cwd="frontend")
    passed += print_test(success, "ESLint passes")
    
    # TypeScript compilation
    total += 1
    print_info("Running TypeScript check...")
    success, stdout, stderr = run_command("npx tsc --noEmit", cwd="frontend")
    passed += print_test(success, "TypeScript compilation passes")
    
    return passed, total


def test_backend_structure():
    """Test backend project structure"""
    print_header("6. Backend Structure Tests")
    passed = 0
    total = 0
    
    # Check key directories
    dirs = [
        "backend/lambda_functions",
        "backend/shared",
        "backend/shared/models",
        "backend/shared/services",
        "backend/shared/aws",
        "backend/tests",
    ]
    
    for dir_path in dirs:
        total += 1
        exists = Path(dir_path).is_dir()
        passed += print_test(exists, f"Directory exists: {dir_path}")
    
    # Check key files
    files = [
        "backend/requirements.txt",
        "backend/pyproject.toml",
        "backend/pytest.ini",
        "backend/seed_data.py",
    ]
    
    for file_path in files:
        total += 1
        exists = Path(file_path).is_file()
        passed += print_test(exists, f"File exists: {file_path}")
    
    return passed, total


def test_lambda_functions():
    """Test all Lambda functions exist"""
    print_header("7. Lambda Functions Tests")
    passed = 0
    total = 0
    
    functions = [
        "voice_transcribe",
        "create_transaction",
        "get_transactions",
        "get_market_prices",
        "classify_freshness",
        "create_marketplace_listing",
        "get_marketplace_buyers",
        "notify_marketplace_buyers",
        "get_trust_score",
    ]
    
    for func in functions:
        total += 1
        func_dir = Path(f"backend/lambda_functions/{func}")
        exists = func_dir.is_dir()
        passed += print_test(exists, f"Lambda function exists: {func}")
    
    return passed, total


def test_backend_code_quality():
    """Test backend code quality"""
    print_header("8. Backend Code Quality Tests")
    passed = 0
    total = 0
    
    # Black formatting check
    total += 1
    print_info("Checking Black formatting...")
    success, stdout, stderr = run_command("python -m black . --check", cwd="backend")
    passed += print_test(success, "Black formatting passes")
    
    return passed, total


def test_backend_tests():
    """Test backend test suite"""
    print_header("9. Backend Tests")
    passed = 0
    total = 1
    
    print_info("Running backend tests (this may take a minute)...")
    success, stdout, stderr = run_command("python -m pytest tests/ -v --tb=short", cwd="backend")
    
    if success:
        passed += print_test(True, "Backend tests pass")
        
        # Count test results
        if "passed" in stdout:
            import re
            match = re.search(r'(\d+) passed', stdout)
            if match:
                test_count = match.group(1)
                print_info(f"Total tests passed: {test_count}")
    else:
        print_test(False, "Backend tests failed")
        if stderr:
            print(f"  Error: {stderr[:300]}")
    
    return passed, total


def test_documentation():
    """Test documentation exists"""
    print_header("10. Documentation Tests")
    passed = 0
    total = 0
    
    docs = [
        "README.md",
        "LICENSE",
        "CONTRIBUTING.md",
        ".gitignore",
        ".env.example",
        "docs/API.md",
        "docs/ARCHITECTURE.md",
        "docs/DEPLOYMENT.md",
    ]
    
    for doc in docs:
        total += 1
        exists = Path(doc).is_file()
        passed += print_test(exists, f"Documentation exists: {doc}")
    
    # Check README content
    total += 1
    readme = Path("README.md")
    if readme.exists():
        content = readme.read_text()
        has_aws = "AWS" in content or "Amazon" in content
        passed += print_test(has_aws, "README mentions AWS services")
    else:
        print_test(False, "README missing")
    
    return passed, total


def test_deployment_files():
    """Test deployment configuration"""
    print_header("11. Deployment Configuration Tests")
    passed = 0
    total = 0
    
    files = [
        "docker-compose.yml",
        "setup.sh",
        "backend/Dockerfile",
        "frontend/Dockerfile",
        "backend/deploy_lambda.sh",
        "DEPLOYMENT_CHECKLIST.md",
        "SUBMISSION_CHECKLIST.md",
    ]
    
    for file_path in files:
        total += 1
        exists = Path(file_path).is_file()
        passed += print_test(exists, f"Deployment file exists: {file_path}")
    
    return passed, total


def test_aws_services_documentation():
    """Test AWS services are documented"""
    print_header("12. AWS Services Documentation Tests")
    passed = 0
    total = 0
    
    aws_services = [
        "Bedrock",
        "Lambda",
        "DynamoDB",
        "S3",
        "SageMaker",
        "Transcribe",
        "API Gateway",
    ]
    
    readme = Path("README.md")
    if readme.exists():
        content = readme.read_text()
        
        for service in aws_services:
            total += 1
            mentioned = service in content
            passed += print_test(mentioned, f"AWS {service} documented in README")
    else:
        print_info("README.md not found, skipping AWS services check")
    
    return passed, total


def test_demo_credentials():
    """Test demo credentials are documented"""
    print_header("13. Demo Credentials Tests")
    passed = 0
    total = 0
    
    # Check in README
    total += 1
    readme = Path("README.md")
    if readme.exists():
        content = readme.read_text()
        has_demo = "demo_vendor" in content or "Demo Credentials" in content
        passed += print_test(has_demo, "Demo credentials in README")
    else:
        print_test(False, "README missing")
    
    # Check in frontend config
    total += 1
    config = Path("frontend/src/config/api.ts")
    if config.exists():
        content = config.read_text()
        has_demo = "demo_vendor" in content and "hackathon2024" in content
        passed += print_test(has_demo, "Demo credentials in frontend config")
    else:
        print_test(False, "Frontend config missing")
    
    return passed, total


def generate_summary(all_results):
    """Generate final summary"""
    print_header("FINAL SUMMARY")
    
    total_passed = sum(r[0] for r in all_results)
    total_tests = sum(r[1] for r in all_results)
    percentage = (total_passed / total_tests * 100) if total_tests > 0 else 0
    
    print(f"Total Tests: {total_tests}")
    print(f"Passed: {total_passed}")
    print(f"Failed: {total_tests - total_passed}")
    print(f"Success Rate: {percentage:.1f}%")
    
    if percentage == 100:
        print(f"\n{Colors.GREEN}🎉 ALL TESTS PASSED! Project is ready!{Colors.END}")
        return 0
    elif percentage >= 80:
        print(f"\n{Colors.YELLOW}⚠️  Most tests passed. Review failures.{Colors.END}")
        return 1
    else:
        print(f"\n{Colors.RED}❌ Many tests failed. Please fix issues.{Colors.END}")
        return 2


def main():
    """Main test runner"""
    print(f"\n{Colors.BLUE}{'=' * 70}{Colors.END}")
    print(f"{Colors.BLUE}Smart Vendors - Comprehensive Requirements Testing{Colors.END}")
    print(f"{Colors.BLUE}{'=' * 70}{Colors.END}")
    
    results = []
    
    # Run all test suites
    results.append(test_frontend_structure())
    results.append(test_frontend_pages())
    results.append(test_frontend_features())
    results.append(test_frontend_linting())
    results.append(test_frontend_build())
    results.append(test_backend_structure())
    results.append(test_lambda_functions())
    results.append(test_backend_code_quality())
    results.append(test_backend_tests())
    results.append(test_documentation())
    results.append(test_deployment_files())
    results.append(test_aws_services_documentation())
    results.append(test_demo_credentials())
    
    # Generate summary
    return generate_summary(results)


if __name__ == "__main__":
    sys.exit(main())
