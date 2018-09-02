# -*- coding: utf-8 -*-


class packetReceiver:

    buffer = b''
    packet = b''

    def dataReceived(self, data):

        self.buffer += data
        while self.buffer:
            if self.packet:
                packet_id = int.from_bytes(self.packet[:2], "big")
                packet_length = int.from_bytes(self.packet[2:5], "big")

                if len(self.buffer) >= packet_length:
                    self.packet += self.buffer[:packet_length]
                    self.processPacket(packet_id, self.packet)
                    self.packet = b""
                    self.buffer = self.buffer[packet_length:]

                else:
                    break

            elif len(self.buffer) >= 7:
                self.packet = self.buffer[:7]

                if len(self.buffer) == 7 and int.from_bytes(self.packet[2:5], 'big') == 0:
                    packet_id = int.from_bytes(self.packet[:2], "big")
                    self.processPacket(packet_id, self.packet)

                self.buffer = self.buffer[7:]
