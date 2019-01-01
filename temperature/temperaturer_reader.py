import Adafruit_DHT as DHT
import datetime
import time
import requests

name = 'temperatureRPI'
sensorType = 'DHT11'
gpio = 26
interval = 5

def register():
    payload = {'name': name, 'sensorType': sensorType, 'gpio': gpio}
    r = requests.post("http://localhost:3000/register", params=payload)
    print(r)
    startReading()

def read():
    return DHT.read_retry(DHT.DHT11, 26)

def prepareResult():
    t = read()[1]
    h = read()[0]
    x = 0
    readList = []
    while x < 3:
        print("petla")
        readList.append({'temperature':self.read()[1],'humidity':self.read()[0]})
        x += 1
        print(x)
    print ("wyjscie")
    temperature = sum(item['temperature'] for item in readList)/len(readList)
    humidity = sum(item['humidity'] for item in readList)/len(readList)
    date = datetime.datetime.now().strftime('%d-%m-%y %H:%M')
    sendResult(name, temperature, humidity,date)

def sendResult(id, temperature, humidity, date):
    payload = {'id' : id, 'temp' : temperature, 'humidity' : humidity, 'date' : date}
    r = requests.post("http://localhost:3000/temperature", params=payload)

def startReading():
    while True:
        prepareResult()
        time.sleep(interval)

register()