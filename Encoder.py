import json

from PublicKey import PublicKey


class Encoder:

    __CHUNK_SIZE = 32

    def __init__(self, public_key: PublicKey):
        self.__key = public_key

    def encode_file(self, in_path: str, out_path: str):
        encoded_data = []
        last_chunk_len: int

        with open(in_path, 'rb') as file:
            while True:
                chunk = file.read(self.__CHUNK_SIZE)
                if not chunk:
                    break

                last_chunk_len = len(chunk)
                encoded_data.append(self.__encode_chunk(chunk))

        with open(out_path, 'w') as file:
            json.dump(
                {'payload': encoded_data, 'last_chunk_len': last_chunk_len},
                file
            )

    def __encode_chunk(self, chunk):
        bits = self.__bytes_to_bits(chunk)
        items_sum = 0
        for add_item, key_item in zip(bits, self.__key.sequence):
            if add_item:
                items_sum += key_item

        return items_sum

    @staticmethod
    def __bytes_to_bits(chunk):
        number = int.from_bytes(chunk, byteorder="big")

        bit_string = bin(number)[2:].zfill(256)
        return [bit == '1' for bit in bit_string]
