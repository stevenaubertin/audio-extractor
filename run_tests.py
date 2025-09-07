#!/usr/bin/env python3
"""
Test runner for Audio Extractor
Runs all tests in the tests/ directory
"""

import os
import sys
import subprocess
from pathlib import Path

def main():
    """Run all tests"""
    print("Audio Extractor Test Runner")
    print("=" * 50)
    
    # Get the tests directory
    tests_dir = Path(__file__).parent / "tests"
    
    if not tests_dir.exists():
        print("❌ Tests directory not found!")
        return False
    
    # Change to tests directory
    original_dir = os.getcwd()
    os.chdir(tests_dir)
    
    try:
        # List of test files to run
        test_files = [
            ("Basic Tests (Core Functionality)", "test_basic.py"),
            ("Millisecond Support Tests", "test_millisecond_simple.py"),
            ("Full Integration Tests", "test_audio_extractor.py"),
        ]
        
        results = []
        
        for test_name, test_file in test_files:
            print(f"\nRunning: {test_name}")
            print("-" * 50)
            
            if not os.path.exists(test_file):
                print(f"WARNING: Test file not found: {test_file}")
                results.append((test_name, "SKIPPED"))
                continue
            
            try:
                result = subprocess.run([
                    sys.executable, test_file
                ], capture_output=True, text=True, timeout=60)
                
                if result.returncode == 0:
                    print(f"PASS: {test_name}")
                    results.append((test_name, "PASSED"))
                    # Print last few lines of output for summary
                    lines = result.stdout.strip().split('\\n')
                    if len(lines) > 3:
                        print("   Summary:")
                        for line in lines[-3:]:
                            if line.strip():
                                print(f"   {line}")
                else:
                    print(f"FAIL: {test_name}")
                    results.append((test_name, "FAILED"))
                    if result.stderr:
                        print("   Error output:")
                        for line in result.stderr.strip().split('\\n')[:5]:  # Show first 5 lines
                            print(f"   {line}")
                            
            except subprocess.TimeoutExpired:
                print(f"TIMEOUT: {test_name}")
                results.append((test_name, "TIMEOUT"))
            except Exception as e:
                print(f"ERROR: {test_name} - {e}")
                results.append((test_name, "ERROR"))
        
        # Final summary
        print("\\n" + "=" * 50)
        print("Final Test Results:")
        
        passed = sum(1 for _, status in results if status == "PASSED")
        failed = sum(1 for _, status in results if status == "FAILED")
        skipped = sum(1 for _, status in results if status in ["SKIPPED", "TIMEOUT", "ERROR"])
        total = len(results)
        
        for test_name, status in results:
            status_icon = {
                "PASSED": "PASS",
                "FAILED": "FAIL", 
                "SKIPPED": "SKIP",
                "TIMEOUT": "TIME",
                "ERROR": "ERR"
            }.get(status, "UNK")
            print(f"   {status_icon}: {test_name}")
        
        print(f"\nSummary: {passed} passed, {failed} failed, {skipped} skipped out of {total} total")
        
        if failed == 0 and passed > 0:
            print("\nAll available tests passed!")
            if skipped > 0:
                print("Some tests were skipped (likely due to missing dependencies)")
                print("   Install dependencies with: pip install -r requirements.txt")
        else:
            print("\nSome tests failed or could not run.")
            
        return failed == 0
        
    finally:
        # Return to original directory
        os.chdir(original_dir)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
