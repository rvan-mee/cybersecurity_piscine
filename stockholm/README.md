# Stockholm Program

## Overview

The Stockholm program is designed to encrypt and decrypt files in a specific directory on the Linux platform. It is intended to reverse the effects of ransomware by restoring files to their original state.

## Usage

There are multiple different options for this script:

```bash
./stockholm.py --help/-h
./stockholm.py --version/v
./stockholm.py --reverse/-r <key>
./stockholm.py --silent/-s
```

## Infecting Files

To encrypt files in the `infection` folder, ensure the `STOCKHOLM_KEY` environment variable is defined. You can do this by running:

```bash
export STOCKHOLM_KEY=$(cat example_key.txt)
./stockholm.py
```

## File Extensions

The program will only act on files with extensions affected by WannaCry. Ensure that the files you want to encrypt are in the `infection` folder in the user's HOME directory.


## Makefile

A Makefile is included to facilitate the running of the program. Use the following commands:

- To reverse the infection:
  ```bash
  make reverse
  ```

- To infect files:
  ```bash
  make infect
  ```

## Notes

- The encryption key must be at least 16 characters long.  
- Files will be renamed with the `.ft` extension upon encryption. If they already have this extension, they will not be renamed.
