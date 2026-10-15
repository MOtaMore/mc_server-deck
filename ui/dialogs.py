"""
MC Server-Deck - Diálogos Táctiles y Modales
Componentes emergentes diseñados para pantallas táctiles de 1280x800.
"""

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QProgressBar,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
)


class TouchInputDialog(QDialog):
    """Diálogo emergente táctil para ingresar nombres de jugadores o comandos."""

    def __init__(self, title: str, prompt: str, default_val: str = "", parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setModal(True)
        self.setMinimumWidth(480)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        # Título / Etiqueta de instrucción
        title_label = QLabel(prompt)
        title_label.setStyleSheet("font-size: 16px; font-weight: 700; color: #f8fafc;")
        title_label.setWordWrap(True)
        layout.addWidget(title_label)

        # Campo de entrada
        self.line_edit = QLineEdit(default_val)
        self.line_edit.setPlaceholderText("Ejemplo: Steve, Alex...")
        self.line_edit.setStyleSheet(
            "font-size: 16px; padding: 12px; border-radius: 8px; min-height: 28px;"
        )
        self.line_edit.returnPressed.connect(self.accept)
        layout.addWidget(self.line_edit)

        # Botones de acción táctiles grandes
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(12)

        self.btn_cancel = QPushButton("Cancelar")
        self.btn_cancel.setStyleSheet(
            "background-color: #263345; color: #94a3b8; font-size: 15px; padding: 12px 20px;"
        )
        self.btn_cancel.clicked.connect(self.reject)
        btn_layout.addWidget(self.btn_cancel)

        self.btn_confirm = QPushButton("Confirmar")
        self.btn_confirm.setStyleSheet(
            "background-color: #0284c7; color: white; font-weight: 700; font-size: 15px; padding: 12px 24px;"
        )
        self.btn_confirm.clicked.connect(self.accept)
        btn_layout.addWidget(self.btn_confirm)

        layout.addLayout(btn_layout)
        self.line_edit.setFocus()

    def get_text(self) -> str:
        return self.line_edit.text().strip()


class ConfirmDialog(QDialog):
    """Diálogo de confirmación para acciones críticas (detener servidor, etc.)."""

    def __init__(
        self,
        title: str,
        message: str,
        confirm_text: str = "Confirmar",
        cancel_text: str = "Cancelar",
        is_danger: bool = False,
        parent=None,
    ):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setModal(True)
        self.setMinimumWidth(460)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(18)

        # Mensaje
        msg_label = QLabel(message)
        msg_label.setStyleSheet("font-size: 15px; line-height: 1.4; color: #f1f5f9;")
        msg_label.setWordWrap(True)
        layout.addWidget(msg_label)

        # Botones
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(14)

        btn_cancel = QPushButton(cancel_text)
        btn_cancel.setStyleSheet("background-color: #263345; font-size: 15px; padding: 12px 20px;")
        btn_cancel.clicked.connect(self.reject)
        btn_layout.addWidget(btn_cancel)

        btn_confirm = QPushButton(confirm_text)
        if is_danger:
            btn_confirm.setStyleSheet(
                "background-color: #dc2626; color: white; font-weight: 700; font-size: 15px; padding: 12px 24px;"
            )
        else:
            btn_confirm.setStyleSheet(
                "background-color: #0284c7; color: white; font-weight: 700; font-size: 15px; padding: 12px 24px;"
            )
        btn_confirm.clicked.connect(self.accept)
        btn_layout.addWidget(btn_confirm)

        layout.addLayout(btn_layout)


class DeployProgressDialog(QDialog):
    """Modal de progreso con visualización de registros durante el despliegue de Podman."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Desplegando Servidor de Minecraft...")
        self.setModal(True)
        self.setMinimumSize(600, 380)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(14)

        # Título descriptivo
        self.status_title = QLabel("Preparando contenedores en espacio de usuario...")
        self.status_title.setStyleSheet("font-size: 16px; font-weight: 700; color: #38bdf8;")
        layout.addWidget(self.status_title)

        # Barra de progreso
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 0)  # Modo indeterminado / pulsante
        layout.addWidget(self.progress_bar)

        # Consola de detalles en vivo
        self.log_view = QTextEdit()
        self.log_view.setReadOnly(True)
        self.log_view.setStyleSheet(
            "background-color: #070b0f; color: #a5b4fc; font-family: monospace; font-size: 12px; border-radius: 8px; border: 1px solid #1e293b;"
        )
        layout.addWidget(self.log_view)

        # Botón de cierre (inicia deshabilitado hasta terminar)
        self.btn_close = QPushButton("Finalizar")
        self.btn_close.setEnabled(False)
        self.btn_close.setStyleSheet(
            "background-color: #0284c7; color: white; font-weight: 700; font-size: 15px; padding: 12px 24px;"
        )
        self.btn_close.clicked.connect(self.accept)
        layout.addWidget(self.btn_close, alignment=Qt.AlignmentFlag.AlignRight)

    def append_log(self, text: str):
        """Agrega una línea al registro del diálogo."""
        self.log_view.append(text)
        sb = self.log_view.verticalScrollBar()
        sb.setValue(sb.maximum())

    def set_finished(self, success: bool, final_msg: str):
        """Marca el proceso como finalizado."""
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(100)
        if success:
            self.status_title.setText("✔ Despliegue completado con éxito")
            self.status_title.setStyleSheet("font-size: 16px; font-weight: 700; color: #34d399;")
        else:
            self.status_title.setText("✖ Ocurrió un error en el despliegue")
            self.status_title.setStyleSheet("font-size: 16px; font-weight: 700; color: #f87171;")

        self.append_log(f"\n[Resultado]: {final_msg}")
        self.btn_close.setEnabled(True)
        self.btn_close.setFocus()
