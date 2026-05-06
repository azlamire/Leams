# NOTE: https://docs.astral.sh/uv/guides/integration/docker/#available-images
FROM mcr.microsoft.com/playwright/python:v1.50.0-noble
WORKDIR /backend
COPY ./ /backend
RUN uv sync
COPY . .
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "6000"]

