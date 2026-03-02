#!/bin/bash

# Quick Verification Script
# Tests key requirements are met

set -e

echo "🚀 Smart Vendors - Quick Verification"
echo "======================================"
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

PASSED=0
FAILED=0

check_pass() {
    echo -e "${GREEN}✅ PASS: $1${NC}"
    ((PASSED++))
}

check_fail() {
    echo -e "${RED}❌ FAIL: $1${NC}"
    ((FAILED++))
}

check_info() {
    echo -e "${YELLOW}ℹ️  INFO: $1${NC}"
}

echo "1. Frontend Structure"
echo "---------------------"
[ -d "frontend/src" ] && check_pass "frontend/src exists" || check_fail "frontend/src missing"
[ -d "frontend/src/pages" ] && check_pass "frontend/src/pages exists" || check_fail "frontend/src/pages missing"
[ -f "frontend/package.json" ] && check_pass "package.json exists" || check_fail "package.json missing"
[ -f "frontend/tsconfig.json" ] && check_pass "tsconfig.json exists" || check_fail "tsconfig.json missing"
echo ""

echo "2. Frontend Pages"
echo "-----------------"
[ -f "frontend/src/pages/Home.tsx" ] && check_pass "Home page exists" || check_fail "Home page missing"
[ -f "frontend/src/pages/VoiceTransaction.tsx" ] && check_pass "VoiceTransaction page exists" || check_fail "VoiceTransaction page missing"
[ -f "frontend/src/pages/PriceIntelligence.tsx" ] && check_pass "PriceIntelligence page exists" || check_fail "PriceIntelligence page missing"
[ -f "frontend/src/pages/FreshnessScanner.tsx" ] && check_pass "FreshnessScanner page exists" || check_fail "FreshnessScanner page missing"
[ -f "frontend/src/pages/Marketplace.tsx" ] && check_pass "Marketplace page exists" || check_fail "Marketplace page missing"
[ -f "frontend/src/pages/TrustScore.tsx" ] && check_pass "TrustScore page exists" || check_fail "TrustScore page missing"
echo ""

echo "3. Backend Structure"
echo "--------------------"
[ -d "backend/lambda_functions" ] && check_pass "lambda_functions exists" || check_fail "lambda_functions missing"
[ -d "backend/shared" ] && check_pass "shared directory exists" || check_fail "shared directory missing"
[ -d "backend/tests" ] && check_pass "tests directory exists" || check_fail "tests directory missing"
[ -f "backend/requirements.txt" ] && check_pass "requirements.txt exists" || check_fail "requirements.txt missing"
echo ""

echo "4. Lambda Functions"
echo "-------------------"
[ -d "backend/lambda_functions/voice_transcribe" ] && check_pass "voice_transcribe exists" || check_fail "voice_transcribe missing"
[ -d "backend/lambda_functions/create_transaction" ] && check_pass "create_transaction exists" || check_fail "create_transaction missing"
[ -d "backend/lambda_functions/get_market_prices" ] && check_pass "get_market_prices exists" || check_fail "get_market_prices missing"
[ -d "backend/lambda_functions/classify_freshness" ] && check_pass "classify_freshness exists" || check_fail "classify_freshness missing"
[ -d "backend/lambda_functions/get_trust_score" ] && check_pass "get_trust_score exists" || check_fail "get_trust_score missing"
echo ""

echo "5. Documentation"
echo "----------------"
[ -f "README.md" ] && check_pass "README.md exists" || check_fail "README.md missing"
[ -f "LICENSE" ] && check_pass "LICENSE exists" || check_fail "LICENSE missing"
[ -f "CONTRIBUTING.md" ] && check_pass "CONTRIBUTING.md exists" || check_fail "CONTRIBUTING.md missing"
[ -f "docs/API.md" ] && check_pass "API.md exists" || check_fail "API.md missing"
[ -f "docs/ARCHITECTURE.md" ] && check_pass "ARCHITECTURE.md exists" || check_fail "ARCHITECTURE.md missing"
[ -f "docs/DEPLOYMENT.md" ] && check_pass "DEPLOYMENT.md exists" || check_fail "DEPLOYMENT.md missing"
echo ""

echo "6. Deployment Files"
echo "-------------------"
[ -f "docker-compose.yml" ] && check_pass "docker-compose.yml exists" || check_fail "docker-compose.yml missing"
[ -f "setup.sh" ] && check_pass "setup.sh exists" || check_fail "setup.sh missing"
[ -f "backend/Dockerfile" ] && check_pass "backend Dockerfile exists" || check_fail "backend Dockerfile missing"
[ -f "frontend/Dockerfile" ] && check_pass "frontend Dockerfile exists" || check_fail "frontend Dockerfile missing"
echo ""

echo "7. Code Quality Files"
echo "---------------------"
[ -f "frontend/.eslintrc.cjs" ] && check_pass "ESLint config exists" || check_fail "ESLint config missing"
[ -f "frontend/.prettierrc" ] && check_pass "Prettier config exists" || check_fail "Prettier config missing"
[ -f "backend/pyproject.toml" ] && check_pass "pyproject.toml exists" || check_fail "pyproject.toml missing"
[ -f ".pre-commit-config.yaml" ] && check_pass "pre-commit config exists" || check_fail "pre-commit config missing"
echo ""

echo "8. Demo Mode Features"
echo "---------------------"
[ -f "frontend/src/contexts/DemoModeContext.tsx" ] && check_pass "DemoModeContext exists" || check_fail "DemoModeContext missing"
[ -f "frontend/src/data/demoData.ts" ] && check_pass "Demo data exists" || check_fail "Demo data missing"
echo ""

echo "9. Frontend Running"
echo "-------------------"
if curl -s http://localhost:3000 > /dev/null 2>&1; then
    check_pass "Frontend is running on http://localhost:3000"
else
    check_fail "Frontend is NOT running on http://localhost:3000"
    check_info "Start with: cd frontend && npm run dev"
fi
echo ""

echo "10. README AWS Services"
echo "-----------------------"
if [ -f "README.md" ]; then
    grep -q "Bedrock" README.md && check_pass "Bedrock mentioned" || check_fail "Bedrock not mentioned"
    grep -q "Lambda" README.md && check_pass "Lambda mentioned" || check_fail "Lambda not mentioned"
    grep -q "DynamoDB" README.md && check_pass "DynamoDB mentioned" || check_fail "DynamoDB not mentioned"
    grep -q "S3" README.md && check_pass "S3 mentioned" || check_fail "S3 not mentioned"
    grep -q "SageMaker" README.md && check_pass "SageMaker mentioned" || check_fail "SageMaker not mentioned"
fi
echo ""

echo "======================================"
echo "SUMMARY"
echo "======================================"
TOTAL=$((PASSED + FAILED))
PERCENTAGE=$((PASSED * 100 / TOTAL))

echo "Total Checks: $TOTAL"
echo -e "${GREEN}Passed: $PASSED${NC}"
echo -e "${RED}Failed: $FAILED${NC}"
echo "Success Rate: $PERCENTAGE%"
echo ""

if [ $PERCENTAGE -eq 100 ]; then
    echo -e "${GREEN}🎉 ALL CHECKS PASSED! Project is ready!${NC}"
    exit 0
elif [ $PERCENTAGE -ge 80 ]; then
    echo -e "${YELLOW}⚠️  Most checks passed. Review failures.${NC}"
    exit 1
else
    echo -e "${RED}❌ Many checks failed. Please fix issues.${NC}"
    exit 2
fi
