#!/usr/bin/env python3

import sys

from antlr4 import *

from PERLexer import PERLexer
from PERParser import PERParser
from FormattedPERListener import FormattedPERListener

def main(argv):
    inp = FileStream(argv[1])
    lexer = PERLexer(inp)
    stream = CommonTokenStream(lexer)
    parser = PERParser(stream)
    tree = parser.per()

    output = open("out.per", "w", encoding="utf8", newline="\r\n")

    formatter = FormattedPERListener(output)
    walker = ParseTreeWalker()
    walker.walk(formatter, tree)

if __name__ == "__main__":
    main(sys.argv)
