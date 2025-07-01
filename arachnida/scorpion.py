#!/usr/bin/python3

from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
from colorama import init as colorama_init
from colorama import Fore
from colorama import Style
from datetime import datetime
import sys
import os

file_paths = set()

def parse_input():
    for file_path in sys.argv[1:]:
        if not os.path.exists(file_path) or not os.path.isfile(file_path) or not os.access(file_path, os.R_OK):
            print(Fore.RED + 'Unable to open file: ' + file_path + Fore.RESET)
        else:
            file_paths.add(file_path)

file_exif_data = dict()

def parse_exif():
    for path in file_paths:
        img = Image.open(path)
        exif_data = img._getexif()

        if exif_data is not None:
            current_exif_data = dict()
            for tag_id, value in exif_data.items():
                # Get the tag name
                tag_name = TAGS.get(tag_id, tag_id)
                current_exif_data[tag_name] = value
            file_exif_data[path] = current_exif_data


def timeConvert(time):
#   dt = time
  newtime = datetime.fromtimestamp(time)
  return str(newtime.date())
   
def sizeFormat(size):
    newform = format(size/1024, ".2f")
    return newform + " KB"

file_metadata = dict()
def parse_file_metadata():
    for file in file_paths:
        data = os.stat(file)
        attrs = {
            'Name: ' + os.path.basename(file),
            'Size (KB): ' + sizeFormat(data.st_size),
            'Creation Date: ' + timeConvert(data.st_ctime),
            'Modified Date: ' + timeConvert(data.st_mtime),
            'Last Access Date: ' + timeConvert(data.st_atime),
        }
        file_metadata[file] = attrs

def print_data():
    for file in file_paths:
        print('Data for file: ' + Fore.GREEN + file + Fore.RESET)
        for attr in file_metadata[file]:
            print('\t' + attr)
        
        if file in file_exif_data:
            print('\n\tEXIF:')
            data = file_exif_data[file]
            max_key_length = max(len(key) for key in data.keys())
            longest_str_len = 0
            for key, value in data.items():
                print_str = f'\t\t{key.ljust(max_key_length)} | {value}'
                if len(print_str) > longest_str_len:
                    longest_str_len = len(print_str)
                print(print_str)
            print(Fore.LIGHTBLACK_EX + str('-' * longest_str_len) + Fore.RESET)
        else:
            print(Fore.LIGHTBLACK_EX + '\t\tno exif data found for file: ' + file + Fore.RESET)

if __name__=="__main__":
    colorama_init()
    parse_input()
    parse_exif()
    parse_file_metadata()
    print_data()
