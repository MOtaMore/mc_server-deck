"""
MC Server-Deck - Ventana Principal (SteamOS 1280x800)
Soporte multilenguaje i18n dinámico (Español, English, Português, Français).
"""

from typing import Optional

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (
    QComboBox,
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

from i18n import LANGUAGES, get_language, set_language, t
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

        # Cargar idioma guardado
        cfg = self.pm.load_config()
        saved_lang = cfg.get("language", "es")
        set_language(saved_lang)

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

        self.deck_badge = QLabel(t("edition_badge"))
        self.deck_badge.setStyleSheet(
            "background-color: #1e3a5f; color: #93c5fd; font-size: 11px; font-weight: 800; "
            "padding: 4px 8px; border-radius: 6px; border: 1px solid #3b82f6;"
        )
        top_layout.addWidget(self.deck_badge)

        top_layout.addStretch()

        # Selector de Idioma (ES / EN / PT / FR)
        self.combo_lang = QComboBox()
        self.combo_lang.setStyleSheet(
            "background-color: #1a2536; color: #e2e8f0; font-size: 13px; font-weight: 700; "
            "border: 1px solid #2e4159; border-radius: 8px; padding: 4px 10px; min-width: 120px;"
        )
        self.combo_lang.addItem("🌐 Español", "es")
        self.combo_lang.addItem("🌐 English", "en")
        self.combo_lang.addItem("🌐 Português", "pt")
        self.combo_lang.addItem("🌐 Français", "fr")

        # Seleccionar idioma activo
        curr_lang = get_language()
        for i in range(self.combo_lang.count()):
            if self.combo_lang.itemData(i) == curr_lang:
                self.combo_lang.setCurrentIndex(i)
                break
        self.combo_lang.currentIndexChanged.connect(self._on_language_changed)
        top_layout.addWidget(self.combo_lang)

        # Botón Protector de Pantalla OLED
        self.btn_oled = QPushButton(t("btn_oled_mode"))
        self.btn_oled.setStyleSheet(
            "background-color: #0f172a; color: #38bdf8; border: 1px solid #0284c7; "
            "font-weight: 700; font-size: 13px; padding: 6px 14px; border-radius: 8px;"
        )
        self.btn_oled.setToolTip(t("btn_oled_tooltip"))
        self.btn_oled.clicked.connect(self.start_screensaver)
        top_layout.addWidget(self.btn_oled)

        # Botón Añadir a Steam
        self.btn_add_steam = QPushButton(t("btn_add_steam"))
        self.btn_add_steam.setStyleSheet(
            "background-color: #1e293b; color: #f1f5f9; border: 1px solid #334155; "
            "font-weight: 700; font-size: 13px; padding: 6px 14px; border-radius: 8px;"
        )
        self.btn_add_steam.setToolTip(t("btn_add_steam_tooltip"))
        self.btn_add_steam.clicked.connect(self._on_add_to_steam)
        top_layout.addWidget(self.btn_add_steam)

        # Indicador de estado de Podman
        podman_avail = self.pm.is_podman_available()
        self.podman_badge = QLabel(t("podman_active") if podman_avail else t("podman_missing"))
        if podman_avail:
            self.podman_badge.setStyleSheet(
                "background-color: #064e3b; color: #34d399; font-size: 11px; font-weight: 700; "
                "padding: 4px 10px; border-radius: 6px; border: 1px solid #059669;"
            )
        else:
            self.podman_badge.setStyleSheet(
                "background-color: #450a0a; color: #f87171; font-size: 11px; font-weight: 700; "
                "padding: 4px 10px; border-radius: 6px; border: 1px solid #dc2626;"
            )
        top_layout.addWidget(self.podman_badge)

        root_layout.addWidget(top_bar)

        # ---------------------------------------------------------------------
        # PESTAÑAS PRINCIPALES
        # ---------------------------------------------------------------------
        self.tabs = QTabWidget()

        self.tab_dashboard = DashboardTab(self.pm, parent=self)
        self.tab_setup = SetupWizardTab(self.pm, parent=self)
        self.tab_guide = GuideTab(parent=self)

        self.tabs.addTab(self.tab_dashboard, t("tab_dashboard"))
        self.tabs.addTab(self.tab_setup, t("tab_setup"))
        self.tabs.addTab(self.tab_guide, t("tab_guide"))

        self.tab_setup.server_deployed_signal.connect(self._on_server_deployed)

        root_layout.addWidget(self.tabs, 1)

        # ---------------------------------------------------------------------
        # BARRA DE ESTADO INFERIOR
        # ---------------------------------------------------------------------
        self.status_bar = QStatusBar()
        self.status_bar.setStyleSheet(
            "background-color: #0c1219; color: #94a3b8; font-size: 12px; border-top: 1px solid #1a2533;"
        )
        self.status_bar.showMessage(t("status_footer", data_dir=self.pm.data_dir))
        self.setStatusBar(self.status_bar)

    def _on_language_changed(self, index: int):
        """Cambia el idioma de la aplicación dinámicamente y actualiza toda la interfaz."""
        lang_code = self.combo_lang.itemData(index)
        set_language(lang_code)

        # Guardar idioma en la configuración del usuario
        cfg = self.pm.load_config()
        cfg["language"] = lang_code
        self.pm.save_config(cfg)

        self.retranslate_ui()

    def retranslate_ui(self):
        """Actualiza todos los textos de la ventana principal y de cada pestaña."""
        self.deck_badge.setText(t("edition_badge"))
        self.btn_oled.setText(t("btn_oled_mode"))
        self.btn_oled.setToolTip(t("btn_oled_tooltip"))
        self.btn_add_steam.setText(t("btn_add_steam"))
        self.btn_add_steam.setToolTip(t("btn_add_steam_tooltip"))

        podman_avail = self.pm.is_podman_available()
        self.podman_badge.setText(t("podman_active") if podman_avail else t("podman_missing"))

        self.tabs.setTabText(0, t("tab_dashboard"))
        self.tabs.setTabText(1, t("tab_setup"))
        self.tabs.setTabText(2, t("tab_guide"))

        self.status_bar.showMessage(t("status_footer", data_dir=self.pm.data_dir))

        # Re-traducir contenido de cada pestaña
        self.tab_dashboard.retranslate_ui()
        self.tab_setup.retranslate_ui()
        self.tab_guide.retranslate_ui()

    def _setup_screensaver(self):
        self.screensaver = OledScreensaverWidget(self.pm)
        if self.inactivity_mgr:
            self.inactivity_mgr.inactivity_timeout_signal.connect(self.start_screensaver)

    def start_screensaver(self):
        if self.screensaver and not self.screensaver.isVisible():
            self.screensaver.start()

    def _on_add_to_steam(self):
        integrator = SteamIntegrator()
        success, message = integrator.add_to_steam_library()
        if success:
            QMessageBox.information(self, "Steam", message)
        else:
            QMessageBox.warning(self, "Steam", message)

    def _on_server_deployed(self):
        self.tabs.setCurrentIndex(0)
        self.status_bar.showMessage(t("server_deployed_msg"), 5000)

    def closeEvent(self, event):
        if self.screensaver:
            self.screensaver.stop()
            self.screensaver.close()
        self.tab_dashboard.closeEvent(event)
        super().closeEvent(event)
