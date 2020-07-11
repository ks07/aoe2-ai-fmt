import sys

from antlr4 import *

from perparse import PERParser, PERListener
from CommentSpooler import CommentSpooler

class FormattedPERListener(PERListener):
    "An ANTLR4 listener for AoE2 .per AI files that writes formatted rules to an output stream"

    def __init__(self, outStream, indent='    '):
        self.__out = outStream
        self.__indentLevel = 0
        self.__indent = indent
        self.__begun = False
        self.__commentSpooler = CommentSpooler()
        self.__withinStatement = False

    def __write_inline_comments(self):
        if self.__commentSpooler.hasComments():
            self.__write(self.__commentSpooler.getInlineComments())
            return True

    def __line(self, s):
        if self.__write_inline_comments():
            self.__begun = True

        if self.__begun:
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

    def exitPer(self, ctx:PERParser.PerContext):
        assert self.__indentLevel == 0
        self.__line('')

    def enterStatement(self, ctx:PERParser.StatementContext):
        self.__withinStatement = True

    def exitStatement(self, ctx:PERParser.StatementContext):
        self.__withinStatement = False
        self.__line('')
        self.__line('')

    def enterLone_comment(self, ctx:PERParser.Lone_commentContext):
        self.__line(ctx.COMMENT().getText())

    def enterWhitespace_comment(self, ctx:PERParser.Whitespace_commentContext):
        # Because the formatter will remove newlines, comments must be spooled up to display at line end
        self.__commentSpooler.spool(ctx.COMMENT())

    def enterDefrule(self, ctx:PERParser.DefruleContext):
        entertxt = '(' + ctx.DEFRULE().getText()
        self.__line(entertxt)
        self.__enter()

    def enterProposition(self, ctx:PERParser.PropositionContext):
        self.__line(ctx.getText())

    def enterAction_list(self, ctx:PERParser.Action_listContext):
        self.__line('=>')

    def enterAction(self, ctx:PERParser.ActionContext):
        self.__line(ctx.getText())

    def exitDefrule(self, ctx:PERParser.DefruleContext):
        self.__leave()
        self.__line(')')
