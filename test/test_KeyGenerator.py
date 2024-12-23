import math
import unittest

from KeyGenerator import KeyGenerator


class KeyGeneratorTest(unittest.TestCase):

    __keygen = KeyGenerator()

    def test_private_key_has_super_increasing_sequence(self):
        privateKey, publicKey = self.__keygen.generate_keys()

        sumItems = 0
        for i in privateKey.sequence:
            self.assertGreater(i, sumItems)
            sumItems += i

    def test_m_is_greater_than_sum_items(self):
        privateKey, publicKey = self.__keygen.generate_keys()
        sumItems = sum(privateKey.sequence)
        self.assertGreater(privateKey.m, sumItems)

    def test_gcd_of_m_and_r_is_equal_to_1(self):
        privateKey, publicKey = self.__keygen.generate_keys()
        self.assertEqual(1, math.gcd(privateKey.m, privateKey.n))


if __name__ == '__main__':
    unittest.main()
