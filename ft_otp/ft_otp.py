#!/usr/bin/python3

from cryptography.fernet import Fernet
from colorama import init, Fore
import qrcode_terminal
import hashlib
import argparse
import base64
import time
import hmac
import os



default_encrypted_secret_file_name = 'ft_otp.key'
extremely_safe_key = b'se5z6AvGwqCP9Q5c77UvONgRIZtYF5_i-7gyTtIgFDc='

def parse_input():
    parser = argparse.ArgumentParser(prog='ft_otp', usage='%(prog)s [options] [input]', description='A script to get a time based one time password')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-g', action='store_true', help='Generate a OTP using the given key file')
    group.add_argument('-k', action='store_true', help='A file containing a hexadecimal key of at least 64 characters, it will be stored inside an encrypted file called \'' + default_encrypted_secret_file_name + '\'')
    group.add_argument('-q', action='store_true', help='Generates a qr code for the given key')
    group.add_argument('-v', action='store_true', help='Validate a one-time-password')
    parser.add_argument('input_file', metavar='[FILE]', type=str, help='The required file to be used with the selected option')

    args = parser.parse_args()

    if os.path.exists(args.input_file):
        if not os.access(args.input_file, os.R_OK):
            print(Fore.RED + 'No read permissions for input file: ' + args.input_file + Fore.RESET)
            exit(1)
    else:
        print(Fore.RED + 'Input file: ' + args.input_file + ' does not exist' + Fore.RESET)
        exit(1)

    return args


def encrypt_file_contents(file_content):
    fernet = Fernet(extremely_safe_key)
    return fernet.encrypt(file_content)

def decrypt_file_contents(file_content):
    try:
        fernet = Fernet(extremely_safe_key)
        decrypted_content = fernet.decrypt(file_content)
    except Exception as error:
        print(Fore.RED + 'Error decrypting the secret: ' + str(error) + Fore.RESET)
        exit(1)
    return decrypted_content

def is_hexadecimal_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
        for char in content:
            if char not in '0123456789abcdefABCDEF':
                return False
        return True

def generate_secret(key_file_path):
    if os.path.exists(default_encrypted_secret_file_name):
        if not os.access(default_encrypted_secret_file_name, os.W_OK):
            print(Fore.RED + 'No write permissions to secret file: ' + default_encrypted_secret_file_name)
            exit(1)
        else:
            print(Fore.RED + default_encrypted_secret_file_name + ': Already exists, do you wish to overwrite it?' + Fore.RESET)
            while True:
                response = input('Overwrite it? (y/n): ').strip().lower()
                if response in ['n', 'no']:
                    exit(1)
                if response in ['y', 'yes', '']:
                    break
                print(Fore.RED + '\'' + response + '\' is not a valid option' + Fore.RESET)

    if os.path.getsize(key_file_path) < 64:
        print(Fore.RED + 'Secret file: ' + key_file_path + ': does not contain enough characters, a minimum of 64 is required' + Fore.RESET)
        exit(1)

    if not is_hexadecimal_file(key_file_path):
        print(Fore.RED + 'Secret file: ' + key_file_path + ': must only contain hexadecimal characters' + Fore.RESET)
        exit(1)

    if not os.path.getsize(key_file_path) % 2 == 0:
        print(Fore.RED + 'Secret file: ' + key_file_path + ': contains an odd-length string' + Fore.RESET)
        exit(1)

    with open(default_encrypted_secret_file_name, 'wb') as encrypted_file:
        with open(key_file_path, 'rb') as key_file:
            encrypted_file.write(encrypt_file_contents(key_file.read()))
            print(Fore.GREEN + 'Successfully generated the encrypted file: ' + default_encrypted_secret_file_name + Fore.RESET)


def generate_counter():
    # '//' is a floor division so we get a new counter every 30 seconds
    return int(time.time() // 30).to_bytes(8, 'big')

# HOTP works by using a HMAC(K, C) function, where K is the key and C is the counter (in this case the current time, changing every 30 seconds)
def generate_HOTP(encrypted_key_file_path):
    decrypted_file_content = decrypt_file_contents(open(encrypted_key_file_path, 'rb').read())

    # Convert the decrypted file into the key, where a pair of hex characters represent the value of a single byte:
    K = bytes.fromhex(decrypted_file_content.decode('utf-8').upper())
    C = generate_counter()

    # generate the OTP using sha1: https://datatracker.ietf.org/doc/html/rfc6238 page 13
    hash = hmac.new(K, C, hashlib.sha1).digest()

    offset = hash[-1] & 0x0F

    binary = (hash[offset] & 0x7F) << 24 \
           | (hash[offset + 1] & 0xFF) << 16 \
           | (hash[offset + 2] & 0xFF) << 8 \
           | (hash[offset + 3] & 0xFF)

    # We have to take 6 digits:
    digits = 6
    otp = str(binary % (10 ** digits))
    otp = otp.zfill(digits)

    return otp


def generate_QR(encrypted_key_file_path):
    decrypted_key_content = decrypt_file_contents(open(encrypted_key_file_path, 'rb').read())
    # Convert the decrypted file into the key, where a pair of hex characters represent the value of a single byte:
    secret = bytes.fromhex(decrypted_key_content.decode('utf-8').upper())
    # The standard requires the secret to be base32 encoded:
    secret_b32 = base64.b32encode(secret).decode('utf-8')
    # Remove the padding, some authenticators do not support this
    secret_b32 = secret_b32.rstrip('=')

    issuer = 'ft_otp'
    account = os.getlogin()

    # Generate and print the QR code URI
    uri = f'otpauth://totp/{issuer}:{account}?secret={secret_b32}&issuer={issuer}'
    qrcode_terminal.draw(uri)


def validate_code(encrypted_key_file_path):
    while True:
        code = input('Please enter your code: ')
        if code.isdigit() and len(code) == 6:
            break
        else:
            print(Fore.RED + 'Code is not 6 digits!' + Fore.RESET)

    otp = generate_HOTP(encrypted_key_file_path)
    if (otp == code):
        print(Fore.GREEN + 'Code matched, access granted!' + Fore.RESET)
    else:
        print(Fore.RED + 'Code mismatch, access denied' + Fore.RESET)
        exit(403)


if __name__ == "__main__":
    init() # colorama
    args = parse_input()
    if args.q:
        generate_QR(args.input_file)
    elif args.v:
        validate_code(args.input_file)
    elif args.g:
        print(generate_HOTP(args.input_file))
    elif args.k:
        generate_secret(args.input_file)
