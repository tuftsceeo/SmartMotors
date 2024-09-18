from machine import Pin, SoftI2C

i2c = SoftI2C(scl=Pin(7), sda=Pin(6))

import ledmatrix
a=ledmatrix.LEDMATRIX(i2c)
a.display_emoji(10,1,1)