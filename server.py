"""
Chat server
"""
from twisted.internet.protocol import Factory
from twisted.internet import reactor

from protocol import Chat


class ChatFactory(Factory):
    """
    build chat protocol.
    """

    def __init__(self):
        """
        factory initialization.
        """
        self.users = {}

    def buildProtocol(self, addr):
        """
        call Chat
        """
        return Chat(self.users)


reactor.listenTCP(8123, ChatFactory())
reactor.run()
