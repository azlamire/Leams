#NOTE: https://docs.astral.sh/uv/guides/integration/docker/#available-images
# В качестве основы берем официальный образ Playwright для Python 
# (версия v1.44.0 - можете поменять на нужную вам, если в uv.lock другая)
FROM mcr.microsoft.com/playwright/python:v1.44.0-jammy
WORKDIR /pre_ansible

COPY pyproject.toml uv.lock /pre_ansible/

RUN uv sync
RUN uv run playwright install
COPY . /pre_ansible/

# Оставляем CMD как вы и просили
CMD ["uv", "run", "ansible-playbook", "-i", "inventory.yaml", "playbook.yaml", "--tags", "pre_ansible"]
