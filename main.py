import argparse
import json

from Decoder import Decoder
from Encoder import Encoder
from KeyGenerator import KeyGenerator
from PrivateKey import PrivateKey
from PublicKey import PublicKey


def generate_keys(public_key_name, private_key_name):
    private_key, public_key = KeyGenerator().generate_keys()

    with open(public_key_name, "w") as public_key_file:
        json.dump(public_key.dict(), public_key_file)

    with open(private_key_name, "w") as private_key_file:
        json.dump(private_key.dict(), private_key_file)

    print(f"Ключі збережено у файлах: {public_key_name}, {private_key_name}")


def encrypt(public_key, input_file, output_file):
    with open(public_key, "r") as public_key_file:
        public_key = PublicKey.from_dict(json.load(public_key_file))

    Encoder(public_key).encode_file(input_file, output_file)
    print(f"Файл зашифровано: {output_file}")


def decrypt(private_key, input_file, output_file):
    with open(private_key, "r") as private_key_file:
        private_key = PrivateKey.from_dict(json.load(private_key_file))

    Decoder(private_key).decode_file(input_file, output_file)
    print(f"Файл розшифровано: {output_file}")


def main():
    parser = argparse.ArgumentParser(description="Програма для роботи з ключами, шифрування та дешифрування.")

    subparsers = parser.add_subparsers(dest="command", required=True, help="Режим роботи програми")

    generate_parser = subparsers.add_parser("generate", help="Генерація ключів")
    generate_parser.add_argument("--public-key", required=True, help="Ім'я файлу для збереження публічного ключа")
    generate_parser.add_argument("--private-key", required=True, help="Ім'я файлу для збереження приватного ключа")

    encrypt_parser = subparsers.add_parser("encrypt", help="Шифрування файлу")
    encrypt_parser.add_argument("--public-key", required=True, help="Ім'я файлу з публічним ключем")
    encrypt_parser.add_argument("--input", required=True, help="Ім'я вхідного файлу для шифрування")
    encrypt_parser.add_argument("--output",
                                required=True,
                                help="Ім'я вихідного файлу для збереження зашифрованих даних")

    decrypt_parser = subparsers.add_parser("decrypt", help="Дешифрування файлу")
    decrypt_parser.add_argument("--private-key", required=True, help="Ім'я файлу з приватним ключем")
    decrypt_parser.add_argument("--input", required=True, help="Ім'я вхідного файлу для дешифрування")
    decrypt_parser.add_argument("--output",
                                required=True,
                                help="Ім'я вихідного файлу для збереження розшифрованих даних")

    args = parser.parse_args()

    if args.command == "generate":
        generate_keys(args.public_key, args.private_key)
    elif args.command == "encrypt":
        encrypt(args.public_key, args.input, args.output)
    elif args.command == "decrypt":
        decrypt(args.private_key, args.input, args.output)


if __name__ == "__main__":
    main()
