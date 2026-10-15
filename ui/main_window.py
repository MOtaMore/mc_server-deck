"""
MC Server-Deck - Ventana Principal (SteamOS 1280x800)
"""

from typing import Optional

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QStatusBar,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from podman_manager import PodmanManager
from steam_integrator import SteamIntegrator
from ui.dashboard_tab import DashboardTab
from ui.guide_tab import GuideTab
from ui.screensaver import InactivityManager, OledScreensaverWidget
from ui.setup_wizard_tab import SetupWizardTab


class MainWindow(QMainWindow):
    """Ventana principal optimizada para la resolución 1280x800 de Steam Deck."""

    def __init__(
        self,
        podman_mgr: PodmanManager,
        inactivity_mgr: Optional[InactivityManager] = None,
    ):
        super().__init__()
        self.pm = podman_mgr
        self.inactivity_mgr = inactivity_mgr
        self.screensaver: Optional[OledScreensaverWidget] = None

        self.setWindowTitle("MC Server-Deck - Steam Deck")
        self.resize(1280, 800)
        self.setMinimumSize(1024, 600)

        # Si se detecta Gamescope (Gaming Mode), ajustar a tamaño completo
        if SteamIntegrator.is_gaming_mode():
            self.showMaximized()

        self._build_ui()
        self._setup_screensaver()

    def _build_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        root_layout = QVBoxLayout(central_widget)
        root_layout.setContentsMargins(12, 10, 12, 8)
        root_layout.setSpacing(10)

        # ---------------------------------------------------------------------
        # BARRA DE TÍTULO / HEADER STEAM DECK
        # ---------------------------------------------------------------------
        top_bar = QFrame()
        top_bar.setObjectName("HeaderFrame")
        top_layout = QHBoxLayout(top_bar)
        top_layout.setContentsMargins(14, 8, 14, 8)
        top_layout.setSpacing(10)

        # Logo / Título
        app_title = QLabel("🎮 MC Server-Deck")
        app_title.setStyleSheet("font-size: 18px; font-weight: 800; color: #38bdf8;")
        top_layout.addWidget(app_title)

        deck_badge = QLabel("STEAM DECK EDITION")
        deck_badge.setStyleSheet(
            "background-color: #1e3a5f; color: #93c5fd; font-size: 11px; font-weight: 800; "
            "padding: 4px 8px; border-radius: 6px; border: 1px solid #3b82f6;"
        )
        top_layout.addWidget(deck_badge)

        top_layout.addStretch()

        # Botón Protector de Pantalla OLED (Anti-Quemado)
        btn_oled = QPushButton("🌙 Modo OLED")
        btn_oled.setStyleSheet(
            "background-color: #0f172a; color: #38bdf8; border: 1px solid #0284c7; "
            "font-weight: 700; font-size: 13px; padding: 6px 14px; border-radius: 8px;"
        )
        btn_oled.setToolTip(
            "Activa el protector de pantalla rebotante anti-quemado OLED sobre negro puro.\n"
            "Mantiene el servidor activo y la pantalla protegida sin apagar la consola."
        )
        btn_oled.clicked.connect(self.start_screensaver)
        top_layout.addWidget(btn_oled)

        # Botón Añadir a Steam
        btn_add_steam = QPushButton("➕ Añadir a Steam")
        btn_add_steam.setStyleSheet(
            "background-color: #1e293b; color: #f1f5f9; border: 1px solid #334155; "
            "font-weight: 700; font-size: 13px; padding: 6px 14px; border-radius: 8px;"
        )
        btn_add_steam.setToolTip(
            "Registra MC Server-Deck con icono y carátulas en tu biblioteca de Steam\n"
            "para que aparezca en el Modo Juego (Gaming Mode)."
        )
        btn_add_steam.clicked.connect(self._on_add_to_steam)
        top_layout.addWidget(btn_add_steam)

        # Indicador de estado de Podman
        podman_avail = self.pm.is_podman_available()
        podman_badge = QLabel("PODMAN ROOTLESS: ACTIVO" if podman_avail else "PODMAN: NO ENCONTRADO")
        if podman_avail:
            podman_badge.setStyleSheet(
                "background-color: #064e3b; color: #34d399; font-size: 11px; font-weight: 700; "
                "padding: 4px 10px; border-radius: 6px; border: 1px solid #059669;"
            )
        else:
            podman_badge.setStyleSheet(
                "background-color: #450a0a; color: #f87171; font-size: 11px; font-weight: 700; "
                "padding: 4px 10px; border-radius: 6px; border: 1px solid #dc2626;"
            )
        top_layout.addWidget(podman_badge)

        root_layout.addWidget(top_bar)

        # ---------------------------------------------------------------------
        # PESTAÑAS PRINCIPALES
        # ---------------------------------------------------------------------
        self.tabs = QTabWidget()

        self.tab_dashboard = DashboardTab(self.pm, parent=self)
        self.tab_setup = SetupWizardTab(self.pm, parent=self)
        self.tab_guide = GuideTab(parent=self)

        self.tabs.addTab(self.tab_dashboard, "🎮 Panel de Control y Consola")
        self.tabs.addTab(self.tab_setup, "⚙️ Configurar Servidor (Asistente)")
        self.tabs.addTab(self.tab_guide, "📖 Guía de Conexión & Red")

        # Al completar el despliegue en el asistente, cambiar automáticamente a la consola
        self.tab_setup.server_deployed_signal.connect(self._on_server_deployed)

        root_layout.addWidget(self.tabs, 1)

        # ---------------------------------------------------------------------
        # BARRA DE ESTADO INFERIOR
        # ---------------------------------------------------------------------
        self.status_bar = QStatusBar()
        self.status_bar.setStyleSheet(
            "background-color: #0c1219; color: #94a3b8; font-size: 12px; border-top: 1px solid #1a2533;"
        )
        self.status_bar.showMessage(
            f"Directorio de datos: {self.pm.data_dir}  |  Espacio de usuario: /home/deck  |  Puertos: 25565 (Java), 19132 (Bedrock)"
        )
        self.setStatusBar(self.status_bar)

    def _setup_screensaver(self):
        """Inicializa el protector de pantalla OLED y conecta el temporizador de inactividad."""
        self.screensaver = OledScreensaverWidget(self.pm)
        if self.inactivity_mgr:
            self.inactivity_mgr.inactivity_timeout_signal.connect(self.start_screensaver)

    def start_screensaver(self):
        """Activa el protector de pantalla anti-quemado OLED."""
        if self.screensaver and not self.screensaver.isVisible():
            self.screensaver.start()

    def _on_add_to_steam(self):
        """Registra la aplicación en shortcuts.vdf de Steam."""
        integrator = SteamIntegrator()
        success, message = integrator.add_to_steam_library()
        if success:
            QMessageBox.information(self, "Integración con Steam", message)
        else:
            QMessageBox.warning(self, "Integración con Steam", message)

    def _on_server_deployed(self):
        """Cambia a la pestaña de consola cuando el servidor termina de desplegarse."""
        self.tabs.setCurrentIndex(0)
        self.status_bar.showMessage("✔ Servidor desplegado. Mostrando registros en vivo...", 5000)

    def closeEvent(self, event):
        """Asegura el cierre limpio de los hilos de dashboard y el salvapantallas."""
        if self.screensaver:
            self.screensaver.stop()
            self.screensaver.close()
        self.tab_dashboard.closeEvent(event)
        super().closeEvent(event)
