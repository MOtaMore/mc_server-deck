#!/usr/bin/env bash
# ==============================================================================
# MC Server-Deck: Instalador Oficial para Steam Deck (SteamOS / Arch Linux)
# Versión: 2.0 (Rust + Tauri Native Engine)
# ==============================================================================

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}====================================================${NC}"
echo -e "${BLUE}      MC Server-Deck: Instalador para Steam Deck     ${NC}"
echo -e "${BLUE}         Motor Nativo en Rust con Podman Rootless     ${NC}"
echo -e "${BLUE}====================================================${NC}"
echo ""

# 1. Comprobar Podman nativo de SteamOS
echo -e "${YELLOW}[1/5] Verificando Podman en SteamOS...${NC}"
if ! command -v podman &> /dev/null; then
    echo -e "${RED}Error: Podman no está instalado o no se encuentra en PATH.${NC}"
    echo "SteamOS incluye podman de forma predeterminada. Verifica tu instalación."
    exit 1
fi
PODMAN_VER=$(podman --version)
echo -e "${GREEN}✔ Podman detectado:${NC} $PODMAN_VER"

# 2. Comprobar Node.js / npm
echo -e "${YELLOW}[2/5] Verificando entorno de compilación frontend...${NC}"
if ! command -v npm &> /dev/null; then
    echo -e "${YELLOW}npm no encontrado. Instalando dependencias básicas...${NC}"
fi

# 3. Comprobar Rust / Cargo
echo -e "${YELLOW}[3/5] Verificando Rust y Cargo...${NC}"
if ! command -v cargo &> /dev/null; then
    echo -e "${YELLOW}Rust no está instalado. ¿Deseas instalar rustup automáticamente? (S/n)${NC}"
    read -r resp
    if [[ "$resp" =~ ^([nN][oO]|[nN])$ ]]; then
        echo -e "${RED}Se requiere Rust para compilar el proyecto.${NC}"
        exit 1
    else
        curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
        source "$HOME/.cargo/env"
    fi
fi
RUST_VER=$(rustc --version)
echo -e "${GREEN}✔ Rust detectado:${NC} $RUST_VER"

# 4. Compilar proyecto
echo -e "${YELLOW}[4/5] Compilando MC Server-Deck en Release...${NC}"
npm install
npm run build
cd src-tauri
cargo build --release
cd ..

# 5. Instalar en ~/.local/share/mc-server-deck
echo -e "${YELLOW}[5/5] Instalando archivos y accesos directos...${NC}"
INSTALL_DIR="$HOME/.local/share/mc-server-deck"
mkdir -p "$INSTALL_DIR/assets"
mkdir -p "$HOME/minecraft-server/data"
mkdir -p "$HOME/minecraft-server/ssh-config"
mkdir -p "$HOME/Desktop"
mkdir -p "$HOME/.local/share/applications"

cp src-tauri/target/release/app "$INSTALL_DIR/mc-server-deck" || cp src-tauri/target/release/mc-server-deck "$INSTALL_DIR/mc-server-deck"
chmod +x "$INSTALL_DIR/mc-server-deck"
cp assets/icon.png "$INSTALL_DIR/assets/icon.png"

# Crear lanzador .desktop
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
