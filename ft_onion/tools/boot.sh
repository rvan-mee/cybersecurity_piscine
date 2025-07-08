#!/bin/bash

# Start Tor in the background
tor &

# Ensure SSH privilege separation directory exists
mkdir -p /run/sshd

# Start ssh in the background
/usr/sbin/sshd &

# Start Nginx in foreground to keep container alive
nginx -g "daemon off;"
