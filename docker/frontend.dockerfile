# docker/frontend.Dockerfile
FROM node:22-slim

WORKDIR /app

# 1. Install system utilities required for potential native C++ node compilation modules
RUN apt-get update && apt-get install -y \
    python3 \
    make \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# 2. Install Quasar CLI globally using corepack/npm under Node 22 runtime
RUN npm install -g @quasar/cli

# 3. Copy ALL app source code files into the container context
# This guarantees that 'quasar prepare' has access to src/, tsconfig, etc. during postinstall
COPY . .

# 4. Clear cache and trigger clean installation
RUN npm cache clean --force && npm install --legacy-peer-deps

EXPOSE 9000

CMD ["quasar", "dev", "-m", "spa", "--hostname", "0.0.0.0", "--port", "9000"]