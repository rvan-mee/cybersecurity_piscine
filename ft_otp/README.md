# ft_otp

`ft_otp` is a command-line script designed to generate time-based one-time passwords (TOTPs) using a specified key file. This tool is useful for implementing two-factor authentication (2FA) in your applications.

## Usage

```bash
./ft_otp.py [options]
```

## Options

- `-k [FILE]`
  - **Description**: Provide a file containing a hexadecimal key of at least 64 characters. This key will be stored inside an encrypted file called `ft_otp.key`.
  - **Type**: String

- `-g [FILE]`
  - **Description**: Generate a one-time password (OTP) using the specified key file.
  - **Type**: String

- `-q`
  - **Description**: Generate a QR code for the given key file. This QR code can be scanned by authenticator apps to easily set up two-factor authentication.
  - **Type**: Flag (-g required required)

- `-v`
  - **Description**: Validate your password. This option checks if the provided password is correct.
  - **Type**: Flag (-g required)

## Requirements

- Python 3.x
- Install any required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Example

To provide a hexadecimal key and store it in an encrypted file:
```bash
./ft_otp.py -k example.key
```

To generate a one-time password using a key file:
```bash
./ft_otp.py -g ft_otp.key
```

To generate a QR code for the key:
```bash
./ft_otp.py -q -g ft_otp.key
```

To validate your password:
```bash
./ft_otp.py -v -g ft_otp.key
```
