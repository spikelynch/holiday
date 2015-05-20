# stub object for Holiday lights

from holidaysecretapi import HolidaySecretAPI 


class Lights:

    def __init__(self, ip):
        self.ip = ip
        self.holiday = HolidaySecretAPI(addr=ip)

    def send(self, message):
        pass

    def tick(self):
        pass
