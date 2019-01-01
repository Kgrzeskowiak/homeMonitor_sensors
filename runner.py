from temperature_reader import TemperatureReader
import i2c

i2c.lcd_init()
i2c.clear()
i2c.lcd_string("Aplikacja uruchomiona",0x80)
tr = TemperatureReader()
tr.startReading()
