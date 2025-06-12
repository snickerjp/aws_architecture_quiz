# Use the official Python 3.12 image as a base
FROM python:3.12

# Install necessary tools and dependencies
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    sudo \
    # Download and install Amazon Q
    && wget -qO /tmp/amazon-q.deb https://desktop-release.q.us-east-1.amazonaws.com/latest/amazon-q.deb \
    && apt-get install -y /tmp/amazon-q.deb \
    && rm /tmp/amazon-q.deb \
    && rm -rf /var/lib/apt/lists/*

# Set up a non-root user for VS Code
ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    # Set default shell to bash for the new user
    && usermod --shell /bin/bash $USERNAME \
    && apt-get install -y sudo \
    && echo "$USERNAME ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

# Switch to the non-root user
USER $USERNAME

# 必要なディレクトリを作成し、ファイルをコピー
RUN mkdir -p ~/.aws/amazonq
COPY mcp.json ~/.aws/amazonq/mcp.json

# Install Python tools
RUN python3 -m pip install --upgrade pip \
    && python3 -m pip install --user pipx \
    && /home/${USERNAME}/.local/bin/pipx install uv

# Set PATH environment variable
ENV PATH="/home/${USERNAME}/.local/bin:${PATH}"

# Set the working directory
WORKDIR /workspace

# Default command
CMD ["/bin/bash"]
