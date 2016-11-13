import ustruct

_REGISTER_SHIFT_BIT = const(0x35)
_REGISTER_DISTANCE = const(0x5e)


"""
import gp2y0e03
from machine import I2C, Pin
i2c = I2C(Pin(0), Pin(2))
s = gp2y0e03.GP2Y0E03(i2c)
"""

class GP2Y0E03:
    def __init__(self, i2c, address=0x40):
        self.i2c = i2c
        self.address = address
        self.shift(1)

    def _register8(self, register, value=None):
        if value is None:
            return self.i2c.readfrom_mem(self.address, register, 1)[0]
        self.i2c.writeto_mem(self.address, register, bytearray([value]))

    def _register16(self, register, value=None):
        if value is None:
            data = self.i2c.readfrom_mem(self.address, register, 2)
            return ustruct.unpack(">H", data)[0]
        self.i2c.writeto_mem(self.address, register, ustruct.pack(">H", value))

    def shift(self, value=None):
        if value not in {1, 2, None}:
            raise ValueError("Shift has to be 1 or 2")
        reading = self._register8(_REGISTER_SHIFT_BIT, value)
        if value is not None:
            self._shift = value
        else:
            self._shift = reading
        return reading

    def read(self, raw=False):
        value = self._register16(_REGISTER_DISTANCE)
        if raw:
            return value
        if value & 0xff00:
            return 0 # out of range
        # value in mm
        return (value / 16) / (1 << self._shift)
