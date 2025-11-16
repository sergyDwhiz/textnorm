#!/usr/bin/env python3
"""

Main script for normalizing cardinal numbers (0-1000) in sentences.
Usage:
    python normalize.py "I have 3 dogs and 21 cats"
    python normalize.py --file input.txt --output output.txt
    python normalize.py --interactive
"""

import argparse
import sys
import time
from cardinal_grammar import TextNormalizer


def normalize_text(text, normalizer):
    start_time = time.perf_counter()
    normalized = normalizer.normalize(text)
    end_time = time.perf_counter()
    
    processing_time = (end_time - start_time) * 1000  # Convert to milliseconds
    return normalized, processing_time


def process_file(input_file, output_file, normalizer):
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        total_time = 0
        normalized_lines = []
        
        print(f"Processing {len(lines)} lines...")
        for i, line in enumerate(lines, 1):
            normalized, proc_time = normalize_text(line.strip(), normalizer)
            normalized_lines.append(normalized)
            total_time += proc_time
            
            if i % 100 == 0:
                print(f"Processed {i}/{len(lines)} lines...")
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(normalized_lines))
        
        print(f"\n Processing complete")
        print(f"  Total lines: {len(lines)}")
        print(f"  Total time: {total_time:.2f} ms")
        print(f"  Average time per line: {total_time/len(lines):.3f} ms")
        print(f"  Output written to: {output_file}")
        
    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error processing file: {e}", file=sys.stderr)
        sys.exit(1)


def interactive_mode(normalizer):
    print("=" * 60)
    print("Text Normalization ")
    print("=" * 60)
    print("Enter text to normalize (or 'quit' to exit):\n")
    
    while True:
        try:
            text = input("> ")
            
            if text.lower() in ['quit', 'exit', 'q']:
                print("Goodbye!")
                break
            
            if not text.strip():
                continue
            
            normalized, proc_time = normalize_text(text, normalizer)
            print(f"Normalized: {normalized}")
            print(f"Time: {proc_time:.3f} ms\n")
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except EOFError:
            break


def main():
    """Main entry point for the text normalization system."""
    parser = argparse.ArgumentParser(
        description="Normalize cardinal numbers (0-1000) in text.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s "I have 3 dogs and 21 cats"
  %(prog)s --file input.txt --output output.txt
  %(prog)s --interactive
        """
    )
    
    parser.add_argument(
        'text',
        nargs='?',
        help='Text to normalize (if not using --file or --interactive)'
    )
    
    parser.add_argument(
        '--file', '-f',
        help='Input file to process'
    )
    
    parser.add_argument(
        '--output', '-o',
        help='Output file (required with --file)'
    )
    
    parser.add_argument(
        '--interactive', '-i',
        action='store_true',
        help='Run in interactive mode'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Show detailed processing information'
    )
    
    args = parser.parse_args()
    
    # Initialize normalizer
    if args.verbose:
        print("Initializing text normalizer...")
    
    start_init = time.perf_counter()
    normalizer = TextNormalizer()
    end_init = time.perf_counter()
    
    if args.verbose:
        print(f"Initialization time: {(end_init - start_init) * 1000:.2f} ms\n")
    
    # Determine mode
    if args.interactive:
        interactive_mode(normalizer)
    
    elif args.file:
        if not args.output:
            print("Error: --output is required when using --file", file=sys.stderr)
            sys.exit(1)
        process_file(args.file, args.output, normalizer)
    
    elif args.text:
        normalized, proc_time = normalize_text(args.text, normalizer)
        print(normalized)
        if args.verbose:
            print(f"Processing time: {proc_time:.3f} ms", file=sys.stderr)
    
    else:
        # Read from stdin
        try:
            for line in sys.stdin:
                normalized, _ = normalize_text(line.strip(), normalizer)
                print(normalized)
        except KeyboardInterrupt:
            pass


if __name__ == "__main__":
    main()
