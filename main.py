#!/usr/bin/env python3
"""
MC Server-Deck - Steam Deck (SteamOS / Arch Linux)
Punto de entrada principal de la aplicación GUI.
"""

import os
import sys
from pathlib import Path

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication

from podman_manager import PodmanManager
from ui.main_window import MainWindow
from ui.styles import STEAM_DECK_QSS


def main():
    # Habilitar escalado High-DPI
    if hasattr(Qt.ApplicationAttribute, "AA_EnableHighDpiScaling"):
        QApplication.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling, True)
    if hasattr(Qt.ApplicationAttribute, "AA_UseHighDpiPixmaps"):
        QApplication.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps, True)

    app = QApplication(sys.argv)
    app.setApplicationName("MC-Server-Deck")
    app.setDesktopFileName("MC-Server-Deck.desktop")

    # Aplicar hoja de estilos SteamOS
    app.setStyleSheet(STEAM_DECK_QSS)

    # Configurar icono de la aplicación
    base_dir = Path(__file__).resolve().parent
    icon_png = base_dir / "assets" / "icon.png"
    icon_svg = base_dir / "assets" / "icon.svg"

    if icon_png.exists():
        app.setWindowIcon(QIcon(str(icon_png)))
    elif icon_svg.exists():
        app.setWindowIcon(QIcon(str(icon_svg)))

    # Configurar gestor de inactividad para protector de pantalla OLED (5 min por defecto)
    from ui.screensaver import InactivityManager
    inactivity_mgr = InactivityManager(timeout_minutes=5)
    app.installEventFilter(inactivity_mgr)

    # Inicializar manager de Podman y ventana principal
    podman_mgr = PodmanManager()
    window = MainWindow(podman_mgr, inactivity_mgr=inactivity_mgr)
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
