#!/bin/bash

set -xe

# Start Xvfb
rm -f /tmp/.X99-lock
rm -f /tmp/.X11-unix/X99
Xvfb :99 -screen 0 1980x1024x24 &
export DISPLAY=:99

# Wait for Xvfb to be ready
echo "Waiting for Xvfb...."
for i in {1..10}; do
    if xdpyinfo -display :99 >/dev/null 2>&1; then
        echo "Xvfb is ready."
        break
    fi
    echo "Waiting for Xvfb..."
    sleep 1
done

# Start x11vnc
x11vnc -display :99 -forever -nopw -quiet -listen localhost -xkb &

# Start noVNC
/opt/novnc/utils/novnc_proxy --vnc localhost:5900 --listen 6080 &

# Execute passed command
exec "$@"
