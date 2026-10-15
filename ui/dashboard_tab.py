"""
MC Server-Deck - Pestaña 1: Panel de Control y Consola en Vivo
Panel principal con monitoreo en tiempo real, streaming de logs y consola RCON.
"""

import subprocess
import time
from typing import Optional

from PyQt6.QtCore import QObject, QThread, QTimer, Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QCheckBox,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPlainTextEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from podman_manager import PodmanManager
from steam_integrator import SteamIntegrator
from ui.dialogs import ConfirmDialog, TouchInputDialog


class LogStreamerThread(QThread):
    """Hilo secundario para transmitir la salida en vivo de 'podman logs -f'."""

    log_received = pyqtSignal(str)

    def __init__(self, container_name: str = "mc-server", parent: Optional[QObject] = None):
        super().__init__(parent)
        self.container_name = container_name
        self.is_running = True
        self.process: Optional[subprocess.Popen] = None

    def run(self):
        while self.is_running:
            try:
                cmd = ["podman", "logs", "-f", "--tail", "100", self.container_name]
                self.process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    encoding="utf-8",
                    errors="replace",
                    bufsize=1,
                )

                for line in iter(self.process.stdout.readline, ""):
                    if not self.is_running:
                        break
                    if line:
                        self.log_received.emit(line.rstrip())

                if self.process:
                    self.process.stdout.close()
                    self.process.wait()

            except Exception as e:
                if self.is_running:
                    self.log_received.emit(f"[MC Server-Deck Logs Error]: {e}")

            # Esperar antes de intentar reconectar si el contenedor no está activo
            time.sleep(2)

    def stop(self):
        self.is_running = False
        if self.process:
            try:
                self.process.terminate()
                self.process.kill()
            except Exception:
                pass
        self.wait(2000)


class WorkerActionThread(QThread):
    """Hilo para ejecutar acciones de Podman en segundo plano sin congelar la GUI."""

    finished_signal = pyqtSignal(bool, str, str)  # success, action_name, output

    def __init__(self, action_name: str, target_fn, *args, parent=None):
        super().__init__(parent)
        self.action_name = action_name
        self.target_fn = target_fn
        self.args = args

    def run(self):
        try:
            success, output = self.target_fn(*self.args)
            self.finished_signal.emit(success, self.action_name, output)
        except Exception as e:
            self.finished_signal.emit(False, self.action_name, str(e))


class DashboardTab(QWidget):
    """Pestaña del Panel de Control y Consola Interactiva."""

    def __init__(self, podman_mgr: PodmanManager, parent=None):
        super().__init__(parent)
        self.pm = podman_mgr
        self.log_thread: Optional[LogStreamerThread] = None
        self.active_workers: list[WorkerActionThread] = []

        self._build_ui()
        self._start_status_timer()
        self._start_log_stream()

    def _build_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(14, 14, 14, 14)
        main_layout.setSpacing(14)

        # ---------------------------------------------------------------------
        # 1. GRID DE ESTADO EN TIEMPO REAL
        # ---------------------------------------------------------------------
        status_card = QFrame()
        status_card.setObjectName("CardFrame")
        status_layout = QGridLayout(status_card)
        status_layout.setContentsMargins(16, 12, 16, 12)
        status_layout.setHorizontalSpacing(24)
        status_layout.setVerticalSpacing(6)

        # Labels de título
        title_pod = QLabel("Pod (Red y Contenedores):")
        title_pod.setStyleSheet("font-weight: 700; color: #cbd5e1;")
        self.pill_pod = self._create_status_pill("Comprobando...")

        title_server = QLabel("Servidor Minecraft (itzg):")
        title_server.setStyleSheet("font-weight: 700; color: #cbd5e1;")
        self.pill_server = self._create_status_pill("Comprobando...")

        title_playit = QLabel("Túnel Playit.gg:")
        title_playit.setStyleSheet("font-weight: 700; color: #cbd5e1;")
        self.pill_playit = self._create_status_pill("Comprobando...")

        title_ssh = QLabel("Acceso SFTP / SSH:")
        title_ssh.setStyleSheet("font-weight: 700; color: #cbd5e1;")
        self.pill_ssh = self._create_status_pill("Comprobando...")

        # Disposición en 2 filas x 4 columnas
        status_layout.addWidget(title_pod, 0, 0)
        status_layout.addWidget(self.pill_pod, 0, 1)

        status_layout.addWidget(title_server, 0, 2)
        status_layout.addWidget(self.pill_server, 0, 3)

        status_layout.addWidget(title_playit, 1, 0)
        status_layout.addWidget(self.pill_playit, 1, 1)

        status_layout.addWidget(title_ssh, 1, 2)
        status_layout.addWidget(self.pill_ssh, 1, 3)

        main_layout.addWidget(status_card)

        # ---------------------------------------------------------------------
        # 2. BOTONES DE ACCIÓN RÁPIDA (TOUCH-FRIENDLY GRANDES)
        # ---------------------------------------------------------------------
        actions_card = QFrame()
        actions_card.setObjectName("CardFrame")
        actions_layout = QHBoxLayout(actions_card)
        actions_layout.setContentsMargins(12, 10, 12, 10)
        actions_layout.setSpacing(12)

        self.btn_start = QPushButton("▶ Iniciar Servidor")
        self.btn_start.setObjectName("BtnStart")
        self.btn_start.clicked.connect(self._on_start_server)

        self.btn_stop = QPushButton("⏹ Detener Servidor")
        self.btn_stop.setObjectName("BtnStop")
        self.btn_stop.clicked.connect(self._on_stop_server)

        self.btn_restart = QPushButton("🔄 Reiniciar Servidor")
        self.btn_restart.setObjectName("BtnRestart")
        self.btn_restart.clicked.connect(self._on_restart_server)

        self.btn_fix_perms = QPushButton("🔧 Corregir Permisos")
        self.btn_fix_perms.setObjectName("BtnFix")
        self.btn_fix_perms.setToolTip(
            "Ejecuta podman unshare chown -R 0:0 y chmod 777 para reparar errores de permisos en /home/deck"
        )
        self.btn_fix_perms.clicked.connect(self._on_fix_permissions)

        actions_layout.addWidget(self.btn_start, 1)
        actions_layout.addWidget(self.btn_stop, 1)
        actions_layout.addWidget(self.btn_restart, 1)
        actions_layout.addWidget(self.btn_fix_perms, 1)

        main_layout.addWidget(actions_card)

        # ---------------------------------------------------------------------
        # 3. CONSOLA INTERACTIVA (LOGS EN VIVO)
        # ---------------------------------------------------------------------
        console_card = QFrame()
        console_card.setObjectName("CardFrame")
        console_layout = QVBoxLayout(console_card)
        console_layout.setContentsMargins(12, 12, 12, 12)
        console_layout.setSpacing(8)

        # Barra superior de la consola
        console_header = QHBoxLayout()
        console_title = QLabel("🖥 Salida de Consola en Vivo (itzg mc-server)")
        console_title.setStyleSheet("font-weight: 700; font-size: 14px; color: #38bdf8;")
        console_header.addWidget(console_title)

        console_header.addStretch()

        self.chk_autoscroll = QCheckBox("Auto-scroll")
        self.chk_autoscroll.setChecked(True)
        console_header.addWidget(self.chk_autoscroll)

        btn_clear = QPushButton("Limpiar Vista")
        btn_clear.setStyleSheet("font-size: 12px; padding: 4px 12px; min-height: 20px;")
        btn_clear.clicked.connect(self._clear_console)
        console_header.addWidget(btn_clear)

        console_layout.addLayout(console_header)

        # Área de texto de la consola
        self.console_output = QPlainTextEdit()
        self.console_output.setObjectName("ConsoleOutput")
        self.console_output.setReadOnly(True)
        self.console_output.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
        self.console_output.appendPlainText(
            "[MC Server-Deck] Sistema iniciado. Monitoreando registros de mc-server...\n"
        )
        console_layout.addWidget(self.console_output, 1)

        # Barra de envío de comando RCON
        cmd_layout = QHBoxLayout()
        cmd_layout.setSpacing(10)

        self.cmd_input = QLineEdit()
        self.cmd_input.setPlaceholderText(
            "Escribe un comando de Minecraft (ej: list, time set day, weather clear, say ¡Hola!)..."
        )
        self.cmd_input.returnPressed.connect(self._on_send_command)
        cmd_layout.addWidget(self.cmd_input, 1)

        # Botón para abrir el teclado táctil oficial de Steam Deck
        self.btn_keyboard = QPushButton("⌨️ Teclado")
        self.btn_keyboard.setStyleSheet(
            "background-color: #1e293b; color: #94a3b8; font-weight: 600; padding: 10px 14px;"
        )
        self.btn_keyboard.setToolTip("Abre el teclado virtual en pantalla de Steam Deck (o pulsa STEAM + X)")
        self.btn_keyboard.clicked.connect(self._open_virtual_keyboard)
        cmd_layout.addWidget(self.btn_keyboard)

        self.btn_send_cmd = QPushButton("Enviar Comando ↵")
        self.btn_send_cmd.setStyleSheet(
            "background-color: #0284c7; color: white; font-weight: 700; padding: 10px 18px;"
        )
        self.btn_send_cmd.clicked.connect(self._on_send_command)
        cmd_layout.addWidget(self.btn_send_cmd)

        console_layout.addLayout(cmd_layout)

        # ---------------------------------------------------------------------
        # 4. BOTONES RÁPIDOS DE CONSOLA
        # ---------------------------------------------------------------------
        quick_btns_layout = QHBoxLayout()
        quick_btns_layout.setSpacing(10)

        btn_op = QPushButton("👑 Hacer OP")
        btn_op.setToolTip("Otorga permisos de operador a un jugador con 'op <nombre>'")
        btn_op.clicked.connect(self._quick_op)

        btn_wl_java = QPushButton("📋 Whitelist Add (Java)")
        btn_wl_java.setToolTip("Añade un jugador de Java a la lista blanca")
        btn_wl_java.clicked.connect(self._quick_whitelist_java)

        btn_wl_bedrock = QPushButton("🎮 Bedrock Whitelist (Floodgate)")
        btn_wl_bedrock.setToolTip("Añade un jugador de Bedrock con 'fwhitelist add <Gamertag>'")
        btn_wl_bedrock.clicked.connect(self._quick_whitelist_bedrock)

        btn_save = QPushButton("💾 Guardar Mundo")
        btn_save.setToolTip("Fuerza el guardado de los datos del mundo en disco con 'save-all'")
        btn_save.clicked.connect(self._quick_save_all)

        btn_list = QPushButton("👥 Ver Jugadores")
        btn_list.setToolTip("Muestra los jugadores conectados en la consola con 'list'")
        btn_list.clicked.connect(lambda: self._dispatch_rcon("list"))

        btn_oled_quick = QPushButton("🌙 Modo OLED")
        btn_oled_quick.setStyleSheet(
            "background-color: #0f172a; color: #38bdf8; border: 1px solid #0284c7; font-weight: 700;"
        )
        btn_oled_quick.setToolTip("Activa el salvapantallas anti-quemado OLED con el icono rebotante")
        btn_oled_quick.clicked.connect(self._trigger_oled_mode)

        quick_btns_layout.addWidget(btn_op)
        quick_btns_layout.addWidget(btn_wl_java)
        quick_btns_layout.addWidget(btn_wl_bedrock)
        quick_btns_layout.addWidget(btn_save)
        quick_btns_layout.addWidget(btn_list)
        quick_btns_layout.addWidget(btn_oled_quick)

        console_layout.addLayout(quick_btns_layout)

        main_layout.addWidget(console_card, 1)

    def _create_status_pill(self, initial_text: str) -> QLabel:
        """Crea una etiqueta con estilo de píldora de estado."""
        pill = QLabel(initial_text)
        pill.setObjectName("StatusUnknown")
        pill.setAlignment(Qt.AlignmentFlag.AlignCenter)
        pill.setMinimumWidth(110)
        return pill

    # -------------------------------------------------------------------------
    # GESTIÓN DE LOGS Y CONSOLA
    # -------------------------------------------------------------------------

    def _start_log_stream(self):
        """Inicia el hilo de captura de logs."""
        if not self.log_thread:
            self.log_thread = LogStreamerThread("mc-server", self)
            self.log_thread.log_received.connect(self._append_log_line)
            self.log_thread.start()

    def _append_log_line(self, line: str):
        """Inserta una línea de registro en la consola con auto-scroll."""
        self.console_output.appendPlainText(line)
        if self.chk_autoscroll.isChecked():
            sb = self.console_output.verticalScrollBar()
            sb.setValue(sb.maximum())

    def _clear_console(self):
        self.console_output.clear()

    # -------------------------------------------------------------------------
    # TEMPORIZADOR Y ACTUALIZACIÓN DE ESTADOS
    # -------------------------------------------------------------------------

    def _start_status_timer(self):
        self.status_timer = QTimer(self)
        self.status_timer.setInterval(3000)  # Cada 3 segundos
        self.status_timer.timeout.connect(self._update_statuses)
        self.status_timer.start()
        self._update_statuses()

    def _update_statuses(self):
        """Actualiza los badges visuales en base a la inspección de Podman."""
        try:
            statuses = self.pm.get_all_statuses()

            # mc-pod
            pod_st = statuses.get("pod", "Not Created")
            if "Running" in pod_st:
                self._set_pill_status(self.pill_pod, "ACTIVO", "running")
            elif "Exited" in pod_st or "Stopped" in pod_st:
                self._set_pill_status(self.pill_pod, "DETENIDO", "stopped")
            elif "Degraded" in pod_st:
                self._set_pill_status(self.pill_pod, "DEGRADADO", "warning")
            else:
                self._set_pill_status(self.pill_pod, "NO CREADO", "unknown")

            # mc-server
            srv_st = statuses.get("server", "not found")
            if srv_st == "running":
                self._set_pill_status(self.pill_server, "ONLINE", "running")
            elif srv_st in ["exited", "stopped"]:
                self._set_pill_status(self.pill_server, "OFFLINE", "stopped")
            else:
                self._set_pill_status(self.pill_server, "NO EXISTE", "unknown")

            # mc-playit
            playit_st = statuses.get("playit", "not found")
            if playit_st == "running":
                self._set_pill_status(self.pill_playit, "CONECTADO", "running")
            elif playit_st in ["exited", "stopped"]:
                self._set_pill_status(self.pill_playit, "DETENIDO", "stopped")
            else:
                self._set_pill_status(self.pill_playit, "NO ACTIVO", "unknown")

            # mc-ssh
            ssh_st = statuses.get("ssh", "not found")
            if ssh_st == "running":
                self._set_pill_status(self.pill_ssh, "PUERTO 2222", "running")
            elif ssh_st in ["exited", "stopped"]:
                self._set_pill_status(self.pill_ssh, "DETENIDO", "stopped")
            else:
                self._set_pill_status(self.pill_ssh, "DESACTIVADO", "unknown")

        except Exception as e:
            print(f"[DashboardTab] Error actualizando estados: {e}")

    def _set_pill_status(self, pill: QLabel, text: str, state_type: str):
        pill.setText(text)
        if state_type == "running":
            pill.setObjectName("StatusRunning")
        elif state_type == "stopped":
            pill.setObjectName("StatusStopped")
        elif state_type == "warning":
            pill.setObjectName("StatusWarning")
        else:
            pill.setObjectName("StatusUnknown")

        # Refrescar estilo de Qt
        pill.style().unpolish(pill)
        pill.style().polish(pill)

    # -------------------------------------------------------------------------
    # ACCIONES RÁPIDAS (EJECUTADAS EN HILOS)
    # -------------------------------------------------------------------------

    def _run_async_action(self, action_name: str, target_fn, *args):
        """Ejecuta una acción en un hilo secundario para mantener la fluidez de la GUI."""
        worker = WorkerActionThread(action_name, target_fn, *args, parent=self)
        worker.finished_signal.connect(self._on_action_finished)
        self.active_workers.append(worker)
        worker.start()

    def _on_action_finished(self, success: bool, action_name: str, output: str):
        # Limpiar workers completados
        self.active_workers = [w for w in self.active_workers if not w.isFinished()]

        prefix = "✔" if success else "✖"
        self._append_log_line(f"\n[MC Server-Deck {action_name}] {prefix} {output}\n")
        self._update_statuses()

    def _on_start_server(self):
        self._append_log_line("[MC Server-Deck] Solicitando inicio del pod 'mc-pod'...")
        self._run_async_action("Iniciar Servidor", self.pm.start_pod)

    def _on_stop_server(self):
        dlg = ConfirmDialog(
            "Detener Servidor",
            "¿Deseas detener el servidor de Minecraft y todos sus servicios asociados?",
            confirm_text="Detener",
            is_danger=True,
            parent=self,
        )
        if dlg.exec():
            self._append_log_line("[MC Server-Deck] Deteniendo el pod 'mc-pod' de forma segura...")
            self._run_async_action("Detener Servidor", self.pm.stop_pod)

    def _on_restart_server(self):
        dlg = ConfirmDialog(
            "Reiniciar Servidor",
            "¿Deseas reiniciar todos los contenedores de Minecraft?",
            confirm_text="Reiniciar",
            is_danger=False,
            parent=self,
        )
        if dlg.exec():
            self._append_log_line("[MC Server-Deck] Reiniciando pod 'mc-pod'...")
            self._run_async_action("Reiniciar Servidor", self.pm.restart_pod)

    def _on_fix_permissions(self):
        self._append_log_line("[MC Server-Deck] Ejecutando corrección de permisos para Steam Deck rootless...")
        self._run_async_action("Corregir Permisos", self.pm.fix_permissions)

    # -------------------------------------------------------------------------
    # RCON COMANDOS
    # -------------------------------------------------------------------------

    def _on_send_command(self):
        cmd = self.cmd_input.text().strip()
        if not cmd:
            return
        self.cmd_input.clear()
        self._dispatch_rcon(cmd)

    def _dispatch_rcon(self, command: str):
        self._append_log_line(f"> {command}")
        self._run_async_action(f"RCON ({command})", self.pm.send_rcon_command, command)

    def _quick_op(self):
        dlg = TouchInputDialog("Hacer Operador", "Introduce el nombre del jugador para hacer OP:", parent=self)
        if dlg.exec():
            player = dlg.get_text()
            if player:
                self._dispatch_rcon(f"op {player}")

    def _quick_whitelist_java(self):
        dlg = TouchInputDialog("Añadir a Whitelist (Java)", "Nombre de usuario de Minecraft Java:", parent=self)
        if dlg.exec():
            player = dlg.get_text()
            if player:
                self._dispatch_rcon(f"whitelist add {player}")

    def _quick_whitelist_bedrock(self):
        dlg = TouchInputDialog(
            "Añadir a Whitelist (Bedrock)",
            "Gamertag del jugador de Bedrock (Xbox / Consola / Móvil):",
            parent=self,
        )
        if dlg.exec():
            player = dlg.get_text()
            if player:
                self._dispatch_rcon(f"fwhitelist add {player}")

    def _open_virtual_keyboard(self):
        """Abre el teclado virtual de Steam en pantalla y enfoca el campo de comando."""
        self.cmd_input.setFocus()
        SteamIntegrator.open_steam_virtual_keyboard()

    def _trigger_oled_mode(self):
        """Dispara el modo salvapantallas OLED desde el botón de la consola."""
        main_win = self.window()
        if hasattr(main_win, "start_screensaver"):
            main_win.start_screensaver()

    def _quick_save_all(self):
        self._dispatch_rcon("save-all")

    def closeEvent(self, event):
        """Detiene de forma limpia los hilos al cerrar la ventana."""
        if self.log_thread:
            self.log_thread.stop()
        super().closeEvent(event)
