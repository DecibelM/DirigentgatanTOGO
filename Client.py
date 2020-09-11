# Cred to https://github.com/danneedebro/Nasta-tur-vasttrafik

import requests
import base64
from datetime import datetime
from PyQt5.QtCore import QTimer

class Client:

    # USER INPUT
    def __init__(self):
        self.KEY = 'zRglBR_EmPfQ60PknwY_Ja5WOFMa'
        self.SECRET = 'GhqGMLcJ9rwdPSIStI03NLUNKQ4a'
        self.ACCESS_TOKEN = ''
        self.getAccess()
        self.automatic_getAccessToken()

    def getAccess(self):
        # Step 1: Get Access token
        parameters = {'format': 'json', 'grant_type': 'client_credentials'}
        url = 'https://api.vasttrafik.se/token'
        head = {'Authorization': 'Basic ' + base64.b64encode((self.KEY + ':' + self.SECRET).encode()).decode(),
                'Content-Type': 'application/x-www-form-urlencoded'}

        r = requests.post(url, headers=head, params=parameters)
        tmp = r.json()
        self.ACCESS_TOKEN = tmp['access_token']

    def getStopID(self, STOP):
        # Step 2: Get stop id from stop string using api method 'location.name'
        url = 'https://api.vasttrafik.se/bin/rest.exe/v2/location.name'
        parameters = {'format': 'json', 'input': STOP}
        head = {'Authorization': 'Bearer ' + self.ACCESS_TOKEN}
        r = requests.get(url, headers=head, params=parameters)
        tmp = r.json()
        STOP_ID = tmp['LocationList']['StopLocation'][0]['id']
        return STOP_ID

    def getDepartures(self, stop):
        # self.getAccess()
        STOP_ID = self.getStopID(stop)

        # Step 3: Get list of depatures using api method 'departureBoard'
        now = datetime.now()
        url = 'https://api.vasttrafik.se/bin/rest.exe/v2/departureBoard'
        parameters = {'format': 'json', 'id': STOP_ID, 'date': now.strftime("%Y-%m-%d"), 'time': now.strftime("%H:%M")}
        head = {'Authorization': 'Bearer ' + self.ACCESS_TOKEN}
        r = requests.get(url, headers=head, params=parameters)
        tmp = r.json()
        return tmp

    def automatic_getAccessToken(self):
        # creating a timer object
        self.timer = QTimer()
        # adding action to timer
        self.timer.timeout.connect(self.getAccess)
        # update the timer every 50 min = 5e3 sec = 5e6 msec
        self.timer.start(5e6)