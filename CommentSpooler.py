class CommentSpooler:

    def __init__(self):
        self.__spooledComments = []

    def spool(self, comment):
        if comment is None:
            return

        cmt = comment.getText().strip()

        if cmt == ';':
            return

        self.__spooledComments.append(cmt)

    def hasComments(self):
        return len(self.__spooledComments)

    def getInlineComments(self):
        if self.__spooledComments:
            text = ' ' + ' '.join(self.__spooledComments)
            self.__spooledComments = []
            return text

    def getComments(self):
        ret = self.__spooledComments
        self.__spooledComments = []
        return ret
