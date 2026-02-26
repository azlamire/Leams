#NOTE: https://docs.astral.sh/uv/guides/integration/docker/#available-images
FROM python:3.14-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin
WORKDIR /backend
COPY pyproject.toml uv.lock ./
RUN uv sync
COPY . .
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "6000"]
