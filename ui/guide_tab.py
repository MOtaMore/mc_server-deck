"""
MC Server-Deck - Pestaña 3: Guía de Conexión y Ayuda
Muestra la IP local del Steam Deck e instrucciones paso a paso para jugar y transferir archivos.
Soporte multilenguaje i18n y modos de conexión SSH (IP Local vs Playit.gg).
"""

import socket
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QDesktopServices
from PyQt6.QtWidgets import (
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from i18n import t
from podman_manager import PodmanManager


class GuideTab(QWidget):
    """Pestaña de instrucciones y referencias de red para el usuario de Steam Deck."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.pm = PodmanManager()
        self._build_ui()

    def _get_local_ip(self) -> str:
        """Detecta la IP local de la Steam Deck en la red WiFi/Ethernet actual."""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except Exception:
            return "192.168.x.x"

    def _build_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)

        container = QWidget()
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(6, 6, 6, 6)
        container_layout.setSpacing(14)

        # ---------------------------------------------------------------------
        # TARJETA IP LOCAL DEL STEAM DECK
        # ---------------------------------------------------------------------
        ip_card = QFrame()
        ip_card.setObjectName("HeaderFrame")
        ip_layout = QHBoxLayout(ip_card)
        ip_layout.setContentsMargins(18, 14, 18, 14)

        ip_icon = QLabel("📡")
        ip_icon.setStyleSheet("font-size: 32px;")
        ip_layout.addWidget(ip_icon)

        ip_text_layout = QVBoxLayout()
        self.ip_title = QLabel(t("guide_ip_title"))
        self.ip_title.setStyleSheet("font-size: 13px; font-weight: 700; color: #94a3b8;")
        self.lbl_ip_val = QLabel(self._get_local_ip())
        self.lbl_ip_val.setStyleSheet("font-size: 22px; font-weight: 800; color: #38bdf8;")
        ip_text_layout.addWidget(self.ip_title)
        ip_text_layout.addWidget(self.lbl_ip_val)
        ip_layout.addLayout(ip_text_layout, 1)

        self.btn_refresh_ip = QPushButton(t("btn_refresh_ip"))
        self.btn_refresh_ip.setStyleSheet("padding: 8px 16px; font-size: 13px;")
        self.btn_refresh_ip.clicked.connect(self._refresh_ip)
        ip_layout.addWidget(self.btn_refresh_ip)

        container_layout.addWidget(ip_card)

        # ---------------------------------------------------------------------
        # GRID DE GUÍAS DE CONEXIÓN
        # ---------------------------------------------------------------------
        self.grid = QGridLayout()
        self.grid.setSpacing(14)

        ip = self.lbl_ip_val.text()
        cfg = self.pm.load_config()
        ssh_user = cfg.get("ssh_user", "adminmc")

        self.card_java, self.lbl_java_title, self.lbl_java_body = self._create_card(
            t("guide_java_title"),
            t("guide_java_body", ip=ip),
            color_accent="#38bdf8"
        )
        self.grid.addWidget(self.card_java, 0, 0)

        self.card_bedrock, self.lbl_bedrock_title, self.lbl_bedrock_body = self._create_card(
            t("guide_bedrock_title"),
            t("guide_bedrock_body", ip=ip),
            color_accent="#a78bfa"
        )
        self.grid.addWidget(self.card_bedrock, 0, 1)

        self.card_playit, self.lbl_playit_title, self.lbl_playit_body = self._create_card(
            t("guide_playit_title"),
            t("guide_playit_body"),
            color_accent="#10b981"
        )
        self.grid.addWidget(self.card_playit, 1, 0)

        self.card_sftp, self.lbl_sftp_title, self.lbl_sftp_body = self._create_card(
            t("guide_sftp_title"),
            t("guide_sftp_body", ip=ip, user=ssh_user),
            color_accent="#f59e0b"
        )
        self.grid.addWidget(self.card_sftp, 1, 1)

        container_layout.addLayout(self.grid)

        # ---------------------------------------------------------------------
        # CONSEJOS PARA STEAM DECK (SUSPENSIÓN / GAMING MODE / OLED)
        # ---------------------------------------------------------------------
        tips_card = QFrame()
        tips_card.setObjectName("CardFrame")
        tips_layout = QVBoxLayout(tips_card)
        tips_layout.setContentsMargins(16, 16, 16, 16)
        tips_layout.setSpacing(8)

        self.tips_title = QLabel(t("guide_tips_title"))
        self.tips_title.setStyleSheet("font-size: 15px; font-weight: 700; color: #f8fafc;")
        tips_layout.addWidget(self.tips_title)

        self.tips_content = QLabel(t("guide_tips_body"))
        self.tips_content.setStyleSheet("font-size: 13px; color: #94a3b8; line-height: 1.5;")
        self.tips_content.setWordWrap(True)
        tips_layout.addWidget(self.tips_content)

        container_layout.addWidget(tips_card)

        scroll_area.setWidget(container)
        main_layout.addWidget(scroll_area)

    def _refresh_ip(self):
        new_ip = self._get_local_ip()
        self.lbl_ip_val.setText(new_ip)
        self.retranslate_ui()

    def retranslate_ui(self):
        """Actualiza todas las etiquetas y tarjetas según el idioma activo."""
        ip = self.lbl_ip_val.text()
        cfg = self.pm.load_config()
        ssh_user = cfg.get("ssh_user", "adminmc")

        self.ip_title.setText(t("guide_ip_title"))
        self.btn_refresh_ip.setText(t("btn_refresh_ip"))

        self.lbl_java_title.setText(t("guide_java_title"))
        self.lbl_java_body.setText(t("guide_java_body", ip=ip))

        self.lbl_bedrock_title.setText(t("guide_bedrock_title"))
        self.lbl_bedrock_body.setText(t("guide_bedrock_body", ip=ip))

        self.lbl_playit_title.setText(t("guide_playit_title"))
        self.lbl_playit_body.setText(t("guide_playit_body"))

        self.lbl_sftp_title.setText(t("guide_sftp_title"))
        self.lbl_sftp_body.setText(t("guide_sftp_body", ip=ip, user=ssh_user))

        self.tips_title.setText(t("guide_tips_title"))
        self.tips_content.setText(t("guide_tips_body"))

    def _create_card(self, title: str, html_body: str, color_accent: str = "#38bdf8"):
        card = QFrame()
        card.setObjectName("CardFrame")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(16, 16, 16, 16)
        card_layout.setSpacing(10)

        lbl_title = QLabel(title)
        lbl_title.setStyleSheet(f"font-size: 15px; font-weight: 700; color: {color_accent};")
        card_layout.addWidget(lbl_title)

        lbl_body = QLabel(html_body)
        lbl_body.setStyleSheet("font-size: 13px; color: #e2e8f0; line-height: 1.4;")
        lbl_body.setWordWrap(True)
        lbl_body.setOpenExternalLinks(True)
        card_layout.addWidget(lbl_body)
        card_layout.addStretch()

        return card, lbl_title, lbl_body
