"""
Provides a formatter for AoE2 AI rule files (.per)
"""

from antlr4 import FileStream, CommonTokenStream, ParseTreeWalker

from .perparse import PERLexer, PERParser
from .formatted_per_listener import FormattedPERListener

def format_per(in_path, out_stream):
    """Parses and formats a .per file, writing formatted output to the supplied text stream."""
    inp = FileStream(in_path)
    lexer = PERLexer(inp)
    stream = CommonTokenStream(lexer)
    parser = PERParser(stream)
    tree = parser.per()

    formatter = FormattedPERListener(out_stream)
    walker = ParseTreeWalker()
    walker.walk(formatter, tree)
