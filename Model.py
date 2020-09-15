from Client import Client
from Departure import Departure
from datetime import datetime

class Model():
    #Constructor for Model class
    def __init__(self,stopList):
        self.client = Client()
        self.stopList = stopList
        self.stopIDList = self.getStopID(stopList)

    def getDeparturesList(self,departures,stop):
        rawDepList = departures['DepartureBoard']['Departure']
        departureObjectList = []
        now = datetime.now()
        for departure in rawDepList:

            if 'rtTime' in departure:
                time = datetime.strptime(departure['rtDate'] + " " + departure['rtTime'], "%Y-%m-%d %H:%M")
                deltastr=" "
            else:
                time = datetime.strptime(departure['date'] + " " + departure['time'], "%Y-%m-%d %H:%M")
                deltastr=" ca "

            if departure['name']=="286 Älvsnabbare":
                departure['name']="Färja 286"
            elif departure['name']=="285 Älvsnabben":
                departure['name']="Färja 285"

            if time >= now:
                deltatimefloat=self.get_deltatime(time, now)
                deltatime=deltastr + str(deltatimefloat)
                prevDepartureObject = self.findDeparture(departure, departureObjectList)
                if prevDepartureObject == None:
                    departureObject = Departure(departure['name'], time , departure['direction'],stop,
                                                departure['track'],departure['fgColor'],departure['bgColor'], deltatime)
                    departureObjectList.append(departureObject)
                # If the string is 10 or less add deltatime
                elif len(prevDepartureObject.deltatime)<11:
                    prevDepartureObject.deltatime += deltatime
                # Use the commented part if we only want to show departures within 30 min
                # elif deltatimefloat < 30:
                #     prevDepartureObject.deltatime += deltatime
        return departureObjectList

    def findDeparture(self, departure, departureObjectList):
        for otherDeparture in departureObjectList:
            if otherDeparture.name == departure['name'] and otherDeparture.track == departure['track'] and \
                    otherDeparture.direction == departure['direction']:
                return otherDeparture
        return None

    def get_deltatime(self,time,now):
        difference = time - now
        noSeconds = difference.seconds
        deltatime = round(noSeconds / 60.0)
        return deltatime

    def printDepartures(self,departureList):
        now = datetime.now()

        for departureObject in departureList:
                print("Avgång: " + departureObject.name +
                      ", Mot: " + departureObject.direction +
                      ", Hållplats, Läge: " + departureObject.stop +", "+ departureObject.track+
                      #", Tid: " + str(departureObject.time) +
                      #" - Now: " + str(now) +
                      ", Om " + departureObject.deltatime + " minuter")

    def getStopID(self, stopList):
        stopIDList = []
        for stop in self.stopList:
            stopId = self.client.getStopID(stop)
            stopIDList.append(stopId)
        return stopIDList

    def update(self):
        depList = []

        for i in range(0,len(self.stopList)):
            departures = self.client.getDepartures(self.stopIDList[i])
            departureList = self.getDeparturesList(departures, self.stopList[i])
            depList.extend(departureList)
        depList.sort(key=lambda x: x.time)
        return depList

if __name__ == '__main__':
    stopList = ['Lindholmenspiren', 'Lindholmen']
    model = Model(stopList)
    data = model.update()
    #model.printDepartures(data)