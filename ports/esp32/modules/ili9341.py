import ustruct
import utime


class Display(object):
    _POS = bytearray(4)
    width = 320
    height = 240

    def __init__(self, spi, dc, cs=None, rst=None):
        self.spi = spi
        self.dc = dc
        self.cs = cs or (lambda x: x)
        self.rst = rst
        self.reset()

    def reset(self):
        if self.rst:
            self.rst(0)
            utime.sleep_ms(50)
            self.rst(1)
            utime.sleep_ms(50)
        self.cs(0)
        self.write(b'\x36', b'\x00')  # MADCTL
        self.write(b'\x3a', b'\x55')  # 16bit color
        self.write(b'\x11')
        self.write(b'\x29')
        self.cs(1)
        utime.sleep_ms(50)

    def write(self, command=None, data=None):
        if command is not None:
            self.dc(0)
            self.spi.write(command)
        if data:
            self.dc(1)
            self.spi.write(data)

    def block(self, x0, y0, x1, y1):
        ustruct.pack_into('>HH', self._POS, 0, x0, x1)
        self.write(b'\x2a', self._POS)
        ustruct.pack_into('>HH', self._POS, 0, y0, y1)
        self.write(b'\x2b', self._POS)
        self.write(b'\x2c')
        self.dc(1)

    def clear(self, color=0x00):
        self.cs(0)
        self.block(0, 0, self.width, self.height)
        chunks, rest = divmod(self.width * self.height, 512)
        pixel = ustruct.pack('>H', color)
        if chunks:
            data = pixel * 512
            for count in range(chunks):
                self.spi.write(data)
        if rest:
            self.spi.write(pixel * rest)
        self.cs(1)

    def __enter__(self):
        self.cs(0)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cs(1)
