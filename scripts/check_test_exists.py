#!/usr/bin/env python3
"""
Check if test files exist for all source code files.
This enforces Test-Driven Development by ensuring tests are written.
"""
import sys
import os
from pathlib import Path


def get_test_path(src_path: Path) -> list[Path]:
    """Get potential test file paths for a given source file."""
    # Convert src/marvin/module.py to tests/unit/test_module.py
    relative_path = src_path.relative_to("src")
    stem = src_path.stem
    parent = relative_path.parent
    
    # Multiple test file naming conventions
    test_paths = [
        Path("tests/unit") / parent / f"test_{stem}.py",
        Path("tests/unit") / parent / f"{stem}_test.py",
        Path("tests/integration") / parent / f"test_{stem}.py",
    ]
    
    # Special case for adapters
    if "adapters" in str(parent):
        test_paths.append(Path("tests/unit") / f"test_{stem}.py")
    
    return test_paths


def check_test_exists(filepath: str) -> tuple[bool, str]:
    """
    Check if a test file exists for the given source file.
    
    Returns:
        tuple: (exists: bool, message: str)
    """
    src_path = Path(filepath)
    
    # Skip files that don't need tests
    skip_patterns = [
        "__init__.py",
        "__main__.py",
        "_version.py",
        "py.typed",
    ]
    
    if any(pattern in src_path.name for pattern in skip_patterns):
        return True, f"✓ {filepath} - Skipped (no test required)"
    
    # Get potential test paths
    test_paths = get_test_path(src_path)
    
    # Check if any test file exists
    for test_path in test_paths:
        if test_path.exists():
            return True, f"✓ {filepath} → {test_path}"
    
    # No test found
    expected_paths = "\n    ".join(str(p) for p in test_paths)
    message = f"✗ {filepath} - No test file found!\n  Expected one of:\n    {expected_paths}"
    return False, message


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: check_test_exists.py <file1> [file2] ...")
        sys.exit(1)
    
    all_good = True
    messages = []
    
    for filepath in sys.argv[1:]:
        exists, message = check_test_exists(filepath)
        messages.append(message)
        if not exists:
            all_good = False
    
    # Print results
    print("\n🧪 Test Coverage Check Results:\n")
    for message in messages:
        print(message)
    
    if not all_good:
        print("\n❌ ERROR: Missing test files detected!")
        print("📝 Remember: Write tests FIRST (TDD)!")
        print("\nTo fix:")
        print("1. Create the missing test file(s)")
        print("2. Write failing tests for your new code")
        print("3. Implement the code to make tests pass")
        print("4. Refactor while keeping tests green")
        sys.exit(1)
    else:
        print("\n✅ All source files have corresponding tests!")


if __name__ == "__main__":
    main()