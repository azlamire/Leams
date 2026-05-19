#NOTE: https://docs.astral.sh/uv/guides/integration/docker/#available-images
# В качестве основы берем официальный образ Playwright для Python 
# (версия v1.44.0 - можете поменять на нужную вам, если в uv.lock другая)
FROM python:3.14-slim

# Фиксируем версию uv для воспроизводимости
COPY --from=ghcr.io/astral-sh/uv:0.6.15 /uv /uvx /bin/

WORKDIR /pre_ansible

RUN apt-get update && apt-get install -y --no-install-recommends \
    xvfb x11vnc procps xauth chromium git curl wget ca-certificates net-tools \
    && rm -rf /var/lib/apt/lists/*

RUN git clone --branch v1.4.0 --depth 1 https://github.com/novnc/noVNC.git /opt/novnc \
    && git clone --branch v0.12.0 --depth 1 https://github.com/novnc/websockify /opt/novnc/utils/websockify \
    && ln -s /opt/novnc/vnc.html /opt/novnc/index.html

COPY pyproject.toml uv.lock /pre_ansible/


ENV UV_PYTHON_PREFERENCE=only-system
ENV UV_PROJECT_ENVIRONMENT=/pre_ansible/.venv
ENV UV_LINK_MODE=copy

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen

ENV PLAYWRIGHT_BROWSERS_PATH=/opt/ms-playwright

RUN --mount=type=cache,target=/root/.cache/ms-playwright \
    uv run playwright install --with-deps chromium

COPY . .

COPY --chmod=755 execution_entrypoint.sh /pre_ansible/

EXPOSE 6080

ENTRYPOINT ["/pre_ansible/execution_entrypoint.sh"]

CMD ["uv", "run", "ansible-playbook", "-i", "inventory.yaml", "playbook.yaml", "--tags", "pre_ansible", "-vvv"]
