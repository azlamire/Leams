FROM mcr.microsoft.com/playwright:v1.56.0-noble

# Install required packages
RUN apt-get update && apt-get install -y \
    xvfb \
    x11vnc \
    python3-pip \
    git \
    net-tools \
    && rm -rf /var/lib/apt/lists/*

# Install noVNC
RUN git clone https://github.com/novnc/noVNC.git /opt/novnc \
    && git clone https://github.com/novnc/websockify /opt/novnc/utils/websockify \
    && ln -s /opt/novnc/vnc.html /opt/novnc/index.html

# Install Python dependencies
RUN pip3 install pytest pytest-playwright playwright==1.56.0 allure-pytest --break-system-packages

# Copy entrypoint
COPY execution_entrypoint.sh /execution_entrypoint.sh
RUN chmod +x /execution_entrypoint.sh

WORKDIR /app

EXPOSE 6080

ENTRYPOINT ["/execution_entrypoint.sh"]
