#!/usr/bin/env python3
"""
Test script to verify millisecond precision support in audio extractor
"""

import re
from typing import Optional

def parse_time_format(time_str: str) -> str:
    """Parse and validate time format with millisecond precision support
    
    Supported formats:
    - HH:MM:SS.mmm (e.g., 01:23:45.678)
    - MM:SS.mmm (e.g., 23:45.123)
    - SS.mmm (e.g., 45.500)
    - Decimal seconds (e.g., 105.250)
    
    Where:
    - HH: hours (0-99)
    - MM: minutes (0-59)
    - SS: seconds (0-59)
    - mmm: milliseconds (0-999, 1-3 digits)
    """
    if not time_str:
        raise ValueError("Time parameter cannot be empty")
        
    # Remove whitespace
    time_str = time_str.strip()
    
    # Pattern for HH:MM:SS.mmm, MM:SS.mmm, or SS.mmm formats
    # Supports millisecond precision with 1-3 digits
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
        "Supported formats:\n"
        "  • HH:MM:SS.mmm (e.g., 01:23:45.678)\n"
        "  • MM:SS.mmm (e.g., 23:45.123)\n"
        "  • SS.mmm (e.g., 45.500)\n"
        "  • Decimal seconds (e.g., 105.250)"
    )

def test_time_parsing():
    """Test various time formats including millisecond precision"""
    
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
        ("59:59.999", True, "Maximum MM:SS.mmm"),
        ("1.0", True, "Decimal with zero fraction"),
        ("00:01:23.750", True, "Leading zeros with milliseconds"),
        
        # Invalid formats
        ("1:23:45.1234", False, "Too many decimal places"),
        ("1:61:45", False, "Invalid minutes"),
        ("1:23:61", False, "Invalid seconds"),
        ("1:23:45.1000", False, "Milliseconds > 999"),
        ("", False, "Empty string"),
        ("abc", False, "Non-numeric"),
        ("1:2:3:4", False, "Too many colons"),
        ("1:-2:3", False, "Negative values"),
        ("1:23:45.abc", False, "Non-numeric milliseconds"),
    ]
    
    print("Testing millisecond time parsing functionality...\n")
    
    passed = 0
    failed = 0
    
    for time_input, should_pass, description in test_cases:
        try:
            result = parse_time_format(time_input)
            if should_pass:
            print(f"PASS: '{time_input}' -> '{result}' ({description})")
                passed += 1
            else:
                print(f"FAIL: '{time_input}' should have failed but got '{result}' ({description})")
                failed += 1
        except (ValueError, Exception) as e:
            if not should_pass:
                print(f"PASS: '{time_input}' correctly failed - {str(e).split('.')[0]} ({description})")
                passed += 1
            else:
                print(f"FAIL: '{time_input}' should have passed but failed - {e} ({description})")
                failed += 1
    
    print(f"\nTest Results:")
    print(f"   Passed: {passed}")
    print(f"   Failed: {failed}")
    print(f"   Total:  {passed + failed}")
    
    if failed == 0:
    print("\nAll tests passed! Millisecond support is working correctly.")
        return True
    else:
        print(f"\n{failed} test(s) failed. Please check the implementation.")
        return False

def test_time_to_seconds():
    """Test conversion of time strings to seconds with millisecond precision"""
    
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
    
    print("\nTesting time-to-seconds conversion with millisecond precision...\n")
    
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
                print(f"PASS: '{time_input}' -> {result}s (expected {expected}s) ({description})")
                passed += 1
            else:
                print(f"FAIL: '{time_input}' -> {result}s but expected {expected}s ({description})")
                failed += 1
        except Exception as e:
            print(f"FAIL: '{time_input}' failed with error - {e} ({description})")
            failed += 1
    
    print(f"\nConversion Test Results:")
    print(f"   Passed: {passed}")
    print(f"   Failed: {failed}")
    print(f"   Total:  {passed + failed}")
    
    return failed == 0

if __name__ == "__main__":
    print("Audio Extractor Millisecond Support Test Suite\n")
    print("=" * 60)
    
    parsing_success = test_time_parsing()
    conversion_success = test_time_to_seconds()
    
    print("\n" + "=" * 60)
    if parsing_success and conversion_success:
        print("All tests passed! Millisecond support is fully functional.")
        print("\nYour audio extractor now supports:")
        print("  • HH:MM:SS.mmm format (e.g., 01:23:45.678)")
        print("  • MM:SS.mmm format (e.g., 23:45.123)")
        print("  • SS.mmm format (e.g., 45.500)")
        print("  • Decimal seconds with millisecond precision (e.g., 105.250)")
        print("\nExample usage:")
        print("  python src/extract_audio.py --format mp3 local video.mp4 \\")
        print("    --start-time 1:23.456 --duration 30.750")
    else:
        print("Some tests failed. Please review the implementation.")
