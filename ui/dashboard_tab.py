"""
MC Server-Deck - Pestaña 1: Panel de Control y Consola en Vivo
Panel principal con monitoreo en tiempo real, streaming de logs y consola RCON.
Soporte multilenguaje i18n (ES, EN, PT, FR).
"""

import shutil
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

from i18n import t
from podman_manager import PodmanManager
from steam_integrator import SteamIntegrator
from ui.dialogs import ConfirmDialog, DeployProgressDialog, TouchInputDialog


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
            if not shutil.which("podman"):
                for _ in range(30):
                    if not self.is_running:
                        break
                    self.msleep(100)
                continue
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

            for _ in range(20):
                if not self.is_running:
                    break
                self.msleep(100)

    def stop(self):
        self.is_running = False
        if self.process:
            try:
                self.process.terminate()
                self.process.kill()
            except Exception:
                pass
        self.quit()
        self.wait(1500)


class WorkerActionThread(QThread):
    """Hilo para ejecutar acciones de Podman en segundo plano sin congelar la GUI."""

    finished_signal = pyqtSignal(bool, str, str)

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


class RecreatePodWorker(QThread):
    """Hilo para la eliminación y recreación limpia del pod mc-pod."""

    progress_signal = pyqtSignal(str)
    finished_signal = pyqtSignal(bool, str)

    def __init__(self, podman_mgr: PodmanManager, parent=None):
        super().__init__(parent)
        self.pm = podman_mgr

    def run(self):
        try:
            success, msg = self.pm.recreate_pod(progress_callback=self.progress_signal.emit)
            self.finished_signal.emit(success, msg)
        except Exception as e:
            self.finished_signal.emit(False, str(e))


class DashboardTab(QWidget):
    """Pestaña del Panel de Control y Consola Interactiva con soporte i18n."""

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

        self.title_pod = QLabel(t("status_pod_title"))
        self.title_pod.setStyleSheet("font-weight: 700; color: #cbd5e1;")
        self.pill_pod = self._create_status_pill(t("status_checking"))

        self.title_server = QLabel(t("status_server_title"))
        self.title_server.setStyleSheet("font-weight: 700; color: #cbd5e1;")
        self.pill_server = self._create_status_pill(t("status_checking"))

        self.title_playit = QLabel(t("status_playit_title"))
        self.title_playit.setStyleSheet("font-weight: 700; color: #cbd5e1;")
        self.pill_playit = self._create_status_pill(t("status_checking"))

        self.title_ssh = QLabel(t("status_ssh_title"))
        self.title_ssh.setStyleSheet("font-weight: 700; color: #cbd5e1;")
        self.pill_ssh = self._create_status_pill(t("status_checking"))

        status_layout.addWidget(self.title_pod, 0, 0)
        status_layout.addWidget(self.pill_pod, 0, 1)

        status_layout.addWidget(self.title_server, 0, 2)
        status_layout.addWidget(self.pill_server, 0, 3)

        status_layout.addWidget(self.title_playit, 1, 0)
        status_layout.addWidget(self.pill_playit, 1, 1)

        status_layout.addWidget(self.title_ssh, 1, 2)
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

        self.btn_start = QPushButton(t("btn_start_server"))
        self.btn_start.setObjectName("BtnStart")
        self.btn_start.clicked.connect(self._on_start_server)

        self.btn_stop = QPushButton(t("btn_stop_server"))
        self.btn_stop.setObjectName("BtnStop")
        self.btn_stop.clicked.connect(self._on_stop_server)

        self.btn_restart = QPushButton(t("btn_restart_server"))
        self.btn_restart.setObjectName("BtnRestart")
        self.btn_restart.clicked.connect(self._on_restart_server)

        self.btn_recreate_pod = QPushButton(t("btn_recreate_pod"))
        self.btn_recreate_pod.setObjectName("BtnRecreate")
        self.btn_recreate_pod.setStyleSheet(
            "background-color: #334155; color: #f8fafc; font-weight: 700; padding: 10px 14px; min-height: 24px;"
        )
        self.btn_recreate_pod.setToolTip(t("btn_recreate_pod_tooltip"))
        self.btn_recreate_pod.clicked.connect(self._on_recreate_pod_clicked)

        self.btn_fix_perms = QPushButton(t("btn_fix_perms"))
        self.btn_fix_perms.setObjectName("BtnFix")
        self.btn_fix_perms.setToolTip(t("btn_fix_perms_tooltip"))
        self.btn_fix_perms.clicked.connect(self._on_fix_permissions)

        actions_layout.addWidget(self.btn_start, 1)
        actions_layout.addWidget(self.btn_stop, 1)
        actions_layout.addWidget(self.btn_restart, 1)
        actions_layout.addWidget(self.btn_recreate_pod, 1)
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

        console_header = QHBoxLayout()
        self.console_title = QLabel(t("console_title"))
        self.console_title.setStyleSheet("font-weight: 700; font-size: 14px; color: #38bdf8;")
        console_header.addWidget(self.console_title)

        console_header.addStretch()

        self.chk_autoscroll = QCheckBox(t("chk_autoscroll"))
        self.chk_autoscroll.setChecked(True)
        console_header.addWidget(self.chk_autoscroll)

        self.btn_clear = QPushButton(t("btn_clear_console"))
        self.btn_clear.setStyleSheet("font-size: 12px; padding: 4px 12px; min-height: 20px;")
        self.btn_clear.clicked.connect(self._clear_console)
        console_header.addWidget(self.btn_clear)

        console_layout.addLayout(console_header)

        # Área de texto de consola
        self.console_output = QPlainTextEdit()
        self.console_output.setObjectName("ConsoleOutput")
        self.console_output.setReadOnly(True)
        self.console_output.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
        self.console_output.appendPlainText(
            "[MC Server-Deck] Sistema iniciado. Monitoreando registros de mc-server...\n"
        )
        console_layout.addWidget(self.console_output, 1)

        # Barra de comandos
        cmd_layout = QHBoxLayout()
        cmd_layout.setSpacing(10)

        self.cmd_input = QLineEdit()
        self.cmd_input.setPlaceholderText(t("console_placeholder"))
        self.cmd_input.returnPressed.connect(self._on_send_command)
        cmd_layout.addWidget(self.cmd_input, 1)

        self.btn_keyboard = QPushButton(t("btn_keyboard"))
        self.btn_keyboard.setStyleSheet(
            "background-color: #1e293b; color: #94a3b8; font-weight: 600; padding: 10px 14px;"
        )
        self.btn_keyboard.setToolTip(t("btn_keyboard_tooltip"))
        self.btn_keyboard.clicked.connect(self._open_virtual_keyboard)
        cmd_layout.addWidget(self.btn_keyboard)

        self.btn_send_cmd = QPushButton(t("btn_send_cmd"))
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

        self.btn_op = QPushButton(t("btn_quick_op"))
        self.btn_op.setToolTip(t("btn_quick_op_tooltip"))
        self.btn_op.clicked.connect(self._quick_op)

        self.btn_wl_java = QPushButton(t("btn_quick_wl_java"))
        self.btn_wl_java.setToolTip(t("btn_quick_wl_java_tooltip"))
        self.btn_wl_java.clicked.connect(self._quick_whitelist_java)

        self.btn_wl_bedrock = QPushButton(t("btn_quick_wl_bedrock"))
        self.btn_wl_bedrock.setToolTip(t("btn_quick_wl_bedrock_tooltip"))
        self.btn_wl_bedrock.clicked.connect(self._quick_whitelist_bedrock)

        self.btn_save = QPushButton(t("btn_quick_save"))
        self.btn_save.setToolTip(t("btn_quick_save_tooltip"))
        self.btn_save.clicked.connect(self._quick_save_all)

        self.btn_list = QPushButton(t("btn_quick_list"))
        self.btn_list.setToolTip(t("btn_quick_list_tooltip"))
        self.btn_list.clicked.connect(lambda: self._dispatch_rcon("list"))

        self.btn_oled_quick = QPushButton(t("btn_oled_mode"))
        self.btn_oled_quick.setStyleSheet(
            "background-color: #0f172a; color: #38bdf8; border: 1px solid #0284c7; font-weight: 700;"
        )
        self.btn_oled_quick.setToolTip(t("btn_oled_tooltip"))
        self.btn_oled_quick.clicked.connect(self._trigger_oled_mode)

        quick_btns_layout.addWidget(self.btn_op)
        quick_btns_layout.addWidget(self.btn_wl_java)
        quick_btns_layout.addWidget(self.btn_wl_bedrock)
        quick_btns_layout.addWidget(self.btn_save)
        quick_btns_layout.addWidget(self.btn_list)
        quick_btns_layout.addWidget(self.btn_oled_quick)

        console_layout.addLayout(quick_btns_layout)

        main_layout.addWidget(console_card, 1)

    def retranslate_ui(self):
        """Actualiza todos los textos de la interfaz según el idioma actual."""
        self.title_pod.setText(t("status_pod_title"))
        self.title_server.setText(t("status_server_title"))
        self.title_playit.setText(t("status_playit_title"))
        self.title_ssh.setText(t("status_ssh_title"))

        self.btn_start.setText(t("btn_start_server"))
        self.btn_stop.setText(t("btn_stop_server"))
        self.btn_restart.setText(t("btn_restart_server"))
        self.btn_recreate_pod.setText(t("btn_recreate_pod"))
        self.btn_recreate_pod.setToolTip(t("btn_recreate_pod_tooltip"))
        self.btn_fix_perms.setText(t("btn_fix_perms"))
        self.btn_fix_perms.setToolTip(t("btn_fix_perms_tooltip"))

        self.console_title.setText(t("console_title"))
        self.chk_autoscroll.setText(t("chk_autoscroll"))
        self.btn_clear.setText(t("btn_clear_console"))
        self.cmd_input.setPlaceholderText(t("console_placeholder"))
        self.btn_keyboard.setText(t("btn_keyboard"))
        self.btn_keyboard.setToolTip(t("btn_keyboard_tooltip"))
        self.btn_send_cmd.setText(t("btn_send_cmd"))

        self.btn_op.setText(t("btn_quick_op"))
        self.btn_op.setToolTip(t("btn_quick_op_tooltip"))
        self.btn_wl_java.setText(t("btn_quick_wl_java"))
        self.btn_wl_java.setToolTip(t("btn_quick_wl_java_tooltip"))
        self.btn_wl_bedrock.setText(t("btn_quick_wl_bedrock"))
        self.btn_wl_bedrock.setToolTip(t("btn_quick_wl_bedrock_tooltip"))
        self.btn_save.setText(t("btn_quick_save"))
        self.btn_save.setToolTip(t("btn_quick_save_tooltip"))
        self.btn_list.setText(t("btn_quick_list"))
        self.btn_list.setToolTip(t("btn_quick_list_tooltip"))
        self.btn_oled_quick.setText(t("btn_oled_mode"))
        self.btn_oled_quick.setToolTip(t("btn_oled_tooltip"))

        self._update_statuses()

    def _create_status_pill(self, initial_text: str) -> QLabel:
        pill = QLabel(initial_text)
        pill.setObjectName("StatusUnknown")
        pill.setAlignment(Qt.AlignmentFlag.AlignCenter)
        pill.setMinimumWidth(110)
        return pill

    # -------------------------------------------------------------------------
    # GESTIÓN DE LOGS Y CONSOLA
    # -------------------------------------------------------------------------

    def _start_log_stream(self):
        if not self.log_thread:
            self.log_thread = LogStreamerThread("mc-server", self)
            self.log_thread.log_received.connect(self._append_log_line)
            self.log_thread.start()

    def _append_log_line(self, line: str):
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
        self.status_timer.setInterval(3000)
        self.status_timer.timeout.connect(self._update_statuses)
        self.status_timer.start()
        self._update_statuses()

    def _update_statuses(self):
        try:
            statuses = self.pm.get_all_statuses()

            # mc-pod
            pod_st = statuses.get("pod", "Not Created")
            if "Running" in pod_st:
                self._set_pill_status(self.pill_pod, t("st_active"), "running")
            elif "Exited" in pod_st or "Stopped" in pod_st:
                self._set_pill_status(self.pill_pod, t("st_stopped"), "stopped")
            elif "Degraded" in pod_st:
                self._set_pill_status(self.pill_pod, t("st_degraded"), "warning")
            else:
                self._set_pill_status(self.pill_pod, t("st_not_created"), "unknown")

            # mc-server
            srv_st = statuses.get("server", "not found")
            if srv_st == "running":
                self._set_pill_status(self.pill_server, t("st_online"), "running")
            elif srv_st in ["exited", "stopped"]:
                self._set_pill_status(self.pill_server, t("st_offline"), "stopped")
            else:
                self._set_pill_status(self.pill_server, t("st_not_created"), "unknown")

            # mc-playit
            playit_st = statuses.get("playit", "not found")
            if playit_st == "running":
                self._set_pill_status(self.pill_playit, t("st_connected"), "running")
            elif playit_st in ["exited", "stopped"]:
                self._set_pill_status(self.pill_playit, t("st_stopped"), "stopped")
            else:
                self._set_pill_status(self.pill_playit, t("st_inactive"), "unknown")

            # mc-ssh
            ssh_st = statuses.get("ssh", "not found")
            if ssh_st == "running":
                self._set_pill_status(self.pill_ssh, "PORT 2222", "running")
            elif ssh_st in ["exited", "stopped"]:
                self._set_pill_status(self.pill_ssh, t("st_stopped"), "stopped")
            else:
                self._set_pill_status(self.pill_ssh, t("st_disabled"), "unknown")

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

        pill.style().unpolish(pill)
        pill.style().polish(pill)

    # -------------------------------------------------------------------------
    # ACCIONES RÁPIDAS
    # -------------------------------------------------------------------------

    def _run_async_action(self, action_name: str, target_fn, *args):
        worker = WorkerActionThread(action_name, target_fn, *args, parent=self)
        worker.finished_signal.connect(self._on_action_finished)
        self.active_workers.append(worker)
        worker.start()

    def _on_action_finished(self, success: bool, action_name: str, output: str):
        self.active_workers = [w for w in self.active_workers if not w.isFinished()]
        prefix = "✔" if success else "✖"
        self._append_log_line(f"\n[MC Server-Deck {action_name}] {prefix} {output}\n")
        self._update_statuses()

        # Si falló al iniciar o reiniciar por conflicto o desincronización de pod:
        if not success and action_name in ["Iniciar Servidor", "Reiniciar Servidor"]:
            dlg = ConfirmDialog(
                t("dlg_pod_conflict_title"),
                f"{t('dlg_pod_conflict_msg')}\n\n(Detalle: {output})",
                confirm_text=t("dlg_pod_recreate_btn"),
                cancel_text=t("dlg_pod_do_nothing_btn"),
                is_danger=True,
                parent=self,
            )
            if dlg.exec():
                self._recreate_pod_flow()
            else:
                self._append_log_line("[MC Server-Deck] Acción cancelada por el usuario (No hacer nada).")

    def _on_start_server(self):
        # 1. Comprobar si mc-pod presenta un conflicto o estado inconsistente
        has_conflict, reason = self.pm.check_pod_conflict()
        if has_conflict:
            dlg = ConfirmDialog(
                t("dlg_pod_conflict_title"),
                f"{t('dlg_pod_conflict_msg')}\n\n({reason})",
                confirm_text=t("dlg_pod_recreate_btn"),
                cancel_text=t("dlg_pod_do_nothing_btn"),
                is_danger=True,
                parent=self,
            )
            if dlg.exec():
                self._recreate_pod_flow()
            else:
                self._append_log_line("[MC Server-Deck] Inicio cancelado: el usuario eligió no hacer nada.")
            return

        self._append_log_line("[MC Server-Deck] Solicitando inicio del pod 'mc-pod'...")
        self._run_async_action("Iniciar Servidor", self.pm.start_pod)

    def _on_recreate_pod_clicked(self):
        """Permite al usuario elegir si eliminar y recrear mc-pod desde cero o no hacer nada."""
        dlg = ConfirmDialog(
            t("dlg_pod_conflict_title"),
            t("dlg_pod_conflict_msg"),
            confirm_text=t("dlg_pod_recreate_btn"),
            cancel_text=t("dlg_pod_do_nothing_btn"),
            is_danger=True,
            parent=self,
        )
        if dlg.exec():
            self._recreate_pod_flow()
        else:
            self._append_log_line("[MC Server-Deck] Reparación cancelada: el usuario eligió no hacer nada.")

    def _recreate_pod_flow(self):
        """Orquesta la recreación limpia del pod mc-pod con barra de progreso táctil."""
        self._append_log_line("[MC Server-Deck] Iniciando recreación limpia de 'mc-pod'...")
        progress_dlg = DeployProgressDialog(parent=self)
        progress_dlg.status_title.setText(t("dlg_pod_recreate_btn"))
        progress_dlg.append_log("[MC Server-Deck] Recreando pod 'mc-pod' y limpiando puertos...")

        worker = RecreatePodWorker(self.pm, parent=self)
        worker.progress_signal.connect(progress_dlg.append_log)
        worker.progress_signal.connect(self._append_log_line)

        def on_done(success: bool, msg: str):
            progress_dlg.set_finished(success, msg)
            self._update_statuses()
            if success:
                self._append_log_line(f"\n✔ mc-pod recreado exitosamente: {msg}\n")
            else:
                self._append_log_line(f"\n✖ Error recreando mc-pod: {msg}\n")

        worker.finished_signal.connect(on_done)
        worker.start()
        progress_dlg.exec()

    def _on_stop_server(self):
        dlg = ConfirmDialog(
            t("dlg_stop_title"),
            t("dlg_stop_msg"),
            confirm_text=t("dlg_stop_btn"),
            is_danger=True,
            parent=self,
        )
        if dlg.exec():
            self._append_log_line("[MC Server-Deck] Deteniendo el pod 'mc-pod' de forma segura...")
            self._run_async_action("Detener Servidor", self.pm.stop_pod)

    def _on_restart_server(self):
        dlg = ConfirmDialog(
            t("dlg_restart_title"),
            t("dlg_restart_msg"),
            confirm_text=t("dlg_restart_btn"),
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
    # RCON COMANDOS Y ACCIONES
    # -------------------------------------------------------------------------

    def _open_virtual_keyboard(self):
        self.cmd_input.setFocus()
        SteamIntegrator.open_steam_virtual_keyboard()

    def _trigger_oled_mode(self):
        main_win = self.window()
        if hasattr(main_win, "start_screensaver"):
            main_win.start_screensaver()

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
        dlg = TouchInputDialog(t("dlg_op_title"), t("dlg_op_prompt"), parent=self)
        if dlg.exec():
            player = dlg.get_text()
            if player:
                self._dispatch_rcon(f"op {player}")

    def _quick_whitelist_java(self):
        dlg = TouchInputDialog(t("dlg_wl_java_title"), t("dlg_wl_java_prompt"), parent=self)
        if dlg.exec():
            player = dlg.get_text()
            if player:
                self._dispatch_rcon(f"whitelist add {player}")

    def _quick_whitelist_bedrock(self):
        dlg = TouchInputDialog(t("dlg_wl_bedrock_title"), t("dlg_wl_bedrock_prompt"), parent=self)
        if dlg.exec():
            player = dlg.get_text()
            if player:
                self._dispatch_rcon(f"fwhitelist add {player}")

    def _quick_save_all(self):
        self._dispatch_rcon("save-all")

    def closeEvent(self, event):
        if self.log_thread:
            self.log_thread.stop()
        super().closeEvent(event)
