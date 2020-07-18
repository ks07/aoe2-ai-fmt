"""Provides the ANTLR4 listener class for producing formatted .per output."""

from enum import Enum, auto

from perparse import PERParser, PERListener
from comment_spooler import CommentSpooler

class FormattedPERListener(PERListener):
    """An ANTLR4 listener for AoE2 .per AI files that writes formatted rules to an output stream."""

    # pylint: disable=too-many-public-methods

    def __init__(self, outStream, indent='    '):
        """Instantiates a listener with a given output stream, and an option configurable indent."""
        self.__out = outStream
        self.__indent_level = 0
        self.__indent = indent
        self.__comment_spooler = CommentSpooler()
        self.__exploded_proposition_mode = []
        self.__previous_type = [None]

    def __write_inline_comments(self):
        if self.__comment_spooler.has_comments():
            self.__write(self.__comment_spooler.get_inline_comments())

    def __line(self, cont=''):
        self.__write_inline_comments()

        # Only output a line if we've already started output, to prevent leading blank lines
        if self.__get_previous_type():
            self.__write('\n')
        pfix = self.__indent * self.__indent_level
        self.__write(pfix)
        self.__write(cont)

    def __write(self, cont):
        self.__out.write(cont)

    def __enter(self, as_top_level=False):
        self.__indent_level += 1
        if as_top_level:
            self.__previous_type.append(TopLevelType.NESTED)

    def __leave(self, as_top_level=False):
        assert self.__indent_level > 0
        self.__indent_level -= 1
        if as_top_level:
            assert len(self.__previous_type) > 1
            self.__previous_type.pop()

    def __get_previous_type(self):
        return self.__previous_type[-1]

    def __set_previous_type(self, prev):
        self.__previous_type[-1] = prev

    def enterConditional_cond(self, ctx: PERParser.Conditional_condContext):
        if ctx.CONDLOAD_DEFINED():
            self.__line(ctx.CONDLOAD_DEFINED().getText())
        else:
            self.__line(ctx.CONDLOAD_UNDEFINED().getText())
        self.__write(' ')
        self.__write(ctx.SYMBOL().getText())
        self.__set_previous_type(TopLevelType.OTHER)

    def enterConditional_else(self, ctx: PERParser.Conditional_elseContext):
        self.__line(ctx.CONDLOAD_ELSE().getText())

    def enterConditional_content(self, ctx: PERParser.Conditional_contentContext):
        self.__enter(True)

    def exitConditional_content(self, ctx: PERParser.Conditional_contentContext):
        self.__leave(True)

    def exitConditional_block(self, ctx: PERParser.Conditional_blockContext):
        self.__line(ctx.CONDLOAD_END().getText())

    def exitPer(self, ctx: PERParser.PerContext):
        # Balanced nesting should be enforced on the input by the ANTLR grammar
        # If the nesting is unbalanced once we're done with the tree, must be a formatter bug
        assert self.__indent_level == 0
        self.__line()

    def exitStatement(self, ctx: PERParser.StatementContext):
        # When we leave a statement, the proposition mode stack should be empty
        assert not self.__exploded_proposition_mode
        # if this statement was for a defconst command, then don't close on a new line
        if ctx.command().defconst() or ctx.command().load():
            self.__write(ctx.CLOSE().getText())
        else:
            self.__line(ctx.CLOSE().getText())

    def enterLone_comment(self, ctx: PERParser.Lone_commentContext):
        self.__line(ctx.COMMENT().getText().strip())
        self.__set_previous_type(TopLevelType.COMMENT)

    def enterWhitespace_comment(self, ctx: PERParser.Whitespace_commentContext):
        # Comments must be at EOL, spool them up to display at line end
        self.__comment_spooler.spool(ctx.COMMENT())

    def enterToplevel_content(self, ctx: PERParser.Toplevel_contentContext):
        # Insert a blank line based on the transition between top level statement types
        current_type = TopLevelType.from_context(ctx)
        if self.__get_previous_type() and self.__get_previous_type().should_add_line(current_type):
            self.__line()

    def enterStatement(self, ctx: PERParser.StatementContext):
        self.__line(ctx.OPEN().getText())

    def enterDefconst(self, ctx: PERParser.DefconstContext):
        self.__write(ctx.DEFCONST().getText())
        self.__write(' ')
        self.__write(ctx.SYMBOL().getText())
        self.__write(' ')
        self.__write(ctx.SHORT().getText())
        self.__set_previous_type(TopLevelType.DEFCONST)

    def enterDefrule(self, ctx: PERParser.DefruleContext):
        self.__write(ctx.DEFRULE().getText())
        self.__enter()
        self.__set_previous_type(TopLevelType.OTHER)

    def enterProposition(self, ctx: PERParser.PropositionContext):
        self.__line(ctx.OPEN().getText())
        self.__write(ctx.SYMBOL().getText())
        # If this proposition contains nested propositions, then format it differently
        # Check all children in advance to prevent a proposition mixing styles
        args = ctx.proposition_arg()
        if args and any((a.proposition() for a in args)):
            self.__exploded_proposition_mode.append(True)
            self.__enter()
        else:
            self.__exploded_proposition_mode.append(False)

    def enterProposition_arg(self, ctx: PERParser.Proposition_argContext):
        if ctx.SYMBOL():
            self.__write(' ')
            self.__write(ctx.SYMBOL().getText())
        elif ctx.REL_OP():
            self.__write(' ')
            self.__write(ctx.REL_OP().getText())
        elif ctx.SHORT():
            self.__write(' ')
            self.__write(ctx.SHORT().getText())
        elif ctx.proposition():
            # Nested propositions will format and output themselves
            pass
        else:
            raise NotImplementedError(
                f'Proposition argument type is not supported in the formatter: '
                f'[{ctx.getText().strip()}]'
            )

    def exitProposition(self, ctx: PERParser.PropositionContext):
        if self.__exploded_proposition_mode.pop():
            self.__leave()
            self.__line()
        self.__write(ctx.CLOSE().getText())

    def enterAction_list(self, ctx: PERParser.Action_listContext):
        self.__line('=>')

    def enterAction(self, ctx: PERParser.ActionContext):
        self.__line(ctx.OPEN().getText())
        self.__write(ctx.SYMBOL().getText())

    def enterAction_arg(self, ctx: PERParser.Action_argContext):
        self.__write(' ')
        if ctx.SYMBOL():
            self.__write(ctx.SYMBOL().getText())
        elif ctx.SHORT():
            self.__write(ctx.SHORT().getText())
        elif ctx.STRING():
            self.__write(ctx.STRING().getText())
        else:
            raise NotImplementedError(
                f'Action argument type is not supported in the formatter: '
                f'[{ctx.getText().strip()}]'
            )

    def exitAction(self, ctx: PERParser.ActionContext):
        self.__write(ctx.CLOSE().getText())

    def exitDefrule(self, ctx: PERParser.DefruleContext):
        self.__leave()

    def enterLoad(self, ctx: PERParser.LoadContext):
        if ctx.LOAD():
            self.__write(ctx.LOAD().getText())
        else:
            # TODO: This is valid but not useful - should the formatter normalise to a simple load and/or warn?
            self.__write(ctx.LOADRANDOM().getText())
        self.__write(' ')
        self.__write(ctx.STRING().getText())
        self.__set_previous_type(TopLevelType.LOAD)

    def enterLoad_random_list(self, ctx: PERParser.Load_random_listContext):
        self.__write(ctx.LOADRANDOM().getText())
        self.__enter()
        self.__set_previous_type(TopLevelType.OTHER)

    def enterRandom_file(self, ctx: PERParser.Random_fileContext):
        self.__line(ctx.SHORT().getText())
        self.__write(' ')
        self.__write(ctx.STRING().getText())

    def exitLoad_random_list(self, ctx: PERParser.Load_random_listContext):
        if ctx.STRING():
            self.__line(ctx.STRING().getText())
        self.__leave()

class TopLevelType(Enum):
    """Top level statement types, to control whitespace generation.

    These are used when blank lines are desired between certain pairs of statements, but not all.
    An OTHER member is provided for statements that require no special interaction.
    """

    # pylint: disable=bad-whitespace
    COMMENT  = auto()
    DEFCONST = auto()
    LOAD     = auto()
    OTHER    = auto()
    NESTED   = auto()

    @classmethod
    def from_context(cls, ctx: PERParser.Toplevel_contentContext):
        """Gets the top level type for the given content."""
        if ctx.statement() and ctx.statement().command() and ctx.statement().command().defconst():
            return cls.DEFCONST
        if ctx.statement() and ctx.statement().command() and ctx.statement().command().load():
            return cls.LOAD
        if ctx.lone_comment():
            return cls.COMMENT
        return cls.OTHER

    # Shortcoming in py 3.6 means that we can't refer to TopLevelType in a method def
    def should_add_line(self, next_type: 'TopLevelType'):
        """Returns True if a blank line should separate this statement and the next."""
        return (self is not TopLevelType.COMMENT
                and self is not TopLevelType.NESTED
                and (self is not TopLevelType.DEFCONST or next_type is not TopLevelType.DEFCONST)
                and (self is not TopLevelType.LOAD or next_type is not TopLevelType.LOAD))
