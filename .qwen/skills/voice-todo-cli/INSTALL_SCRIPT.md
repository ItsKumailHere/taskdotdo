# Installation Script

Complete installation script for curl-based global installation of the voice-enabled todo CLI.

## install.sh

```bash
#!/usr/bin/env bash

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
REPO_URL="https://github.com/yourusername/voice-todo-cli"
INSTALL_DIR="${HOME}/.local/share/voice-todo-cli"
BIN_DIR="${HOME}/.local/bin"
APP_NAME="todo-voice"

echo -e "${GREEN}Voice-Enabled Todo CLI - Installer${NC}"
echo "======================================"
echo ""

# Detect OS
OS="$(uname -s)"
case "${OS}" in
    Linux*)     MACHINE=Linux;;
    Darwin*)    MACHINE=Mac;;
    CYGWIN*)    MACHINE=Windows;;
    MINGW*)     MACHINE=Windows;;
    *)          MACHINE="UNKNOWN:${OS}"
esac

echo "Detected OS: ${MACHINE}"

# Check prerequisites
check_prerequisites() {
    echo ""
    echo "Checking prerequisites..."
    
    # Check Python
    if ! command -v python3 &> /dev/null; then
        echo -e "${RED}Error: Python 3.12+ is required but not installed.${NC}"
        echo "Please install Python from https://www.python.org/"
        exit 1
    fi
    
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
    REQUIRED_VERSION="3.12"
    
    if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
        echo -e "${RED}Error: Python $REQUIRED_VERSION+ required, found $PYTHON_VERSION${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}✓ Python $PYTHON_VERSION${NC}"
    
    # Check pip
    if ! command -v pip3 &> /dev/null; then
        echo -e "${RED}Error: pip is required but not installed.${NC}"
        exit 1
    fi
    echo -e "${GREEN}✓ pip${NC}"
    
    # Check for required system packages
    if [ "$MACHINE" = "Linux" ]; then
        if ! dpkg -l | grep -q portaudio; then
            echo -e "${YELLOW}Warning: portaudio19-dev may be required for microphone support${NC}"
            echo "Install with: sudo apt-get install portaudio19-dev"
        fi
    elif [ "$MACHINE" = "Mac" ]; then
        if ! brew list portaudio &> /dev/null; then
            echo -e "${YELLOW}Warning: portaudio may be required for microphone support${NC}"
            echo "Install with: brew install portaudio"
        fi
    fi
}

# Check UV package manager
check_uv() {
    if ! command -v uv &> /dev/null; then
        echo ""
        echo "UV package manager not found. Installing..."
        curl -LsSf https://astral.sh/uv/install.sh | sh
        export PATH="$HOME/.cargo/bin:$PATH"
        
        if ! command -v uv &> /dev/null; then
            echo -e "${RED}Error: Failed to install UV${NC}"
            exit 1
        fi
        echo -e "${GREEN}✓ UV installed${NC}"
    else
        echo -e "${GREEN}✓ UV package manager${NC}"
    fi
}

# Download and install
install_app() {
    echo ""
    echo "Installing voice-todo-cli..."
    
    # Create install directory
    mkdir -p "$INSTALL_DIR"
    cd "$INSTALL_DIR"
    
    # Download latest release or clone repo
    if command -v git &> /dev/null; then
        echo "Cloning repository..."
        if [ -d "voice-todo-cli" ]; then
            cd voice-todo-cli
            git pull
        else
            git clone "$REPO_URL" voice-todo-cli
            cd voice-todo-cli
        fi
    else
        echo "Downloading latest release..."
        curl -L "${REPO_URL}/archive/refs/heads/main.zip" -o voice-todo-cli.zip
        unzip -o voice-todo-cli.zip
        cd voice-todo-cli-main
    fi
    
    # Install using UV
    echo "Installing dependencies..."
    uv pip install -e .
    
    # Create bin directory if it doesn't exist
    mkdir -p "$BIN_DIR"
    
    # Create executable script
    cat > "$BIN_DIR/$APP_NAME" << 'EOF'
#!/usr/bin/env bash
# Voice-Enabled Todo CLI launcher

INSTALL_DIR="${HOME}/.local/share/voice-todo-cli/voice-todo-cli"
cd "$INSTALL_DIR"
exec uv run python -m voice_todo_cli.main "$@"
EOF
    
    chmod +x "$BIN_DIR/$APP_NAME"
    
    echo -e "${GREEN}✓ Installation complete${NC}"
}

# Setup shell configuration
setup_path() {
    echo ""
    echo "Configuring PATH..."
    
    # Detect shell
    SHELL_NAME=$(basename "$SHELL")
    
    case "$SHELL_NAME" in
        bash)
            RC_FILE="$HOME/.bashrc"
            ;;
        zsh)
            RC_FILE="$HOME/.zshrc"
            ;;
        fish)
            RC_FILE="$HOME/.config/fish/config.fish"
            ;;
        *)
            RC_FILE="$HOME/.profile"
            ;;
    esac
    
    # Check if PATH already includes bin directory
    if [[ ":$PATH:" != *":$BIN_DIR:"* ]]; then
        echo ""
        echo "Adding $BIN_DIR to PATH in $RC_FILE"
        echo "export PATH=\"\$PATH:$BIN_DIR\"" >> "$RC_FILE"
        export PATH="$PATH:$BIN_DIR"
        echo -e "${GREEN}✓ PATH updated${NC}"
        echo -e "${YELLOW}Please restart your terminal or run: source $RC_FILE${NC}"
    else
        echo -e "${GREEN}✓ PATH already configured${NC}"
    fi
}

# Initialize app data directory
init_data_dir() {
    echo ""
    echo "Initializing data directory..."
    
    DATA_DIR="$HOME/.todo-app"
    mkdir -p "$DATA_DIR"
    
    # Create initial tasks.json if it doesn't exist
    if [ ! -f "$DATA_DIR/tasks.json" ]; then
        echo '{"tasks": []}' > "$DATA_DIR/tasks.json"
        echo -e "${GREEN}✓ Data directory created at $DATA_DIR${NC}"
    else
        echo -e "${GREEN}✓ Data directory exists at $DATA_DIR${NC}"
    fi
}

# Post-installation instructions
show_completion() {
    echo ""
    echo "======================================"
    echo -e "${GREEN}Installation Complete!${NC}"
    echo "======================================"
    echo ""
    echo "Usage:"
    echo "  $APP_NAME              # Start the app"
    echo "  $APP_NAME --help       # Show help"
    echo ""
    echo "Voice Commands:"
    echo "  'add [task]'           # Add a new task"
    echo "  'list' or 'show'       # List all tasks"
    echo "  'mark complete id [#]' # Mark task as complete"
    echo "  'delete id [#]'        # Delete a task"
    echo ""
    echo "Data location: $HOME/.todo-app/tasks.json"
    echo ""
    echo "To uninstall, run:"
    echo "  curl -sSL ${REPO_URL}/raw/main/uninstall.sh | bash"
    echo ""
}

# Main installation flow
main() {
    check_prerequisites
    check_uv
    install_app
    setup_path
    init_data_dir
    show_completion
}

# Run installation
main
```

## uninstall.sh

```bash
#!/usr/bin/env bash

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

INSTALL_DIR="${HOME}/.local/share/voice-todo-cli"
BIN_DIR="${HOME}/.local/bin"
DATA_DIR="${HOME}/.todo-app"
APP_NAME="todo-voice"

echo -e "${YELLOW}Voice-Enabled Todo CLI - Uninstaller${NC}"
echo "========================================"
echo ""

# Ask for confirmation
read -p "Are you sure you want to uninstall? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Uninstallation cancelled."
    exit 0
fi

# Ask about data
echo ""
read -p "Do you want to delete your task data as well? (y/N): " -n 1 -r
echo
DELETE_DATA=false
if [[ $REPLY =~ ^[Yy]$ ]]; then
    DELETE_DATA=true
fi

# Remove installation directory
if [ -d "$INSTALL_DIR" ]; then
    echo "Removing installation files..."
    rm -rf "$INSTALL_DIR"
    echo -e "${GREEN}✓ Installation files removed${NC}"
fi

# Remove executable
if [ -f "$BIN_DIR/$APP_NAME" ]; then
    echo "Removing executable..."
    rm -f "$BIN_DIR/$APP_NAME"
    echo -e "${GREEN}✓ Executable removed${NC}"
fi

# Remove data if requested
if [ "$DELETE_DATA" = true ] && [ -d "$DATA_DIR" ]; then
    echo "Removing task data..."
    rm -rf "$DATA_DIR"
    echo -e "${GREEN}✓ Task data removed${NC}"
else
    if [ -d "$DATA_DIR" ]; then
        echo -e "${YELLOW}Task data preserved at: $DATA_DIR${NC}"
    fi
fi

echo ""
echo -e "${GREEN}Uninstallation complete!${NC}"
echo ""
if [ "$DELETE_DATA" = false ] && [ -d "$DATA_DIR" ]; then
    echo "Your tasks are still available at: $DATA_DIR"
    echo "You can reinstall later and your tasks will be restored."
fi
```

## Usage Instructions

### Installation

Users install the app with a single command:

```bash
curl -sSL https://raw.githubusercontent.com/yourusername/voice-todo-cli/main/install.sh | bash
```

### What the Installer Does

1. **Checks prerequisites**: Python 3.12+, pip, system audio libraries
2. **Installs UV**: If not already installed
3. **Downloads app**: Clones repo or downloads latest release
4. **Installs dependencies**: Uses UV to install Python packages
5. **Creates executable**: Places `todo-voice` in `~/.local/bin`
6. **Configures PATH**: Updates shell configuration
7. **Initializes data**: Creates `~/.todo-app/tasks.json`

### Directory Structure After Installation

```
~/.local/
├── bin/
│   └── todo-voice              # Executable launcher
└── share/
    └── voice-todo-cli/         # Application files
        └── voice-todo-cli/
            ├── src/
            ├── pyproject.toml
            └── ...

~/.todo-app/
└── tasks.json                  # User's task data
```

### Platform-Specific Notes

#### Linux (Ubuntu/Debian)
```bash
# Install audio dependencies first
sudo apt-get update
sudo apt-get install portaudio19-dev python3-pyaudio

# Then run installer
curl -sSL https://... | bash
```

#### macOS
```bash
# Install audio dependencies first
brew install portaudio

# Then run installer
curl -sSL https://... | bash
```

#### Windows (WSL)
```bash
# Use Windows Subsystem for Linux
# Install audio dependencies
sudo apt-get install portaudio19-dev

# Then run installer
curl -sSL https://... | bash
```

### Uninstallation

```bash
curl -sSL https://raw.githubusercontent.com/yourusername/voice-todo-cli/main/uninstall.sh | bash
```

## Publishing to GitHub

### Release Checklist

1. **Create GitHub repository**: `voice-todo-cli`
2. **Add install scripts**: Commit `install.sh` and `uninstall.sh` to root
3. **Test installation**: Test on clean machine
4. **Create release tag**: `git tag v0.1.0 && git push --tags`
5. **Update documentation**: Add installation instructions to README.md

### README Installation Section

```markdown
## Installation

Install with a single command:

```bash
curl -sSL https://raw.githubusercontent.com/yourusername/voice-todo-cli/main/install.sh | bash
```

### Prerequisites

- Python 3.12 or higher
- pip package manager
- Microphone (for voice input)
- Audio libraries (installed automatically on most systems)

### Manual Installation

If you prefer to install manually:

```bash
git clone https://github.com/yourusername/voice-todo-cli
cd voice-todo-cli
uv pip install -e .
```

## Troubleshooting Installation

### Audio Library Issues

**Linux**: Install portaudio
```bash
sudo apt-get install portaudio19-dev python3-pyaudio
```

**macOS**: Install portaudio via Homebrew
```bash
brew install portaudio
```

### PATH Not Updated

If `todo-voice` command is not found after installation:

```bash
# Add to PATH manually
export PATH="$PATH:$HOME/.local/bin"

# Make permanent (bash)
echo 'export PATH="$PATH:$HOME/.local/bin"' >> ~/.bashrc
source ~/.bashrc

# Make permanent (zsh)
echo 'export PATH="$PATH:$HOME/.local/bin"' >> ~/.zshrc
source ~/.zshrc
```

### Permission Issues

If you get permission denied errors:

```bash
chmod +x ~/.local/bin/todo-voice
```