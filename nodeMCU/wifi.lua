
wifi.setmode(wifi.STATION)
print('set mode=STATION (mode='..wifi.getmode()..')\n')
print('MAC Address: ',wifi.sta.getmac())
print('Chip ID: ',node.chipid())
print('Heap Size: ',node.heap(),'\n')
gpio.mode(1, gpio.OUTPUT)
gpio.write(1, gpio.LOW)
myTimer = tmr.create()

-- Configure WiFi
wifi.sta.config{ssid="SSID", pwd="PASSWORD"}
tmr.alarm(0, 1000, 1, function()
	if wifi.sta.getip() == nil then
		print("Connecting to AP...\n")

   	else
    	ip, nm, gw = wifi.sta.getip()
      	
    	-- Debug info
      	print("\n\nIP Info: \nIP Address: ",ip)
      	print("Netmask: ",nm)
      	print("Gateway Addr: ",gw,'\n')
      	
      	tmr.stop(0)		-- Stop the polling loop
      	
          -- Continue to main function after network connection
        gpio.write(1, gpio.HIGH)
        myTimer:register(8000, tmr.ALARM_SINGLE, function() print("hey there") end)
        gpio.write(1, gpio.LOW)
      	dofile("main.lua")
   	end
end)
