FROM oven/bun:alpine
WORKDIR /frontend
COPY package.json ./
RUN bun install
COPY . .
EXPOSE 3000
CMD ["bun","run","dev"]
