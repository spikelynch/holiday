#!/usr/bin/python

# Holiday server using Twisted instead of asyncore


from twisted.internet.protocol import Factory, Protocol
from twisted.internet.endpoints import TCP4ServerEndpoint
from twisted.internet.task import LoopingCall, deferLater
from twisted.internet import reactor

import eurovision
import flags


state = ""

HOLIDAY_IP = "10.1.1.4"

class HolidayServer(Protocol):

    def __init__(self):
        self.state = ""
    
    def connectionMade(self):
        # self.factory was set by the factory's default buildProtocol:
        print "Connected"
        self.transport.write("connected\r\n")

    def dataReceived(self, data):
        print "Data received " + data
        
        nation = data[:-1]
        eurovision.show_flag(HOLIDAY_IP, nation)

        
    def connectionLost(self, reason):
        print "Goodbye"

class HolidayServerFactory(Factory):
    protocol = HolidayServer



        

endpoint = TCP4ServerEndpoint(reactor, 8007)
endpoint.listen(HolidayServerFactory())
reactor.run()
