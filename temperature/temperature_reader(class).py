import Adafruit_DHT as DHT
import datetime
import time

class TemperatureReader:
    def __init__(self, interval = None):
        self.pin = 26
        self.interval = interval or 5

    def read(self):
        return DHT.read_retry(DHT.DHT11, self.pin)
    def saveResult(self):
        t = self.read()[1]
        h = self.read()[0]
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
        with open('results.txt', 'a+') as fileHandler:
            fileHandler.write(datetime.datetime.now().strftime('%d-%m-%y %H:%M;'))
            fileHandler.write(str(temperature)+';')
            fileHandler.write(str(humidity))
            fileHandler.write('\n')
    def startReading(self):
        while True:
            self.saveResult()
            time.sleep(self.interval)






