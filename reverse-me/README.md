# reverse-me

## Project Overview

The goal of the 'reverse-me' project is to reverse engineer the binaries located in the `level1`, `level2`, and `level3` directories. Each binary has the same name as its directory and requires a specific password to pass. The project also includes a `source.c` file for each level that replicates the behavior of the corresponding binary. Additionally, there are patch files available to modify the binaries so that they will pass with any input.

## Directory Structure

```
reverse-me/
├── level1/
│   ├── level1
│   ├── level1_patch
│   ├── source.c
│   └── password
├── level2/
│   ├── level2
│   ├── level2_patch
│   ├── source.c
│   └── password
└── level3/
    ├── level3
    ├── level3_patch
    ├── source.c
    └── password
```

## Level 1

- **Binary**: `level1`
- **Password**: The password can be found by inspecting the defined data of the binary. It directly compares the input to the password `__stack_check`.
- **User Input**: The input must match the password exactly.
- **Patch**: The patch file `level1_patch` modifies the binary to set the return value of `strcmp` to 0 after it has been called, allowing any input to pass.

## Level 2

- **Binary**: `level2`
- **Password**: The full password inside the binary is `delabere`. The input needs to be ASCII values representing each byte of this string, but the first character is skipped, and the value needs to be `00`. The correct password input that passes is: `00101108097098101114101`.
- **Patch**: The patch file `level2_patch` modifies the binary to perform a JMP instruction before any checks are done on the input, redirecting to the code that sets it to pass.

## Level 3

- **Binary**: `level3`
- **Password**: Similar to level 2, the internal password is `********`, but the first two numbers need to be `4` and `2`. The correct user input is `42042042042042042042042`.
- **Patch**: The patch file `level3_patch` works the same way as level 2, applying a JMP instruction to bypass the password check.

## Applying Patches

Patches can be applied using the `bspatch` tool. To apply a patch, use the following command:

```bash
bspatch <original_binary> <patched_binary> <patch_file>
```

For example, to patch the `level1` binary:

```bash
bspatch level1 level1_patched level1_patch
```
