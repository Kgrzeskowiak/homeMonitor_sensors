#!/usr/bin/env python3


import paho.mqtt.client as mqtt
import time  # Can never get enough...

MQTT_HOST = "192.168.1.9" 
MQTT_PORT = 1883
client_id = "node1"


def on_connect(client, userdata, rc):
    print("Connected with result code "+str(rc))
    # client.subscribe("loopback/hello")
    client.publish("register", payload= client_id)


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
temperature = 11
humidty = 22
message = "Temperature:" + str(temperature) + "Humdity:" + str(humidty)
while True:
    index = index + 1
    time.sleep(5)
    client.publish("sensors/temperature", payload= message,
                   qos=0, retain=False)