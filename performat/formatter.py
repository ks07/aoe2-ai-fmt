"""
Provides a formatter for AoE2 AI rule files (.per)
"""

from antlr4 import FileStream, InputStream, StdinStream, CommonTokenStream, ParseTreeWalker

from .perparse import PERLexer, PERParser
from .formatted_per_listener import FormattedPERListener

def format_per(*, in_path=None, in_string=None, in_stdin=False, out_stream):
    """Parses and formats a .per file, writing formatted output to the supplied text stream."""
    if [in_path is not None, in_string is not None, in_stdin].count(True) > 1:
        raise ValueError("Only one of in_path or in_stream must be provided.")

    if in_path is not None:
        antlr_stream = FileStream(in_path)
    elif in_string is not None:
        antlr_stream = InputStream(in_string)
    elif in_stdin:
        antlr_stream = StdinStream()
    else:
        raise ValueError("Either in_path, in_string, or in_stdin must be provided.")

    lexer = PERLexer(antlr_stream)
    stream = CommonTokenStream(lexer)
    parser = PERParser(stream)
    tree = parser.per()

    formatter = FormattedPERListener(out_stream)
    walker = ParseTreeWalker()
    walker.walk(formatter, tree)
