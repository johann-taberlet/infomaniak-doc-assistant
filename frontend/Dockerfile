# Build stage
FROM node:20-alpine AS builder

WORKDIR /app

# Accept build arguments for Vite environment variables
ARG VITE_API_URL
ENV VITE_API_URL=$VITE_API_URL

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci

# Copy source code
COPY . .

# Build the application (VITE_API_URL will be embedded)
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
