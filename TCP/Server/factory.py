# -*- coding: utf-8 -*-

from twisted.internet.protocol import Factory
from TCP.Server.protocol import ServerProtocol


class ServerFactory(Factory):

    def __init__(self, client_endpoint, crypto, replay, arguments):
        self.client_endpoint = client_endpoint
        self.replay = replay
        self.crypto = crypto
        self.args = arguments

    def buildProtocol(self, endpoint):
        return ServerProtocol(self)
