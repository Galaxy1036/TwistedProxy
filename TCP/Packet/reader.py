# -*- coding: utf-8 -*-

from io import BytesIO


class Reader(BytesIO):

    def __init__(self, data):
        super().__init__(data)

    @property
    def has_remaining_bytes(self):
        return len(self.getvalue()) > self.tell()

    def reinit(self, data):
        self.flush()
        self.seek(0)
        self.truncate(0)
        self.write(data)
        self.seek(0)

    def read_byte(self):
        return int.from_bytes(self.read(1), 'big')

    def read_uint32(self):
        return int.from_bytes(self.read(4), 'big')

    def read_string(self):
        return self.read(self.read_uint32()).decode('utf-8')

    def read_vint(self):
        shift = 0
        result = 0

        while True:
            byte = self.read(1)
            if shift == 0:
                byte = self._sevenBitRotateLeft(byte)

            i = int.from_bytes(byte, "big")
            result |= (i & 0x7f) << shift
            shift += 7
            if not (i & 0x80):
                break

        return (((result) >> 1) ^ (-((result) & 1)))

    def _sevenBitRotateLeft(self, byte):
        n = int.from_bytes(byte, 'big')
        seventh = (n & 0x40) >> 6  # save 7th bit
        msb = (n & 0x80) >> 7  # save msb
        n <<= 1  # rotate to the left
        n &= ~(0x181)  # clear 8th and 1st bit and 9th if any
        n |= (msb << 7) | (seventh)  # insert msb and 6th back in
        return bytes([n])

    def read_bytearray(self):
        return self.read(self.read_uint32())
