#!/usr/bin/env python3

import argparse
import sys

from antlr4 import *

from perparse import PERLexer, PERParser
from FormattedPERListener import FormattedPERListener

def main():
    parser = argparse.ArgumentParser(description = 'Formatter for AoE2 .per files')
    parser.add_argument('inpath', type=str, help='The path to the .per file to format')
    parser.add_argument('out', type=str, help='The path to write output to, or stdout if -')
    args = parser.parse_args()

    if args.out == '-':
        format(args.inpath, sys.stdout)
    else:
        with open(args.out, "w", encoding="utf8", newline="\r\n") as output:
            format(args.inpath, output)

def format(in_path, out_stream):
    inp = FileStream(in_path)
    lexer = PERLexer(inp)
    stream = CommonTokenStream(lexer)
    parser = PERParser(stream)
    tree = parser.per()

    formatter = FormattedPERListener(out_stream)
    walker = ParseTreeWalker()
    walker.walk(formatter, tree)

if __name__ == "__main__":
    main()
