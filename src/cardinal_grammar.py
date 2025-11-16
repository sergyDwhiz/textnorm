"""
Converts numbers 0-1000 to their written form using a rule-based FST-inspired approach.
"""

import re


class CardinalGrammar:
    def __init__(self):
        """Initialize the cardinal number grammar with lookup tables."""
        # Basic number words
        self.ones = [
            "zero", "one", "two", "three", "four",
            "five", "six", "seven", "eight", "nine"
        ]
        
        self.teens = [
            "ten", "eleven", "twelve", "thirteen", "fourteen",
            "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"
        ]
        
        self.tens = [
            "", "", "twenty", "thirty", "forty",
            "fifty", "sixty", "seventy", "eighty", "ninety"
        ]
    
    def normalize_number(self, num_str):
        """
        Convert a number string to its written form.
        
        Args:
            num_str: String representation of a number (0-1000)
        
        Returns:
            Written form of the number
        """
        try:
            # Check for leading zeros - read digit by digit
            if len(num_str) > 1 and num_str[0] == '0':
                return ' '.join(self.ones[int(d)] for d in num_str)
            
            num = int(num_str)
            
            if num < 0 or num > 1000:
                return num_str  # Out of range, return as-is
            
            if num == 0:
                return "zero"
            elif num == 1000:
                return "one thousand"
            elif num < 10:
                return self.ones[num]
            elif num < 20:
                return self.teens[num - 10]
            elif num < 100:
                return self._two_digits(num)
            else:  # 100-999
                return self._three_digits(num)
                
        except ValueError:
            return num_str  # Invalid number, return as-is
    
    def _two_digits(self, num):
        """Convert two-digit number (10-99) to words."""
        tens_digit = num // 10
        ones_digit = num % 10
        
        if ones_digit == 0:
            return self.tens[tens_digit]
        else:
            return f"{self.tens[tens_digit]} {self.ones[ones_digit]}"
    
    def _three_digits(self, num):
        """Convert three-digit number (100-999) to words."""
        hundreds_digit = num // 100
        remainder = num % 100
        
        result = f"{self.ones[hundreds_digit]} hundred"
        
        if remainder == 0:
            return result
        elif remainder < 10:
            return f"{result} and {self.ones[remainder]}"
        elif remainder < 20:
            return f"{result} and {self.teens[remainder - 10]}"
        else:
            return f"{result} and {self._two_digits(remainder)}"
    
    def get_fst(self):
        """Return a representation of the FST (for compatibility)."""
        return self


class TextNormalizer:
    """
    Text normalizer that processes sentences and normalizes cardinal numbers.
    """
    
    def __init__(self):
        """Initialize the text normalizer with cardinal grammar."""
        self.grammar = CardinalGrammar()
        # Pattern to match numbers in text
        self.number_pattern = re.compile(r'\b\d+\b')
    
    def normalize(self, text):
        """
        Normalize cardinal numbers in text.
        
        Args:
            text: Input text containing cardinal numbers
        
        Returns:
            Text with numbers converted to written form
        """
        def replace_number(match):
            number_str = match.group(0)
            return self.grammar.normalize_number(number_str)
        
        return self.number_pattern.sub(replace_number, text)


if __name__ == "__main__":
    # Test the grammar
    grammar = CardinalGrammar()
    
    test_numbers = [
        "0", "1", "5", "9", "10", "11", "12", "15", "19",
        "20", "21", "23", "30", "42", "50", "99",
        "100", "101", "105", "110", "115", "120", "123",
        "200", "234", "300", "456", "789", "999", "1000"
    ]
    
    print("Cardinal Number Grammar Test:")
    for num in test_numbers:
        result = grammar.normalize_number(num)
        print(f"{num:>4} -> {result}")
    
    print("\n" + "=" * 50)
    print("Text Normalization Test:")
    
    normalizer = TextNormalizer()
    
    test_sentences = [
        "I have 3 dogs and 21 cats",
        "There are 42 students in the class",
        "The number is 0",
        "She bought 100 apples and 25 oranges",
        "It costs 999 dollars",
        "The year 1000 was important"
    ]
    
    for sentence in test_sentences:
        normalized = normalizer.normalize(sentence)
        print(f"Input : {sentence}")
        print(f"Output: {normalized}")
        print()
