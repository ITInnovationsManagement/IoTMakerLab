"""
Module Name:  SendData.py
Project:      IoTHubRestSample
Copyright (c) Microsoft Corporation & Sandro Veiga Perez.
Using [Send device-to-cloud message](https://msdn.microsoft.com/en-US/library/azure/mt590784.aspx) API to send device-to-cloud message from the simulated device application to IoT Hub.
This source is subject to the Microsoft Public License.
See http://www.microsoft.com/en-us/openness/licenses.aspx#MPL
All other rights reserved.
THIS CODE AND INFORMATION IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, 
EITHER EXPRESSED OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED 
WARRANTIES OF MERCHANTABILITY AND/OR FITNESS FOR A PARTICULAR PURPOSE.
"""

from json import JSONEncoder
import time #to get timestamp
import datetime #to convert timestamp to SQL Date
import base64
import hmac
import hashlib
import requests
import urllib
import os
import glob
import time
import RPi.GPIO as GPIO


class D2CMsgSender:
    
    API_VERSION = '2016-02-03'
    TOKEN_VALID_SECS = 10
    TOKEN_FORMAT = 'SharedAccessSignature sig=%s&se=%s&skn=%s&sr=%s'
    
    def __init__(self, connectionString=None):
        if connectionString != None:
            iotHost, keyName, keyValue = [sub[sub.index('=') + 1:] for sub in connectionString.split(";")]
            self.iotHost = iotHost
            self.keyName = keyName
            self.keyValue = keyValue
            
    def _buildExpiryOn(self):
        return '%d' % (time.time() + self.TOKEN_VALID_SECS)
    
    def _buildIoTHubSasToken(self, deviceId):
        resourceUri = '%s/devices/%s' % (self.iotHost, deviceId)
        targetUri = resourceUri.lower()
        expiryTime = self._buildExpiryOn()
        toSign = '%s\n%s' % (targetUri, expiryTime)
        key = base64.b64decode(self.keyValue.encode('utf-8'))
        signature = urllib.quote(
            base64.b64encode(
                hmac.HMAC(key, toSign.encode('utf-8'), hashlib.sha256).digest()
            )
        ).replace('/', '%2F')
        return self.TOKEN_FORMAT % (signature, expiryTime, self.keyName, targetUri)
    
    def sendD2CMsg(self, deviceId, message):
        sasToken = self._buildIoTHubSasToken(deviceId)
        url = 'https://%s/devices/%s/messages/events?api-version=%s' % (self.iotHost, deviceId, self.API_VERSION)
        r = requests.post(url, headers={'Authorization': sasToken}, data=message)
        return r.text, r.status_code
    
    def read_pir(self):
        GPIO.setup(10, GPIO.IN)
        GPIO.setup(3, GPIO.OUT)
        GPIO.input(10)

#Die Main-Methode in der die Daten geschickt werden
if __name__ == '__main__':
    assigned_number = ''
    primary_key = ''
    connectionString = 'HostName=IoT-Makerlab-Hub.azure-devices.net;SharedAccessKeyName=iothubowner;SharedAccessKey='+primary_key
    #Erzeugt einen D2CMsgSender-Objekt zum Senden von Device-to-Cloud Nachrichten
    d2cMsgSender = D2CMsgSender(connectionString)
    room = 'iot_maker_'+assigned_number
    deviceId = "iotmaker"+assigned_number
    
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)

    
    GPIO.setup(10, GPIO.IN) #PIN10 wird als Input definiert um die Sensordaten aufzunehmen
    GPIO.setup(3, GPIO.OUT) #PIN3 ist ein Ausgang zum Ansteuern der LED
    
    occ_old = GPIO.input(10)
    try:
        while True:
            occ=GPIO.input(10)
            if(occ_old != occ):
                print "Status geaendert"
                if occ==0:                 #Wenn der Output des Bewegungssensors LOW ist
                    print "No intruders",occ
                    GPIO.output(3, GPIO.LOW)
                elif occ==1:               #Wenn der Output des Bewegungssensors LOW ist
                    print "Intruder detected",occ
                    GPIO.output(3,GPIO.HIGH)
                time_seconds = time.time()
                timestamp = datetime.datetime.fromtimestamp(time_seconds).strftime('%Y-%m-%d %H:%M:%S')
                jsonString = JSONEncoder().encode({
                    "room" : room, 
                    "occupied": occ,
                    "timestamp": timestamp
                })
                d2cMsgSender.sendD2CMsg(deviceId, jsonString)
                occ_old = occ
                time.sleep(0.2)
    except:
        GPIO.output(3, GPIO.LOW)
