"""
Unit tests for Cardinal Number Text Normalization
Tests the normalization of numbers 0-1000
"""

import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from cardinal_grammar import CardinalGrammar, TextNormalizer


class TestResults:
    """Track test results."""
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.failures = []
    
    def add_pass(self):
        self.passed += 1
    
    def add_fail(self, test_name, expected, got):
        self.failed += 1
        self.failures.append((test_name, expected, got))
    
    def print_summary(self):
        total = self.passed + self.failed
        print("\n" + "=" * 60)
        print("TEST SUMMARY")
        print("=" * 60)
        print(f"Total tests: {total}")
        print(f"Passed: {self.passed} ({100*self.passed/total:.1f}%)")
        print(f"Failed: {self.failed} ({100*self.failed/total:.1f}%)")
        
        if self.failures:
            print("\nFailed tests:")
            for test_name, expected, got in self.failures:
                print(f"  {test_name}")
                print(f"    Expected: {expected}")
                print(f"    Got:      {got}")
        
        return self.failed == 0


def test_single_digit():
    """Test single digit numbers (0-9)"""
    results = TestResults()
    grammar = CardinalGrammar()
    
    test_cases = [
        ("0", "zero"),
        ("1", "one"),
        ("2", "two"),
        ("3", "three"),
        ("4", "four"),
        ("5", "five"),
        ("6", "six"),
        ("7", "seven"),
        ("8", "eight"),
        ("9", "nine"),
    ]
    
    print("Testing single digits (0-9)...")
    for num, expected in test_cases:
        result = grammar.normalize_number(num)
        if result == expected:
            results.add_pass()
            print(f"  ✓ {num} -> {result}")
        else:
            results.add_fail(f"Single digit: {num}", expected, result)
            print(f"  ✗ {num} -> {result} (expected: {expected})")
    
    return results


def test_teens():
    """Test teen numbers (10-19)"""
    results = TestResults()
    grammar = CardinalGrammar()
    
    test_cases = [
        ("10", "ten"),
        ("11", "eleven"),
        ("12", "twelve"),
        ("13", "thirteen"),
        ("14", "fourteen"),
        ("15", "fifteen"),
        ("16", "sixteen"),
        ("17", "seventeen"),
        ("18", "eighteen"),
        ("19", "nineteen"),
    ]
    
    print("\nTesting teens (10-19)...")
    for num, expected in test_cases:
        result = grammar.normalize_number(num)
        if result == expected:
            results.add_pass()
            print(f"  ✓ {num} -> {result}")
        else:
            results.add_fail(f"Teen: {num}", expected, result)
            print(f"  ✗ {num} -> {result} (expected: {expected})")
    
    return results


def test_tens():
    """Test multiples of ten (20-90)"""
    results = TestResults()
    grammar = CardinalGrammar()
    
    test_cases = [
        ("20", "twenty"),
        ("30", "thirty"),
        ("40", "forty"),
        ("50", "fifty"),
        ("60", "sixty"),
        ("70", "seventy"),
        ("80", "eighty"),
        ("90", "ninety"),
    ]
    
    print("\nTesting tens (20-90)...")
    for num, expected in test_cases:
        result = grammar.normalize_number(num)
        if result == expected:
            results.add_pass()
            print(f"  ✓ {num} -> {result}")
        else:
            results.add_fail(f"Tens: {num}", expected, result)
            print(f"  ✗ {num} -> {result} (expected: {expected})")
    
    return results


def test_compound_two_digit():
    """Test compound two-digit numbers (21-99)"""
    results = TestResults()
    grammar = CardinalGrammar()
    
    test_cases = [
        ("21", "twenty-one"),
        ("22", "twenty-two"),
        ("35", "thirty-five"),
        ("42", "forty-two"),
        ("56", "fifty-six"),
        ("67", "sixty-seven"),
        ("78", "seventy-eight"),
        ("89", "eighty-nine"),
        ("99", "ninety-nine"),
    ]
    
    print("\nTesting compound two-digit numbers...")
    for num, expected in test_cases:
        result = grammar.normalize_number(num)
        if result == expected:
            results.add_pass()
            print(f"  ✓ {num} -> {result}")
        else:
            results.add_fail(f"Compound: {num}", expected, result)
            print(f"  ✗ {num} -> {result} (expected: {expected})")
    
    return results


def test_hundreds():
    """Test three-digit numbers (100-999)"""
    results = TestResults()
    grammar = CardinalGrammar()
    
    test_cases = [
        ("100", "one hundred"),
        ("101", "one hundred one"),
        ("110", "one hundred ten"),
        ("115", "one hundred fifteen"),
        ("120", "one hundred twenty"),
        ("123", "one hundred twenty-three"),
        ("200", "two hundred"),
        ("234", "two hundred thirty-four"),
        ("300", "three hundred"),
        ("456", "four hundred fifty-six"),
        ("500", "five hundred"),
        ("678", "six hundred seventy-eight"),
        ("789", "seven hundred eighty-nine"),
        ("900", "nine hundred"),
        ("999", "nine hundred ninety-nine"),
    ]
    
    print("\nTesting hundreds (100-999)...")
    for num, expected in test_cases:
        result = grammar.normalize_number(num)
        if result == expected:
            results.add_pass()
            print(f"  ✓ {num} -> {result}")
        else:
            results.add_fail(f"Hundreds: {num}", expected, result)
            print(f"  ✗ {num} -> {result} (expected: {expected})")
    
    return results


def test_thousand():
    """Test number 1000"""
    results = TestResults()
    grammar = CardinalGrammar()
    
    print("\nTesting 1000...")
    result = grammar.normalize_number("1000")
    expected = "one thousand"
    if result == expected:
        results.add_pass()
        print(f"  ✓ 1000 -> {result}")
    else:
        results.add_fail("Thousand: 1000", expected, result)
        print(f"  ✗ 1000 -> {result} (expected: {expected})")
    
    return results


def test_sentences():
    """Test normalization in complete sentences"""
    results = TestResults()
    normalizer = TextNormalizer()
    
    test_cases = [
        ("I have 3 dogs and 21 cats", "I have three dogs and twenty-one cats"),
        ("There are 42 students in the class", "There are forty-two students in the class"),
        ("The number is 0", "The number is zero"),
        ("She bought 100 apples", "She bought one hundred apples"),
        ("It costs 999 dollars", "It costs nine hundred ninety-nine dollars"),
        ("The year 1000 was important", "The year one thousand was important"),
        ("Room 205 has 15 seats", "Room two hundred five has fifteen seats"),
    ]
    
    print("\nTesting complete sentences...")
    for sentence, expected in test_cases:
        result = normalizer.normalize(sentence)
        if result == expected:
            results.add_pass()
            print(f"  ✓ {sentence}")
            print(f"    -> {result}")
        else:
            results.add_fail(f"Sentence: {sentence}", expected, result)
            print(f"  ✗ {sentence}")
            print(f"    Got:      {result}")
            print(f"    Expected: {expected}")
    
    return results


def run_all_tests():
    """Run all test suites"""
    print("=" * 60)
    print("CARDINAL NUMBER NORMALIZATION - UNIT TESTS")
    print("=" * 60)
    
    all_results = TestResults()
    
    # Run each test suite
    test_suites = [
        test_single_digit,
        test_teens,
        test_tens,
        test_compound_two_digit,
        test_hundreds,
        test_thousand,
        test_sentences,
    ]
    
    for test_suite in test_suites:
        suite_results = test_suite()
        all_results.passed += suite_results.passed
        all_results.failed += suite_results.failed
        all_results.failures.extend(suite_results.failures)
    
    # Print summary
    success = all_results.print_summary()
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(run_all_tests())
