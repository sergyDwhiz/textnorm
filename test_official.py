#!/usr/bin/env python3
"""
Test against official HuggingFace test cases
"""
import sys
import os
sys.path.insert(0, 'src')

from cardinal_grammar import TextNormalizer

def load_test_cases(filename):
    """Load test cases from file"""
    test_cases = []
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('~')
            if len(parts) == 2:
                input_text, expected = parts
                test_cases.append((input_text, expected))
    return test_cases

def filter_0_1000_range(test_cases):
    """Filter test cases to only include 0-1000 range (no commas, negatives, etc)"""
    filtered = []
    for input_text, expected in test_cases:
        # Skip if has comma, negative, or other special chars
        if ',' in input_text or '-' in input_text or '.' in input_text:
            continue
        
        # Try to parse as integer
        try:
            num = int(input_text)
            if 0 <= num <= 1000:
                filtered.append((input_text, expected))
        except ValueError:
            continue
    
    return filtered

def main():
    normalizer = TextNormalizer()
    
    # Load official test cases
    test_cases = load_test_cases('tests/test_cases_cardinal_en.txt')
    
    # Filter to 0-1000 range
    filtered_cases = filter_0_1000_range(test_cases)
    

    print(f"HuggingFace Test cases")
    print(f"Total cases in file: {len(test_cases)}")
    print(f"Cases in 0-1000 range: {len(filtered_cases)}")
    print()
    
    passed = 0
    failed = 0
    failures = []
    
    for input_text, expected in filtered_cases:
        result = normalizer.normalize(input_text)
        
        # Normalize expected output (remove "and", adjust spacing)
        expected_normalized = expected.replace(' and ', ' ').strip()
        result_normalized = result.strip()
        
        if result_normalized == expected_normalized or result == expected:
            passed += 1
            print(f"{input_text} - {result}")
        else:
            failed += 1
            failures.append((input_text, expected, result))
            print(f" {input_text}")
            print(f"  Expected: {expected}")
            print(f"  Got:      {result}")
    
    print()
    print(f"Passed: {passed}/{len(filtered_cases)} ({100*passed/len(filtered_cases):.1f}%)")
    print(f"Failed: {failed}/{len(filtered_cases)} ({100*failed/len(filtered_cases):.1f}%)")
    
    return 0 if failed == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
