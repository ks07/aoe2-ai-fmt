import sys

from enum import Enum, auto

from antlr4 import *

from perparse import PERParser, PERListener
from CommentSpooler import CommentSpooler

class FormattedPERListener(PERListener):
    "An ANTLR4 listener for AoE2 .per AI files that writes formatted rules to an output stream"

    def __init__(self, outStream, indent='    '):
        self.__out = outStream
        self.__indentLevel = 0
        self.__indent = indent
        self.__commentSpooler = CommentSpooler()
        self.__explodedPropositionMode = []
        self.__previousType = None

    def __write_inline_comments(self):
        if self.__commentSpooler.hasComments():
            self.__write(self.__commentSpooler.getInlineComments())

    def __line(self, s=''):
        self.__write_inline_comments()

        # Only actually output a line if we've already output something, to prevent leading blank lines
        if self.__previousType:
            self.__write('\n')
        pfix = self.__indent * self.__indentLevel
        self.__write(pfix)
        self.__write(s)

    def __write(self, s):
        self.__begun = True
        self.__out.write(s)

    def __enter(self):
        self.__indentLevel += 1

    def __leave(self):
        assert self.__indentLevel > 0
        self.__indentLevel -= 1

    def enterConditional_block(self, ctx:PERParser.Conditional_blockContext):
        self.__previousType = TopLevelType.OTHER

    def enterConditional_cond(self, ctx:PERParser.Conditional_condContext):
        if ctx.CONDLOAD_DEFINED():
            self.__line(ctx.CONDLOAD_DEFINED().getText())
        else:
            self.__line(ctx.CONDLOAD_UNDEFINED().getText())
        self.__write(' ')
        self.__write(ctx.SYMBOL().getText())

    def enterConditional_else(self, ctx:PERParser.Conditional_elseContext):
        self.__line(ctx.CONDLOAD_ELSE().getText())

    def enterConditional_content(self, ctx:PERParser.Conditional_contentContext):
        self.__enter()

    def exitConditional_content(self, ctx:PERParser.Conditional_contentContext):
        self.__leave()

    def exitConditional_block(self, ctx:PERParser.Conditional_blockContext):
        self.__line(ctx.CONDLOAD_END().getText())

    def exitPer(self, ctx:PERParser.PerContext):
        # Balanced nesting should be enforced on the input by the ANTLR grammar
        # If the nesting is unbalanced once we're done with the parse tree, then that's a formatter bug
        assert self.__indentLevel == 0
        self.__line()

    def exitStatement(self, ctx:PERParser.StatementContext):
        # When we leave a statement, the proposition mode stack should be empty
        assert not self.__explodedPropositionMode
        # if this statement was for a defconst command, then don't close on a new line
        if ctx.command().defconst() or ctx.command().load():
            self.__write(ctx.CLOSE().getText())
        else:
            self.__line(ctx.CLOSE().getText())

    def enterLone_comment(self, ctx:PERParser.Lone_commentContext):
        if self.__previousType and self.__previousType is not TopLevelType.COMMENT:
            self.__line()
        self.__line(ctx.COMMENT().getText().strip())
        self.__previousType = TopLevelType.COMMENT

    def enterWhitespace_comment(self, ctx:PERParser.Whitespace_commentContext):
        # Because the formatter will remove newlines, comments must be spooled up to display at line end
        self.__commentSpooler.spool(ctx.COMMENT())

    def enterStatement(self, ctx:PERParser.StatementContext):
        # Insert a blank line based on the transition between top level statement types
        if (
            self.__previousType
            and self.__previousType is not TopLevelType.COMMENT
            and (self.__previousType is not TopLevelType.DEFCONST or not ctx.command().defconst())
            and (self.__previousType is not TopLevelType.LOAD or not ctx.command().load())
        ):
            self.__line()
        self.__line(ctx.OPEN().getText())

    def enterDefconst(self, ctx:PERParser.DefconstContext):
        self.__write(ctx.DEFCONST().getText())
        self.__write(' ')
        self.__write(ctx.SYMBOL().getText())
        self.__write(' ')
        self.__write(ctx.SHORT().getText())
        self.__previousType = TopLevelType.DEFCONST

    def enterDefrule(self, ctx:PERParser.DefruleContext):
        self.__write(ctx.DEFRULE().getText())
        self.__enter()
        self.__previousType = TopLevelType.OTHER

    def enterProposition(self, ctx:PERParser.PropositionContext):
        self.__line(ctx.OPEN().getText())
        self.__write(ctx.SYMBOL().getText())
        # If this proposition contains nested propositions, then we want to format it differently
        # We need to check all the children in advance because we don't want a proposition with both types of args to mix both styles
        args = ctx.proposition_arg()
        if args and any((a.proposition() for a in args)):
            self.__explodedPropositionMode.append(True)
            self.__enter()
        else:
            self.__explodedPropositionMode.append(False)

    def enterProposition_arg(self, ctx:PERParser.Proposition_argContext):
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
            raise NotImplementedError(f'Proposition argument type is not supported in the formatter: [{ctx.getText().strip()}]')

    def exitProposition(self, ctx:PERParser.PropositionContext):
        if self.__explodedPropositionMode.pop():
            self.__leave()
            self.__line()
        self.__write(ctx.CLOSE().getText())

    def enterAction_list(self, ctx:PERParser.Action_listContext):
        self.__line('=>')

    def enterAction(self, ctx:PERParser.ActionContext):
        self.__line(ctx.OPEN().getText())
        self.__write(ctx.SYMBOL().getText())

    def enterAction_arg(self, ctx:PERParser.Action_argContext):
        self.__write(' ')
        if ctx.SYMBOL():
            self.__write(ctx.SYMBOL().getText())
        elif ctx.SHORT():
            self.__write(ctx.SHORT().getText())
        elif ctx.STRING():
            self.__write(ctx.STRING().getText())
        else:
            raise NotImplementedError(f'Action argument type is not supported in the formatter: [{ctx.getText().strip()}]')

    def exitAction(self, ctx:PERParser.ActionContext):
        self.__write(ctx.CLOSE().getText())

    def exitDefrule(self, ctx:PERParser.DefruleContext):
        self.__leave()

    def enterLoad(self, ctx:PERParser.LoadContext):
        if ctx.LOAD():
            self.__write(ctx.LOAD().getText())
        else:
            # TODO: This is valid but not useful - should the formatter normalise to a simple load and/or warn?
            self.__write(ctx.LOADRANDOM().getText())
        self.__write(' ')
        self.__write(ctx.STRING().getText())
        self.__previousType = TopLevelType.LOAD

    def enterLoad_random_list(self, ctx:PERParser.Load_random_listContext):
        self.__write(ctx.LOADRANDOM().getText())
        self.__enter()
        self.__previousType = TopLevelType.OTHER

    def enterRandom_file(self, ctx:PERParser.Random_fileContext):
        self.__line(ctx.SHORT().getText())
        self.__write(' ')
        self.__write(ctx.STRING().getText())

    def exitLoad_random_list(self, ctx:PERParser.Load_random_listContext):
        if ctx.STRING():
            self.__line(ctx.STRING().getText())
        self.__leave()

class TopLevelType(Enum):
    "Top level statement types, to control whitespace generation. An OTHER member is provided for statements that require no special interaction"
    COMMENT  = auto()
    DEFCONST = auto()
    LOAD     = auto()
    OTHER    = auto()
