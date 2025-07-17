import sys


class StdoutRedirector:
    def __init__(self):
        self.messages = []

    def write(self, message):
        self.messages.append(message)

    def flush(self):
        pass


redirector = StdoutRedirector()
sys.stdout = redirector
