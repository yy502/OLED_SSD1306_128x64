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

#### Dependencies (Pillow and SMBus) ####

    sudo apt-get install python-dev python-setuptools libjpeg-dev python-smbus
    sudo easy_install Pillow

#### I2C ####

- Ensure `/etc/modules` contains `i2c-dev`.
- Use `raspi-config` to enable I2C on Raspberry Pi. 
- Reboot
- Ensure `i2c-1` is listed in `/dev` as a working device.

