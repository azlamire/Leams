FROM python:3.12-slim
WORKDIR /docs
COPY package.json ./
RUN npm install 
RUN source .venv/bin/activate
COPY . .
EXPOSE 3001
CMD ["mkdocs","serve","-a","localhost:8001","--livereload"]
