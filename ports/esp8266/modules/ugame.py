"""
A helper module that initializes the display and buttons for the uGame
game console. See https://hackaday.io/project/27629-game
"""

from machine import SPI, I2C, Pin
import st7735r


K_X = 0x02
K_DOWN = 0x80
K_LEFT = 0x40
K_RIGHT = 0x20
K_UP = 0x10
K_O = 0x04


class Audio:
    def __init__(self):
        pass

    def play(self, audio_file):
        pass

    def stop(self):
        pass

    def mute(self, value=True):
        pass


class Buttons:
    def __init__(self, i2c, address=0x10):
        self._i2c = i2c
        self._address = address

    def get_pressed(self):
        return self._i2c.readfrom(self._address, 1)[0]


spi = SPI(1, baudrate=40000000)
dc = Pin(12, Pin.OUT)
cs = Pin(15, Pin.OUT)
cs(0)
display = st7735r.ST7735R(spi, dc, 0b110)
i2c = I2C(-1, sda=Pin(4), scl=Pin(5))
buttons = Buttons(i2c)
audio = Audio()
