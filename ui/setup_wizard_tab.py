"""
MC Server-Deck - Pestaña 2: Asistente de Instalación y Guía de Opciones
Formulario guiado con persistencia de datos para configurar o actualizar el servidor.
Soporte multilenguaje i18n y opciones de SSH (Red Local vs Playit.gg).
"""

import socket
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

from i18n import t
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
    """Pestaña de Asistente de Configuración del Servidor con soporte i18n."""

    server_deployed_signal = pyqtSignal()

    def __init__(self, podman_mgr: PodmanManager, parent=None):
        super().__init__(parent)
        self.pm = podman_mgr
        self.deploy_worker: Optional[DeployWorkerThread] = None
        self.progress_dialog: Optional[DeployProgressDialog] = None

        self._build_ui()
        self._load_saved_values()

    def _get_local_ip(self) -> str:
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
        main_layout.setSpacing(10)

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
        self.h_title = QLabel(t("wizard_banner_title"))
        self.h_title.setStyleSheet("font-size: 16px; font-weight: 800; color: #38bdf8;")
        self.h_desc = QLabel(t("wizard_banner_desc"))
        self.h_desc.setStyleSheet("font-size: 13px; color: #94a3b8;")
        self.h_desc.setWordWrap(True)
        desc_layout.addWidget(self.h_title)
        desc_layout.addWidget(self.h_desc)
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

        self.lbl_version = QLabel(t("lbl_version_title"))
        self.lbl_version.setStyleSheet("font-size: 15px; font-weight: 700; color: #f8fafc;")
        ver_ram_layout.addWidget(self.lbl_version, 0, 0, 1, 2)

        self.combo_version = QComboBox()
        self.combo_version.addItems([
            "LATEST",
            "1.21.4",
            "1.21.1",
            "1.20.4",
            "1.20.1",
            "1.19.4",
            "1.18.2",
            "1.16.5",
            "Custom...",
        ])
        self.combo_version.currentIndexChanged.connect(self._on_version_changed)
        ver_ram_layout.addWidget(self.combo_version, 1, 0)

        self.txt_custom_version = QLineEdit()
        self.txt_custom_version.setPlaceholderText(t("custom_version_placeholder"))
        self.txt_custom_version.setEnabled(False)
        ver_ram_layout.addWidget(self.txt_custom_version, 1, 1)

        self.lbl_ram = QLabel(t("lbl_ram_title"))
        self.lbl_ram.setStyleSheet("font-size: 15px; font-weight: 700; color: #f8fafc;")
        ver_ram_layout.addWidget(self.lbl_ram, 2, 0, 1, 2)

        ram_slider_layout = QHBoxLayout()
        self.slider_ram = QSlider(Qt.Orientation.Horizontal)
        self.slider_ram.setRange(2, 8)
        self.slider_ram.setValue(4)
        self.slider_ram.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.slider_ram.setTickInterval(1)
        self.slider_ram.valueChanged.connect(self._on_ram_slider_changed)
        ram_slider_layout.addWidget(self.slider_ram, 1)

        self.lbl_ram_val = QLabel(f"4G ({t('ram_recommended')})")
        self.lbl_ram_val.setStyleSheet(
            "font-size: 15px; font-weight: 800; color: #38bdf8; background-color: #0c1520; "
            "padding: 6px 14px; border-radius: 8px; border: 1px solid #233347;"
        )
        ram_slider_layout.addWidget(self.lbl_ram_val)
        ver_ram_layout.addLayout(ram_slider_layout, 3, 0, 1, 2)

        self.note_ram = QLabel(t("ram_warning"))
        self.note_ram.setStyleSheet(
            "font-size: 12px; color: #f59e0b; background-color: #261b0c; padding: 8px 12px; "
            "border-radius: 8px; border: 1px solid #78350f;"
        )
        self.note_ram.setWordWrap(True)
        ver_ram_layout.addWidget(self.note_ram, 4, 0, 1, 2)

        container_layout.addWidget(ver_ram_card)

        # ---------------------------------------------------------------------
        # SECCIÓN 2: TIPO DE SERVIDOR Y MODLOADER
        # ---------------------------------------------------------------------
        type_card = QFrame()
        type_card.setObjectName("CardFrame")
        type_layout = QVBoxLayout(type_card)
        type_layout.setContentsMargins(16, 16, 16, 16)
        type_layout.setSpacing(14)

        self.lbl_type_title = QLabel(t("lbl_type_title"))
        self.lbl_type_title.setStyleSheet("font-size: 15px; font-weight: 700; color: #f8fafc;")
        type_layout.addWidget(self.lbl_type_title)

        cat_layout = QHBoxLayout()
        cat_layout.setSpacing(14)

        self.radio_vanilla = QRadioButton(t("type_vanilla"))
        self.radio_plugins = QRadioButton(t("type_plugins"))
        self.radio_mods = QRadioButton(t("type_mods"))
        self.radio_plugins.setChecked(True)

        self.radio_vanilla.toggled.connect(self._on_category_changed)
        self.radio_plugins.toggled.connect(self._on_category_changed)
        self.radio_mods.toggled.connect(self._on_category_changed)

        cat_layout.addWidget(self.radio_vanilla)
        cat_layout.addWidget(self.radio_plugins)
        cat_layout.addWidget(self.radio_mods)
        type_layout.addLayout(cat_layout)

        loader_sublayout = QHBoxLayout()
        self.lbl_loader = QLabel(t("lbl_specific_software"))
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

        self.lbl_conn = QLabel(t("lbl_connectivity_title"))
        self.lbl_conn.setStyleSheet("font-size: 15px; font-weight: 700; color: #f8fafc;")
        conn_layout.addWidget(self.lbl_conn)

        self.chk_crossplay = QCheckBox(t("chk_crossplay"))
        self.chk_crossplay.setStyleSheet("font-size: 14px; font-weight: 700; color: #a78bfa;")
        self.chk_crossplay.setChecked(True)
        conn_layout.addWidget(self.chk_crossplay)

        self.lbl_cross_info = QLabel(t("crossplay_info"))
        self.lbl_cross_info.setStyleSheet("font-size: 12px; color: #94a3b8; margin-left: 32px;")
        self.lbl_cross_info.setWordWrap(True)
        conn_layout.addWidget(self.lbl_cross_info)

        self.btn_apply_floodgate = QPushButton(t("btn_apply_floodgate"))
        self.btn_apply_floodgate.setStyleSheet(
            "background-color: #312e81; color: #e0e7ff; font-size: 13px; font-weight: 600; "
            "border: 1px solid #4338ca; border-radius: 8px; padding: 8px 14px;"
        )
        self.btn_apply_floodgate.clicked.connect(self._on_apply_floodgate_fix)
        conn_layout.addWidget(self.btn_apply_floodgate)

        auth_layout = QHBoxLayout()
        self.auth_lbl = QLabel(t("lbl_auth_mode"))
        self.auth_lbl.setStyleSheet("font-weight: 600; color: #cbd5e1;")
        auth_layout.addWidget(self.auth_lbl)

        self.radio_auth_online = QRadioButton(t("auth_premium"))
        self.radio_auth_offline = QRadioButton(t("auth_offline"))
        self.radio_auth_offline.setChecked(True)

        auth_layout.addWidget(self.radio_auth_online)
        auth_layout.addWidget(self.radio_auth_offline)
        conn_layout.addLayout(auth_layout)

        self.chk_whitelist = QCheckBox(t("chk_whitelist"))
        conn_layout.addWidget(self.chk_whitelist)

        container_layout.addWidget(conn_card)

        # ---------------------------------------------------------------------
        # SECCIÓN 4: TÚNEL PLAYIT.GG
        # ---------------------------------------------------------------------
        playit_card = QFrame()
        playit_card.setObjectName("CardFrame")
        playit_layout = QVBoxLayout(playit_card)
        playit_layout.setContentsMargins(16, 16, 16, 16)
        playit_layout.setSpacing(12)

        self.lbl_playit = QLabel(t("lbl_playit_title"))
        self.lbl_playit.setStyleSheet("font-size: 15px; font-weight: 700; color: #f8fafc;")
        playit_layout.addWidget(self.lbl_playit)

        key_layout = QHBoxLayout()
        self.lbl_key = QLabel(t("lbl_playit_key"))
        self.lbl_key.setStyleSheet("font-weight: 600; color: #94a3b8;")
        key_layout.addWidget(self.lbl_key)

        self.txt_playit_key = QLineEdit()
        self.txt_playit_key.setEchoMode(QLineEdit.EchoMode.Password)
        self.txt_playit_key.setPlaceholderText(t("playit_key_placeholder"))
        key_layout.addWidget(self.txt_playit_key, 1)

        self.btn_toggle_key = QPushButton("👁")
        self.btn_toggle_key.setFixedWidth(44)
        self.btn_toggle_key.clicked.connect(self._toggle_key_visibility)
        key_layout.addWidget(self.btn_toggle_key)

        self.btn_open_playit = QPushButton(t("btn_open_playit"))
        self.btn_open_playit.clicked.connect(lambda: QDesktopServices.openUrl(QUrl("https://playit.gg/manage")))
        key_layout.addWidget(self.btn_open_playit)

        playit_layout.addLayout(key_layout)

        self.playit_info = QLabel(t("playit_card_info"))
        self.playit_info.setStyleSheet(
            "font-size: 12px; color: #94a3b8; background-color: #0b121b; padding: 10px 14px; "
            "border-radius: 8px; border: 1px solid #1e293b;"
        )
        playit_layout.addWidget(self.playit_info)

        container_layout.addWidget(playit_card)

        # ---------------------------------------------------------------------
        # SECCIÓN 5: SERVIDOR SSH / SFTP (CON MODO IP vs PLAYIT)
        # ---------------------------------------------------------------------
        ssh_card = QFrame()
        ssh_card.setObjectName("CardFrame")
        ssh_layout = QVBoxLayout(ssh_card)
        ssh_layout.setContentsMargins(16, 16, 16, 16)
        ssh_layout.setSpacing(12)

        self.chk_enable_ssh = QCheckBox(t("chk_enable_ssh"))
        self.chk_enable_ssh.setStyleSheet("font-size: 15px; font-weight: 700; color: #38bdf8;")
        self.chk_enable_ssh.toggled.connect(self._on_ssh_toggled)
        ssh_layout.addWidget(self.chk_enable_ssh)

        self.ssh_fields_frame = QFrame()
        ssh_fields_layout = QVBoxLayout(self.ssh_fields_frame)
        ssh_fields_layout.setContentsMargins(10, 8, 10, 8)
        ssh_fields_layout.setSpacing(12)

        # Selector de Modo de Conexión SSH (Red Local vs Playit.gg)
        ssh_mode_header = QHBoxLayout()
        self.lbl_ssh_mode = QLabel(t("lbl_ssh_mode"))
        self.lbl_ssh_mode.setStyleSheet("font-weight: 700; color: #f1f5f9;")
        ssh_mode_header.addWidget(self.lbl_ssh_mode)

        self.radio_ssh_local = QRadioButton(t("ssh_mode_local"))
        self.radio_ssh_playit = QRadioButton(t("ssh_mode_playit"))
        self.radio_ssh_local.setChecked(True)
        self.radio_ssh_local.toggled.connect(self._update_ssh_info_label)
        self.radio_ssh_playit.toggled.connect(self._update_ssh_info_label)

        ssh_mode_header.addWidget(self.radio_ssh_local)
        ssh_mode_header.addWidget(self.radio_ssh_playit)
        ssh_mode_header.addStretch()
        ssh_fields_layout.addLayout(ssh_mode_header)

        # Campos Usuario y Contraseña
        user_pass_layout = QGridLayout()
        self.lbl_user = QLabel(t("lbl_ssh_user"))
        self.lbl_user.setStyleSheet("font-weight: 600; color: #cbd5e1;")
        self.txt_ssh_user = QLineEdit("adminmc")

        self.lbl_pass = QLabel(t("lbl_ssh_pass"))
        self.lbl_pass.setStyleSheet("font-weight: 600; color: #cbd5e1;")
        self.txt_ssh_pass = QLineEdit("deckcraft123")

        user_pass_layout.addWidget(self.lbl_user, 0, 0)
        user_pass_layout.addWidget(self.txt_ssh_user, 0, 1)
        user_pass_layout.addWidget(self.lbl_pass, 0, 2)
        user_pass_layout.addWidget(self.txt_ssh_pass, 0, 3)
        ssh_fields_layout.addLayout(user_pass_layout)

        # Mensaje de ayuda contextual según el modo seleccionado
        self.ssh_info = QLabel()
        self.ssh_info.setStyleSheet("font-size: 12px; color: #60a5fa; line-height: 1.4;")
        self._update_ssh_info_label()
        ssh_fields_layout.addWidget(self.ssh_info)

        self.ssh_fields_frame.setEnabled(False)
        ssh_layout.addWidget(self.ssh_fields_frame)

        container_layout.addWidget(ssh_card)

        # ---------------------------------------------------------------------
        # BOTÓN PRINCIPAL DE GUARDAR Y DESPLEGAR
        # ---------------------------------------------------------------------
        self.btn_deploy = QPushButton(t("btn_deploy"))
        self.btn_deploy.setObjectName("BtnDeploy")
        self.btn_deploy.clicked.connect(self._on_deploy_clicked)
        container_layout.addWidget(self.btn_deploy)

        scroll_area.setWidget(container)
        main_layout.addWidget(scroll_area)

    def _update_ssh_info_label(self):
        """Actualiza el texto informativo de conexión SFTP según el modo activo."""
        ip = self._get_local_ip()
        if self.radio_ssh_local.isChecked():
            self.ssh_info.setText(t("ssh_info_local", ip=ip))
        else:
            self.ssh_info.setText(t("ssh_info_playit"))

    def retranslate_ui(self):
        """Actualiza todos los textos estáticos del asistente según el idioma actual."""
        self.h_title.setText(t("wizard_banner_title"))
        self.h_desc.setText(t("wizard_banner_desc"))

        self.lbl_version.setText(t("lbl_version_title"))
        self.txt_custom_version.setPlaceholderText(t("custom_version_placeholder"))

        self.lbl_ram.setText(t("lbl_ram_title"))
        rec_tag = f" ({t('ram_recommended')})" if self.slider_ram.value() == 4 else ""
        self.lbl_ram_val.setText(f"{self.slider_ram.value()}G{rec_tag}")
        self.note_ram.setText(t("ram_warning"))

        self.lbl_type_title.setText(t("lbl_type_title"))
        self.radio_vanilla.setText(t("type_vanilla"))
        self.radio_plugins.setText(t("type_plugins"))
        self.radio_mods.setText(t("type_mods"))
        self.lbl_loader.setText(t("lbl_specific_software"))

        self.lbl_conn.setText(t("lbl_connectivity_title"))
        self.chk_crossplay.setText(t("chk_crossplay"))
        self.lbl_cross_info.setText(t("crossplay_info"))
        self.btn_apply_floodgate.setText(t("btn_apply_floodgate"))
        self.auth_lbl.setText(t("lbl_auth_mode"))
        self.radio_auth_online.setText(t("auth_premium"))
        self.radio_auth_offline.setText(t("auth_offline"))
        self.chk_whitelist.setText(t("chk_whitelist"))

        self.lbl_playit.setText(t("lbl_playit_title"))
        self.lbl_key.setText(t("lbl_playit_key"))
        self.txt_playit_key.setPlaceholderText(t("playit_key_placeholder"))
        self.btn_open_playit.setText(t("btn_open_playit"))
        self.playit_info.setText(t("playit_card_info"))

        self.chk_enable_ssh.setText(t("chk_enable_ssh"))
        self.lbl_ssh_mode.setText(t("lbl_ssh_mode"))
        self.radio_ssh_local.setText(t("ssh_mode_local"))
        self.radio_ssh_playit.setText(t("ssh_mode_playit"))
        self.lbl_user.setText(t("lbl_ssh_user"))
        self.lbl_pass.setText(t("lbl_ssh_pass"))
        self._update_ssh_info_label()

        self.btn_deploy.setText(t("btn_deploy"))

    # -------------------------------------------------------------------------
    # CONTROL DE EVENTOS DE INTERFAZ
    # -------------------------------------------------------------------------

    def _on_version_changed(self, index: int):
        is_custom = "Custom" in self.combo_version.currentText() or "Personalizada" in self.combo_version.currentText()
        self.txt_custom_version.setEnabled(is_custom)
        if is_custom:
            self.txt_custom_version.setFocus()

    def _on_ram_slider_changed(self, val: int):
        rec_tag = f" ({t('ram_recommended')})" if val == 4 else ""
        self.lbl_ram_val.setText(f"{val}G{rec_tag}")

    def _on_category_changed(self):
        self.combo_loader.clear()
        if self.radio_vanilla.isChecked():
            self.combo_loader.addItem("VANILLA")
            self.combo_loader.setEnabled(False)
            self.chk_crossplay.setEnabled(False)
            self.chk_crossplay.setChecked(False)
        elif self.radio_plugins.isChecked():
            self.combo_loader.setEnabled(True)
            self.combo_loader.addItems([
                "PAPER (Recomendado)",
                "PURPUR",
                "SPIGOT",
            ])
            self.chk_crossplay.setEnabled(True)
            self.chk_crossplay.setChecked(True)
        elif self.radio_mods.isChecked():
            self.combo_loader.setEnabled(True)
            self.combo_loader.addItems([
                "FABRIC",
                "FORGE",
                "NEOFORGE",
                "QUILT",
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

        # SSH
        enable_ssh = cfg.get("enable_ssh", False)
        self.chk_enable_ssh.setChecked(enable_ssh)
        ssh_mode = cfg.get("ssh_mode", "local")
        if ssh_mode == "playit":
            self.radio_ssh_playit.setChecked(True)
        else:
            self.radio_ssh_local.setChecked(True)

        self.txt_ssh_user.setText(cfg.get("ssh_user", "adminmc"))
        self.txt_ssh_pass.setText(cfg.get("ssh_pass", "deckcraft123"))
        self._update_ssh_info_label()

    def _collect_config(self) -> dict:
        curr_ver_txt = self.combo_version.currentText()
        if "Custom" in curr_ver_txt or "Personalizada" in curr_ver_txt:
            version = self.txt_custom_version.text().strip() or "LATEST"
        elif "LATEST" in curr_ver_txt:
            version = "LATEST"
        else:
            version = curr_ver_txt.strip()

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

        ssh_mode = "playit" if self.radio_ssh_playit.isChecked() else "local"

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
            "ssh_mode": ssh_mode,
            "ssh_user": self.txt_ssh_user.text().strip() or "adminmc",
            "ssh_pass": self.txt_ssh_pass.text().strip() or "deckcraft123",
        }

    # -------------------------------------------------------------------------
    # EJECUCIÓN DEL DESPLIEGUE ASÍNCRONO
    # -------------------------------------------------------------------------

    def _on_deploy_clicked(self):
        config = self._collect_config()

        self.progress_dialog = DeployProgressDialog(parent=self)
        self.progress_dialog.append_log("[MC Server-Deck] Iniciando orquestación de Podman...")
        self.progress_dialog.append_log(f"  • Versión: {config['version']}")
        self.progress_dialog.append_log(f"  • RAM: {config['memory']}")
        self.progress_dialog.append_log(f"  • Motor: {config['server_type']}")
        self.progress_dialog.append_log(f"  • Crossplay Bedrock: {config['crossplay']}")
        self.progress_dialog.append_log(f"  • Modo Online: {config['online_mode']}")
        self.progress_dialog.append_log(f"  • Modo SSH: {config['ssh_mode']}")

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
