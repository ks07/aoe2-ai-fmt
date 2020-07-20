#!/usr/bin/env python3

"""
Usage: format.py <Input Path> <Output Path>

Formats an Age of Empires 2 AI rule file (.per), into a standardised
human readable format. Comments are preserved.

Input path may be '-', in which case the .per content will be read from
stdin.

Output path may be '-', in which case the formatted .per content will
be output on stdout.

This script does not do any validation of actions or propositions (such
as verifying valid action names, or verifying parameter counts). Only
syntax will be checked. Invalid syntax on the input file will result in
an error.
"""

import argparse
import sys

from performat import format_per

def main():
    """Main script function, providing a simple CLI for the formatter."""
    parser = argparse.ArgumentParser(description='Formatter for AoE2 .per files')
    parser.add_argument('src', type=str, help='The path to the .per file to format, or stdin if -')
    parser.add_argument('out', type=str, help='The path to write output to, or stdout if -')
    args = parser.parse_args()

    format_args = {}

    if args.src == '-':
        format_args['in_stdin'] = True
    else:
        format_args['in_path'] = args.src

    if args.out == '-':
        format_per(out_stream=sys.stdout, **format_args)
    else:
        with open(args.out, "w", encoding="utf8", newline="\r\n") as output:
            format_per(out_stream=output, **format_args)

if __name__ == "__main__":
    main()
