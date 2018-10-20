# -*- coding: utf-8 -*-

import os


class Replay:

    def __init__(self, dirname):
        self.session = None
        self.dirname = dirname

        self.tcp_path = '{}/TCP'.format(self.dirname)
        self.udp_path = '{}/UDP'.format(self.dirname)

        self.tcp_message_index_path = '{}/message.index'.format(self.tcp_path)
        self.udp_session_index_path = '{}/session.index'.format(self.udp_path)

        self.udp_session_path = None
        self.udp_message_index_path = None

        if not os.path.isdir(self.dirname):
            self.init_directory()

        else:
            self.check_directory()

    def init_directory(self):
        os.makedirs(self.dirname)
        os.makedirs(self.tcp_path)
        os.makedirs(self.udp_path)

        self.write_index(self.tcp_message_index_path)
        self.write_index(self.udp_session_index_path)

    def check_directory(self):
        if not os.path.isdir(self.tcp_path):
            os.makedirs(self.tcp_path)
            self.write_index(self.tcp_message_index_path)

        elif not os.path.isfile(self.tcp_message_index_path):
            self.write_index(self.tcp_message_index_path)

        if not os.path.isdir(self.udp_path):
            os.makedirs(self.udp_path)
            self.write_index(self.udp_session_index_path)

        elif not os.path.isfile(self.udp_session_index_path):
            self.write_index(self.udp_session_index_path)

    def write_index(self, path, index='0'):
        with open(path, 'w') as f:
            f.write(index)

    def increment_index(self, path, index):
        self.write_index(path, str(index + 1))

    def get_index(self, path):
        with open(path, 'r') as f:
            return int(f.read())

    def save_tcp_packet(self, packet_name, data):
        index = self.get_index(self.tcp_message_index_path)

        with open('{}/{}-{}.bin'.format(self.tcp_path, index, packet_name), 'wb') as f:
            f.write(data)

        self.increment_index(self.tcp_message_index_path, index)

    def save_udp_packet(self, session, packet_name, data):
        session_index = self.get_index(self.udp_session_index_path)

        if self.session is None:
            self.session = session

            self.udp_session_path = '{}/Session-{}'.format(self.udp_path, session_index)
            self.udp_message_index_path = '{}/packet.index'.format(self.udp_session_path)

            if not os.path.isdir(self.udp_session_path):
                os.makedirs(self.udp_session_path)
                self.write_index(self.udp_message_index_path)

        elif session != self.session:
            self.session = session
            self.increment_index(self.udp_session_index_path, session_index)

            session_index += 1

            self.udp_session_path = '{}/Session-{}'.format(self.udp_path, session_index)
            self.udp_message_index_path = '{}/packet.index'.format(self.udp_session_path)

            os.makedirs(self.udp_session_path)
            self.write_index(self.udp_message_index_path)

        packet_index = self.get_index(self.udp_message_index_path)

        with open('{}/{}-{}.bin'.format(self.udp_session_path, packet_index, packet_name), 'wb') as f:
            f.write(data)

        self.increment_index(self.udp_message_index_path, packet_index)
