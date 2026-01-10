# Base image
FROM ubuntu:22.04

# Set DEBIAN_FRONTEND to noninteractive to avoid prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Set working directory
WORKDIR /root

# Install essential dependencies and common tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    curl \
    wget \
    tar \
    build-essential \
    lsb-release \
    gnupg \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies for OpenROAD, KLayout, and Yosys
# RUN apt-get update && apt-get install -y --no-install-recommends \
#     qtbase5-dev \
#     qttools5-dev \
#     libqt5xmlpatterns5-dev \
#     qtmultimedia5-dev \
#     libqt5multimediawidgets5 \
#     libqt5svg5-dev \
#     python3-dev \
#     ruby \
#     ruby-dev \
#     libz-dev \
#     libgit2-dev \
#     libx11-xcb1 \
#     libxcb-icccm4 \
#     libxcb-image0 \
#     libxcb-keysyms1 \
#     libxcb-randr0 \
#     libxcb-render-util0 \
#     libxcb-xinerama0 \
#     libxcb-xkb1 \
#     libxkbcommon-x11-0 \
#     x11-apps \
#     libqt5x11extras5 \
#     qt5-default \
#     libxcb-xfixes0 \
#     libxcb-cursor0 \
#     libgl1-mesa-glx \
#     xvfb \
#     bc \
#     && rm -rf /var/lib/apt/lists/*
RUN apt-get update && apt-get install -y --no-install-recommends \
    qtbase5-dev \
    qtbase5-dev-tools \
    qtchooser \
    qt5-qmake \
    qttools5-dev \
    qttools5-dev-tools \
    libqt5xmlpatterns5-dev \
    qtmultimedia5-dev \
    libqt5multimediawidgets5 \
    libqt5svg5-dev \
    libqt5x11extras5 \
    python3-dev \
    ruby \
    ruby-dev \
    libz-dev \
    libgit2-dev \
    libx11-xcb1 \
    libxcb-icccm4 \
    libxcb-image0 \
    libxcb-keysyms1 \
    libxcb-randr0 \
    libxcb-render-util0 \
    libxcb-xinerama0 \
    libxcb-xkb1 \
    libxkbcommon-x11-0 \
    x11-apps \
    libxcb-xfixes0 \
    libxcb-cursor0 \
    libgl1-mesa-glx \
    xvfb \
    bc \
    && rm -rf /var/lib/apt/lists/*

# Install OSS CAD Suite
# RUN curl -L -O https://github.com/YosysHQ/oss-cad-suite-build/releases/download/2025-03-14/oss-cad-suite-linux-x64-20250314.tgz && \
#     tar -xzf oss-cad-suite-linux-x64-20250314.tgz -C /root && \
#     rm oss-cad-suite-linux-x64-20250314.tgz
# ENV PATH="/root/oss-cad-suite/bin:${PATH}"
COPY oss-cad-suite-linux-x64-20250314.tgz  /root/
RUN tar -xzf oss-cad-suite-linux-x64-20250314.tgz -C /root && \
    rm oss-cad-suite-linux-x64-20250314.tgz
ENV PATH="/root/oss-cad-suite/bin:${PATH}"

# Install KLayout
RUN curl -L -O https://www.klayout.org/downloads/Ubuntu-22/klayout_0.29.12-1_amd64.deb && \
    curl -L -O https://www.klayout.org/downloads/gpg-public-expires-2028-03-03.key && \
    apt-key add gpg-public-expires-2028-03-03.key && \
    apt-get update && \
    # Use apt-get install -y ./file.deb which handles dependencies automatically
    apt-get install -y ./klayout_0.29.12-1_amd64.deb && \
    rm klayout_0.29.12-1_amd64.deb gpg-public-expires-2028-03-03.key && \
    rm -rf /var/lib/apt/lists/*

# Install OpenROAD
# Using the specific version from your commands, downloaded from GitHub releases
# RUN wget https://github.com/The-OpenROAD-Project/OpenROAD/releases/download/latest/openroad-2.0-19576-gec1bf1a13-Ubuntu-22.04.deb && \
#     apt-get update && apt-get install -y --no-install-recommends ./openroad-2.0-19576-gec1bf1a13-Ubuntu-22.04.deb && \
#     rm openroad-2.0-19576-gec1bf1a13-Ubuntu-22.04.deb && \
#     rm -rf /var/lib/apt/lists/*
COPY openroad_2.0-19576-gec1bf1a13_amd64-ubuntu-22.04.deb /root/
RUN apt-get update && apt-get install -y --no-install-recommends ./openroad_2.0-19576-gec1bf1a13_amd64-ubuntu-22.04.deb && \
    rm openroad_2.0-19576-gec1bf1a13_amd64-ubuntu-22.04.deb && \
    rm -rf /var/lib/apt/lists/*

# Clone OpenROAD repository (needed for ppa_scripts, etc.)
# RUN git clone --recursive https://github.com/The-OpenROAD-Project/OpenROAD.git /root/OpenROAD
COPY ./OpenROAD /root/OpenROAD

# Set environment variables needed at runtime
ENV QT_QPA_PLATFORM=offscreen
ENV OPENROAD_EXE="/usr/bin/openroad"

# Add environment variables to .bashrc for interactive sessions
RUN echo 'export PATH="/root/oss-cad-suite/bin:$PATH"' >> /root/.bashrc && \
    echo 'export QT_QPA_PLATFORM=offscreen' >> /root/.bashrc && \
    echo 'export OPENROAD_EXE="/usr/bin/openroad"' >> /root/.bashrc

# Copy the PPA script into the container and make it executable
COPY src/ppa_script/run_synthesis_ppa.sh /root/ppa_scripts/
RUN chmod +x /root/ppa_scripts/run_synthesis_ppa.sh

# Verify installations (optional, prints versions during build)
RUN yosys -V || echo "Yosys verification failed"
RUN klayout -v || echo "KLayout verification failed"
RUN openroad -version || echo "OpenROAD verification failed"

# Default command could be bash for interactive use
# CMD ["/bin/bash"]
