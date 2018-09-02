# -*- coding: utf-8 -*-

from TCP.Client.protocol import ClientProtocol
from twisted.internet.protocol import ClientFactory


class ClientFactory(ClientFactory):

    def __init__(self, server):
        self.server = server

    def buildProtocol(self, addr):
        return ClientProtocol(self)
