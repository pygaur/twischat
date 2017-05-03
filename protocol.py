"""
char protocol
"""
from twisted.protocols.basic import LineReceiver

class Chat(LineReceiver):
    """
    chat protocol class with extending line receiver
    """

    def __init__(self, users):
        """
        Pass current user information while creation new instance of Chat .
        """
        self.users = users
        self.name = None
        self.state = 'GET_NAME'

    def connectionMade(self):
        """
        when new user is connected.
        """
        self.sendLine('Your name please')

    def connectionLost(self, reason):
        """
        user disconnects.
        """
        if self.name in self.users:
            del self.users[self.name]
            self.send_message('<<%s>> Left' % self.name)

    def lineReceived(self, line):
        """
        received data(line by line)
        """
        if self.state == 'GET_NAME':
            self.handle_get_name(line)
            self.send_message('<<%s>> joined' % line)
        else:
            self.handle_chat(line)

    def handle_get_name(self, name):
        """
        if user visit first time.
        """
        if name in self.users:
            self.sendLine('User name not available')
            return
        self.sendLine('welcome <<%s>>'% name)
        self.name = name
        self.users[name] = self
        self.state = 'CHAT'

    def send_message(self, message):
        """
        send message to other user.
        """
        for protocol in self.users.itervalues():
            if protocol != self:
                protocol.sendLine(message)

    def handle_chat(self, line):
        """
        display message
        """
        message = '<%s> , %s' % (self.name, line)
        self.send_message(message)
