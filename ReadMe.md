### Acknowledgement ###

This library was initially developed by [RM Hull](https://github.com/rm-hull/ssd1306), and them simplified by [BLavery](https://github.com/BLavery/lib_oled96). I have forked BLavery's version and simplified it more to suit my needs.

### Summary ###

A Python library for 0.96" 128x64 I2C OLED display (4-pin version) using SSD1306 chip for Raspberry Pi.

The OLED display works with 3.3V and 5V power.

Texts, fonts, images and vector graphics are handled by the Python Imaging Library.

#### Fonts ####

`ttf` format seems to work fine, with scaling.

#### Images ####

Supports 1-bit `BMP` or `PNG` images.

#### Pillow ####

    sudo apt-get install python-dev python-setuptools
    sudo easy_install Pillow                                # or pip install?
    
    sudo apt-get install python3-dev python3-setuptools     # for Python 3
    sudo easy_install3 Pillow

#### I2C and SMBus ####

- Ensure `i2c-dev` is listed in `/etc/modules`
- Use `raspi-config` to enable I2C on Raspberry Pi. 
- Reboot
- Enter `ls /dev` in terminal and `i2c-1` should be listed as a working device.
- Now install `smbus` for Python

    sudo apt-get install python-smbus
    sudo apt-get install python3-smbus                      # for Python 3
