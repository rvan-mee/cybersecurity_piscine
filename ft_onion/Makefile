# Variables
PUB_KEY_PATH := $(HOME)/.ssh/id_rsa.pub
IMAGE_NAME := ft_onion_image
CONTAINER_NAME := ft_onion

.PHONY: check-key build rebuild start stop clean

start: clean-known-host build
	@docker-compose up

check-key:
	@if [ ! -f "$(PUB_KEY_PATH)" ]; then \
		echo "SSH public key not found at $(PUB_KEY_PATH)."; \
		read -p "Do you want to create one now? (y/n) " answer; \
		if [ "$$answer" = "y" ] || [ "$$answer" = "Y" ]; then \
			ssh-keygen -t rsa -b 4096 -f $(HOME)/.ssh/id_rsa -N ""; \
		else \
			echo "Please create an SSH key before continuing."; \
			exit 1; \
		fi \
	else \
		echo "SSH public key found at $(PUB_KEY_PATH)"; \
	fi

build: check-key
	@DOCKER_BUILDKIT=1 PUB_KEY_PATH=$(PUB_KEY_PATH) docker-compose build

rebuild: check-key
	@DOCKER_BUILDKIT=1 PUB_KEY_PATH=$(PUB_KEY_PATH) docker-compose build --no-cache

clean-known-host:
	@echo "Removing old SSH host key for [localhost]:4242 from known_hosts..."
	@ssh-keygen -f "$(HOME)/.ssh/known_hosts" -R "[localhost]:4242" || true

clean: stop
	@echo "Removing container: $(CONTAINER_NAME)..."
	@docker rm $(CONTAINER_NAME) || true
	@echo "Cleaning images..."
	@docker image prune -a -f
	@echo "Done!"
