#!/usr/bin/env python3
"""
Version bumping script for Marvin.

Usage:
    python scripts/bump_version.py patch  # 0.1.0 -> 0.1.1
    python scripts/bump_version.py minor  # 0.1.0 -> 0.2.0
    python scripts/bump_version.py major  # 0.1.0 -> 1.0.0
    python scripts/bump_version.py --current  # Show current version
"""

import argparse
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Tuple

# Version regex pattern
VERSION_PATTERN = re.compile(r'^(\d+)\.(\d+)\.(\d+)(?:-(alpha|beta|rc)\.(\d+))?$')

# Files that contain version information
VERSION_FILES = [
    ("pyproject.toml", r'version = "([^"]+)"'),
    ("src/marvin/__init__.py", r'__version__ = "([^"]+)"'),
]


def parse_version(version_str: str) -> Tuple[int, int, int, str, int]:
    """Parse version string into components."""
    match = VERSION_PATTERN.match(version_str)
    if not match:
        raise ValueError(f"Invalid version format: {version_str}")
    
    major = int(match.group(1))
    minor = int(match.group(2))
    patch = int(match.group(3))
    pre_type = match.group(4) or ""
    pre_num = int(match.group(5)) if match.group(5) else 0
    
    return major, minor, patch, pre_type, pre_num


def format_version(major: int, minor: int, patch: int, pre_type: str = "", pre_num: int = 0) -> str:
    """Format version components into string."""
    version = f"{major}.{minor}.{patch}"
    if pre_type:
        version += f"-{pre_type}.{pre_num}"
    return version


def get_current_version() -> str:
    """Get current version from pyproject.toml."""
    pyproject_path = Path("pyproject.toml")
    if not pyproject_path.exists():
        raise FileNotFoundError("pyproject.toml not found")
    
    content = pyproject_path.read_text()
    match = re.search(r'version = "([^"]+)"', content)
    if not match:
        raise ValueError("Version not found in pyproject.toml")
    
    return match.group(1)


def bump_version(version_str: str, bump_type: str) -> str:
    """Bump version according to bump type."""
    major, minor, patch, pre_type, pre_num = parse_version(version_str)
    
    if bump_type == "major":
        major += 1
        minor = 0
        patch = 0
        pre_type = ""
        pre_num = 0
    elif bump_type == "minor":
        minor += 1
        patch = 0
        pre_type = ""
        pre_num = 0
    elif bump_type == "patch":
        if pre_type:
            # If it's a pre-release, just remove the pre-release tag
            pre_type = ""
            pre_num = 0
        else:
            patch += 1
    elif bump_type == "alpha":
        if pre_type == "alpha":
            pre_num += 1
        else:
            patch += 1
            pre_type = "alpha"
            pre_num = 1
    elif bump_type == "beta":
        if pre_type == "beta":
            pre_num += 1
        elif pre_type == "alpha":
            pre_type = "beta"
            pre_num = 1
        else:
            patch += 1
            pre_type = "beta"
            pre_num = 1
    elif bump_type == "rc":
        if pre_type == "rc":
            pre_num += 1
        elif pre_type in ["alpha", "beta"]:
            pre_type = "rc"
            pre_num = 1
        else:
            patch += 1
            pre_type = "rc"
            pre_num = 1
    else:
        raise ValueError(f"Unknown bump type: {bump_type}")
    
    return format_version(major, minor, patch, pre_type, pre_num)


def update_version_in_files(old_version: str, new_version: str) -> None:
    """Update version in all version files."""
    for filename, pattern in VERSION_FILES:
        filepath = Path(filename)
        if not filepath.exists():
            print(f"Warning: {filename} not found, skipping...")
            continue
        
        content = filepath.read_text()
        new_content = re.sub(pattern, f'\\g<0>'.replace(old_version, new_version), content)
        
        if content != new_content:
            filepath.write_text(new_content)
            print(f"Updated {filename}: {old_version} -> {new_version}")
        else:
            print(f"No changes needed in {filename}")


def update_changelog(new_version: str) -> None:
    """Add new version section to changelog."""
    changelog_path = Path("CHANGELOG.md")
    if not changelog_path.exists():
        print("Warning: CHANGELOG.md not found, skipping...")
        return
    
    content = changelog_path.read_text()
    date_str = datetime.now().strftime("%Y-%m-%d")
    
    # Check if version already exists
    if f"## [{new_version}]" in content:
        print(f"Version {new_version} already exists in CHANGELOG.md")
        return
    
    # Find the insertion point (after the header, before the first version)
    lines = content.split('\n')
    insert_index = 0
    
    for i, line in enumerate(lines):
        if line.startswith("## ["):  # First version entry
            insert_index = i
            break
        elif line.strip() == "":  # Empty line after header
            insert_index = i + 1
    
    # Insert new version section
    new_section = [
        f"## [{new_version}] - {date_str}",
        "",
        "### Added",
        "- ",
        "",
        "### Changed",
        "- ",
        "",
        "### Fixed",
        "- ",
        "",
    ]
    
    lines[insert_index:insert_index] = new_section
    changelog_path.write_text('\n'.join(lines))
    print(f"Added version {new_version} to CHANGELOG.md")


def main():
    parser = argparse.ArgumentParser(description="Bump version for Marvin")
    parser.add_argument(
        "bump_type",
        nargs="?",
        choices=["major", "minor", "patch", "alpha", "beta", "rc"],
        help="Type of version bump"
    )
    parser.add_argument(
        "--current",
        action="store_true",
        help="Show current version"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without making changes"
    )
    
    args = parser.parse_args()
    
    try:
        current_version = get_current_version()
        
        if args.current or not args.bump_type:
            print(f"Current version: {current_version}")
            return
        
        new_version = bump_version(current_version, args.bump_type)
        print(f"Bumping version: {current_version} -> {new_version}")
        
        if not args.dry_run:
            update_version_in_files(current_version, new_version)
            update_changelog(new_version)
            print("\nVersion bump complete!")
            print(f"\nNext steps:")
            print(f"1. Update CHANGELOG.md with actual changes")
            print(f"2. Commit: git add -A && git commit -m 'chore: bump version to {new_version}'")
            print(f"3. Tag: git tag -a v{new_version} -m 'Release v{new_version}'")
            print(f"4. Push: git push && git push --tags")
        else:
            print("\nDry run complete. No files were modified.")
            
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()