#!/usr/bin/env bash
# MC Server-Deck - Launcher Script para SteamOS / Linux
set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
LOCAL_VENV="$DIR/venv"
SHARED_VENV="$HOME/.local/share/mc-server-deck/venv"
FALLBACK_VENV="$HOME/.local/share/deckcraft-manager/venv"

if [ -f "$LOCAL_VENV/bin/python" ]; then
    PYTHON_EXEC="$LOCAL_VENV/bin/python"
elif [ -f "$SHARED_VENV/bin/python" ]; then
    PYTHON_EXEC="$SHARED_VENV/bin/python"
elif [ -f "$FALLBACK_VENV/bin/python" ]; then
    PYTHON_EXEC="$FALLBACK_VENV/bin/python"
elif command -v python3 >/dev/null 2>&1; then
    PYTHON_EXEC="python3"
else
    echo "Error: No se encontró Python 3 instalado en el sistema."
    exit 1
fi

# Entorno para compatibilidad con Steam Deck Gamescope / Gaming Mode
export STEAM_DECK="${STEAM_DECK:-1}"
if [ -z "$QT_QPA_PLATFORM" ]; then
    # Wayland preferido con fallback a xcb en Gamescope
    export QT_QPA_PLATFORM="wayland;xcb"
fi

# Prevenir suspensión de SteamOS mientras el servidor esté abierto (Anti-Sleep)
if command -v systemd-inhibit >/dev/null 2>&1; then
    exec systemd-inhibit \
        --what=sleep:idle \
        --who="MC Server-Deck" \
        --why="Mantener activo el servidor de Minecraft y proteger la pantalla OLED" \
        "$PYTHON_EXEC" "$DIR/main.py" "$@"
else
    exec "$PYTHON_EXEC" "$DIR/main.py" "$@"
fi
