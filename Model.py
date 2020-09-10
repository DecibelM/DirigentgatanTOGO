from Client import Client
from Departure import Departure
from datetime import datetime

class Model():
    #Constructor for Model class
    def __init__(self,stopList):
        self.client = Client()
        self.stopList = stopList

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
                deltastr="ca "

            if time >= now:
                deltatime=deltastr + self.get_deltatime(time, now)
                prevDepartureObject = self.findDeparture(departure, departureObjectList)
                if prevDepartureObject == None:
                    departureObject = Departure(departure['name'], time , departure['direction'],stop,
                                                departure['track'],departure['fgColor'],departure['bgColor'], deltatime)
                    departureObjectList.append(departureObject)
                else:
                    prevDepartureObject.deltatime += deltatime
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
        deltatime = str(round(noSeconds / 60.0))
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


    def update(self):
        depList = []

        for stop in self.stopList:
            departures = self.client.getDepartures(stop)
            departureList = self.getDeparturesList(departures,stop)
            depList.extend(departureList)
        depList.sort(key=lambda x: x.time)

        return depList

if __name__ == '__main__':
    stopList = ['Lindholmenspiren', 'Lindholmen']
    model = Model(stopList)
    data = model.update()
    #model.printDepartures(data)