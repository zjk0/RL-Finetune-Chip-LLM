FROM ubuntu:22.04

# Avoid interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Install Icarus Verilog and other dependencies
RUN apt-get update && apt-get install -y \
    iverilog \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Set up working directory
WORKDIR /workspace

# Default command
CMD ["bash"]
