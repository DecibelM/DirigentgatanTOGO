from Client import Client
from Departure import Departure
from datetime import datetime

class Model():
    #Constructor for Model class
    def __init__(self,stopList):
        self.client = Client()
        self.stopList = stopList

    def getDeparturesList(self,departures):
        rawDepList = departures['DepartureBoard']['Departure']
        departureObjectList = []
        now = datetime.now()
        for departure in rawDepList:

            if 'rtTime' in departure:
                time = datetime.strptime(departure['rtDate'] + " " + departure['rtTime'], "%Y-%m-%d %H:%M")
            else:
                time = datetime.strptime(departure['date'] + " " + departure['time'], "%Y-%m-%d %H:%M")

            if time >= now:
                difference = time - now
                noSeconds = difference.seconds
                deltatime = str(round(noSeconds / 60.0))

                departureObject = Departure(departure['name'], time , departure['direction'], deltatime)
                departureObjectList.append(departureObject)
        departureObjectList.sort(key=lambda x: x.time)
        return departureObjectList


    def printDepartures(self,departureList):
        now = datetime.now()

        for departureObject in departureList:
            if departureObject.time >= now:
                difference = departureObject.time - now
                noSeconds = difference.seconds
                noSecondsRounded = round(noSeconds/60.0)
                print("Avgång: " + departureObject.name +
                      ", Mot: " + departureObject.direction +
                      ", Tid: " + str(departureObject.time) +
                      " - Now: " + str(now) +
                      ", Om " + str(noSecondsRounded) + " minuter")


    def update(self):
        depDict = {}

        for stop in self.stopList:
            departures = self.client.getDepartures(stop)
            departureList = self.getDeparturesList(departures)
            depDict[stop] = departureList

        return depDict

if __name__ == '__main__':
    stopList = ['Lantmilsgatan', 'Fyrktorget']
    model = Model(stopList)
    data=model.update()
    #print("first entries at stop")
    #model.printDepartures(data['Lindholmen'][:2])
    print("all entries at stop")
    model.printDepartures(data['Lantmilsgatan'])
    model.printDepartures(data['Fyrktorget'])