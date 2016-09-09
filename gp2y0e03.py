
_REGISTER_SHIFT_BIT = const(0x35)
_REGISTER_DISTANCE1 = const(0x5e)
_REGISTER_DISTANCE2 = const(0x5f)


class GP2Y0E03:
    def __init__(self, i2c, address=0x40):
        self.i2c = i2c
        self.address = address
        self.shift(1)

    def _register8(self, register, value=None):
        if value is None:
            return self.i2c.readfrom_mem(self.address, register, 1)[0]
        self.i2c.writeto_mem(self.address, register, bytearray([value]))

    def shift(self, value=None):
        if value not in (1, 2, None):
            raise ValueError("shift has to be 1 or 2")
        if value is not None:
            self._shift = value
        return self._register8(_REGISTER_SHIFT_BIT, value)

    def read(self, raw=False):
        low = self._register8(_REGISTER_DISTANCE2)
        high = self._register8(_REGISTER_DISTANCE1)
        value =  (high << 4 | low & 0x0f)
        if raw:
            return high, low, value
        # value in cm
        return (value / 16) / (1 << self._shift)
