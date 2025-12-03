FROM python:3.12-slim
WORKDIR /backend
COPY package.json ./
RUN source .venv/bin/activate
COPY . .
EXPOSE 3001
CMD ["python","./app/main.py"]
