# Use Debian Bookworm based
FROM ghcr.io/astral-sh/uv:python3.13-bookworm

# Create working directory
WORKDIR /app

# Copy local files to container
COPY . /app

# Path environment
ENV PATH="/app/.venv/bin:$PATH"
ENV CI=true

# Add NodeSource repository for Node.js 22
RUN apt update && apt install -y curl
RUN curl -fsSL https://deb.nodesource.com/setup_22.x | bash -

# Install nodejs
RUN apt install -y nodejs

# uv sync 
RUN uv sync

# Set default command to run the script
ENTRYPOINT ["uv", "run"]
CMD ["main.py"]
