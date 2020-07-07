import sys

from antlr4 import *

from perparse import PERParser, PERListener

class FormattedPERListener(PERListener):
    "An ANTLR4 listener for AoE2 .per AI files that writes formatted rules to an output stream"

    def __init__(self, outStream, indent='    '):
        self.__out = outStream
        self.__indentLevel = 0
        self.__indent = indent
        self.__begun = False

    def __line(self, s):
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
