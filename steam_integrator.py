"""
MC Server-Deck - Steam Integrator
Permite agregar automáticamente la aplicación a la biblioteca de Steam (Gaming Mode)
manipulando shortcuts.vdf, generando portadas para la cuadrícula de Steam (Steam Grid)
e interactuando con el teclado virtual de la consola.
"""

import os
import shutil
import struct
import subprocess
import time
import zlib
from pathlib import Path
from typing import List, Optional, Tuple


class SteamIntegrator:
    """Maneja la integración con SteamOS y la biblioteca de Steam."""

    APP_NAME = "MC Server-Deck"

    def __init__(self, base_install_dir: Optional[Path] = None):
        self.home = Path.home()
        self.install_dir = base_install_dir or (self.home / ".local/share/mc-server-deck")
        self.run_script = self.install_dir / "run.sh"
        self.icon_path = self.install_dir / "assets" / "icon.png"

    def find_steam_userdata_dirs(self) -> List[Path]:
        """Localiza las carpetas de configuración de usuarios de Steam en SteamOS."""
        possible_roots = [
            self.home / ".steam" / "steam" / "userdata",
            self.home / ".local" / "share" / "Steam" / "userdata",
            self.home / ".steam" / "root" / "userdata",
        ]

        found = []
        for root in possible_roots:
            if root.exists() and root.is_dir():
                for user_dir in root.iterdir():
                    if user_dir.is_dir() and user_dir.name.isdigit() and user_dir.name != "0":
                        config_dir = user_dir / "config"
                        config_dir.mkdir(parents=True, exist_ok=True)
                        if config_dir not in found:
                            found.append(config_dir)
        return found

    @staticmethod
    def calculate_shortcut_appid(exe: str, app_name: str) -> int:
        """
        Calcula el AppID de 32 bits de Steam para un acceso directo no Steam:
        CRC32(exe + app_name) con el bit más significativo activado (0x80000000).
        """
        key = f"{exe}{app_name}".encode("utf-8")
        crc = zlib.crc32(key) & 0xFFFFFFFF
        return (crc | 0x80000000) & 0xFFFFFFFF

    def add_to_steam_library(self) -> Tuple[bool, str]:
        """
        Agrega o actualiza MC Server-Deck en shortcuts.vdf para todos los usuarios de Steam.
        Retorna (exitoso, mensaje_detallado).
        """
        config_dirs = self.find_steam_userdata_dirs()
        if not config_dirs:
            return (
                False,
                "No se encontró el directorio de usuario de Steam.\n"
                "Asegúrate de haber iniciado sesión en Steam al menos una vez.",
            )

        exe_str = f'"{self.run_script}"'
        start_dir_str = f'"{self.install_dir}"'
        icon_str = str(self.icon_path.resolve())

        updated_count = 0
        details = []

        for c_dir in config_dirs:
            shortcuts_file = c_dir / "shortcuts.vdf"
            grid_dir = c_dir / "grid"
            grid_dir.mkdir(parents=True, exist_ok=True)

            try:
                # 1. Leer o inicializar diccionario de accesos directos
                shortcuts = self._read_shortcuts_vdf(shortcuts_file)

                # 2. Comprobar si ya existe y actualizar o agregar
                found_idx = None
                for idx, sc in shortcuts.items():
                    if sc.get("AppName") == self.APP_NAME:
                        found_idx = idx
                        break

                new_entry = {
                    "AppName": self.APP_NAME,
                    "Exe": exe_str,
                    "StartDir": start_dir_str,
                    "icon": icon_str,
                    "ShortcutPath": "",
                    "LaunchOptions": "",
                    "IsHidden": 0,
                    "AllowDesktopConfig": 1,
                    "AllowOverlay": 1,
                    "OpenVR": 0,
                    "Devkit": 0,
                    "DevkitGameID": "",
                    "DevkitOverrideAppId": 0,
                    "LastPlayTime": 0,
                    "FlatpakAppID": "",
                    "tags": {0: "Servidor", 1: "Minecraft"},
                }

                if found_idx is not None:
                    shortcuts[found_idx] = new_entry
                    details.append(f"✔ Acceso directo actualizado en cuenta de Steam ({c_dir.parent.name})")
                else:
                    new_idx = str(len(shortcuts))
                    shortcuts[new_idx] = new_entry
                    details.append(f"✔ Agregado a la biblioteca de Steam ({c_dir.parent.name})")

                # 3. Guardar archivo binario VDF con copia de respaldo
                if shortcuts_file.exists():
                    shutil.copy2(shortcuts_file, shortcuts_file.with_suffix(".vdf.bak"))

                self._write_shortcuts_vdf(shortcuts_file, shortcuts)
                updated_count += 1

                # 4. Configurar carátulas Steam Grid (Banner, Poster, Icono)
                appid_32 = self.calculate_shortcut_appid(exe_str, self.APP_NAME)
                self._setup_grid_assets(grid_dir, appid_32)

            except Exception as e:
                details.append(f"✖ Error procesando {c_dir}: {e}")

        if updated_count > 0:
            return (
                True,
                "✔ ¡MC Server-Deck se añadió con éxito a tu biblioteca de Steam!\n\n"
                "Para verlo en Modo Juego:\n"
                "1. Reinicia Steam si está abierto.\n"
                "2. Regresa al Modo Juego (Gaming Mode).\n"
                "3. Aparecerá en tu biblioteca con carátula e icono personalizado.",
            )
        return False, "\n".join(details)

    def _setup_grid_assets(self, grid_dir: Path, appid: int):
        """Copia el icono como portada e imagen de biblioteca para Steam Gaming Mode."""
        if not self.icon_path.exists():
            return

        try:
            # En Steam Deck Gaming Mode, las imágenes de cuadrícula usan el AppID:
            # <appid>p.png (vertical poster)
            # <appid>.png (banner horizontal)
            # <appid>_hero.png (hero background)
            # <appid>_logo.png (logo transparente)
            targets = [
                grid_dir / f"{appid}p.png",
                grid_dir / f"{appid}.png",
                grid_dir / f"{appid}_hero.png",
                grid_dir / f"{appid}_logo.png",
                grid_dir / f"{appid}_icon.png",
            ]
            for t in targets:
                shutil.copy2(self.icon_path, t)
        except Exception as e:
            print(f"[SteamIntegrator] Error copiando grid assets: {e}")

    # -------------------------------------------------------------------------
    # PARSER BINARIO VDF DE STEAM SHORTCUTS
    # -------------------------------------------------------------------------

    def _read_shortcuts_vdf(self, filepath: Path) -> dict:
        """Lee y deserializa el formato binario shortcuts.vdf de Steam."""
        if not filepath.exists() or filepath.stat().st_size == 0:
            return {}

        data = filepath.read_bytes()
        pos = 0

        def read_cstring(p: int) -> Tuple[str, int]:
            end = data.find(b"\x00", p)
            if end == -1:
                return "", len(data)
            return data[p:end].decode("utf-8", errors="replace"), end + 1

        shortcuts = {}

        try:
            # Cabecera: \x00shortcuts\x00
            if data[0:1] != b"\x00":
                return {}
            name, pos = read_cstring(1)
            if name != "shortcuts":
                return {}

            while pos < len(data) and data[pos:pos+1] != b"\x08":
                t = data[pos:pos+1]
                pos += 1
                if t == b"\x00":
                    entry_idx, pos = read_cstring(pos)
                    entry_data = {}

                    while pos < len(data) and data[pos:pos+1] != b"\x08":
                        item_type = data[pos:pos+1]
                        pos += 1
                        key, pos = read_cstring(pos)

                        if item_type == b"\x01":  # String
                            val, pos = read_cstring(pos)
                            entry_data[key] = val
                        elif item_type == b"\x02":  # Int32
                            val = struct.unpack("<I", data[pos:pos+4])[0]
                            pos += 4
                            entry_data[key] = val
                        elif item_type == b"\x00":  # Tags / Sub-object
                            tags_dict = {}
                            while pos < len(data) and data[pos:pos+1] != b"\x08":
                                sub_type = data[pos:pos+1]
                                pos += 1
                                tag_idx, pos = read_cstring(pos)
                                if sub_type == b"\x01":
                                    tag_val, pos = read_cstring(pos)
                                    tags_dict[tag_idx] = tag_val
                            if pos < len(data) and data[pos:pos+1] == b"\x08":
                                pos += 1
                            entry_data[key] = tags_dict

                    if pos < len(data) and data[pos:pos+1] == b"\x08":
                        pos += 1
                    shortcuts[entry_idx] = entry_data

        except Exception as e:
            print(f"[SteamIntegrator] Aviso al parsear shortcuts.vdf: {e}")

        return shortcuts

    def _write_shortcuts_vdf(self, filepath: Path, shortcuts: dict):
        """Serializa y escribe shortcuts.vdf en el formato binario nativo de Steam."""
        buf = bytearray()

        def write_cstring(s: str):
            buf.extend(s.encode("utf-8"))
            buf.append(0)

        # Inicio de objeto raíz: \x00shortcuts\x00
        buf.append(0)
        write_cstring("shortcuts")

        for idx_key, entry in shortcuts.items():
            buf.append(0)
            write_cstring(str(idx_key))

            for k, v in entry.items():
                if isinstance(v, str):
                    buf.append(1)  # Tipo string
                    write_cstring(k)
                    write_cstring(v)
                elif isinstance(v, int):
                    buf.append(2)  # Tipo int32
                    write_cstring(k)
                    buf.extend(struct.pack("<I", v & 0xFFFFFFFF))
                elif isinstance(v, dict):
                    buf.append(0)  # Sub-objeto (tags)
                    write_cstring(k)
                    for sub_k, sub_v in v.items():
                        buf.append(1)
                        write_cstring(str(sub_k))
                        write_cstring(str(sub_v))
                    buf.append(8)  # Fin de sub-objeto

            buf.append(8)  # Fin de entrada de acceso directo

        buf.append(8)  # Fin de objeto shortcuts
        buf.append(8)  # Fin de archivo

        filepath.write_bytes(buf)

    # -------------------------------------------------------------------------
    # TECLADO VIRTUAL DE STEAM Y DETECCIÓN DE GAMING MODE
    # -------------------------------------------------------------------------

    @staticmethod
    def is_gaming_mode() -> bool:
        """Determina si la aplicación se está ejecutando en el Modo Juego de Steam Deck."""
        return (
            os.environ.get("GAMESCOPE_WAYLAND_DISPLAY") is not None
            or os.environ.get("STEAM_DECK") == "1"
        )

    @staticmethod
    def open_steam_virtual_keyboard():
        """Abre el teclado en pantalla oficial de Steam en la Steam Deck."""
        # 1. Probar mediante URL oficial de Steam
        try:
            subprocess.Popen(
                ["xdg-open", "steam://open/keyboard"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            return
        except Exception:
            pass

        # 2. Alternativa mediante llamada DBus en KDE Plasma / SteamOS
        try:
            subprocess.Popen(
                ["qdbus", "org.kde.kded5", "/modules/steamdeck", "org.kde.kded5.steamdeck.showKeyboard"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        except Exception:
            pass
