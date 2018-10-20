# -*- coding: utf-8 -*-

from UDP.CryptoRC4 import Crypto
from TCP.Packet.reader import Reader
from TCP.Packet.writer import Writer
from UDP.packetProcessor import packetProcessor
from twisted.internet.protocol import DatagramProtocol


class UDPProtocol(DatagramProtocol):

    def __init__(self, listen_host, listen_port, replay):
        self.connection_dict = {}
        self.listen_host = listen_host
        self.listen_port = listen_port
        self.packetProcessor = packetProcessor(self.connection_dict, replay)

        self.packetProcessor.start()

    def build_udp_info_packet(self, client_host, data):
        udp_info_reader = Reader(data)
        udp_info_writer = Writer()

        server_port = udp_info_reader.read_vint()
        server_host = udp_info_reader.read_string()
        session_key = udp_info_reader.read_bytearray()
        nonce = udp_info_reader.read_string()

        print('[*] Received Udp Info Message with host: {}, port: {} !'.format(server_host, server_port))

        self.connection_dict[session_key] = {}
        session = self.connection_dict[session_key]

        session['nonce'] = nonce
        session['client_port_setted'] = False

        print('Nonce: {}'.format(nonce.encode('utf-8').hex()))

        session[server_host] = {
                                'host': [client_host, None],
                                'next_sequence_id': 1,
                                'crypto': Crypto(b'fhsd6f86f67rt8fw78fw789we78r9789wer6re', nonce.encode('utf-8'))
                                }

        session[client_host] = {
                                'host': [server_host, server_port],
                                'next_sequence_id': 1,
                                'crypto': Crypto(b'fhsd6f86f67rt8fw78fw789we78r9789wer6re', nonce.encode('utf-8'))
                                }

        udp_info_writer.write_vint(self.listen_port)
        udp_info_writer.write_string(self.listen_host)
        udp_info_writer.write_bytearray(session_key)
        udp_info_writer.write_string(nonce)

        return udp_info_writer.getvalue()

    def datagramReceived(self, data, addr):
        self.packetProcessor.queue.put([addr[0], data])

        session_key = data[:10]
        session = self.connection_dict[session_key]

        if not session['client_port_setted']:
            session['client_port_setted'] = True
            session[session[addr[0]]['host'][0]]['host'][1] = addr[1]

        self.transport.write(data, tuple(session[addr[0]]['host']))
