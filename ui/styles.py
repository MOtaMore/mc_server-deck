"""
MC Server-Deck - SteamOS Theme & Stylesheet
Diseño adaptado a Steam Deck (1280x800) con estética oscura moderna,
contrastes de alta visibilidad, elementos táctiles grandes y acentos SteamOS.
"""

# Paleta de colores SteamOS
COLOR_BG_DARK = "#0b1016"
COLOR_BG_SECONDARY = "#131b26"
COLOR_CARD_BG = "#192433"
COLOR_CARD_BORDER = "#253549"
COLOR_CARD_HOVER = "#1f2c3d"

COLOR_ACCENT_BLUE = "#1a9fff"
COLOR_ACCENT_BLUE_HOVER = "#38b6ff"
COLOR_ACCENT_BLUE_PRESSED = "#0e7cc9"

COLOR_GREEN = "#10b981"
COLOR_GREEN_HOVER = "#34d399"
COLOR_GREEN_PRESSED = "#059669"

COLOR_RED = "#ef4444"
COLOR_RED_HOVER = "#f87171"
COLOR_RED_PRESSED = "#dc2626"

COLOR_AMBER = "#f59e0b"
COLOR_AMBER_HOVER = "#fbbf24"
COLOR_AMBER_PRESSED = "#d97706"

COLOR_PURPLE = "#8b5cf6"
COLOR_PURPLE_HOVER = "#a78bfa"

COLOR_TEXT_PRIMARY = "#f8fafc"
COLOR_TEXT_SECONDARY = "#94a3b8"
COLOR_TEXT_MUTED = "#64748b"

COLOR_CONSOLE_BG = "#070b0f"
COLOR_CONSOLE_TEXT = "#e2e8f0"


STEAM_DECK_QSS = f"""
/* ================= GLOBAL ================= */
QWidget {{
    background-color: {COLOR_BG_DARK};
    color: {COLOR_TEXT_PRIMARY};
    font-family: 'Segoe UI', 'Ubuntu', 'Noto Sans', 'DejaVu Sans', sans-serif;
    font-size: 14px;
}}

QMainWindow {{
    background-color: {COLOR_BG_DARK};
}}

/* ================= TAB WIDGET ================= */
QTabWidget::pane {{
    border: 1px solid {COLOR_CARD_BORDER};
    border-radius: 12px;
    background-color: {COLOR_BG_SECONDARY};
    padding: 6px;
    margin-top: -1px;
}}

QTabBar::tab {{
    background-color: {COLOR_BG_DARK};
    color: {COLOR_TEXT_SECONDARY};
    font-weight: 700;
    font-size: 15px;
    padding: 12px 28px;
    margin-right: 6px;
    margin-bottom: 2px;
    border-top-left-radius: 10px;
    border-top-right-radius: 10px;
    border: 1px solid {COLOR_CARD_BORDER};
    border-bottom: none;
    min-height: 28px;
}}

QTabBar::tab:selected {{
    background-color: {COLOR_BG_SECONDARY};
    color: {COLOR_ACCENT_BLUE};
    border-top: 3px solid {COLOR_ACCENT_BLUE};
    border-left: 1px solid {COLOR_CARD_BORDER};
    border-right: 1px solid {COLOR_CARD_BORDER};
}}

QTabBar::tab:hover:!selected {{
    background-color: {COLOR_CARD_BG};
    color: {COLOR_TEXT_PRIMARY};
}}

/* ================= CARDS & FRAMES ================= */
QFrame#CardFrame {{
    background-color: {COLOR_CARD_BG};
    border: 1px solid {COLOR_CARD_BORDER};
    border-radius: 12px;
    padding: 14px;
}}

QFrame#HeaderFrame {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #121d2c, stop:1 #1a273b);
    border: 1px solid {COLOR_CARD_BORDER};
    border-radius: 12px;
    padding: 10px 16px;
}}

/* ================= BOTONES GENERALES ================= */
QPushButton {{
    background-color: #223145;
    color: {COLOR_TEXT_PRIMARY};
    border: 1px solid #334760;
    border-radius: 9px;
    font-size: 14px;
    font-weight: 600;
    padding: 10px 16px;
    min-height: 26px;
}}

QPushButton:hover {{
    background-color: #2b3e56;
    border-color: {COLOR_ACCENT_BLUE};
}}

QPushButton:pressed {{
    background-color: #172332;
}}

QPushButton:disabled {{
    background-color: #131a22;
    color: {COLOR_TEXT_MUTED};
    border-color: #1a2430;
}}

/* Botones de acción principales (Touch targets grandes) */
QPushButton#BtnStart {{
    background-color: #065f46;
    color: #ecfdf5;
    border: 1px solid {COLOR_GREEN};
    font-size: 15px;
    font-weight: 700;
    border-radius: 10px;
    padding: 12px 20px;
}}

QPushButton#BtnStart:hover {{
    background-color: {COLOR_GREEN};
    color: #022c22;
}}

QPushButton#BtnStart:pressed {{
    background-color: {COLOR_GREEN_PRESSED};
    color: #ffffff;
}}

QPushButton#BtnStop {{
    background-color: #7f1d1d;
    color: #fef2f2;
    border: 1px solid {COLOR_RED};
    font-size: 15px;
    font-weight: 700;
    border-radius: 10px;
    padding: 12px 20px;
}}

QPushButton#BtnStop:hover {{
    background-color: {COLOR_RED};
    color: #450a0a;
}}

QPushButton#BtnStop:pressed {{
    background-color: {COLOR_RED_PRESSED};
    color: #ffffff;
}}

QPushButton#BtnRestart {{
    background-color: #78350f;
    color: #fffbeb;
    border: 1px solid {COLOR_AMBER};
    font-size: 15px;
    font-weight: 700;
    border-radius: 10px;
    padding: 12px 20px;
}}

QPushButton#BtnRestart:hover {{
    background-color: {COLOR_AMBER};
    color: #451a03;
}}

QPushButton#BtnRestart:pressed {{
    background-color: {COLOR_AMBER_PRESSED};
    color: #ffffff;
}}

QPushButton#BtnFix {{
    background-color: #1e3a8a;
    color: #eff6ff;
    border: 1px solid {COLOR_ACCENT_BLUE};
    font-size: 14px;
    font-weight: 600;
    border-radius: 10px;
    padding: 12px 18px;
}}

QPushButton#BtnFix:hover {{
    background-color: {COLOR_ACCENT_BLUE};
    color: #0f172a;
}}

QPushButton#BtnFix:pressed {{
    background-color: {COLOR_ACCENT_BLUE_PRESSED};
    color: #ffffff;
}}

QPushButton#BtnDeploy {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #0284c7, stop:1 #059669);
    color: #ffffff;
    border: 1px solid #38bdf8;
    font-size: 17px;
    font-weight: 800;
    border-radius: 12px;
    padding: 16px 30px;
    min-height: 32px;
}}

QPushButton#BtnDeploy:hover {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #0ea5e9, stop:1 #10b981);
    border-color: #7dd3fc;
}}

QPushButton#BtnDeploy:pressed {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #0369a1, stop:1 #047857);
}}

/* ================= INPUTS & CONTROLES ================= */
QLineEdit {{
    background-color: #0e1520;
    color: {COLOR_TEXT_PRIMARY};
    border: 1px solid #2a3d54;
    border-radius: 8px;
    padding: 10px 14px;
    font-size: 14px;
    min-height: 24px;
}}

QLineEdit:focus {{
    border: 2px solid {COLOR_ACCENT_BLUE};
    background-color: #121b28;
}}

QComboBox {{
    background-color: #172332;
    color: {COLOR_TEXT_PRIMARY};
    border: 1px solid #2b3e55;
    border-radius: 8px;
    padding: 8px 14px;
    font-size: 14px;
    font-weight: 600;
    min-height: 28px;
}}

QComboBox:hover {{
    border-color: {COLOR_ACCENT_BLUE};
}}

QComboBox::drop-down {{
    border: none;
    width: 32px;
}}

QComboBox QAbstractItemView {{
    background-color: #121a24;
    color: {COLOR_TEXT_PRIMARY};
    border: 1px solid {COLOR_CARD_BORDER};
    selection-background-color: {COLOR_ACCENT_BLUE};
    selection-color: #0b1016;
    padding: 4px;
}}

QSlider::groove:horizontal {{
    height: 12px;
    background: #0f1621;
    border-radius: 6px;
    border: 1px solid #223245;
}}

QSlider::sub-page:horizontal {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 {COLOR_ACCENT_BLUE}, stop:1 {COLOR_GREEN});
    border-radius: 6px;
}}

QSlider::handle:horizontal {{
    background: #ffffff;
    border: 2px solid {COLOR_ACCENT_BLUE};
    width: 28px;
    margin-top: -8px;
    margin-bottom: -8px;
    border-radius: 14px;
}}

QSlider::handle:horizontal:hover {{
    background: #dbeafe;
    border: 2px solid #60a5fa;
}}

QCheckBox {{
    font-size: 14px;
    font-weight: 600;
    spacing: 12px;
    color: {COLOR_TEXT_PRIMARY};
}}

QCheckBox::indicator {{
    width: 22px;
    height: 22px;
    border: 2px solid #3b506b;
    border-radius: 6px;
    background-color: #0f1722;
}}

QCheckBox::indicator:hover {{
    border-color: {COLOR_ACCENT_BLUE};
}}

QCheckBox::indicator:checked {{
    background-color: {COLOR_ACCENT_BLUE};
    border-color: {COLOR_ACCENT_BLUE};
    image: none;
}}

QRadioButton {{
    font-size: 14px;
    font-weight: 600;
    spacing: 10px;
    color: {COLOR_TEXT_PRIMARY};
}}

QRadioButton::indicator {{
    width: 22px;
    height: 22px;
    border: 2px solid #3b506b;
    border-radius: 11px;
    background-color: #0f1722;
}}

QRadioButton::indicator:checked {{
    background-color: {COLOR_ACCENT_BLUE};
    border: 5px solid #0f1722;
}}

/* ================= CONSOLA TERMINAL ================= */
QPlainTextEdit#ConsoleOutput {{
    background-color: {COLOR_CONSOLE_BG};
    color: {COLOR_CONSOLE_TEXT};
    border: 1px solid #1a2533;
    border-radius: 10px;
    font-family: 'JetBrains Mono', 'Consolas', 'Courier New', monospace;
    font-size: 13px;
    padding: 10px;
    line-height: 1.4;
}}

/* ================= SCROLLBARS TÁCTILES ================= */
QScrollBar:vertical {{
    border: none;
    background: #0d141e;
    width: 14px;
    margin: 0px;
    border-radius: 7px;
}}

QScrollBar::handle:vertical {{
    background: #27374b;
    min-height: 30px;
    border-radius: 7px;
}}

QScrollBar::handle:vertical:hover {{
    background: {COLOR_ACCENT_BLUE};
}}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0px;
}}

QScrollArea {{
    border: none;
    background-color: transparent;
}}

QScrollArea > QWidget > QWidget {{
    background-color: transparent;
}}

/* ================= DIALOGS & PROGRESS ================= */
QDialog {{
    background-color: {COLOR_BG_SECONDARY};
    border: 2px solid {COLOR_CARD_BORDER};
    border-radius: 14px;
}}

QProgressBar {{
    border: 1px solid #2a3d54;
    border-radius: 8px;
    background-color: #0d141e;
    text-align: center;
    color: #ffffff;
    font-weight: 700;
    height: 22px;
}}

QProgressBar::chunk {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 {COLOR_ACCENT_BLUE}, stop:1 {COLOR_GREEN});
    border-radius: 7px;
}}

/* ================= STATUS PILLS ================= */
QLabel#StatusRunning {{
    background-color: #064e3b;
    color: #34d399;
    border: 1px solid #059669;
    border-radius: 8px;
    padding: 4px 10px;
    font-weight: 700;
    font-size: 12px;
}}

QLabel#StatusStopped {{
    background-color: #450a0a;
    color: #f87171;
    border: 1px solid #b91c1c;
    border-radius: 8px;
    padding: 4px 10px;
    font-weight: 700;
    font-size: 12px;
}}

QLabel#StatusUnknown {{
    background-color: #1e293b;
    color: #94a3b8;
    border: 1px solid #334155;
    border-radius: 8px;
    padding: 4px 10px;
    font-weight: 700;
    font-size: 12px;
}}

QLabel#StatusWarning {{
    background-color: #451a03;
    color: #fbbf24;
    border: 1px solid #d97706;
    border-radius: 8px;
    padding: 4px 10px;
    font-weight: 700;
    font-size: 12px;
}}
"""
