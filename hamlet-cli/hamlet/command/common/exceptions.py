from click import ClickException, style

class CommandError(ClickException):
    """An exception occurred during processing"""

    def format_message(self):
        return style(str(self.message), bold=True, fg='red')
