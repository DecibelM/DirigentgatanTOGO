"""Holds information about a departure"""
class Departure:
    def __init__(self, name, time, direction,stop,track,fgColor,bgColor, deltatime):
        self.name = name
        self.time = time
        self.direction = direction
        self.stop = stop
        self.track = track
        self.fgColor = fgColor #Color of the line number expressed as a string in hex.
        self.bgColor = bgColor #Background color expressed as a string in hex.
        self.deltatime = deltatime #String with each departure, in minutes left.

