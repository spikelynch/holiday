#!/usr/bin/python

# Holiday server using Twisted instead of asyncore


from twisted.internet.protocol import Factory, Protocol
from twisted.internet.endpoints import TCP4ServerEndpoint
from twisted.internet import reactor

class QOTD(Protocol):

    def connectionMade(self):
        # self.factory was set by the factory's default buildProtocol:
        print "Connected"
        self.transport.write(self.factory.quote + '\r\n')

    def dataReceived(self, data):
        print "Data received" + data
        self.transport.write(data)
        
    def connectionLost(self, reason):
        print "Lost connection"

class QOTDFactory(Factory):

    # This will be used by the default buildProtocol to create new protocols:
    protocol = QOTD

    def __init__(self, quote=None):
        self.quote = quote or 'An apple a day keeps the doctor away'

endpoint = TCP4ServerEndpoint(reactor, 8007)
endpoint.listen(QOTDFactory("configurable quote"))
reactor.run()
