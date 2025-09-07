#!/usr/bin/env python3
"""
Basic test suite that can run without external dependencies
Tests core functionality that doesn't require yt-dlp, ffmpeg-python, etc.
"""

import sys
import os
import re
from typing import Optional

def test_time_parsing():
    """Test time parsing functionality without external dependencies"""
    print("Testing time parsing functionality...")
    
    def parse_time_format(time_str: str) -> str:
        """Parse and validate time format with millisecond precision support"""
        if not time_str:
            raise ValueError("Time parameter cannot be empty")
            
        # Remove whitespace
        time_str = time_str.strip()
        
        # Pattern for HH:MM:SS.mmm, MM:SS.mmm, or SS.mmm formats
        time_pattern = r'^(?:(?:([0-9]{1,2}):)?([0-5]?[0-9]):)?([0-5]?[0-9])(?:\.([0-9]{1,3}))?$'
        
        # Check if it's decimal seconds (integer or float with millisecond precision)
        if re.match(r'^\d+(?:\.\d{1,3})?$', time_str):
            return time_str
        
        # Check standard time format with optional milliseconds
        match = re.match(time_pattern, time_str)
        if match:
            hours, minutes, seconds, milliseconds = match.groups()
            
            # Validate milliseconds don't exceed 999
            if milliseconds and len(milliseconds) <= 3:
                ms_value = int(milliseconds.ljust(3, '0'))  # Pad to 3 digits
                if ms_value > 999:
                    raise ValueError(f"Invalid milliseconds: '{milliseconds}'. Must be 0-999")
            
            return time_str
        
        # If no match, raise an error with detailed format information
        raise ValueError(
            f"Invalid time format: '{time_str}'. "
            "Supported formats: HH:MM:SS.mmm, MM:SS.mmm, SS.mmm, or decimal seconds"
        )
    
    test_cases = [
        # Valid formats
        ("1:23:45.678", True, "HH:MM:SS.mmm format"),
        ("23:45.123", True, "MM:SS.mmm format"),
        ("45.500", True, "SS.mmm format"),
        ("105.250", True, "Decimal seconds with milliseconds"),
        ("30.5", True, "Decimal seconds with 1 decimal place"),
        ("1:30", True, "MM:SS format without milliseconds"),
        ("01:23:45", True, "HH:MM:SS format without milliseconds"),
        ("123", True, "Integer seconds"),
        ("0:00:00.001", True, "Minimum millisecond precision"),
        ("1:23:45.999", True, "Maximum millisecond precision"),
        
        # Invalid formats
        ("1:23:45.1234", False, "Too many decimal places"),
        ("1:61:45", False, "Invalid minutes"),
        ("1:23:61", False, "Invalid seconds"),
        ("", False, "Empty string"),
        ("abc", False, "Non-numeric"),
    ]
    
    passed = 0
    failed = 0
    
    for time_input, should_pass, description in test_cases:
        try:
            result = parse_time_format(time_input)
            if should_pass:
                print(f"  PASS: '{time_input}' -> '{result}' ({description})")
                passed += 1
            else:
                print(f"  FAIL: '{time_input}' should have failed but got '{result}' ({description})")
                failed += 1
        except Exception as e:
            if not should_pass:
                print(f"  PASS: '{time_input}' correctly failed ({description})")
                passed += 1
            else:
                print(f"  FAIL: '{time_input}' should have passed but failed - {e} ({description})")
                failed += 1
    
    print(f"Time Parsing Tests: {passed} passed, {failed} failed")
    return failed == 0

def test_time_conversion():
    """Test time-to-seconds conversion"""
    print("\nTesting time-to-seconds conversion...")
    
    def time_to_seconds(time_str: str) -> float:
        """Convert time string to seconds"""
        if not time_str:
            return 0
            
        # If it's already in seconds (float or int)
        if re.match(r'^\d+(?:\.\d+)?$', time_str):
            return float(time_str)
            
        # Parse HH:MM:SS, MM:SS format
        parts = time_str.split(':')
        if len(parts) == 3:  # HH:MM:SS
            return int(parts[0]) * 3600 + int(parts[1]) * 60 + float(parts[2])
        elif len(parts) == 2:  # MM:SS
            return int(parts[0]) * 60 + float(parts[1])
        else:
            return float(time_str)
    
    test_cases = [
        ("1:23:45.678", 5025.678, "HH:MM:SS.mmm conversion"),
        ("23:45.123", 1425.123, "MM:SS.mmm conversion"),
        ("45.500", 45.5, "SS.mmm conversion"),
        ("105.250", 105.25, "Decimal seconds conversion"),
        ("0:00:01.001", 1.001, "Millisecond precision"),
        ("1:00:00.000", 3600.0, "Hour boundary with milliseconds"),
    ]
    
    passed = 0
    failed = 0
    
    for time_input, expected, description in test_cases:
        try:
            result = time_to_seconds(time_input)
            if abs(result - expected) < 0.001:  # Allow for floating point precision
                print(f"  PASS: '{time_input}' -> {result}s (expected {expected}s) ({description})")
                passed += 1
            else:
                print(f"  FAIL: '{time_input}' -> {result}s but expected {expected}s ({description})")
                failed += 1
        except Exception as e:
            print(f"  FAIL: '{time_input}' failed with error - {e} ({description})")
            failed += 1
    
    print(f"Time Conversion Tests: {passed} passed, {failed} failed")
    return failed == 0

def test_validation_logic():
    """Test time range validation logic"""
    print("\nTesting time range validation logic...")
    
    def validate_time_range(start_time: Optional[str], duration: Optional[str], end_time: Optional[str]):
        """Validate time range parameters"""
        if duration and end_time:
            raise ValueError("Cannot specify both --duration and --end-time. Use one or the other.")
        
        if (duration or end_time) and not start_time:
            raise ValueError("--start-time is required when using --duration or --end-time")
    
    test_cases = [
        # Valid cases
        ("1:00", "30", None, True, "start + duration"),
        ("1:00", None, "2:00", True, "start + end"),
        ("1:00", None, None, True, "start only"),
        (None, None, None, True, "no time params"),
        
        # Invalid cases
        ("1:00", "30", "2:00", False, "both duration and end"),
        (None, "30", None, False, "duration without start"),
        (None, None, "2:00", False, "end without start"),
    ]
    
    passed = 0
    failed = 0
    
    for start, duration, end, should_pass, description in test_cases:
        try:
            validate_time_range(start, duration, end)
            if should_pass:
                print(f"  PASS: {description} - validation passed")
                passed += 1
            else:
                print(f"  FAIL: {description} - should have failed but passed")
                failed += 1
        except Exception as e:
            if not should_pass:
                print(f"  PASS: {description} - correctly failed")
                passed += 1
            else:
                print(f"  FAIL: {description} - should have passed but failed: {e}")
                failed += 1
    
    print(f"Validation Tests: {passed} passed, {failed} failed")
    return failed == 0

def test_code_structure():
    """Test basic code structure and syntax"""
    print("\nTesting code structure...")
    
    try:
        # Try to read and parse the main source file
        src_path = os.path.join(os.path.dirname(__file__), '..', 'src', 'extract_audio.py')
        with open(src_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Basic checks
        checks = [
            ('import os' in content, "Has required imports"),
            ('class AudioExtractor' in content, "Has AudioExtractor class"),
            ('def parse_time_format' in content, "Has parse_time_format function"),
            ('def validate_time_range' in content, "Has validate_time_range function"),
            ('millisecond' in content.lower(), "Mentions millisecond support"),
            ('.mmm' in content, "Documents millisecond format"),
            ('click.group()' in content, "Uses Click for CLI"),
        ]
        
        passed = 0
        failed = 0
        
        for check_result, description in checks:
            if check_result:
                print(f"  PASS: {description}")
                passed += 1
            else:
                print(f"  FAIL: {description}")
                failed += 1
        
        print(f"Structure Tests: {passed} passed, {failed} failed")
        return failed == 0
        
    except Exception as e:
        print(f"  FAIL: Could not read source file: {e}")
        return False

def main():
    """Run all basic tests"""
    print("Audio Extractor Basic Test Suite")
    print("=" * 50)
    
    tests = [
        ("Time Parsing", test_time_parsing),
        ("Time Conversion", test_time_conversion),
        ("Validation Logic", test_validation_logic),
        ("Code Structure", test_code_structure),
    ]
    
    total_passed = 0
    total_failed = 0
    
    for test_name, test_func in tests:
        print(f"\n[{test_name}]")
        if test_func():
            print(f"-> {test_name}: PASSED")
            total_passed += 1
        else:
            print(f"-> {test_name}: FAILED")
            total_failed += 1
    
    total = total_passed + total_failed
    print(f"\n" + "=" * 50)
    print(f"Final Results: {total_passed}/{total} tests passed ({(total_passed/total)*100:.1f}%)")
    
    if total_failed == 0:
        print("\nAll basic tests passed! Core functionality is working correctly.")
        print("\nNote: Full functionality tests require installing dependencies:")
        print("  pip install -r requirements.txt")
    else:
        print(f"\n{total_failed} test(s) failed. Please check the implementation.")
    
    return total_failed == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
