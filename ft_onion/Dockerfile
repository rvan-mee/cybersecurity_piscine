FROM debian:bullseye-slim

EXPOSE 4242

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    nginx \
    tor \
    openssh-server \
    ssh \
    sudo \
    curl

# Set correct directory permissions
RUN mkdir -p /var/lib/tor /run/tor && \
    chown -R debian-tor:debian-tor /var/lib/tor /run/tor && \
    chmod 700 /var/lib/tor

# Copy Tor config
COPY --chown=debian-tor:debian-tor tools/torrc /etc/tor/torrc

# Copy nginx config
COPY tools/nginx.conf /etc/nginx/sites-available/default

# Copy static content
COPY tools/index.html /var/www/html/index.html
COPY tools/bonus.html /var/www/html/bonus.html

# Copy and set SSH settings
COPY tools/sshd_config /etc/ssh/sshd_config
# Create user to SSH to and add it to the sudoers
RUN adduser ft_onion
RUN usermod -aG sudo ft_onion && \
    echo "ft_onion ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

RUN --mount=type=secret,id=pubkey \
    cat /run/secrets/pubkey > /pubkey-debug.txt

# Add public key to all non-root users
RUN --mount=type=secret,id=pubkey \
    awk -F: '$3 >= 1000 && $1 != "nobody" {print $1 ":" $6}' /etc/passwd | while IFS=: read user home; do \
        mkdir -p "$home/.ssh" && \
        cat /run/secrets/pubkey > "$home/.ssh/authorized_keys" && \
        chown -R "$user:$user" "$home/.ssh" && \
        chmod 700 "$home/.ssh" && \
        chmod 600 "$home/.ssh/authorized_keys"; \
    done

# Copy the boot script
COPY tools/boot.sh /boot.sh
RUN chmod +x /boot.sh

# Start Tor and Nginx inside a shell and print the hostname
ENTRYPOINT ["/boot.sh"] 