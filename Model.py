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
                deltastr=" "
            else:
                time = datetime.strptime(departure['date'] + " " + departure['time'], "%Y-%m-%d %H:%M")
                deltastr="ca "

            if time >= now:
                deltatime=deltastr + self.get_deltatime(time, now)
                prevDepartureObject = self.findDeparture(departure, departureObjectList)
                if prevDepartureObject == None:
                    departureObject = Departure(departure['name'], time , departure['direction'],departure['track'],
                                        departure['fgColor'],departure['bgColor'], deltatime)
                    departureObjectList.append(departureObject)
                else:
                    prevDepartureObject.deltatime += deltatime
        departureObjectList.sort(key=lambda x: x.time)
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
                      ", Tid: " + str(departureObject.time) +
                      " - Now: " + str(now) +
                      ", Om " + departureObject.deltatime + " minuter")


    def update(self):
        depDict = {}

        for stop in self.stopList:
            departures = self.client.getDepartures(stop)
            departureList = self.getDeparturesList(departures)
            depDict[stop] = departureList

        return depDict

if __name__ == '__main__':
    #stopList = ['Lantmilsgatan', 'Fyrktorget']
    #model = Model(stopList)
    #model.client.getAccess()
    #departures = model.client.getDepartures(stopList[0])
    #departure1 = Departure('Spårvagn 1', '13:00', 'Tynnered', 'B', '#FFFFFF', '#FFFFFF', 'deltatime')
    #departure2 = Departure('Spårvagn 7', '13:00', 'Tynnered', 'B', '#FFFFFF', '#FFFFFF', 'deltatime')
    #departure3 = Departure('Spårvagn 1', '13:00', 'Östra Sjukhuset', 'A', '#FFFFFF', '#FFFFFF', 'deltatime')
    #departureObjectList = [departure1, departure2, departure3]
    #for departure in departures['DepartureBoard']['Departure']:
    #    result = model.findDeparture(departure, departureObjectList)
    #    if result != None:
    #        print(result.name)
    #        print(result.track)
    #    else:
    #        print(result)

    stopList = ['Lindholmenspiren', 'Lindholmen']
    model = Model(stopList)
    data = model.update()
    print("first entries at stop")
    model.printDepartures(data['Lindholmen'][:2])
    print("all entries at stop")
    model.printDepartures(data['Lindholmen'])