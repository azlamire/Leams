FROM oven/bun:latest
WORKDIR /frontend
COPY package.json ./
COPY bun.lock ./
RUN bun install
COPY . .
CMD ["bun", "run", "dev"]
