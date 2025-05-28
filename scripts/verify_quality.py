#!/usr/bin/env python3
"""
Comprehensive quality verification script for Marvin.

This script runs all quality checks and provides a proof of 100% test coverage
and overall code quality. It's used for README demonstration and CI verification.
"""
import subprocess
import sys
import json
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, Any, Tuple


class QualityVerifier:
    """Verify all aspects of code quality."""
    
    def __init__(self):
        self.results: Dict[str, Any] = {}
        self.project_root = Path(__file__).parent.parent
        
    def run_command(self, cmd: str, description: str) -> Tuple[bool, str]:
        """Run a command and capture its output."""
        try:
            result = subprocess.run(
                cmd.split(),
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=300  # 5 minutes timeout
            )
            return result.returncode == 0, result.stdout + result.stderr
        except subprocess.TimeoutExpired:
            return False, f"Command timed out: {cmd}"
        except Exception as e:
            return False, f"Error running command: {e}"
    
    def check_test_coverage(self) -> bool:
        """Check test coverage and verify it's 100%."""
        print("🧪 Checking test coverage...")
        
        # Run pytest with coverage
        success, output = self.run_command(
            "uv run pytest --cov=marvin --cov-report=xml --cov-report=term-missing -q",
            "Running tests with coverage"
        )
        
        if not success:
            print(f"❌ Tests failed:\n{output}")
            return False
        
        # Parse coverage from XML report
        coverage_file = self.project_root / "coverage.xml"
        if coverage_file.exists():
            try:
                tree = ET.parse(coverage_file)
                root = tree.getroot()
                coverage_percent = float(root.attrib.get('line-rate', 0)) * 100
                
                self.results['coverage'] = {
                    'percentage': coverage_percent,
                    'target': 100.0,
                    'passed': coverage_percent >= 100.0
                }
                
                if coverage_percent >= 100.0:
                    print(f"✅ Test Coverage: {coverage_percent:.1f}%")
                    return True
                else:
                    print(f"❌ Test Coverage: {coverage_percent:.1f}% (below 100%)")
                    return False
                    
            except Exception as e:
                print(f"❌ Failed to parse coverage report: {e}")
                return False
        else:
            print("❌ Coverage report not found")
            return False
    
    def check_test_count(self) -> bool:
        """Count and verify test execution."""
        print("📊 Counting tests...")
        
        success, output = self.run_command(
            "uv run pytest --collect-only -q",
            "Collecting tests"
        )
        
        if success:
            # Extract test count from output
            lines = output.split('\n')
            for line in lines:
                if 'collected' in line and 'item' in line:
                    # Parse "collected X items"
                    parts = line.split()
                    if len(parts) >= 2:
                        try:
                            test_count = int(parts[1])
                            self.results['test_count'] = test_count
                            print(f"✅ Tests Collected: {test_count}")
                            return True
                        except ValueError:
                            pass
        
        print("❌ Failed to count tests")
        return False
    
    def check_formatting(self) -> bool:
        """Check code formatting with Black."""
        print("🎨 Checking code formatting...")
        
        success, output = self.run_command(
            "uv run black src tests --check --quiet",
            "Checking Black formatting"
        )
        
        self.results['formatting'] = success
        if success:
            print("✅ Code Formatting: OK")
        else:
            print(f"❌ Code Formatting: FAILED\n{output}")
        
        return success
    
    def check_import_sorting(self) -> bool:
        """Check import sorting with isort."""
        print("📦 Checking import sorting...")
        
        success, output = self.run_command(
            "uv run isort src tests --check-only --quiet",
            "Checking isort"
        )
        
        self.results['import_sorting'] = success
        if success:
            print("✅ Import Sorting: OK")
        else:
            print(f"❌ Import Sorting: FAILED\n{output}")
        
        return success
    
    def check_linting(self) -> bool:
        """Check linting with Ruff."""
        print("🔍 Checking linting...")
        
        success, output = self.run_command(
            "uv run ruff check src tests --quiet",
            "Running Ruff linter"
        )
        
        self.results['linting'] = success
        if success:
            print("✅ Linting: OK")
        else:
            print(f"❌ Linting: FAILED\n{output}")
        
        return success
    
    def check_type_checking(self) -> bool:
        """Check type checking with MyPy."""
        print("📝 Checking type annotations...")
        
        success, output = self.run_command(
            "uv run mypy src --quiet",
            "Running MyPy type checker"
        )
        
        self.results['type_checking'] = success
        if success:
            print("✅ Type Checking: OK")
        else:
            print(f"❌ Type Checking: FAILED\n{output}")
        
        return success
    
    def check_security(self) -> bool:
        """Check for security issues with Bandit."""
        print("🔒 Checking security...")
        
        success, output = self.run_command(
            "uv run bandit -r src -ll --quiet",
            "Running Bandit security scan"
        )
        
        self.results['security'] = success
        if success:
            print("✅ Security Scan: OK")
        else:
            print(f"⚠️ Security Scan: Issues found\n{output}")
        
        return success
    
    def check_test_files_exist(self) -> bool:
        """Verify test files exist for all source files."""
        print("📋 Checking test file coverage...")
        
        success, output = self.run_command(
            "python scripts/check_test_exists.py src/marvin/*.py src/marvin/*/*.py",
            "Checking test file existence"
        )
        
        self.results['test_files'] = success
        if success:
            print("✅ Test Files: All source files have tests")
        else:
            print(f"❌ Test Files: Missing tests\n{output}")
        
        return success
    
    def generate_report(self) -> Dict[str, Any]:
        """Generate comprehensive quality report."""
        print("\n" + "="*60)
        print("📊 QUALITY VERIFICATION REPORT")
        print("="*60)
        
        checks = [
            ('Test Coverage', self.check_test_coverage),
            ('Test Count', self.check_test_count),
            ('Code Formatting', self.check_formatting),
            ('Import Sorting', self.check_import_sorting),
            ('Linting', self.check_linting),
            ('Type Checking', self.check_type_checking),
            ('Security Scan', self.check_security),
            ('Test Files', self.check_test_files_exist),
        ]
        
        passed_checks = 0
        total_checks = len(checks)
        
        print()
        for name, check_func in checks:
            try:
                if check_func():
                    passed_checks += 1
            except Exception as e:
                print(f"❌ {name}: ERROR - {e}")
        
        print("\n" + "="*60)
        print(f"📈 SUMMARY: {passed_checks}/{total_checks} checks passed")
        
        if passed_checks == total_checks:
            print("🎉 ALL QUALITY CHECKS PASSED!")
            print("\n✨ Marvin achieves 100% test coverage and quality!")
            print("🚀 Ready for production deployment!")
            success = True
        else:
            print("❌ Some quality checks failed.")
            print("🔧 Please fix the issues before proceeding.")
            success = False
        
        print("="*60)
        
        # Write results to file for CI
        report_file = self.project_root / "quality_report.json"
        report_data = {
            'timestamp': subprocess.check_output(['date', '-Iseconds']).decode().strip(),
            'passed_checks': passed_checks,
            'total_checks': total_checks,
            'success': success,
            'results': self.results
        }
        
        with open(report_file, 'w') as f:
            json.dump(report_data, f, indent=2)
        
        print(f"\n📄 Detailed report saved to: {report_file}")
        
        return report_data


def main():
    """Main entry point."""
    print("🔍 Starting comprehensive quality verification for Marvin...")
    print("="*60)
    
    verifier = QualityVerifier()
    report = verifier.generate_report()
    
    # Exit with appropriate code
    sys.exit(0 if report['success'] else 1)


if __name__ == "__main__":
    main()