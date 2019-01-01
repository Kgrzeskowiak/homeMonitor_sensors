import RPi.GPIO as GPIO
import time
import i2c
import requests

GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.IN) #PIR
i2c.lcd_init()
i2c.clear()

try:
    time.sleep(2) # to stabilize sensor
    while True:
        if GPIO.input(21):
            print("weszlo")
            i2c.lcd_string("Wykryto ruch", 0x80)
            payload = {'status': 'true'}
            r = requests.post("http://192.168.1.102:5000/endpoint", params=payload)
            time.sleep(4) #to avoid multiple detection
            i2c.clear()
            payload = {'status': 'false'}
            r = requests.post("http://192.168.1.102:5000/endpoint", params=payload)
        time.sleep(0.1) #loop delay, should be less than detection delay

except:
    GPIO.cleanup()