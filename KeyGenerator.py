import math
from random import randint

from PrivateKey import PrivateKey
from PublicKey import PublicKey


class KeyGenerator:
    __MIN_INTERVAL = 1
    __MAX_INTERVAL = 16
    __KEY_SIZE = 256

    def generate_keys(self) -> (PrivateKey, PublicKey):
        privateKey = self.__generate_private_key()
        publicKey = self.__generate_public_key(privateKey)

        return privateKey, publicKey

    def __generate_private_key(self) -> PrivateKey:
        sequence = []
        sumItems = 0
        for i in range(KeyGenerator.__KEY_SIZE):
            newItem = sumItems + randint(self.__MIN_INTERVAL, self.__MAX_INTERVAL)
            sequence.append(newItem)
            sumItems += newItem

        m = sumItems + self.__random_int()
        r = self.__find_r_by_gcd(m)

        return PrivateKey(sequence, m, r)

    @staticmethod
    def __generate_public_key(private_key: PrivateKey) -> PublicKey:
        sequence = []
        for i in private_key.sequence:
            sequence.append((i * private_key.n) % private_key.m)

        return PublicKey(sequence)

    def __random_int(self):
        return randint(self.__MIN_INTERVAL, self.__MAX_INTERVAL)

    @staticmethod
    def __find_r_by_gcd(m) -> int:
        q = 0.79

        r = int(m * q)
        for i in range(4096):
            r += 1
            if math.gcd(m, r) == 1:
                return r

        raise ValueError('Cannot get R value')
