import json

from PrivateKey import PrivateKey


class Decoder:
    def __init__(self, private_key: PrivateKey):
        self.__key = private_key

    def decode_file(self, in_path: str, out_path: str):
        with open(in_path, 'r') as file:
            data = json.load(file)

        encoded_data = data['payload']
        last_chunk_len = data['last_chunk_len']

        decoded_chunks = []

        for encoded_chunk in encoded_data:
            decoded_chunks.append(self.__decode_chunk(encoded_chunk))

        with open(out_path, 'wb') as file:
            for chunk in decoded_chunks[:-1]:
                file.write(chunk)

            file.write(decoded_chunks[-1][-last_chunk_len:])

    def __decode_chunk(self, encoded_chunk):
        modular_inverse = self.__modular_inverse(self.__key.n, self.__key.m)
        c = (encoded_chunk * modular_inverse) % self.__key.m

        decomposition = bytearray()
        current_byte = 0
        bit_count = 0

        for num in reversed(self.__key.sequence):
            if c >= num:
                current_byte |= (1 << bit_count)
                c -= num

            bit_count += 1

            if bit_count == 8:
                decomposition.append(current_byte)
                current_byte = 0
                bit_count = 0

        if bit_count > 0:
            decomposition.append(current_byte)

        return decomposition[::-1]

    @staticmethod
    def __extended_gcd(a, b):
        if b == 0:
            return a, 1, 0
        gcd, x1, y1 = Decoder.__extended_gcd(b, a % b)
        x = y1
        y = x1 - (a // b) * y1
        return gcd, x, y

    @staticmethod
    def __modular_inverse(n, m):
        gcd, x, _ = Decoder.__extended_gcd(n, m)
        if gcd != 1:
            raise ValueError(f"No inverse {n} for modulo {m}.")
        return x % m

    @staticmethod
    def __bits_to_bytes(bits):
        bit_string = ''.join('1' if bit else '0' for bit in bits)
        byte_length = (len(bit_string) + 7) // 8
        return int(bit_string, 2).to_bytes(byte_length, byteorder="big")
