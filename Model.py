from Client import Client
from Departure import Departure
from datetime import datetime

class Model():

    def getDeparturesList(self,departures):
        rawDepList = departures['DepartureBoard']['Departure']
        departureObjectList = []
        for departure in rawDepList:

            if 'rtTime' in departure:
                time = datetime.strptime(departure['rtDate'] + " " + departure['rtTime'], "%Y-%m-%d %H:%M")
            else:
                time = datetime.strptime(departure['date'] + " " + departure['time'], "%Y-%m-%d %H:%M")
            departureObject = Departure(departure['name'], time , departure['direction'])
            departureObjectList.append(departureObject)
        return departureObjectList

    def printDepartures(self,departureList):
        now = datetime.now()

        for departureObject in departureList:
            difference = departureObject.time - now
            noSeconds = difference.seconds
            noSecondsRounded = round(noSeconds/60.0)
            print("Avgång: " + departureObject.name +
                  ", Mot: " + departureObject.direction +
                  ", Tid: " + str(departureObject.time) +
                  " - Now: " + str(now) +
                  ", Om " + str(noSecondsRounded) + " minuter")


    def update(self):
        stopList = ['Lindholmen', 'Lindholmspiren']
        client = Client()
        depDict = {}

        for stop in stopList:
            departures = client.getDepartures(stop)
            departureList = self.getDeparturesList(departures)
            depDict[stop] = departureList
            #print(" ")
            #print(stop)
            #self.printDepartures(departureList)

        return depDict

if __name__ == '__main__':
    model = Model()
    data=model.update()
    #print("first entries at stop")
    #model.printDepartures(data['Lindholmen'][:2])
    print("all entries at stop")
    #model.printDepartures(data['Lindholmen'])
    model.printDepartures(data['Lindholmspiren'])