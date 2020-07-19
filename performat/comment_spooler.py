"""Provides a class for spooling comments until end-of-line."""

class CommentSpooler:
    """Spools comments and joins them for output at end-of-line."""

    def __init__(self):
        """Creates a new CommentSpooler with an empty buffer."""
        self.__spooled_comments = []

    def spool(self, comment):
        """Adds a comment to the buffer. If comment is None, it is ignored."""
        if comment is None:
            return

        cmt = comment.getText().strip()

        if cmt == ';':
            return

        self.__spooled_comments.append(cmt)

    def has_comments(self):
        """Returns True if there are comments in the buffer."""
        return len(self.__spooled_comments)

    def get_inline_comments(self):
        """Returns the spooled comments as a single string, and clears the buffer."""
        if self.__spooled_comments:
            text = ' ' + ' '.join(self.__spooled_comments)
            self.__spooled_comments = []
            return text
        return ''
