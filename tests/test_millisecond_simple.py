#!/usr/bin/env python3
"""
Simple test for millisecond precision support - Windows compatible
"""

import re

def parse_time_format(time_str: str) -> str:
    """Parse and validate time format with millisecond precision support"""
    if not time_str:
        raise ValueError("Time parameter cannot be empty")
        
    time_str = time_str.strip()
    time_pattern = r'^(?:(?:([0-9]{1,2}):)?([0-5]?[0-9]):)?([0-5]?[0-9])(?:\.([0-9]{1,3}))?$'
    
    if re.match(r'^\d+(?:\.\d{1,3})?$', time_str):
        return time_str
    
    match = re.match(time_pattern, time_str)
    if match:
        hours, minutes, seconds, milliseconds = match.groups()
        if milliseconds and len(milliseconds) <= 3:
            ms_value = int(milliseconds.ljust(3, '0'))
            if ms_value > 999:
                raise ValueError(f"Invalid milliseconds: '{milliseconds}'. Must be 0-999")
        return time_str
    
    raise ValueError(f"Invalid time format: '{time_str}'")

def time_to_seconds(time_str: str) -> float:
    """Convert time string to seconds"""
    if not time_str:
        return 0
        
    if re.match(r'^\d+(?:\.\d+)?$', time_str):
        return float(time_str)
        
    parts = time_str.split(':')
    if len(parts) == 3:  # HH:MM:SS
        return int(parts[0]) * 3600 + int(parts[1]) * 60 + float(parts[2])
    elif len(parts) == 2:  # MM:SS
        return int(parts[0]) * 60 + float(parts[1])
    else:
        return float(time_str)

def main():
    print("Audio Extractor Millisecond Support Test")
    print("=" * 45)
    
    # Test cases
    test_cases = [
        ("1:23:45.678", True),
        ("23:45.123", True),
        ("45.500", True),
        ("105.250", True),
        ("1:23:45.1234", False),  # Too many decimals
        ("", False),  # Empty
    ]
    
    passed = 0
    total = len(test_cases)
    
    print("Testing time parsing...")
    for time_input, should_pass in test_cases:
        try:
            result = parse_time_format(time_input)
            if should_pass:
                print(f"  PASS: '{time_input}' -> '{result}'")
                passed += 1
            else:
                print(f"  FAIL: '{time_input}' should have failed")
        except Exception:
            if not should_pass:
                print(f"  PASS: '{time_input}' correctly rejected")
                passed += 1
            else:
                print(f"  FAIL: '{time_input}' should have passed")
    
    # Test conversion
    print("\nTesting time conversion...")
    conversion_tests = [
        ("1:23:45.678", 5025.678),
        ("23:45.123", 1425.123),
        ("105.250", 105.25),
    ]
    
    for time_input, expected in conversion_tests:
        try:
            result = time_to_seconds(time_input)
            if abs(result - expected) < 0.001:
                print(f"  PASS: '{time_input}' -> {result}s")
                passed += 1
            else:
                print(f"  FAIL: '{time_input}' -> {result}s (expected {expected}s)")
        except Exception as e:
            print(f"  FAIL: '{time_input}' failed: {e}")
    
    total += len(conversion_tests)
    
    print(f"\nResults: {passed}/{total} tests passed")
    
    if passed == total:
        print("SUCCESS: All millisecond tests passed!")
        return True
    else:
        print(f"FAILURE: {total - passed} tests failed")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
