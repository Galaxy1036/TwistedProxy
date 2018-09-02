# -*- coding: utf-8 -*-

import os


class Replay:

    def __init__(self, dirname):
        self.dirname = dirname
        if not os.path.exists(self.dirname):
            os.makedirs(dirname)

        if not os.path.exists('{}/message.index'.format(self.dirname)):
            with open('{}/message.index'.format(self.dirname), 'w') as f:
                f.write('0')

    @property
    def index(self):
        with open('{}/message.index'.format(self.dirname), 'r') as f:
            index = int(f.read())

        return index

    def save_packet(self, packet_name, data):
        index = self.index

        with open('{}/{}-{}.bin'.format(self.dirname, index, packet_name), 'wb') as f:
            f.write(data)

        self.increment_index(index)

    def increment_index(self, index):
        with open('{}/message.index'.format(self.dirname), 'w') as f:
            f.write(str(index + 1))
