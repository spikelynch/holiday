#!/usr/bin/python

# Holiday server using Twisted instead of asyncore

from twisted.application import internet, service
from twisted.internet.protocol import ServerFactory, Protocol
from twisted.python import log

#from twisted.internet.endpoints import TCP4ServerEndpoint
#from twisted.internet.task import LoopingCall, deferLater
#from twisted.internet import reactor

import eurovision



class HolidayProtocol(Protocol):

    def connectionMade(self):
        log.msg("Connected")
        self.transport.write("connected\r\n")
    
    def dataReceived(self, data):
        nation = data[:-1]
        ip = self.factory.service.holiday_ip
        eurovision.show_flag(ip, nation)
        log.msg("show " + nation)

    def connectionLost(self, reason):
        log.msg("Disconnected")

        
class HolidayFactory(ServerFactory):
    protocol = HolidayProtocol
    def __init__(self, service):
        self.service = service


class HolidayService(service.Service):

    def __init__(self, holiday_ip):
        self.holiday_ip = holiday_ip

    def startService(self):
        service.Service.startService(self)
        log.msg("Holiday eurod talking to lights at %s" % (self.holiday_ip,))

## TAC stuff
        
port = 8007
#iface = 'localhost'
holiday_ip = '10.1.1.4'

top_service = service.MultiService()

holiday_service = HolidayService(holiday_ip)
holiday_service.setServiceParent(top_service)

factory = HolidayFactory(holiday_service)
tcp_service = internet.TCPServer(port, factory)
tcp_service.setServiceParent(top_service)

application = service.Application("euroflags")

top_service.setServiceParent(application)

#endpoint = TCP4ServerEndpoint(reactor, 8007)
#endpoint.listen(HolidayServerFactory())
#reactor.run()
