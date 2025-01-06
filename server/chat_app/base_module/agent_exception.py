class AgentException(Exception):
    """Base class for exceptions in this module."""

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message
