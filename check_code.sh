#!/bin/bash
# check_code.sh - Run all code quality checks for Marvin project

echo "🔍 Running code quality checks for Marvin..."
echo "==========================================="

# Exit on any error
set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if we're in the right directory
if [ ! -f "pyproject.toml" ]; then
    echo -e "${RED}Error: Not in Marvin project root directory${NC}"
    exit 1
fi

# Activate virtual environment if not already active
if [ -z "$VIRTUAL_ENV" ]; then
    echo -e "${YELLOW}Activating virtual environment...${NC}"
    source .venv/bin/activate || {
        echo -e "${RED}Failed to activate virtual environment. Run 'uv venv' first.${NC}"
        exit 1
    }
fi

echo -e "\n${YELLOW}1. Running Black formatter...${NC}"
uv run black src tests --check --diff || {
    echo -e "${RED}Black found formatting issues. Running formatter...${NC}"
    uv run black src tests
    echo -e "${GREEN}✅ Black formatting applied${NC}"
}

echo -e "\n${YELLOW}2. Running isort...${NC}"
uv run isort src tests --check-only --diff || {
    echo -e "${RED}isort found import sorting issues. Fixing...${NC}"
    uv run isort src tests
    echo -e "${GREEN}✅ Import sorting fixed${NC}"
}

echo -e "\n${YELLOW}3. Running Ruff linter...${NC}"
uv run ruff check src tests || {
    echo -e "${RED}Ruff found issues. Attempting auto-fix...${NC}"
    uv run ruff check src tests --fix
    echo -e "${GREEN}✅ Ruff issues fixed (where possible)${NC}"
}

echo -e "\n${YELLOW}4. Running mypy type checker...${NC}"
uv run mypy src || {
    echo -e "${RED}⚠️  mypy found type issues. Please fix manually.${NC}"
    # Don't exit on mypy errors as some might need manual intervention
}

echo -e "\n${YELLOW}5. Running pytest with coverage...${NC}"
uv run pytest --cov=marvin --cov-report=term-missing --cov-report=html || {
    echo -e "${RED}⚠️  Some tests failed. Please fix.${NC}"
    exit 1
}

echo -e "\n${GREEN}✅ All code quality checks completed!${NC}"
echo -e "${GREEN}Coverage report available in htmlcov/index.html${NC}"