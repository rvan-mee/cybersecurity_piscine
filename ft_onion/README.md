# ft_onion

## Run Your Own Hidden Service with Tor + Nginx

ft_onion is a Dockerized project that sets up a Tor hidden service. It launches a secure Nginx web server inside a container and exposes it on the Tor network.

---

## Getting Started

### 1. Start the Hidden Service

```bash
make start
```

This will:
- Build the Docker image
- Start the container using Docker Compose
- Launch the Tor daemon and configure the hidden service
- Start the Nginx web server

---

### 2. SSH into the Container

```bash
ssh ft_onion@localhost -p 4242
```

> SSH access is secured using **public key authentication**.

---

### 3. Retrieve Your `.onion` Address

To get your Tor hidden service hostname:

```bash
sudo cat /var/lib/tor/ft_onion/hostname
```

This command outputs your service’s unique `.onion` address, e.g.:

```
ExampleOnionString.onion
```

You can now access your Nginx site via Tor at that address.

---


## Makefile Commands

The `Makefile` provides convenient shortcuts to build, run, and manage your `ft_onion` project. Below are the main targets you can use:

### `make start`

Starts the project by:
- Building the Docker image (if needed)
- Running the container using Docker Compose
- Launching the Tor service and Nginx web server

Use this command to initialize and run the hidden service.

---

### `make build`

Builds the Docker image with BuildKit enabled. Ensures SSH access is properly configured with your public key. Use this when setting up the project or after changes to the configuration.

---

### `make rebuild`

Forces a complete rebuild of the Docker image without using any cached layers. Useful for testing or applying changes cleanly.

---

### `make clean`

Cleans up the environment by:
- Stopping and removing the running container
- Pruning unused Docker images

Use this to reset your setup or free system resources.

---
