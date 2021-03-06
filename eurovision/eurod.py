#!/usr/bin/python

# Holiday server using Twisted 

from twisted.application import internet, service
from twisted.internet.protocol import ServerFactory, Protocol
from twisted.python import log

from eurolights import EuroLights




class HolidayProtocol(Protocol):

    def connectionMade(self):
        log.msg("Connected")
        self.transport.write("connected\r\n")  # NetIO needs this
    
    def dataReceived(self, data):
        nation = data[:-1]
        log.msg("Data: " + nation)
        if nation == 'toggle':
            if self.factory.service.state:
                self.factory.service.lights.off()
                self.factory.service.state = False
                log.msg("Switched off")
            else:
                self.factory.service.state = True
                log.msg("Switched on")
        elif self.factory.service.lights.send(nation):
            self.factory.service.state = True
            log.msg("Switched: " + nation)
        else:
            log.msg("Bad nation: " + nation + "not known")

    def connectionLost(self, reason):
        log.msg("Disconnected")

        
class HolidayFactory(ServerFactory):
    protocol = HolidayProtocol
    def __init__(self, service):
        self.service = service


class HolidayService(service.Service):

    def __init__(self, lights):
        self.lights = lights
        self.state = False

    def startService(self):
        service.Service.startService(self)
        log.msg("Holiday eurod talking to lights at %s" % (self.lights.ip,))


def tick_lights(service):
    if service.state:
        service.lights.tick()


        
## TAC stuff
        
port = 8007
holiday_ip = '10.1.1.4'
interval = .25

lights = EuroLights(holiday_ip)


top_service = service.MultiService()

holiday_service = HolidayService(lights)
holiday_service.setServiceParent(top_service)

factory = HolidayFactory(holiday_service)
tcp_service = internet.TCPServer(port, factory)
tcp_service.setServiceParent(top_service)

loop = internet.TimerService(interval, tick_lights, holiday_service)
loop.setServiceParent(top_service)

application = service.Application("euroflags")

top_service.setServiceParent(application)

