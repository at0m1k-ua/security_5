import tempfile
import unittest

from Decoder import Decoder
from Encoder import Encoder
from KeyGenerator import KeyGenerator


class EncoderTest(unittest.TestCase):

    def test_encoder_reads_file_and_writes_encoded_one(self):
        expected_string = \
            """
            Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent viverra vitae arcu sagittis ornare. 
            Nam orci elit, varius commodo tellus vel, congue placerat dui. Etiam id urna bibendum, interdum tellus eu, 
            porttitor lacus. Quisque non nunc risus. Duis convallis diam a odio vestibulum gravida. Phasellus porta 
            sapien vitae congue commodo. Integer id tempus orci. Nulla pharetra dui ac orci ullamcorper tincidunt.
            """

        tempdir = tempfile.gettempdir()

        in_file_path = f'{tempdir}/in_file.txt'
        out_file_path = f'{tempdir}/out_file.txt.bag'
        decoded_file_path = f'{tempdir}/decoded.txt'

        with open(in_file_path, 'w') as file:
            file.write(expected_string)

        keygen = KeyGenerator()
        privateKey, publicKey = keygen.generate_keys()

        encoder = Encoder(publicKey)
        encoder.encode_file(in_file_path, out_file_path)

        decoder = Decoder(privateKey)
        decoder.decode_file(out_file_path, decoded_file_path)

        with open(decoded_file_path, 'r') as decoded_file:
            actual_string = decoded_file.read()

        self.assertEqual(expected_string, actual_string)
