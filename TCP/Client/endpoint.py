# -*- coding: utf-8 -*-

from twisted.internet.endpoints import TCP4ClientEndpoint


class ClientEndpoint(TCP4ClientEndpoint):

    @property
    def host(self):
        return self._host

    @property
    def port(self):
        return self._port
