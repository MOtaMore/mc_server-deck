"""
MC Server-Deck - Pestaña 3: Guía de Conexión y Ayuda
Muestra la IP local del Steam Deck e instrucciones paso a paso para jugar y transferir archivos.
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


class GuideTab(QWidget):
    """Pestaña de instrucciones y referencias de red para el usuario de Steam Deck."""

    def __init__(self, parent=None):
        super().__init__(parent)
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
            return "127.0.0.1 (Sin conexión o modo avión)"

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
        ip_title = QLabel("IP Local de tu Steam Deck en la Red:")
        ip_title.setStyleSheet("font-size: 13px; font-weight: 700; color: #94a3b8;")
        self.lbl_ip_val = QLabel(self._get_local_ip())
        self.lbl_ip_val.setStyleSheet("font-size: 22px; font-weight: 800; color: #38bdf8;")
        ip_text_layout.addWidget(ip_title)
        ip_text_layout.addWidget(self.lbl_ip_val)
        ip_layout.addLayout(ip_text_layout, 1)

        btn_refresh_ip = QPushButton("Refrescar IP")
        btn_refresh_ip.setStyleSheet("padding: 8px 16px; font-size: 13px;")
        btn_refresh_ip.clicked.connect(lambda: self.lbl_ip_val.setText(self._get_local_ip()))
        ip_layout.addWidget(btn_refresh_ip)

        container_layout.addWidget(ip_card)

        # ---------------------------------------------------------------------
        # GRID DE GUÍAS DE CONEXIÓN
        # ---------------------------------------------------------------------
        grid = QGridLayout()
        grid.setSpacing(14)

        # 1. Java Edition (LAN)
        card_java = self._create_card(
            "☕ Conectar desde Minecraft Java (PC / Mac / Linux)",
            "<b>En la misma red WiFi/Cable:</b><br>"
            "1. Abre Minecraft Java Edition.<br>"
            "2. Ve a <i>Multijugador -> Añadir Servidor</i>.<br>"
            f"3. Dirección del servidor: <code>{self.lbl_ip_val.text()}:25565</code>.<br>"
            "4. ¡Haz clic en Unirse al Servidor!",
            color_accent="#38bdf8"
        )
        grid.addWidget(card_java, 0, 0)

        # 2. Bedrock Edition (Consolas, Móviles, Switch)
        card_bedrock = self._create_card(
            "🎮 Conectar desde Bedrock (Xbox, Switch, PS4/5, Celular)",
            "<b>Gracias a GeyserMC + Floodgate:</b><br>"
            "1. Abre Minecraft Bedrock.<br>"
            "2. Ve a la pestaña <i>Servidores -> Añadir Servidor</i>.<br>"
            f"3. IP del Servidor: <code>{self.lbl_ip_val.text()}</code>.<br>"
            "4. Puerto: <code>19132</code> (Puerto estándar de Bedrock).<br>"
            "<i>(Nota: En consolas como Xbox o Switch puedes usar apps como BedrockTogether o DNS).</i>",
            color_accent="#a78bfa"
        )
        grid.addWidget(card_bedrock, 0, 1)

        # 3. Jugar por Internet con Playit.gg
        card_playit = self._create_card(
            "🌐 Jugar por Internet con amigos (Sin abrir puertos)",
            "1. Consigue tu <i>Secret Key</i> registrándote en <a style='color:#38bdf8;' href='https://playit.gg'>playit.gg</a>.<br>"
            "2. Pégala en la pestaña <b>Configurar Servidor</b> y guarda.<br>"
            "3. En tu panel de playit.gg crea un túnel:<br>"
            "   • TCP en puerto 25565 para Java.<br>"
            "   • UDP en puerto 19132 para Bedrock.<br>"
            "4. Comparte la dirección pública asignada (ej: <code>algo.craft.ply.gg</code>) a tus amigos.",
            color_accent="#10b981"
        )
        grid.addWidget(card_playit, 1, 0)

        # 4. Transferencia de Archivos SFTP
        card_sftp = self._create_card(
            "📁 Transferir Mods, Plugins y Mundos (SFTP)",
            "1. Activa el contenedor SSH en <b>Configurar Servidor</b>.<br>"
            "2. Abre <b>FileZilla</b>, <b>WinSCP</b> o <b>Cyberduck</b> en tu PC.<br>"
            "3. Configuración de conexión:<br>"
            "   • Protocolo: <code>SFTP</code><br>"
            f"   • Servidor: <code>{self.lbl_ip_val.text()}</code><br>"
            "   • Puerto: <code>2222</code><br>"
            "   • Usuario: <code>adminmc</code> (o el configurado)<br>"
            "   • Carpeta de destino del mundo: <code>/servidor-mc</code>",
            color_accent="#f59e0b"
        )
        grid.addWidget(card_sftp, 1, 1)

        container_layout.addLayout(grid)

        # ---------------------------------------------------------------------
        # CONSEJOS PARA STEAM DECK (SUSPENSIÓN / GAMING MODE)
        # ---------------------------------------------------------------------
        tips_card = QFrame()
        tips_card.setObjectName("CardFrame")
        tips_layout = QVBoxLayout(tips_card)
        tips_layout.setContentsMargins(16, 16, 16, 16)
        tips_layout.setSpacing(8)

        tips_title = QLabel("🔋 Consejos para el Servidor en Steam Deck:")
        tips_title.setStyleSheet("font-size: 15px; font-weight: 700; color: #f8fafc;")
        tips_layout.addWidget(tips_title)

        tips_content = QLabel(
            "• <b>Protector de Pantalla OLED (Anti-Burn):</b> Para proteger la pantalla OLED de la Steam Deck contra quemados sin apagar el servidor, activa el <b>Modo OLED</b> (botón 🌙 superior). Utiliza fondo negro absoluto (0% emisión OLED con píxeles apagados) e icono rebotante tipo monitor CRT / DVD. Además, el sistema inhibe la suspensión de SteamOS para que nadie se desconecte.<br>"
            "• <b>Añadir a la Biblioteca de Steam:</b> Puedes registrar MC Server-Deck en tu biblioteca de Steam para el Modo Juego en un solo clic usando el botón <b>➕ Añadir a Steam</b> de la barra superior.<br>"
            "• <b>Modo de Energía:</b> Conecta el cargador oficial de 45W si vas a hospedar partidas largas con muchos amigos.<br>"
            "• <b>Teclado en Gaming Mode:</b> Pulsa el botón ⌨️ en la consola o el atajo <b>STEAM + X</b> para abrir el teclado virtual en pantalla."
        )
        tips_content.setStyleSheet("font-size: 13px; color: #94a3b8; line-height: 1.5;")
        tips_content.setWordWrap(True)
        tips_layout.addWidget(tips_content)

        container_layout.addWidget(tips_card)

        scroll_area.setWidget(container)
        main_layout.addWidget(scroll_area)

    def _create_card(self, title: str, html_body: str, color_accent: str = "#38bdf8") -> QFrame:
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

        return card
