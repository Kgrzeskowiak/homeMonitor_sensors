MQTT_CLIENTID = "node_pierwszy"
gpio.mode(1, gpio.OUTPUT)
gpio.write(1, gpio.LOW)
myTimer = tmr.create()
dht_pin = 3
led_pin = 1

print("Main started")
mqtt = mqtt.Client(MQTT_CLIENTID, 60, "", "")
mqtt:on("connect", function(con) register_myself() end)
mqtt:on("offline", function(con) print ("offline") end)

mqtt:connect("192.168.1.9", 1883, 0,1)
  register = {
    ["id"] = MQTT_CLIENTID,
    ["type"] = "temperature"
  }

function register_myself()
    message = sjson.encode(register)  
    mqtt:publish("register", message, 0,0)
    gpio.write(led_pin, gpio.HIGH)
    myTimer:register(9000, tmr.ALARM_SINGLE, function() print("hey there") end)
    gpio.write(led_pin, gpio.LOW)
    myTimer:register(9000, tmr.ALARM_SINGLE, function() print("hey there") end)
    gpio.write(led_pin, gpio.HIGH)
    myTimer:register(9000, tmr.ALARM_SINGLE, function() print("hey there") end)
    gpio.write(led_pin, gpio.LOW)
    a = 0
    while( a < 2 )
    do
        dht_read()
        a = a+1
        myTimer:register(60000, tmr.ALARM_SINGLE, function() print("hey there") end)
    end
  
end
function dht_read()
        gpio.write(1, gpio.HIGH)
        status, temp, humi = dht.read11(3)
        if status == dht.OK then
                reading = {
                    ["temperature"] = temp,
                    ["humidity"] = humi,
                    ["id"] = MQTT_CLIENTID
                }
            messageTemp = sjson.encode(reading)  
            mqtt:publish("sensors/temperature", messageTemp, 0,0)
            myTimer:register(10000, tmr.ALARM_SINGLE, function() print("hey there") end)
            gpio.write(1, gpio.LOW)
elseif status == dht.ERROR_CHECKSUM then
    print( "DHT Checksum error." )
elseif status == dht.ERROR_TIMEOUT then
    print( "DHT timed out." )
end
end
