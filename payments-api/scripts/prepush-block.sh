#!/bin/bash

# Pre-push hook to prevent pushing until all checks pass
# This script blocks git push until lint, tests, and e2e tests all pass

echo "🔍 Running pre-push checks..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    if [ $2 -eq 0 ]; then
        echo -e "${GREEN}✅ $1 passed${NC}"
    else
        echo -e "${RED}❌ $1 failed${NC}"
    fi
}

# Track overall status
OVERALL_STATUS=0

# Run linting
echo -e "${YELLOW}Running linting...${NC}"
make lint
LINT_STATUS=$?
print_status "Linting" $LINT_STATUS
if [ $LINT_STATUS -ne 0 ]; then
    OVERALL_STATUS=1
fi

# Run tests
echo -e "${YELLOW}Running tests...${NC}"
make test
TEST_STATUS=$?
print_status "Tests" $TEST_STATUS
if [ $TEST_STATUS -ne 0 ]; then
    OVERALL_STATUS=1
fi

# Run E2E tests
echo -e "${YELLOW}Running E2E tests...${NC}"
make e2e
E2E_STATUS=$?
print_status "E2E tests" $E2E_STATUS
if [ $E2E_STATUS -ne 0 ]; then
    OVERALL_STATUS=1
fi

# Final status
if [ $OVERALL_STATUS -eq 0 ]; then
    echo -e "${GREEN}🎉 All checks passed! Push allowed.${NC}"
    exit 0
else
    echo -e "${RED}💥 Some checks failed! Push blocked.${NC}"
    echo ""
    echo "To fix issues:"
    echo "  - Run 'make lint' and fix any linting errors"
    echo "  - Run 'make test' and fix any failing tests"
    echo "  - Run 'make e2e' and fix any E2E test failures"
    echo ""
    echo "To bypass this check (not recommended):"
    echo "  - Remove .git/hooks/pre-push"
    echo "  - Or run: git push --no-verify"
    exit 1
fi