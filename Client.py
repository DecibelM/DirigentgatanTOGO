# Cred to https://github.com/danneedebro/Nasta-tur-vasttrafik
import requests
import base64
from datetime import datetime
from PyQt5.QtCore import QTimer
"""Client class which communicates with the API"""
class Client:
    def __init__(self):
        self.KEY = 'zRglBR_EmPfQ60PknwY_Ja5WOFMa'
        self.SECRET = 'INSERTSECRETHERE'
        self.ACCESS_TOKEN = ''
        self.getAccess()
        self.automatic_getAccessToken()

    """Fethes the access token which is valid for 1h"""
    def getAccess(self):
        parameters = {'format': 'json', 'grant_type': 'client_credentials'}
        url = 'https://api.vasttrafik.se/token'
        head = {'Authorization': 'Basic ' + base64.b64encode((self.KEY + ':' + self.SECRET).encode()).decode(),
                'Content-Type': 'application/x-www-form-urlencoded'}
        r_i=0
        while r_i<4:
            try:
                r = requests.post(url, headers=head, params=parameters)
                tmp = r.json()
                self.ACCESS_TOKEN = tmp['access_token']
                break
            except ValueError:
                r_i=r_i+1
                print("In getAccess: r_i=",str(r_i)," Error raised with status code ", r.status_code)

    """Fetches the id associated with the provided stop name"""
    def getStopID(self, STOP):
        url = 'https://api.vasttrafik.se/bin/rest.exe/v2/location.name'
        parameters = {'format': 'json', 'input': STOP}
        head = {'Authorization': 'Bearer ' + self.ACCESS_TOKEN}
        r_i = 0
        while r_i < 3:
            try:
                r = requests.get(url, headers=head, params=parameters)
                tmp = r.json()
                break
            except ValueError:
                r_i = r_i + 1
                print("In getStopID: r_i=",str(r_i)," Error raised with status code ", r.status_code)
        STOP_ID = tmp['LocationList']['StopLocation'][0]['id']
        return STOP_ID
    """Fetches the list of departures (in JSON-format) from the given stop-id"""
    def getDepartures(self, STOP_ID):
        now = datetime.now()
        url = 'https://api.vasttrafik.se/bin/rest.exe/v2/departureBoard'
        parameters = {'format': 'json', 'id': STOP_ID, 'date': now.strftime("%Y-%m-%d"), 'time': now.strftime("%H:%M")}
        head = {'Authorization': 'Bearer ' + self.ACCESS_TOKEN}
        r_i = 0
        while r_i < 3:
            try:
                r = requests.get(url, headers=head, params=parameters)
                tmp = r.json()
                break
            except ValueError:
                r_i = r_i + 1
                print("In getDepartures: r_i=",str(r_i)," Error raised with status code ", r.status_code)
                if r_i==3:
                    return ["Error",r.status_code]
        return tmp
    """Method creating a separate process for fetching the access token every 1 h"""
    def automatic_getAccessToken(self):
        # creating a timer object
        self.timer = QTimer()
        # adding action to timer
        self.timer.timeout.connect(self.getAccess)
        # update the timer every 50 min = 5e3 sec = 5e6 msec
        self.timer.start(5e6)

