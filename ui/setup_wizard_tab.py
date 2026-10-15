"""
MC Server-Deck - Pestaña 2: Asistente de Instalación y Guía de Opciones
Formulario guiado con persistencia de datos para configurar o actualizar el servidor.
"""

from typing import Optional

from PyQt6.QtCore import QThread, QUrl, Qt, pyqtSignal
from PyQt6.QtGui import QDesktopServices
from PyQt6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QFrame,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QRadioButton,
    QScrollArea,
    QSlider,
    QVBoxLayout,
    QWidget,
)

from podman_manager import PodmanManager
from ui.dialogs import DeployProgressDialog


class DeployWorkerThread(QThread):
    """Hilo secundario para la creación y despliegue del servidor sin bloquear la GUI."""

    progress_signal = pyqtSignal(str)
    finished_signal = pyqtSignal(bool, str)

    def __init__(self, podman_mgr: PodmanManager, config: dict, parent=None):
        super().__init__(parent)
        self.pm = podman_mgr
        self.config = config

    def run(self):
        try:
            success, message = self.pm.deploy_server(
                self.config, progress_callback=self.progress_signal.emit
            )
            self.finished_signal.emit(success, message)
        except Exception as e:
            self.finished_signal.emit(False, f"Excepción en despliegue: {str(e)}")


class SetupWizardTab(QWidget):
    """Pestaña de Asistente de Configuración del Servidor."""

    server_deployed_signal = pyqtSignal()

    def __init__(self, podman_mgr: PodmanManager, parent=None):
        super().__init__(parent)
        self.pm = podman_mgr
        self.deploy_worker: Optional[DeployWorkerThread] = None
        self.progress_dialog: Optional[DeployProgressDialog] = None

        self._build_ui()
        self._load_saved_values()

    def _build_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        # Scroll Area para permitir navegación fluida táctil
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)

        container = QWidget()
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(6, 6, 6, 6)
        container_layout.setSpacing(14)

        # ---------------------------------------------------------------------
        # BANNER EXPLICATIVO
        # ---------------------------------------------------------------------
        header_card = QFrame()
        header_card.setObjectName("HeaderFrame")
        header_layout = QHBoxLayout(header_card)
        header_layout.setContentsMargins(16, 12, 16, 12)

        icon_label = QLabel("⚙️")
        icon_label.setStyleSheet("font-size: 28px;")
        header_layout.addWidget(icon_label)

        desc_layout = QVBoxLayout()
        h_title = QLabel("Asistente de Servidor y Opciones de Despliegue")
        h_title.setStyleSheet("font-size: 16px; font-weight: 800; color: #38bdf8;")
        h_desc = QLabel(
            "Crea un servidor nuevo o actualiza las opciones del actual. "
            "Tus mundos y archivos guardados en /home/deck/minecraft-server/data NUNCA se borrarán."
        )
        h_desc.setStyleSheet("font-size: 13px; color: #94a3b8;")
        h_desc.setWordWrap(True)
        desc_layout.addWidget(h_title)
        desc_layout.addWidget(h_desc)
        header_layout.addLayout(desc_layout, 1)

        container_layout.addWidget(header_card)

        # ---------------------------------------------------------------------
        # SECCIÓN 1: VERSIÓN Y MEMORIA RAM
        # ---------------------------------------------------------------------
        ver_ram_card = QFrame()
        ver_ram_card.setObjectName("CardFrame")
        ver_ram_layout = QGridLayout(ver_ram_card)
        ver_ram_layout.setContentsMargins(16, 16, 16, 16)
        ver_ram_layout.setSpacing(16)

        # Versión de Minecraft
        lbl_version = QLabel("1. Versión de Minecraft (-e VERSION):")
        lbl_version.setStyleSheet("font-size: 15px; font-weight: 700; color: #f8fafc;")
        ver_ram_layout.addWidget(lbl_version, 0, 0, 1, 2)

        self.combo_version = QComboBox()
        self.combo_version.addItems([
            "LATEST (Última versión oficial)",
            "1.21.4",
            "1.21.1",
            "1.20.4",
            "1.20.1",
            "1.19.4",
            "1.18.2",
            "1.16.5",
            "Personalizada...",
        ])
        self.combo_version.currentIndexChanged.connect(self._on_version_changed)
        ver_ram_layout.addWidget(self.combo_version, 1, 0)

        self.txt_custom_version = QLineEdit()
        self.txt_custom_version.setPlaceholderText("Ej: 1.21.1 ó snapshot...")
        self.txt_custom_version.setEnabled(False)
        ver_ram_layout.addWidget(self.txt_custom_version, 1, 1)

        # Memoria RAM
        lbl_ram = QLabel("2. Memoria RAM Asignada (-e MEMORY):")
        lbl_ram.setStyleSheet("font-size: 15px; font-weight: 700; color: #f8fafc;")
        ver_ram_layout.addWidget(lbl_ram, 2, 0, 1, 2)

        ram_slider_layout = QHBoxLayout()
        self.slider_ram = QSlider(Qt.Orientation.Horizontal)
        self.slider_ram.setRange(2, 8)
        self.slider_ram.setValue(4)
        self.slider_ram.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.slider_ram.setTickInterval(1)
        self.slider_ram.valueChanged.connect(self._on_ram_slider_changed)
        ram_slider_layout.addWidget(self.slider_ram, 1)

        self.lbl_ram_val = QLabel("4G (Recomendado)")
        self.lbl_ram_val.setStyleSheet(
            "font-size: 15px; font-weight: 800; color: #38bdf8; background-color: #0c1520; "
            "padding: 6px 14px; border-radius: 8px; border: 1px solid #233347;"
        )
        ram_slider_layout.addWidget(self.lbl_ram_val)
        ver_ram_layout.addLayout(ram_slider_layout, 3, 0, 1, 2)

        # Nota para Steam Deck RAM unificada
        note_ram = QLabel(
            "⚠️ Nota Steam Deck: Cuenta con 16 GB compartidos entre RAM y GPU. "
            "Se aconseja asignar 4G (Vanilla / Plugins) o 6G (Modpacks pesados) para evitar micro-tirones en Gaming Mode."
        )
        note_ram.setStyleSheet(
            "font-size: 12px; color: #f59e0b; background-color: #261b0c; padding: 8px 12px; "
            "border-radius: 8px; border: 1px solid #78350f;"
        )
        note_ram.setWordWrap(True)
        ver_ram_layout.addWidget(note_ram, 4, 0, 1, 2)

        container_layout.addWidget(ver_ram_card)

        # ---------------------------------------------------------------------
        # SECCIÓN 2: TIPO DE SERVIDOR Y MODLOADER
        # ---------------------------------------------------------------------
        type_card = QFrame()
        type_card.setObjectName("CardFrame")
        type_layout = QVBoxLayout(type_card)
        type_layout.setContentsMargins(16, 16, 16, 16)
        type_layout.setSpacing(14)

        lbl_type_title = QLabel("3. Motor del Servidor y Tipo de Software (-e TYPE):")
        lbl_type_title.setStyleSheet("font-size: 15px; font-weight: 700; color: #f8fafc;")
        type_layout.addWidget(lbl_type_title)

        # Selección de Categoría Principal
        cat_layout = QHBoxLayout()
        cat_layout.setSpacing(14)

        self.radio_vanilla = QRadioButton("Vanilla (Mojang Oficial)")
        self.radio_plugins = QRadioButton("Plugins (Paper / Purpur / Spigot)")
        self.radio_mods = QRadioButton("Mods (Fabric / Forge / NeoForge)")

        self.radio_plugins.setChecked(True)

        self.radio_vanilla.toggled.connect(self._on_category_changed)
        self.radio_plugins.toggled.connect(self._on_category_changed)
        self.radio_mods.toggled.connect(self._on_category_changed)

        cat_layout.addWidget(self.radio_vanilla)
        cat_layout.addWidget(self.radio_plugins)
        cat_layout.addWidget(self.radio_mods)
        type_layout.addLayout(cat_layout)

        # Selector específico del Software
        loader_sublayout = QHBoxLayout()
        self.lbl_loader = QLabel("Software específico:")
        self.lbl_loader.setStyleSheet("font-weight: 600; color: #94a3b8;")
        loader_sublayout.addWidget(self.lbl_loader)

        self.combo_loader = QComboBox()
        self.combo_loader.currentIndexChanged.connect(self._on_loader_changed)
        loader_sublayout.addWidget(self.combo_loader, 1)

        type_layout.addLayout(loader_sublayout)
        container_layout.addWidget(type_card)

        # ---------------------------------------------------------------------
        # SECCIÓN 3: CONECTIVIDAD, CROSSPLAY Y JUGADORES
        # ---------------------------------------------------------------------
        conn_card = QFrame()
        conn_card.setObjectName("CardFrame")
        conn_layout = QVBoxLayout(conn_card)
        conn_layout.setContentsMargins(16, 16, 16, 16)
        conn_layout.setSpacing(14)

        lbl_conn = QLabel("4. Conectividad, Crossplay y Reglas de Jugador:")
        lbl_conn.setStyleSheet("font-size: 15px; font-weight: 700; color: #f8fafc;")
        conn_layout.addWidget(lbl_conn)

        # Checkbox Geyser / Floodgate
        self.chk_crossplay = QCheckBox(
            "Permitir Crossplay Java + Bedrock (GeyserMC + Floodgate + SkinsRestorer)"
        )
        self.chk_crossplay.setStyleSheet("font-size: 14px; font-weight: 700; color: #a78bfa;")
        self.chk_crossplay.setChecked(True)
        conn_layout.addWidget(self.chk_crossplay)

        lbl_cross_info = QLabel(
            "ℹ Permite que amigos en Android, iOS, Xbox, PlayStation, Switch o Windows Bedrock "
            "se conecten directamente al mismo mundo que los de PC Java (Puerto 19132 UDP)."
        )
        lbl_cross_info.setStyleSheet("font-size: 12px; color: #94a3b8; margin-left: 32px;")
        lbl_cross_info.setWordWrap(True)
        conn_layout.addWidget(lbl_cross_info)

        # Botón de corrección de auth-type floodgate
        btn_apply_floodgate = QPushButton("🔄 Aplicar corrección 'auth-type: floodgate' en Geyser config")
        btn_apply_floodgate.setStyleSheet(
            "background-color: #312e81; color: #e0e7ff; font-size: 13px; font-weight: 600; "
            "border: 1px solid #4338ca; border-radius: 8px; padding: 8px 14px;"
        )
        btn_apply_floodgate.setToolTip(
            "Aplica automáticamente sed -i 's/auth-type: online/auth-type: floodgate/g' "
            "en plugins/Geyser-Spigot/config.yml"
        )
        btn_apply_floodgate.clicked.connect(self._on_apply_floodgate_fix)
        conn_layout.addWidget(btn_apply_floodgate)

        # Modo de Autenticación
        auth_layout = QHBoxLayout()
        auth_lbl = QLabel("Modo de Autenticación:")
        auth_lbl.setStyleSheet("font-weight: 600; color: #cbd5e1;")
        auth_layout.addWidget(auth_lbl)

        self.radio_auth_online = QRadioButton("Solo Cuentas Premium (ONLINE_MODE=TRUE)")
        self.radio_auth_offline = QRadioButton("Premium + No Premium / Offline (ONLINE_MODE=FALSE)")
        self.radio_auth_offline.setChecked(True)

        auth_layout.addWidget(self.radio_auth_online)
        auth_layout.addWidget(self.radio_auth_offline)
        conn_layout.addLayout(auth_layout)

        # Whitelist
        self.chk_whitelist = QCheckBox(
            "Activar Whitelist obligatoria (ENABLE_WHITELIST & ENFORCE_WHITELIST)"
        )
        conn_layout.addWidget(self.chk_whitelist)

        container_layout.addWidget(conn_card)

        # ---------------------------------------------------------------------
        # SECCIÓN 4: TÚNEL PLAYIT.GG (JUGAR CON AMIGOS SIN ABRIR PUERTOS)
        # ---------------------------------------------------------------------
        playit_card = QFrame()
        playit_card.setObjectName("CardFrame")
        playit_layout = QVBoxLayout(playit_card)
        playit_layout.setContentsMargins(16, 16, 16, 16)
        playit_layout.setSpacing(12)

        lbl_playit = QLabel("5. Túnel Playit.gg (Jugar por Internet sin abrir puertos en el router):")
        lbl_playit.setStyleSheet("font-size: 15px; font-weight: 700; color: #f8fafc;")
        playit_layout.addWidget(lbl_playit)

        key_layout = QHBoxLayout()
        lbl_key = QLabel("Playit Secret Key:")
        lbl_key.setStyleSheet("font-weight: 600; color: #94a3b8;")
        key_layout.addWidget(lbl_key)

        self.txt_playit_key = QLineEdit()
        self.txt_playit_key.setEchoMode(QLineEdit.EchoMode.Password)
        self.txt_playit_key.setPlaceholderText("Pega aquí tu clave secreta de agente playit (opcional)")
        key_layout.addWidget(self.txt_playit_key, 1)

        self.btn_toggle_key = QPushButton("👁")
        self.btn_toggle_key.setFixedWidth(44)
        self.btn_toggle_key.clicked.connect(self._toggle_key_visibility)
        key_layout.addWidget(self.btn_toggle_key)

        btn_open_playit = QPushButton("🌐 Panel Playit.gg")
        btn_open_playit.clicked.connect(lambda: QDesktopServices.openUrl(QUrl("https://playit.gg/manage")))
        key_layout.addWidget(btn_open_playit)

        playit_layout.addLayout(key_layout)

        # Tarjeta informativa de puertos en Playit
        playit_info = QLabel(
            "📋 Puertos para configurar en la web de Playit.gg:\n"
            "  • Minecraft Java: Añade un túnel TCP apuntando al puerto local 25565\n"
            "  • Minecraft Bedrock: Añade un túnel UDP apuntando al puerto local 19132\n"
            "  • Servidor SFTP: Añade un túnel TCP apuntando al puerto local 2222"
        )
        playit_info.setStyleSheet(
            "font-size: 12px; color: #94a3b8; background-color: #0b121b; padding: 10px 14px; "
            "border-radius: 8px; border: 1px solid #1e293b;"
        )
        playit_layout.addWidget(playit_info)

        container_layout.addWidget(playit_card)

        # ---------------------------------------------------------------------
        # SECCIÓN 5: SERVIDOR SSH / SFTP (FILEZILLA / WINSCP)
        # ---------------------------------------------------------------------
        ssh_card = QFrame()
        ssh_card.setObjectName("CardFrame")
        ssh_layout = QVBoxLayout(ssh_card)
        ssh_layout.setContentsMargins(16, 16, 16, 16)
        ssh_layout.setSpacing(12)

        self.chk_enable_ssh = QCheckBox(
            "6. Habilitar contenedor SSH / SFTP (Para subir mods y mundos con FileZilla / WinSCP)"
        )
        self.chk_enable_ssh.setStyleSheet("font-size: 15px; font-weight: 700; color: #38bdf8;")
        self.chk_enable_ssh.toggled.connect(self._on_ssh_toggled)
        ssh_layout.addWidget(self.chk_enable_ssh)

        self.ssh_fields_frame = QFrame()
        ssh_fields_layout = QGridLayout(self.ssh_fields_frame)
        ssh_fields_layout.setContentsMargins(10, 8, 10, 8)
        ssh_fields_layout.setSpacing(12)

        lbl_user = QLabel("Usuario SSH:")
        lbl_user.setStyleSheet("font-weight: 600; color: #cbd5e1;")
        self.txt_ssh_user = QLineEdit("adminmc")

        lbl_pass = QLabel("Contraseña SSH:")
        lbl_pass.setStyleSheet("font-weight: 600; color: #cbd5e1;")
        self.txt_ssh_pass = QLineEdit("deckcraft123")

        ssh_fields_layout.addWidget(lbl_user, 0, 0)
        ssh_fields_layout.addWidget(self.txt_ssh_user, 0, 1)
        ssh_fields_layout.addWidget(lbl_pass, 0, 2)
        ssh_fields_layout.addWidget(self.txt_ssh_pass, 0, 3)

        ssh_info = QLabel(
            "💡 Conexión SFTP desde tu PC:\n"
            "Host: IP de tu Steam Deck en la red local (o dominio de Playit) | Puerto: 2222 | Ruta remota: /servidor-mc"
        )
        ssh_info.setStyleSheet("font-size: 12px; color: #60a5fa;")
        ssh_fields_layout.addWidget(ssh_info, 1, 0, 1, 4)

        self.ssh_fields_frame.setEnabled(False)
        ssh_layout.addWidget(self.ssh_fields_frame)

        container_layout.addWidget(ssh_card)

        # ---------------------------------------------------------------------
        # BOTÓN PRINCIPAL DE GUARDAR Y DESPLEGAR
        # ---------------------------------------------------------------------
        btn_deploy = QPushButton("💾 Guardar y Desplegar Servidor en Steam Deck")
        btn_deploy.setObjectName("BtnDeploy")
        btn_deploy.clicked.connect(self._on_deploy_clicked)
        container_layout.addWidget(btn_deploy)

        scroll_area.setWidget(container)
        main_layout.addWidget(scroll_area)

    # -------------------------------------------------------------------------
    # CONTROL DE EVENTOS DE INTERFAZ
    # -------------------------------------------------------------------------

    def _on_version_changed(self, index: int):
        is_custom = "Personalizada" in self.combo_version.currentText()
        self.txt_custom_version.setEnabled(is_custom)
        if is_custom:
            self.txt_custom_version.setFocus()

    def _on_ram_slider_changed(self, val: int):
        rec_tag = " (Recomendado)" if val == 4 else ""
        self.lbl_ram_val.setText(f"{val}G{rec_tag}")

    def _on_category_changed(self):
        self.combo_loader.clear()
        if self.radio_vanilla.isChecked():
            self.combo_loader.addItem("VANILLA (Oficial de Mojang)")
            self.combo_loader.setEnabled(False)
            self.chk_crossplay.setEnabled(False)
            self.chk_crossplay.setChecked(False)
        elif self.radio_plugins.isChecked():
            self.combo_loader.setEnabled(True)
            self.combo_loader.addItems([
                "PAPER (Recomendado - Máximo rendimiento)",
                "PURPUR (Optimizado y personalizable)",
                "SPIGOT (Clásico)",
            ])
            self.chk_crossplay.setEnabled(True)
            self.chk_crossplay.setChecked(True)
        elif self.radio_mods.isChecked():
            self.combo_loader.setEnabled(True)
            self.combo_loader.addItems([
                "FABRIC (Ligero y moderno)",
                "FORGE (Estándar para mods clásicos)",
                "NEOFORGE (Nueva generación)",
                "QUILT (Ecosistema modular)",
            ])
            self._on_loader_changed()

    def _on_loader_changed(self):
        loader_text = self.combo_loader.currentText()
        if self.radio_mods.isChecked():
            if "FABRIC" in loader_text:
                self.chk_crossplay.setEnabled(True)
            else:
                self.chk_crossplay.setEnabled(False)
                self.chk_crossplay.setChecked(False)

    def _toggle_key_visibility(self):
        if self.txt_playit_key.echoMode() == QLineEdit.EchoMode.Password:
            self.txt_playit_key.setEchoMode(QLineEdit.EchoMode.Normal)
            self.btn_toggle_key.setText("🙈")
        else:
            self.txt_playit_key.setEchoMode(QLineEdit.EchoMode.Password)
            self.btn_toggle_key.setText("👁")

    def _on_ssh_toggled(self, checked: bool):
        self.ssh_fields_frame.setEnabled(checked)

    def _on_apply_floodgate_fix(self):
        success, message = self.pm.apply_floodgate_config_fix()
        if success:
            QMessageBox.information(self, "Geyser Floodgate Fix", message)
        else:
            QMessageBox.warning(self, "Geyser Floodgate Fix", message)

    # -------------------------------------------------------------------------
    # PERSISTENCIA Y CARGA DE VALORES
    # -------------------------------------------------------------------------

    def _load_saved_values(self):
        """Carga la configuración almacenada en ~/minecraft-server/mc_server_config.json."""
        cfg = self.pm.load_config()

        # Versión
        ver = cfg.get("version", "LATEST")
        matched = False
        for i in range(self.combo_version.count()):
            if ver in self.combo_version.itemText(i):
                self.combo_version.setCurrentIndex(i)
                matched = True
                break
        if not matched:
            self.combo_version.setCurrentIndex(self.combo_version.count() - 1)
            self.txt_custom_version.setText(ver)
            self.txt_custom_version.setEnabled(True)

        # Memoria
        mem_str = cfg.get("memory", "4G").replace("G", "").strip()
        try:
            mem_val = int(mem_str)
            if 2 <= mem_val <= 8:
                self.slider_ram.setValue(mem_val)
        except ValueError:
            self.slider_ram.setValue(4)

        # Categoría y Loader
        cat = cfg.get("server_category", "plugins")
        if cat == "vanilla":
            self.radio_vanilla.setChecked(True)
        elif cat == "mods":
            self.radio_mods.setChecked(True)
        else:
            self.radio_plugins.setChecked(True)

        srv_type = cfg.get("server_type", "PAPER").upper()
        for i in range(self.combo_loader.count()):
            if srv_type in self.combo_loader.itemText(i):
                self.combo_loader.setCurrentIndex(i)
                break

        # Opciones
        self.chk_crossplay.setChecked(cfg.get("crossplay", True))
        if cfg.get("online_mode", False):
            self.radio_auth_online.setChecked(True)
        else:
            self.radio_auth_offline.setChecked(True)

        self.chk_whitelist.setChecked(cfg.get("enable_whitelist", False))
        self.txt_playit_key.setText(cfg.get("playit_key", ""))

        enable_ssh = cfg.get("enable_ssh", False)
        self.chk_enable_ssh.setChecked(enable_ssh)
        self.txt_ssh_user.setText(cfg.get("ssh_user", "adminmc"))
        self.txt_ssh_pass.setText(cfg.get("ssh_pass", "deckcraft123"))

    def _collect_config(self) -> dict:
        """Extrae el diccionario completo de configuración de los campos del formulario."""
        # Determinar versión
        if "Personalizada" in self.combo_version.currentText():
            version = self.txt_custom_version.text().strip() or "LATEST"
        elif "LATEST" in self.combo_version.currentText():
            version = "LATEST"
        else:
            version = self.combo_version.currentText().strip()

        # Determinar categoría y tipo
        if self.radio_vanilla.isChecked():
            category = "vanilla"
            server_type = "VANILLA"
        elif self.radio_mods.isChecked():
            category = "mods"
            loader_txt = self.combo_loader.currentText()
            if "FABRIC" in loader_txt:
                server_type = "FABRIC"
            elif "FORGE" in loader_txt:
                server_type = "FORGE"
            elif "NEOFORGE" in loader_txt:
                server_type = "NEOFORGE"
            else:
                server_type = "QUILT"
        else:
            category = "plugins"
            loader_txt = self.combo_loader.currentText()
            if "PURPUR" in loader_txt:
                server_type = "PURPUR"
            elif "SPIGOT" in loader_txt:
                server_type = "SPIGOT"
            else:
                server_type = "PAPER"

        return {
            "version": version,
            "memory": f"{self.slider_ram.value()}G",
            "server_category": category,
            "server_type": server_type,
            "crossplay": self.chk_crossplay.isChecked(),
            "online_mode": self.radio_auth_online.isChecked(),
            "enable_whitelist": self.chk_whitelist.isChecked(),
            "playit_key": self.txt_playit_key.text().strip(),
            "enable_ssh": self.chk_enable_ssh.isChecked(),
            "ssh_user": self.txt_ssh_user.text().strip() or "adminmc",
            "ssh_pass": self.txt_ssh_pass.text().strip() or "deckcraft123",
        }

    # -------------------------------------------------------------------------
    # EJECUCIÓN DEL DESPLIEGUE ASÍNCRONO
    # -------------------------------------------------------------------------

    def _on_deploy_clicked(self):
        config = self._collect_config()

        # Abrir modal de progreso
        self.progress_dialog = DeployProgressDialog(parent=self)
        self.progress_dialog.append_log("[MC Server-Deck] Iniciando orquestación de Podman...")
        self.progress_dialog.append_log(f"  • Versión: {config['version']}")
        self.progress_dialog.append_log(f"  • RAM: {config['memory']}")
        self.progress_dialog.append_log(f"  • Motor: {config['server_type']}")
        self.progress_dialog.append_log(f"  • Crossplay Bedrock: {config['crossplay']}")
        self.progress_dialog.append_log(f"  • Modo Online: {config['online_mode']}")

        # Iniciar hilo de trabajo
        self.deploy_worker = DeployWorkerThread(self.pm, config, parent=self)
        self.deploy_worker.progress_signal.connect(self.progress_dialog.append_log)
        self.deploy_worker.finished_signal.connect(self._on_deploy_finished)
        self.deploy_worker.start()

        self.progress_dialog.exec()

    def _on_deploy_finished(self, success: bool, message: str):
        if self.progress_dialog:
            self.progress_dialog.set_finished(success, message)
        if success:
            self.server_deployed_signal.emit()
