# -*- coding: utf-8 -*-

import hexdump


from TCP.PacketReceiver import packetReceiver
from TCP.Packet.packetEnum import packet_enum
from twisted.internet.protocol import Protocol


class ClientProtocol(packetReceiver, Protocol):

    def __init__(self, factory):
        self.factory = factory
        self.factory.server.client = self
        self.server = self.factory.server
        self.crypto = self.server.crypto

    def connectionMade(self):
        self.peer = self.transport.getPeer()
        print('[*] Connected to {}:{}'.format(self.peer.host, self.peer.port))

    def connectionLost(self, reason):
        print('[*] Server closed the connection !')

    def processPacket(self, packet_id, data):
        packet_name = packet_enum.get(packet_id, packet_id)

        print('[*] {} received from server'.format(packet_name))

        decrypted = self.crypto.decrypt_server_packet(packet_id, data[7:])

        if self.server.factory.args.verbose and decrypted:
            print(hexdump.hexdump(decrypted))

        if self.server.factory.args.replay:
            self.server.factory.replay.save_packet(packet_name, data[:7] + decrypted)

        encrypted = self.crypto.encrypt_server_packet(packet_id, decrypted)
        payload = packet_id.to_bytes(2, 'big') + len(encrypted).to_bytes(3, 'big') + data[5:7] + encrypted

        self.server.transport.write(payload)
