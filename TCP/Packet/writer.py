# -*- coding: utf-8 -*-

from io import BytesIO


class Writer(BytesIO):

    def __init__(self):
        super().__init__()

    def write_byte(self, value):
        self.write(value.to_bytes(1, 'big'))

    def write_uint32(self, value):
        self.write(value.to_bytes(4, 'big'))

    def write_string(self, value):
        if value:
            self.write_uint32(len(value))
            self.write(value.encode('utf-8'))

        else:
            self.write_uint32(0xffffffff)

    def write_vint(self, value):
        rotate = True

        if value == 0:
            self.write_byte(0)

        else:
            value = (value << 1) ^ (value >> 31)
            while value:
                b = value & 0x7f

                if value >= 0x80:
                    b |= 0x80

                if rotate:
                    rotate = False
                    lsb = b & 0x1
                    msb = (b & 0x80) >> 7
                    b >>= 1
                    b &= ~(0xC0)
                    b |= (msb << 7) | (lsb << 6)

                self.write_byte(b)
                value >>= 7

    def write_bytearray(self, value):
        self.write_uint32(len(value))
        self.write(value)
