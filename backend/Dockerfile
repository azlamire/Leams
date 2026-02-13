FROM python:3.14-alpine
WORKDIR /backend
COPY pyproject.toml ./
RUN pip install
COPY . .
CMD ["uvicorn","app.main:app"]
