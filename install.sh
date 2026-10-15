#!/usr/bin/env bash
# ==============================================================================
# MC Server-Deck - Script de Instalación para Steam Deck (SteamOS)
# Diseñado para ejecutarse en Konsole sin sudo ni alterar el sistema inmutable.
# ==============================================================================

set -e

# Colores para salida en terminal
COLOR_RESET="\033[0m"
COLOR_CYAN="\033[1;36m"
COLOR_GREEN="\033[1;32m"
COLOR_YELLOW="\033[1;33m"
COLOR_RED="\033[1;31m"
COLOR_BLUE="\033[1;34m"

echo -e "${COLOR_CYAN}"
echo "  __  __  ____   ____                                ____            _    "
echo " |  \/  |/ ___| / ___|  ___ _ ____   _____ _ __     |  _ \  ___  ___| | __"
echo " | |\/| | |     \___ \ / _ \ '__\ \ / / _ \ '__|____| | | |/ _ \/ __| |/ /"
echo " | |  | | |___   ___) |  __/ |   \ V /  __/ | |_____| |_| |  __/ (__|   < "
echo " |_|  |_|\____| |____/ \___|_|    \_/ \___|_|       |____/ \___|\___|_|\_\\"
echo "            Minecraft Server Manager para Steam Deck                      "
echo -e "${COLOR_RESET}"

# 1. Comprobar que no se ejecuta como root (Podman rootless requiere el usuario deck)
if [ "$EUID" -eq 0 ]; then
    echo -e "${COLOR_RED}[!] ERROR: No ejecutes este instalador con 'sudo' ni como root.${COLOR_RESET}"
    echo "MC Server-Deck y Podman rootless están diseñados para ejecutarse en el espacio de usuario 'deck'."
    exit 1
fi

SOURCE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
TARGET_DIR="$HOME/.local/share/mc-server-deck"
VENV_DIR="$TARGET_DIR/venv"
DESKTOP_DIR="$HOME/Desktop"
APPS_DIR="$HOME/.local/share/applications"
SERVER_DATA_DIR="$HOME/minecraft-server"

echo -e "${COLOR_BLUE}[1/6] Verificando dependencias del sistema en SteamOS...${COLOR_RESET}"

# Comprobar Python 3
if ! command -v python3 >/dev/null 2>&1; then
    echo -e "${COLOR_RED}[!] Error: Python 3 no está instalado en el sistema.${COLOR_RESET}"
    exit 1
fi
echo -e "  ✔ Python 3 encontrado: $(python3 --version)"

# Comprobar Podman
if ! command -v podman >/dev/null 2>&1; then
    echo -e "${COLOR_YELLOW}[!] ADVERTENCIA: 'podman' no fue encontrado en el PATH.${COLOR_RESET}"
    echo -e "    En SteamOS 3.5+ Podman suele venir preinstalado."
    echo -e "    Asegúrate de tener Podman habilitado para ejecutar los servidores."
else
    echo -e "  ✔ Podman encontrado: $(podman --version)"
fi

echo -e "\n${COLOR_BLUE}[2/6] Preparando directorios del servidor y aplicación...${COLOR_RESET}"
mkdir -p "$TARGET_DIR"
mkdir -p "$DESKTOP_DIR"
mkdir -p "$APPS_DIR"
mkdir -p "$SERVER_DATA_DIR/data"
mkdir -p "$SERVER_DATA_DIR/ssh-config"
echo -e "  ✔ Directorios creados en: $SERVER_DATA_DIR"

echo -e "\n${COLOR_BLUE}[3/6] Copiando archivos de MC Server-Deck...${COLOR_RESET}"
cp -rf "$SOURCE_DIR/main.py" "$TARGET_DIR/"
cp -rf "$SOURCE_DIR/podman_manager.py" "$TARGET_DIR/"
cp -rf "$SOURCE_DIR/steam_integrator.py" "$TARGET_DIR/"
cp -rf "$SOURCE_DIR/i18n.py" "$TARGET_DIR/"
cp -rf "$SOURCE_DIR/run.sh" "$TARGET_DIR/"
cp -rf "$SOURCE_DIR/requirements.txt" "$TARGET_DIR/"
cp -rf "$SOURCE_DIR/ui" "$TARGET_DIR/"
cp -rf "$SOURCE_DIR/assets" "$TARGET_DIR/"

chmod +x "$TARGET_DIR/main.py"
chmod +x "$TARGET_DIR/run.sh"
echo -e "  ✔ Archivos copiados a: $TARGET_DIR"

echo -e "\n${COLOR_BLUE}[4/6] Configurando entorno virtual de Python (venv)...${COLOR_RESET}"
if [ ! -d "$VENV_DIR" ]; then
    echo "  Creando nuevo venv en $VENV_DIR..."
    python3 -m venv "$VENV_DIR"
else
    echo "  Entorno virtual existente encontrado."
fi

echo "  Instalando dependencias (PyQt6)..."
"$VENV_DIR/bin/pip" install --upgrade pip >/dev/null 2>&1 || true
"$VENV_DIR/bin/pip" install -r "$TARGET_DIR/requirements.txt"
echo -e "  ✔ Dependencias instaladas correctamente."

echo -e "\n${COLOR_BLUE}[5/6] Creando accesos directos y registrando en Steam...${COLOR_RESET}"

ICON_PATH="$TARGET_DIR/assets/icon.png"
EXEC_PATH="$TARGET_DIR/run.sh"

DESKTOP_ENTRY="[Desktop Entry]
Name=MC Server-Deck
Comment=Administrador de Servidores de Minecraft para Steam Deck
Exec=$EXEC_PATH
Icon=$ICON_PATH
Terminal=false
Type=Application
Categories=Game;Utility;
StartupWMClass=MC-Server-Deck
"

# 1. En aplicaciones de usuario
echo "$DESKTOP_ENTRY" > "$APPS_DIR/MC-Server-Deck.desktop"
chmod +x "$APPS_DIR/MC-Server-Deck.desktop"

# 2. En el Escritorio de KDE Plasma
echo "$DESKTOP_ENTRY" > "$DESKTOP_DIR/MC-Server-Deck.desktop"
chmod +x "$DESKTOP_DIR/MC-Server-Deck.desktop"

# Marcar como archivo confiable en KDE Plasma / SteamOS Desktop
if command -v gio >/dev/null 2>&1; then
    gio set "$DESKTOP_DIR/MC-Server-Deck.desktop" metadata::trusted true 2>/dev/null || true
fi

# Actualizar base de datos de aplicaciones
if command -v update-desktop-database >/dev/null 2>&1; then
    update-desktop-database "$APPS_DIR" 2>/dev/null || true
fi

# 3. Integración automática en la biblioteca de Steam (Gaming Mode)
echo "  Registrando acceso directo y carátulas en Steam (Gaming Mode)..."
"$VENV_DIR/bin/python" -c "
import sys
sys.path.insert(0, '$TARGET_DIR')
from steam_integrator import SteamIntegrator
si = SteamIntegrator()
ok, msg = si.add_to_steam_library()
print('    ' + msg.splitlines()[0])
" 2>/dev/null || echo "    (Se podrá añadir manualmente desde Steam en Modo Escritorio)"

echo -e "  ✔ Acceso directo creado en el Escritorio: ~/Desktop/MC-Server-Deck.desktop"
echo -e "  ✔ Acceso directo en el menú de aplicaciones: ~/.local/share/applications/MC-Server-Deck.desktop"

echo -e "\n${COLOR_BLUE}[6/6] Finalización y verificación...${COLOR_RESET}"
echo -e "${COLOR_GREEN}========================================================================${COLOR_RESET}"
echo -e "${COLOR_GREEN}  ¡Instalación de MC Server-Deck completada con éxito!                 ${COLOR_RESET}"
echo -e "${COLOR_GREEN}========================================================================${COLOR_RESET}"
echo -e "
${COLOR_CYAN}¿Cómo agregar MC Server-Deck a Steam (Gaming Mode)?${COLOR_RESET}
 1. Abre la aplicación de Steam en el Modo Escritorio.
 2. Haz clic en el menú superior: ${COLOR_YELLOW}Juegos -> Añadir un producto que no es de Steam a mi biblioteca...${COLOR_RESET}
 3. En la lista, busca y marca ${COLOR_GREEN}MC Server-Deck${COLOR_RESET}.
    (Si no aparece, haz clic en 'Buscar' y selecciona: ${COLOR_CYAN}$EXEC_PATH${COLOR_RESET})
 4. Haz clic en 'Añadir seleccionados'.
 5. ¡Listo! Vuelve al Modo Juego (Gaming Mode) y podrás iniciarlo directamente con controles y pantalla táctil (1280x800).

Para iniciar la aplicación ahora mismo desde la terminal:
  ${COLOR_CYAN}$EXEC_PATH${COLOR_RESET}
"
