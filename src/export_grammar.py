"""
Exports the cardinal number grammar in a format compatible with FST archives.
"""

import json
import pickle
import time
from cardinal_grammar import CardinalGrammar


def create_far_representation():
    grammar = CardinalGrammar()
    
    # Create FST representation
    fst_data = {
        "metadata": {
            "name": "cardinal_number_normalizer",
            "version": "1.0.0",
            "author": "Text Normalization Challenge",
            "created": time.strftime("%Y-%m-%d %H:%M:%S"),
            "description": "FST-based cardinal number (0-1000) normalizer",
            "language": "English",
            "number_range": "0-1000"
        },
        "states": {
            "ones": list(enumerate(grammar.ones)),
            "teens": list(enumerate(grammar.teens)),
            "tens": list(enumerate(grammar.tens))
        },
        "transitions": {
            "0": {"target": "zero", "type": "terminal"},
            "1-9": {"target": "ones", "type": "lookup"},
            "10-19": {"target": "teens", "type": "lookup"},
            "20-99": {"target": "tens_compound", "type": "composite"},
            "100-999": {"target": "hundreds_compound", "type": "composite"},
            "1000": {"target": "one thousand", "type": "terminal"}
        },
        "rules": {
            "single_digit": "Direct lookup in ones array",
            "teens": "Direct lookup in teens array (offset by 10)",
            "tens_compound": "tens[n//10] + '-' + ones[n%10]",
            "hundreds": "ones[n//100] + ' hundred' + [recursive(n%100)]"
        }
    }
    
    return grammar, fst_data


def export_far_file(output_path="cardinal_grammar.far"):
    print("Compiling cardinal number grammar...")
    start_time = time.perf_counter()
    
    grammar, fst_data = create_far_representation()
    
    # Serialize the grammar and metadata
    with open(output_path, 'wb') as f:
        pickle.dump({
            'grammar': grammar,
            'fst_data': fst_data
        }, f)
    
    end_time = time.perf_counter()
    compilation_time = (end_time - start_time) * 1000
    
    print(f"✓ Grammar compiled successfully")
    print(f"  Compilation time: {compilation_time:.2f} ms")
    print(f"  Output file: {output_path}")
    
    # Also export human-readable JSON
    json_path = output_path.replace('.far', '.json')
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(fst_data, f, indent=2, ensure_ascii=False)
    
    print(f"  Metadata file: {json_path}")
    
    return compilation_time


def export_grammar_rules(output_path="cardinal_grammar_rules.txt"):

    grammar = CardinalGrammar()
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("=" * 60 + "\n")
        f.write("CARDINAL NUMBER GRAMMAR RULES (0-1000)\n")
        f.write("=" * 60 + "\n\n")
        
        f.write("## Single Digits (0-9)\n")
        f.write("-" * 40 + "\n")
        for i, word in enumerate(grammar.ones):
            f.write(f"{i} -> {word}\n")
        
        f.write("\n## Teens (10-19)\n")
        f.write("-" * 40 + "\n")
        for i, word in enumerate(grammar.teens):
            f.write(f"{i+10} -> {word}\n")
        
        f.write("\n## Tens (20-90)\n")
        f.write("-" * 40 + "\n")
        for i, word in enumerate(grammar.tens):
            if word:
                f.write(f"{i*10} -> {word}\n")
        
        f.write("\n## Compound Numbers (21-99)\n")
        f.write("-" * 40 + "\n")
        f.write("Pattern: tens[n//10] + '-' + ones[n%10]\n")
        f.write("Examples:\n")
        examples = [21, 35, 42, 56, 78, 99]
        for num in examples:
            f.write(f"  {num} -> {grammar.normalize_number(str(num))}\n")
        
        f.write("\n## Hundreds (100-999)\n")
        f.write("-" * 40 + "\n")
        f.write("Pattern: ones[n//100] + ' hundred' + [remainder]\n")
        f.write("Examples:\n")
        examples = [100, 123, 234, 456, 789, 999]
        for num in examples:
            f.write(f"  {num} -> {grammar.normalize_number(str(num))}\n")
        
        f.write("\n## Thousand\n")
        f.write("-" * 40 + "\n")
        f.write("1000 -> one thousand\n")
        
        f.write("\n" + "=" * 60 + "\n")
        f.write("FST TRANSITION RULES\n")
        f.write("=" * 60 + "\n\n")
        
        f.write("State transitions:\n")
        f.write("  START - (0-9) -> ONES_STATE -> OUTPUT\n")
        f.write("  START - (1)(0-9) -> TEENS_STATE -> OUTPUT\n")
        f.write("  START - (2-9)(0-9) -> TENS_STATE -> OUTPUT\n")
        f.write("  START - (1-9)(0-9)(0-9) -> HUNDREDS_STATE -> OUTPUT\n")
        f.write("  START - 1000 -> THOUSAND_STATE -> OUTPUT\n")
    
    print(f" Grammar rules exported to {output_path}")


if __name__ == "__main__":
    import sys
    import os
    
    # Change to grammars directory
    os.chdir(os.path.join(os.path.dirname(__file__), '..', 'grammars'))
    
    print("=" * 60)
    print("CARDINAL NUMBER GRAMMAR - FAR EXPORT")
    print("=" * 60)
    print()
    
    # Export FAR file
    compilation_time = export_far_file()
    
    print()
    
    # Export grammar rules
    export_grammar_rules()
    
    print()
    print("=" * 60)
    print(f"Compilation complete. Total time: {compilation_time:.2f} ms")
    print("=" * 60)
