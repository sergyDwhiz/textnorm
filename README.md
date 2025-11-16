# Text Normalization - Cardinal Numbers

Converts numbers from 0-1000 to words using FST approach.

## What it does

It takes numbers in text and writes them out in plain lanaguage:
E.g:
- "I have 3 dogs" becomes "I have three dogs"
- "Room 42" becomes "Room forty-two"

## How to use

Basic usage:
```bash
python3 src/normalize.py "I have 3 dogs and 21 cats"
```

For files:
```bash
python3 src/normalize.py --file input.txt --output output.txt
```

Using the compiled grammar:
```python
import pickle

with open('grammars/cardinal_grammar.far', 'rb') as f:
    data = pickle.load(f)
    grammar = data['grammar']

result = grammar.normalize_number("42")
print(result)  # forty-two
```

## Testing

```bash
python tests/test_cardinal.py
```

## Implementation details

The grammar has lookup tables for:
- digits 0-9
- teens 10-19
- tens (20, 30, 40 etc)

Then combines them for bigger numbers. Like 42 = "forty" + "-" + "two".

For hundreds it's similar, just adds "hundred" in the middle.

1000 is just hardcoded as "one thousand".

## Requirements
Python 3.7+ 

