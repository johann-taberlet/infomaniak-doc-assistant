# Build stage
FROM node:20-alpine AS builder

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci

# Copy source code
COPY . .

# Build the application
RUN npm run build

# Production stage with Caddy
FROM caddy:2-alpine

# Copy built files
COPY --from=builder /app/dist /srv

# Copy Caddyfile
COPY Caddyfile /etc/caddy/Caddyfile

# Expose port (Railway will set PORT env var)
EXPOSE 80

# Start Caddy
CMD ["caddy", "run", "--config", "/etc/caddy/Caddyfile", "--adapter", "caddyfile"]
