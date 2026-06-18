FROM python:3.14-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    xvfb x11vnc procps xauth chromium git curl wget ca-certificates net-tools \
    && rm -rf /var/lib/apt/lists/*

RUN git clone --branch v1.4.0 --depth 1 https://github.com/novnc/noVNC.git /opt/novnc \
    && git clone --branch v0.12.0 --depth 1 https://github.com/novnc/websockify /opt/novnc/utils/websockify \
    && ln -s /opt/novnc/vnc.html /opt/novnc/index.html

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV UV_PYTHON_PREFERENCE=only-system \
    UV_PYTHON_DOWNLOADS=never \
    UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1 \
    PLAYWRIGHT_BROWSERS_PATH=/opt/ms-playwright

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-install-project --no-editable

COPY . .
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-editable

RUN --mount=type=cache,target=/root/.cache/ms-playwright \
    uv run playwright install --with-deps chromium

COPY --chmod=755 execution_entrypoint.sh /pre_ansible/
EXPOSE 6080

ENTRYPOINT ["/pre_ansible/execution_entrypoint.sh"]

CMD ["uv", "run", "ansible-playbook", "-i", "inventory.yaml", "playbook.yaml", "--tags", "pre_ansible", "-vvv"]
