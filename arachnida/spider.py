#!/usr/bin/python3

from html.parser import HTMLParser
from urllib.parse import urljoin
from urllib.parse import urlparse
from colorama import init as colorama_init
from colorama import Fore
from colorama import Style
import urllib.request
import argparse
import sys
import os


clear_prev_line = '\33[2K'

def parse_input():
    parser = argparse.ArgumentParser(prog='spider', usage='%(prog)s [options]', description='A script to download images from a given website')
    parser.add_argument('URL', help='The URL used to download the data from')
    parser.add_argument('-r', '--recursive', help='Enables recursive downloads', action='store_true')
    parser.add_argument('-l', '--depth', nargs='?', type=int, help='Sets the depth of the recursion, if the -r flag is enabled and no value is given a default depth of 5 is set', const=5)
    parser.add_argument('-p', '--path', nargs=1, type=str, help='Sets the path where the images will be downloaded to, the default directory being ./data/ which will be created if it does not exist already', default='./data/')

    args = parser.parse_args()

    # Make sure recursion is enabled when the -l flag is selected
    if not args.recursive and ('-l' or 'depth' in sys.argv):
        print(Fore.RED + 'The -r or --recursive must be enabled when -l is given' + Fore.RESET)
        exit(1)

    if args.depth < 0:
        print(Fore.RED + 'Please provide a positive recursion depth' + Fore.RESET)
        exit(2)

    # Check if the given path exists
    if not os.path.isdir(args.path) and args.path != './data/':
        print(Fore.RED + 'Please provide a valid download directory' + Fore.RESET)
        exit(3)

    return args


def check_dir_permissions(path):
    return os.access(path, os.W_OK)

def check_download_dir(path):
    # Create default directory if it does not exist
    if path == './data/' and not os.path.isdir(path):
        if not check_dir_permissions('./'):
            print(Fore.RED + 'No permission to create the default ./data/ directory' + Fore.RESET)
            exit(4)
        else:
            os.mkdir(path)
            return

    # Check if there are write permissions for the given directory
    if not check_dir_permissions(path):
        print(Fore.RED + 'No write permissions for the given download path: ' + path + Fore.RESET)
        exit(5)

    return


accepted_img_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']

# Inherits from HTMLParser and overwrites the 'handle_starttag'
class SpiderParser(HTMLParser):
    def __init__(self):
        # Initialize the base/super class
        super().__init__()

        # If recursion is enabled we use all the links found on the current page to jump to
        self.urls = set()
        # The paths to all the images found in the give HTML
        self.image_paths = set()

    def handle_starttag(self, tag, attrs):
        # parse Images
        if tag == 'img':
            for att in attrs:
                if len(att) < 2 or att[0] != 'src':
                    continue
                for extension in accepted_img_extensions:
                    if att[1].endswith(extension):
                        self.image_paths.add(att[1])
                        print(clear_prev_line + Fore.GREEN + 'Found image url: ' + att[1], Fore.RESET, end='\r')

        # Parse hyperlinks
        if tag == 'a':
            for att in attrs:
                if len(att) < 2 or att[0] != 'href':
                    continue
                href = urlparse(att[1])
                # if these variables are set the href refers to a page outside of the staring url
                if href.netloc == '' and href.scheme == '':
                    self.urls.add(att[1])


    def handle_startendtag(self, tag, attrs):
        # For tags that end with a / (https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/img)
        if tag == 'img':
            for att in attrs:
                if len(att) < 2 or att[0] != 'src':
                    continue
                for extension in accepted_img_extensions:
                    if att[1].endswith(extension):
                        self.image_paths.add(att[1])
                        print(clear_prev_line + Fore.GREEN + 'Found image url: ' + att[1] + Fore.RESET, end='\r')


def validate_url(url):
    try:
        # Just make a request to the given url and see if it succeeds
        urllib.request.urlopen(url)
    except Exception as error:
        print(clear_prev_line + Fore.RED + 'Invalid URL: ' + url, end='')
        print(' Error: ', end='')
        print(error, end='')
        print(Fore.RESET, end = '\r')
        return False
    return True

# key = url, value = depth when url was visited
visited_urls = dict()
images_to_scrape = set()
def scrape_image_urls(current_url, recursion_enabled, depth):
    # Recursive exit conditions
    if recursion_enabled and depth <= 0:
        return

    # If we have already visited this url we check if we visited it
    # with a lower depth, if our current depth is higher we have the
    # possibility of finding new urls at a deeper depth. 
    if current_url in visited_urls and depth < visited_urls[current_url]:
        # Already visited it and our current depth will not give us new information
        return

    # Update the visited urls
    visited_urls[current_url] = depth

    # Parse the current url's HTML
    print(clear_prev_line + Fore.LIGHTBLACK_EX + 'Crawling on url: ' + current_url + Fore.RESET, end='\r')
    html = urllib.request.urlopen(current_url).read().decode('utf-8')
    parser = SpiderParser()
    parser.feed(html)

    # Add the images to the set for downloading
    for image_path in parser.image_paths:
        image_url = urljoin(current_url, image_path)
        if validate_url(image_url):
            images_to_scrape.add(image_url)

    if recursion_enabled:
        if depth - 1 != 0:
            for hyperlink in parser.urls:
                new_url = urljoin(current_url, hyperlink)
                # print('checking url: ' + new_url)
                if not validate_url(new_url):
                    continue                                                                                                                                                                                                                                                                
                scrape_image_urls(new_url, recursion_enabled, depth - 1)
    return


def get_image_filename(download_dir_path, image_url):
    filepath = download_dir_path + image_url.replace('/', '_')

    if not os.path.exists(filepath):
        return filepath

    x = 1
    base, ext = os.path.splitext(filepath)
    new_filepath = f"{base}({x}){ext}"

    while os.path.exists(new_filepath):
        x += 1
        new_filepath = f"{base}({x}){ext}"

    return new_filepath

def download_images(download_dir_path):
    for image_url in images_to_scrape:
        with urllib.request.urlopen(image_url) as image_data:
            file_name = get_image_filename(download_dir_path, image_url)
            with open(file_name, 'wb') as image:
                image.write(image_data.read())
                print(Fore.GREEN + 'Downloaded image: ' + file_name + Fore.RESET)


if __name__=="__main__":
    colorama_init()
    args = parse_input()
    check_download_dir(args.path)
    if not validate_url(args.URL):
        print('Please provide a valid url - have you added the scheme?')
        exit(6)
    scrape_image_urls(args.URL, args.recursive, args.depth)
    download_images(args.path)
