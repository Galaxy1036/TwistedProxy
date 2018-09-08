# -*- coding: utf-8 -*-


packet_enum = {
                # Client Packet
                10100: "ClientHello",
                10101: "Login",
                14888: "ClientCapabilities",
                15665: "KeepAlive",

                # Server Packet
                20100: "ServerHello",
                20103: "LoginFailed",
                24662: "LoginOK",
                20247: "KeepAliveOk",
                25612: "SectorState",
                27691: "GoogleAccountAlreadyBound"
               }
