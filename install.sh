#!/usr/bin/env bash
# ==============================================================================
# MC Server-Deck: Official Installer for Steam Deck (SteamOS / Arch Linux)
# Version: 2.0 (Rust + Tauri Native Engine)
# ==============================================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${BLUE}====================================================${NC}"
echo -e "${BLUE}     MC Server-Deck: Steam Deck Installer           ${NC}"
echo -e "${BLUE}       Rust Native Engine with Rootless Podman      ${NC}"
echo -e "${BLUE}====================================================${NC}"
echo ""

INSTALL_DIR="$HOME/.local/share/mc-server-deck"
mkdir -p "$INSTALL_DIR/assets"
mkdir -p "$HOME/minecraft-server/data"
mkdir -p "$HOME/minecraft-server/ssh-config"
mkdir -p "$HOME/Desktop"
mkdir -p "$HOME/.local/share/applications"

# 1. Check native SteamOS Podman
echo -e "${YELLOW}[1/5] Verifying Podman on SteamOS...${NC}"
if ! command -v podman &> /dev/null; then
    echo -e "${RED}Error: Podman is not installed or not found in PATH.${NC}"
    echo "SteamOS includes podman by default. Please verify your installation."
    exit 1
fi
PODMAN_VER=$(podman --version)
echo -e "${GREEN}✔ Podman detected:${NC} $PODMAN_VER"

# 2. Check system dependencies (WebKitGTK 4.1 for Tauri)
echo -e "${YELLOW}[2/5] Verifying WebKitGTK graphics library...${NC}"
if ! ldconfig -p 2>/dev/null | grep -q "libwebkit2gtk-4.1.so.0" && [ ! -f "/usr/lib/libwebkit2gtk-4.1.so.0" ]; then
    echo -e "${YELLOW}SteamOS does not include the 'webkit2gtk-4.1' library in its base image.${NC}"
    echo -e "It is required to render the application's graphical user interface."
    read -p "Do you want to install 'webkit2gtk-4.1' now with pacman (requires sudo)? (Y/n): " ans
    if [[ "$ans" =~ ^([yYsS]|)$ ]]; then
        echo -e "${CYAN}Unlocking filesystem and installing webkit2gtk-4.1...${NC}"
        sudo steamos-readonly disable
        sudo pacman-key --init
        sudo pacman-key --populate archlinux holo
        sudo pacman -Sy --noconfirm webkit2gtk-4.1
        sudo steamos-readonly enable
        echo -e "${GREEN}✔ webkit2gtk-4.1 installed successfully.${NC}"
    else
        echo -e "${RED}Warning: The application will not be able to display its window without webkit2gtk-4.1.${NC}"
    fi
else
    echo -e "${GREEN}✔ webkit2gtk-4.1 detected on system.${NC}"
fi

# 3. Check Application Binary
echo -e "${YELLOW}[3/5] Verifying executable binary...${NC}"

INSTALLED=false

# Case A: Pre-compiled binary in the repository (Recommended for Steam Deck)
if [ -f "bin/mc-server-deck" ]; then
    echo -e "${GREEN}✔ Pre-compiled Linux binary detected in 'bin/mc-server-deck'.${NC}"
    echo -e "${CYAN}Installing optimized binary without requiring compilers on the console...${NC}"
    cp "bin/mc-server-deck" "$INSTALL_DIR/mc-server-deck"
    INSTALLED=true
elif [ -f "src-tauri/target/release/mc-server-deck" ]; then
    echo -e "${GREEN}✔ Previously compiled binary found in target/release.${NC}"
    cp "src-tauri/target/release/mc-server-deck" "$INSTALL_DIR/mc-server-deck"
    INSTALLED=true
fi

# Case B: If pre-compiled binary is not present, compile from source code
if [ "$INSTALLED" = false ]; then
    echo -e "${YELLOW}Binary not found. Proceeding to compile from source code...${NC}"

    # Check Frontend
    if [ ! -f "dist/index.html" ]; then
        if ! command -v npm &> /dev/null; then
            echo -e "${YELLOW}Downloading portable user-space Node.js to build frontend...${NC}"
            NODE_DIR="$HOME/.local/share/mc-server-deck/tools"
            mkdir -p "$NODE_DIR"
            NODE_VER="v20.18.0"
            NODE_TAR="node-${NODE_VER}-linux-x64.tar.xz"
            curl -fsSL "https://nodejs.org/dist/${NODE_VER}/${NODE_TAR}" -o "/tmp/${NODE_TAR}"
            tar -xf "/tmp/${NODE_TAR}" -C "$NODE_DIR"
            rm -f "/tmp/${NODE_TAR}"
            export PATH="$NODE_DIR/node-${NODE_VER}-linux-x64/bin:$PATH"
        fi
        npm install
        npm run build
    fi

    # Check C compiler ('cc') required by Cargo
    if ! command -v cc &> /dev/null && ! command -v gcc &> /dev/null; then
        echo -e "${YELLOW}SteamOS does not include the C compiler ('cc') by default (immutable filesystem).${NC}"
        echo -e "Do you want to install 'base-devel' and 'webkit2gtk-4.1' via pacman (requires sudo)? (y/N)"
        read -r resp
        if [[ "$resp" =~ ^([yYsS])$ ]]; then
            sudo steamos-readonly disable
            sudo pacman-key --init
            sudo pacman-key --populate archlinux holo
            sudo pacman -Sy --noconfirm base-devel webkit2gtk-4.1
            sudo steamos-readonly enable
        else
            echo -e "${RED}Compilation cancelled. Please use the pre-compiled binary in 'bin/mc-server-deck'.${NC}"
            exit 1
        fi
    fi

    # Check Rust / Cargo
    if ! command -v cargo &> /dev/null; then
        echo -e "${YELLOW}Installing Rust and Cargo in user space...${NC}"
        curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
        source "$HOME/.cargo/env" || export PATH="$HOME/.cargo/bin:$PATH"
    fi

    echo -e "${YELLOW}Compiling with Cargo in Release mode...${NC}"
    cd src-tauri
    cargo build --release
    cd ..
    cp "src-tauri/target/release/mc-server-deck" "$INSTALL_DIR/mc-server-deck"
fi

# 4. Permissions and assets
echo -e "${YELLOW}[4/5] Setting up files and permissions...${NC}"
chmod +x "$INSTALL_DIR/mc-server-deck"
cp assets/icon.png "$INSTALL_DIR/assets/icon.png"

# 5. Create SteamOS shortcuts
echo -e "${YELLOW}[5/5] Creating SteamOS shortcuts...${NC}"
DESKTOP_ENTRY="[Desktop Entry]
Name=MC Server-Deck
Comment=Native Podman Minecraft Server for Steam Deck
Exec=$INSTALL_DIR/mc-server-deck
Icon=$INSTALL_DIR/assets/icon.png
Terminal=false
Type=Application
Categories=Game;Utility;
StartupNotify=true"

echo "$DESKTOP_ENTRY" > "$HOME/Desktop/MC-Server-Deck.desktop"
echo "$DESKTOP_ENTRY" > "$HOME/.local/share/applications/MC-Server-Deck.desktop"
chmod +x "$HOME/Desktop/MC-Server-Deck.desktop"
chmod +x "$HOME/.local/share/applications/MC-Server-Deck.desktop"

echo ""
echo -e "${GREEN}====================================================${NC}"
echo -e "${GREEN}    ✔ MC Server-Deck Installation Complete!        ${NC}"
echo -e "${GREEN}====================================================${NC}"
echo ""
echo -e "You can launch the application from the shortcut on your ${YELLOW}Desktop${NC}."
echo ""
echo -e "${BLUE}To add it to Gaming Mode:${NC}"
echo "1. Open Steam in Desktop Mode."
echo "2. Click 'Games' -> 'Add a Non-Steam Game to My Library...'."
echo "3. Select 'MC Server-Deck' from the list (or browse to $INSTALL_DIR/mc-server-deck)."
echo "4. Done! Return to Gaming Mode and enjoy at 1280x800 with touch controls."
echo ""
