#!/usr/bin/env bash
# ==============================================================================
# MC Server-Deck: Instalador Oficial para Steam Deck (SteamOS / Arch Linux)
# Versión: 2.0 (Rust + Tauri Native Engine)
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
echo -e "${BLUE}      MC Server-Deck: Instalador para Steam Deck     ${NC}"
echo -e "${BLUE}         Motor Nativo en Rust con Podman Rootless     ${NC}"
echo -e "${BLUE}====================================================${NC}"
echo ""

INSTALL_DIR="$HOME/.local/share/mc-server-deck"
mkdir -p "$INSTALL_DIR/assets"
mkdir -p "$HOME/minecraft-server/data"
mkdir -p "$HOME/minecraft-server/ssh-config"
mkdir -p "$HOME/Desktop"
mkdir -p "$HOME/.local/share/applications"

# 1. Comprobar Podman nativo de SteamOS
echo -e "${YELLOW}[1/4] Verificando Podman en SteamOS...${NC}"
if ! command -v podman &> /dev/null; then
    echo -e "${RED}Error: Podman no está instalado o no se encuentra en PATH.${NC}"
    echo "SteamOS incluye podman de forma predeterminada. Verifica tu instalación."
    exit 1
fi
PODMAN_VER=$(podman --version)
echo -e "${GREEN}✔ Podman detectado:${NC} $PODMAN_VER"

# 2. Verificar Binario de la Aplicación
echo -e "${YELLOW}[2/4] Verificando binario ejecutable...${NC}"

INSTALLED=false

# Caso A: Binario pre-compilado en el repositorio (Recomendado para Steam Deck)
if [ -f "bin/mc-server-deck" ]; then
    echo -e "${GREEN}✔ Binario Linux pre-compilado detectado en 'bin/mc-server-deck'.${NC}"
    echo -e "${CYAN}Instalando binario optimizado sin requerir compiladores en la consola...${NC}"
    cp "bin/mc-server-deck" "$INSTALL_DIR/mc-server-deck"
    INSTALLED=true
elif [ -f "src-tauri/target/release/mc-server-deck" ]; then
    echo -e "${GREEN}✔ Binario compilado previamente encontrado en target/release.${NC}"
    cp "src-tauri/target/release/mc-server-deck" "$INSTALL_DIR/mc-server-deck"
    INSTALLED=true
fi

# Caso B: Si no existe el binario pre-compilado, compilar desde código fuente
if [ "$INSTALLED" = false ]; then
    echo -e "${YELLOW}Binario no encontrado. Procediendo a compilar desde código fuente...${NC}"

    # Comprobar Frontend
    if [ ! -f "dist/index.html" ]; then
        if ! command -v npm &> /dev/null; then
            echo -e "${YELLOW}Descargando Node.js portátil en espacio de usuario para compilar frontend...${NC}"
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

    # Comprobar compilador C ('cc') necesario para Cargo
    if ! command -v cc &> /dev/null && ! command -v gcc &> /dev/null; then
        echo -e "${YELLOW}SteamOS no incluye el compilador C ('cc') por defecto (sistema de archivos inmutable).${NC}"
        echo -e "¿Deseas instalar 'base-devel' y 'webkit2gtk-4.1' mediante pacman (requiere sudo)? (s/N)"
        read -r resp
        if [[ "$resp" =~ ^([sS])$ ]]; then
            sudo steamos-readonly disable
            sudo pacman-key --init
            sudo pacman-key --populate archlinux holo
            sudo pacman -Sy --noconfirm base-devel webkit2gtk-4.1
            sudo steamos-readonly enable
        else
            echo -e "${RED}Compilación cancelada. Utiliza el binario pre-compilado en 'bin/mc-server-deck'.${NC}"
            exit 1
        fi
    fi

    # Comprobar Rust / Cargo
    if ! command -v cargo &> /dev/null; then
        echo -e "${YELLOW}Instalando Rust y Cargo en espacio de usuario...${NC}"
        curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
        source "$HOME/.cargo/env" || export PATH="$HOME/.cargo/bin:$PATH"
    fi

    echo -e "${YELLOW}Compilando con Cargo en Release...${NC}"
    cd src-tauri
    cargo build --release
    cd ..
    cp "src-tauri/target/release/mc-server-deck" "$INSTALL_DIR/mc-server-deck"
fi

# 3. Permisos y recursos
echo -e "${YELLOW}[3/4] Configurando archivos y permisos...${NC}"
chmod +x "$INSTALL_DIR/mc-server-deck"
cp assets/icon.png "$INSTALL_DIR/assets/icon.png"

# 4. Crear accesos directos
echo -e "${YELLOW}[4/4] Creando accesos directos de SteamOS...${NC}"
DESKTOP_ENTRY="[Desktop Entry]
Name=MC Server-Deck
Comment=Servidor de Minecraft nativo en Podman para Steam Deck
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
echo -e "${GREEN}   ✔ ¡Instalación de MC Server-Deck Finalizada!    ${NC}"
echo -e "${GREEN}====================================================${NC}"
echo ""
echo -e "Puedes abrir la aplicación desde el acceso directo en tu ${YELLOW}Escritorio${NC}."
echo ""
echo -e "${BLUE}Para añadirla al Modo Juego (Gaming Mode):${NC}"
echo "1. Abre Steam en Modo Escritorio."
echo "2. Haz clic en 'Juegos' -> 'Añadir un producto que no es de Steam a mi biblioteca...'."
echo "3. Selecciona 'MC Server-Deck' de la lista (o busca $INSTALL_DIR/mc-server-deck)."
echo "4. ¡Listo! Vuelve al Modo Juego y disfrútalo a 1280x800 con controles táctiles."
echo ""
