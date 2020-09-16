from Client import Client
from Departure import Departure
from datetime import datetime

"""Class model fetches the data from Vasttrafik through the Client.
    It calculates the minutes left until each departure.
    It creates a sorted list of all departures"""
class Model():
    #Constructor for Model class
    def __init__(self,stopList):
        self.client = Client() #The Client communicating with the API
        self.stopList = stopList #List of stop names
        self.stopIDList = self.getStopID(stopList) #List of id:s associated with the stops

    """Method that creates the sorted list of departures
        and calculates the time left.
        Input:
        departures - the data from the API
        stop - the stop name"""
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

    """Looks for a departure in the departure list. If it is already there,
    that departure is retuned. Otherwise None is returned.
    Input:
    departure - JSON object from the API
    departureObjectList - list of all Departure objects created so far."""
    def findDeparture(self, departure, departureObjectList):
        for otherDeparture in departureObjectList:
            if otherDeparture.name == departure['name'] and otherDeparture.track == departure['track'] and \
                    otherDeparture.direction == departure['direction']:
                return otherDeparture
        return None

    """Calculates minutes left until departure.
    Input: 
    time - dateTime object, the time of the departure
    now - dateTime object, the current time"""
    def get_deltatime(self,time,now):
        difference = time - now
        noSeconds = difference.seconds
        deltatime = round(noSeconds / 60.0)
        return deltatime

    """Method for testing purposes. Prints the departure list to the console"""
    def printDepartures(self,departureList):
        for departureObject in departureList:
                print("Avgång: " + departureObject.name +
                      ", Mot: " + departureObject.direction +
                      ", Hållplats, Läge: " + departureObject.stop +", "+ departureObject.track+
                      ", Om " + departureObject.deltatime + " minuter")

    """Retrieves the associated stop-id:s belonging to the stops"""
    def getStopID(self, stopList):
        stopIDList = []
        for stop in self.stopList:
            stopId = self.client.getStopID(stop)
            stopIDList.append(stopId)
        return stopIDList

    """The metod called by the controller to recieve updated data.
        Returns a list of all departures for the selected stops."""
    def update(self):
        depList = []

        for i in range(0,len(self.stopList)):
            departures = self.client.getDepartures(self.stopIDList[i])
            if "Error" in departures:
                return departures
            departureList = self.getDeparturesList(departures, self.stopList[i])
            depList.extend(departureList)
        depList.sort(key=lambda x: x.time)
        return depList

"""This is a method for testing purpose.
    It can test Model class separately from GUI"""
if __name__ == '__main__':
    stopList = ['Lindholmenspiren', 'Lindholmen']
    model = Model(stopList)
    data = model.update()
