#!/usr/bin/env python

from PIL import Image, ImageDraw

class Const:
    CHARGEPUMP = 0x8D
    COLUMNADDR = 0x21
    COMSCANDEC = 0xC8
    COMSCANINC = 0xC0
    DISPLAYALLON = 0xA5
    DISPLAYALLON_RESUME = 0xA4
    DISPLAYOFF = 0xAE
    DISPLAYON = 0xAF
    EXTERNALVCC = 0x1
    INVERTDISPLAY = 0xA7
    MEMORYMODE = 0x20
    NORMALDISPLAY = 0xA6
    PAGEADDR = 0x22
    SEGREMAP = 0xA0
    SETCOMPINS = 0xDA
    SETCONTRAST = 0x81
    SETDISPLAYCLOCKDIV = 0xD5
    SETDISPLAYOFFSET = 0xD3
    SETHIGHCOLUMN = 0x10
    SETLOWCOLUMN = 0x00
    SETMULTIPLEX = 0xA8
    SETPRECHARGE = 0xD9
    SETSEGMENTREMAP = 0xA1
    SETSTARTLINE = 0x40
    SETVCOMDETECT = 0xDB
    SWITCHCAPVCC = 0x2

class ssd1306():

    def __init__(self, bus, address=0x3C):
        self.cmd_mode = 0x00
        self.data_mode = 0x40
        self.bus = bus
        self.addr = address
        self.width = 128
        self.height = 64
        self.pages = int(self.height / 8)
        self.image = Image.new('1', (self.width, self.height))
        self.canvas = ImageDraw.Draw(self.image) # this is a "draw" object for preparing display contents

        self._command(
            Const.DISPLAYOFF,
            Const.SETDISPLAYCLOCKDIV, 0x80,
            Const.SETMULTIPLEX,       0x3F,
            Const.SETDISPLAYOFFSET,   0x00,
            Const.SETSTARTLINE,
            Const.CHARGEPUMP,         0x14,
            Const.MEMORYMODE,         0x00,
            Const.SEGREMAP,
            Const.COMSCANDEC,
            Const.SETCOMPINS,         0x12,
            Const.SETCONTRAST,        0xCF,
            Const.SETPRECHARGE,       0xF1,
            Const.SETVCOMDETECT,      0x40,
            Const.DISPLAYALLON_RESUME,
            Const.NORMALDISPLAY,
            Const.DISPLAYON)

    def _command(self, *cmd):
        """
        Sends a command or sequence of commands through to the
        device - maximum allowed is 32 bytes in one go.
        LIMIT ON ARDUINO: CMD BYTE + 31 = 32, SO LIMIT TO 31     bl
        """
        assert(len(cmd) <= 31)
        self.bus.write_i2c_block_data(self.addr, self.cmd_mode, list(cmd))

    def _data(self, data):
        """
        Sends a data byte or sequence of data bytes through to the
        device - maximum allowed in one transaction is 32 bytes, so if
        data is larger than this it is sent in chunks.
        In our library, only data operation used is 128x64 long, ie whole canvas.
        """

        for i in range(0, len(data), 31):
            self.bus.write_i2c_block_data(self.addr, self.data_mode, list(data[i:i+31]))


    def flush(self):
        """
        The image on the "canvas" is flushed through to the hardware display.
        Takes the 1-bit image and dumps it to the SSD1306 OLED display.
        """

        self._command(
            Const.COLUMNADDR, 0x00, self.width-1,  # Column start/end address
            Const.PAGEADDR,   0x00, self.pages-1)  # Page start/end address

        pix = list(self.image.getdata())
        buf = []

        def make_byte(*lines):
            # Even though self.image is B/W, the pixel value is sometimes set to 255 instead of 1
            return ((lines[7] & 1) << 7 | (lines[6] & 1) << 6 | (lines[5] & 1) << 5
                | (lines[4] & 1) << 4 | (lines[3] & 1) << 3 | (lines[2] & 1) << 2
                | (lines[1] & 1) << 1 | (lines[0] & 1))

        lines = [ pix[i:i + self.width] for i in xrange(0, self.width * self.height, self.width) ]
        for l in range(0, self.height, 8):
            buf.extend(reversed(map(make_byte, *lines[l:l + 8])))

        self._data(buf) # push out the whole lot

    def clear(self):
        self.canvas.rectangle((0, 0, self.width-1, self.height-1), outline=0, fill=0)
        self.flush()

    def onoff(self, onoff):
        if onoff:
            self._command(Const.DISPLAYON)
        else:
            self._command(Const.DISPLAYOFF)

