# https://bun.com/docs/guides/ecosystem/docker
FROM oven/bun:alpine AS base
WORKDIR /usr/src/app

FROM base AS install
COPY package.json bun.lock ./
RUN bun install --frozen-lockfile

FROM base AS builder
COPY --from=install /usr/src/app/node_modules ./node_modules
COPY . .
RUN bun run build

FROM base AS release
COPY --from=builder /usr/src/app/.next ./.next
COPY package.json bun.lock ./
COPY --from=install /usr/src/app/node_modules ./node_modules

USER bun
EXPOSE 3000/tcp
ENTRYPOINT [ "bun", "run", "start" ]
