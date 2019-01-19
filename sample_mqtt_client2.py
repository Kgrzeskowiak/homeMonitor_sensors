#!/usr/bin/env python3


import paho.mqtt.client as mqtt
import time  # Can never get enough...
import datetime
import json

now = datetime.datetime.now()
MQTT_HOST = "192.168.1.9"
MQTT_PORT = 1883
client_id = "node2"

register = {
  "id" : client_id,
  "type" : "temperature"
}
registerMessage = json.dumps(register)

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # client.subscribe("loopback/hello")
    client.publish("register", payload= registerMessage, qos=0, retain=False)


def on_message(client, userdata, msg):
    print(msg.topic+": "+str(msg.payload))


client = mqtt.Client(client_id)  # Create a client instance

# Callback declarations
client.on_connect = on_connect
client.on_message = on_message
client.connect(MQTT_HOST, MQTT_PORT, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_start()
index = 0
reading = {
  "temperature": 10,
  "humidity": 30,
  "date": now.strftime("%Y-%m-%d %H:%M"),
  "id": client_id
}
message = json.dumps(reading)
# client.publish("register", payload= registerMessage, qos=0, retain=False)
time.sleep(60)
while True:
    index = index + 1
    time.sleep(60)
    client.publish("sensors/temperature", payload= message,
                   qos=0, retain=False)