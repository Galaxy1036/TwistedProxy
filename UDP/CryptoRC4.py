# -*- coding: utf-8 -*-

from Crypto.Cipher import ARC4


class Crypto:

    def __init__(self, key, nonce):
        self.key = key + nonce
        self.stream = ARC4.new(self.key)
        self.stream.encrypt(self.key)

    def decrypt(self, cipher):
        return self.stream.decrypt(cipher)
