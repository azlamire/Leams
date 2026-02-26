FROM node:25
WORKDIR /frontend
COPY package.json bun.lock ./
RUN curl -fsSL https://bun.com/install | bash
ENV PATH="/root/.bun/bin:${PATH}"
RUN bun install 
COPY . .
CMD ["bun", "run", "dev"]
