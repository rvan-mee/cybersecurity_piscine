# README

## Overview

This repository contains two Python scripts: `spider.py` and `scorpion.py`.

- **spider.py**: A script designed to download images from a specified website, with options for recursive downloading and setting the download path.
- **scorpion.py**: A script that extracts metadata and EXIF data from images and files.

## Install Required Packages

To install the necessary dependencies, run:

```bash
pip install -r requirements.txt
```

## spider.py

### Description

`spider.py` is a command-line tool that allows users to download images from a given URL. It supports recursive downloads and allows users to specify the depth of recursion and the download path.

### Usage

```bash
./spider.py <URL> [options]
```

### Arguments

- `URL`: The URL from which to download images (required).
  
### Options

- `-r`, `--recursive`: Enables recursive downloads. If this flag is set, the script will follow links to download images from subpages.
  
- `-l`, `--depth`: Sets the depth of the recursion. If the `-r` flag is enabled and no value is given, a default depth of 5 is set. The depth determines how many levels deep the spider will go when following links. The default value is `1`.

- `-p`, `--path`: Sets the path where the images will be downloaded. The default directory is `./data/`, which will be created if it does not already exist.

### Example

To download images from a website:

```bash
./spider.py https://example.com -r -l 3 -p ./images/
```

## scorpion.py

### Description

`scorpion.py` is a command-line tool that extracts metadata and EXIF data from images and files. It can process multiple files in a single command (duplicates will be shown once).

### Usage

```bash
./scorpion.py <file1> [file2 ...]
```

### Arguments

- `file1`: The first file from which to extract metadata (required).
- `file2`: Additional files from which to extract metadata (optional).

### Example

To extract metadata from one or more files:

```bash
./scorpion.py image1.jpg image2.png
```
