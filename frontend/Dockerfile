FROM oven/bun:latest
WORKDIR /frontend
COPY package.json ./
COPY bun.lock ./
RUN bun install
COPY . .
EXPOSE 3000
CMD ["sleep", "infinity"]
