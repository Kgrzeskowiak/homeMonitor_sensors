//canot be used. temperature
"use strict";
 module.exports = class dhtSensor {
    constructor(pinNumber, dhtVersion, timeout)
    {
        this.pinNumber = pinNumber
        this.dhtVersion = dhtVersion
        this.rpiDhtSensor = require('rpi-dht-sensor');
        this.dht = null;
        this.timeout = timeout
    }

start()
{
    if (this.dhtVersion == 11)
    {
        this.dht = new this.rpiDhtSensor.DHT11(this.pinNumber)
    }
    if (this.dhtVersion == 22)
    {
        this.dht = new this.rpiDhtSensor.DHT22(this.pinNumber)
    }
    this.read(this.dht)
}
read(dht)
{
  var readout = dht.read();
 
    console.log('Temperature: ' + readout.temperature.toFixed(2) + 'C, ' +
        'humidity: ' + readout.humidity.toFixed(2) + '%');
    setTimeout(read, this.timeout);
}
}

