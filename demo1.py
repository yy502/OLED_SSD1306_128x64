#!/usr/bin/env python

from oled import ssd1306
from smbus import SMBus

i2cbus = SMBus(1)        # 1 = Raspberry Pi but NOT early REV1 board
display = ssd1306(i2cbus)   # create oled object, nominating the correct I2C bus, default address

# put border around the screen:
display.canvas.rectangle((0, 0, display.width-1, display.height-1), outline=1, fill=0)

# Write two lines of text.
display.canvas.text((40,15),    'Hello', fill=1)
display.canvas.text((40,40),    'World!', fill=1)

# now display that canvas out to the hardware
display.flush()
