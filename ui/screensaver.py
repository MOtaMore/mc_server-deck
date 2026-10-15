"""
MC Server-Deck - Protector de Pantalla OLED / Monitor de Tubo (CRT Bouncing Icon)
Protege las pantallas OLED de la Steam Deck contra quemados (burn-in),
manteniendo la consola y el servidor activos con fondo 100% negro puro (píxeles apagados).
"""

import math
import random
from pathlib import Path
from typing import Optional

from PyQt6.QtCore import QEvent, QObject, QPointF, QRectF, QTimer, Qt, pyqtSignal
from PyQt6.QtGui import (
    QBrush,
    QColor,
    QCursor,
    QFont,
    QImage,
    QMouseEvent,
    QPainter,
    QPixmap,
)
from PyQt6.QtWidgets import QApplication, QWidget

from podman_manager import PodmanManager


class OledScreensaverWidget(QWidget):
    """
    Widget de salvapantallas de pantalla completa con rebote estilo 'DVD Logo / Monitor CRT'.
    Fondo negro puro (#000000) para apagar los píxeles en la pantalla OLED de la Steam Deck.
    """

    dismissed_signal = pyqtSignal()

    # Colores neón retro para variar tras cada rebote
    GLOW_COLORS = [
        QColor("#38bdf8"),  # Cyan Steam Deck
        QColor("#34d399"),  # Verde esmeralda
        QColor("#f472b6"),  # Rosa neón
        QColor("#fbbf24"),  # Ámbar
        QColor("#a78bfa"),  # Púrpura Geyser
        QColor("#60a5fa"),  # Azul cielo
        QColor("#fb7185"),  # Carmesí
    ]

    def __init__(self, podman_mgr: PodmanManager, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.pm = podman_mgr

        # Ventana completa sin bordes y encima de todo
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, False)
        self.setAttribute(Qt.WidgetAttribute.WA_OpaquePaintEvent, True)
        self.setAttribute(Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.setMouseTracking(True)
        self.setCursor(Qt.CursorShape.BlankCursor)  # Ocultar cursor en modo salvapantallas

        # Cargar icono
        base_dir = Path(__file__).resolve().parent.parent
        icon_path = base_dir / "assets" / "icon.png"
        self.icon_size = 130  # Tamaño del icono rebotante
        if icon_path.exists():
            original_pix = QPixmap(str(icon_path))
            self.icon_pixmap = original_pix.scaled(
                self.icon_size,
                self.icon_size,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
        else:
            self.icon_pixmap = QPixmap(self.icon_size, self.icon_size)
            self.icon_pixmap.fill(QColor("#38bdf8"))

        # Física del rebote
        self.pos_x = 100.0
        self.pos_y = 100.0
        # Velocidad en píxeles por frame (aproximadamente a 60 FPS)
        self.vx = 2.8 * (1 if random.random() > 0.5 else -1)
        self.vy = 2.4 * (1 if random.random() > 0.5 else -1)
        self.glow_color = random.choice(self.GLOW_COLORS)
        self.bounce_count = 0

        # Posición flotante del texto de estado (cambia lentamente para evitar estática)
        self.hud_offset_y = 0.0
        self.hud_drift_dir = 1
        self.last_status_text = "MC Server-Deck | Servidor Activo"

        # Detección de movimiento del ratón/touch para salir
        self.last_mouse_pos = QCursor.pos()
        self.ready_to_dismiss = False

        # Timer de animación (60 FPS ~ 16ms)
        self.anim_timer = QTimer(self)
        self.anim_timer.setInterval(16)
        self.anim_timer.timeout.connect(self._update_physics)

        # Timer de estado del servidor cada 5 segundos
        self.status_timer = QTimer(self)
        self.status_timer.setInterval(5000)
        self.status_timer.timeout.connect(self._refresh_status)

        # Evitar cierre accidental al abrirse inmediatamente
        QTimer.singleShot(400, self._enable_dismiss)

    def _enable_dismiss(self):
        self.ready_to_dismiss = True
        self.last_mouse_pos = QCursor.pos()

    def start(self):
        """Muestra el salvapantallas a pantalla completa e inicia la animación."""
        self.showFullScreen()
        self.raise_()
        self.activateWindow()
        self.setFocus()
        self._refresh_status()
        self.anim_timer.start()
        self.status_timer.start()

    def stop(self):
        """Detiene el salvapantallas."""
        self.anim_timer.stop()
        self.status_timer.stop()
        self.hide()
        self.dismissed_signal.emit()

    def _refresh_status(self):
        """Consulta el estado del pod y mc-server para el texto flotante."""
        try:
            statuses = self.pm.get_all_statuses()
            srv_st = statuses.get("server", "unknown").upper()
            pod_st = statuses.get("pod", "unknown").upper()
            self.last_status_text = (
                f"MC Server-Deck  •  mc-server: {srv_st}  •  mc-pod: {pod_st}  •  (Toca para despertar)"
            )
        except Exception:
            self.last_status_text = "MC Server-Deck  •  Servidor en Ejecución  •  (Toca para despertar)"

    def _update_physics(self):
        """Actualiza la posición del icono y rebota contra los límites de la pantalla."""
        screen_w = self.width()
        screen_h = self.height()

        self.pos_x += self.vx
        self.pos_y += self.vy

        bounced = False

        # Rebote horizontal
        if self.pos_x <= 0:
            self.pos_x = 0
            self.vx = abs(self.vx)
            bounced = True
        elif self.pos_x + self.icon_size >= screen_w:
            self.pos_x = screen_w - self.icon_size
            self.vx = -abs(self.vx)
            bounced = True

        # Rebote vertical
        if self.pos_y <= 0:
            self.pos_y = 0
            self.vy = abs(self.vy)
            bounced = True
        elif self.pos_y + self.icon_size >= screen_h:
            self.pos_y = screen_h - self.icon_size
            self.vy = -abs(self.vy)
            bounced = True

        if bounced:
            self.bounce_count += 1
            # Cambiar color de aura neón
            available_colors = [c for c in self.GLOW_COLORS if c != self.glow_color]
            self.glow_color = random.choice(available_colors)

        # Drift lento del HUD para que no esté nunca en el mismo pixel (Anti burn-in OLED)
        self.hud_offset_y += 0.2 * self.hud_drift_dir
        if abs(self.hud_offset_y) > 20:
            self.hud_drift_dir *= -1

        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)

        # 1. Fondo NEGRO PUERO (#000000): En OLED los píxeles negros están 100% apagados
        painter.fillRect(self.rect(), QColor("#000000"))

        # 2. Aura neón alrededor del icono rebotante
        glow_radius = 16
        glow_rect = QRectF(
            self.pos_x - glow_radius,
            self.pos_y - glow_radius,
            self.icon_size + glow_radius * 2,
            self.icon_size + glow_radius * 2,
        )
        glow_color_trans = QColor(self.glow_color)
        glow_color_trans.setAlpha(40)
        painter.setBrush(QBrush(glow_color_trans))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(glow_rect, 24, 24)

        # 3. Dibujar el icono
        painter.drawPixmap(int(self.pos_x), int(self.pos_y), self.icon_pixmap)

        # 4. Texto informativo inferior atenuado (drift dinámico)
        painter.setPen(QColor(148, 163, 184, 160))  # Slate semitransparente
        font = QFont("Segoe UI", 12)
        font.setBold(True)
        painter.setFont(font)

        hud_y = int(self.height() - 40 + self.hud_offset_y)
        painter.drawText(
            0,
            hud_y,
            self.width(),
            30,
            Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter,
            self.last_status_text,
        )

    # -------------------------------------------------------------------------
    # GESTIÓN DE EVENTOS PARA DESPERTAR (Tocar, mover ratón, pulsar botón)
    # -------------------------------------------------------------------------

    def keyPressEvent(self, event):
        self.stop()

    def mousePressEvent(self, event: QMouseEvent):
        self.stop()

    def mouseMoveEvent(self, event: QMouseEvent):
        if not self.ready_to_dismiss:
            return
        curr_pos = event.globalPosition().toPoint()
        # Requerir un movimiento de al menos 10 píxeles para ignorar vibraciones
        dx = abs(curr_pos.x() - self.last_mouse_pos.x())
        dy = abs(curr_pos.y() - self.last_mouse_pos.y())
        if dx > 10 or dy > 10:
            self.stop()


class InactivityManager(QObject):
    """
    Monitor global de inactividad que dispara automáticamente el salvapantallas
    OLED tras un periodo determinado sin interacción del usuario.
    """

    inactivity_timeout_signal = pyqtSignal()

    def __init__(self, timeout_minutes: int = 5, parent: Optional[QObject] = None):
        super().__init__(parent)
        self.timeout_ms = timeout_minutes * 60 * 1000
        self.is_enabled = True

        self.timer = QTimer(self)
        self.timer.setInterval(self.timeout_ms)
        self.timer.timeout.connect(self._on_timeout)

    def set_enabled(self, enabled: bool):
        self.is_enabled = enabled
        if enabled:
            self.reset_timer()
        else:
            self.timer.stop()

    def set_timeout_minutes(self, minutes: int):
        self.timeout_ms = minutes * 60 * 1000
        self.timer.setInterval(self.timeout_ms)
        if self.is_enabled:
            self.reset_timer()

    def reset_timer(self):
        if self.is_enabled:
            self.timer.start()

    def _on_timeout(self):
        if self.is_enabled:
            self.inactivity_timeout_signal.emit()

    def eventFilter(self, obj, event):
        """Filtro de eventos global para detectar cualquier interacción del usuario."""
        if event.type() in (
            QEvent.Type.MouseMove,
            QEvent.Type.MouseButtonPress,
            QEvent.Type.KeyPress,
            QEvent.Type.TouchBegin,
            QEvent.Type.Wheel,
        ):
            self.reset_timer()
        return super().eventFilter(obj, event)
