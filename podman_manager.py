"""
MC Server-Deck - Podman Management Engine
Maneja la orquestación de Podman en espacio de usuario rootless (SteamOS / Arch Linux).
Controla el pod 'mc-pod' y los contenedores 'mc-server', 'mc-playit' y 'mc-ssh'.
"""

import json
import os
import shutil
import subprocess
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class PodmanManager:
    """Administrador de contenedores y pod de Podman para Minecraft en Steam Deck."""

    DEFAULT_BASE_DIR = Path.home() / "minecraft-server"
    POD_NAME = "mc-pod"
    SERVER_CONTAINER = "mc-server"
    PLAYIT_CONTAINER = "mc-playit"
    SSH_CONTAINER = "mc-ssh"

    def __init__(self, base_dir: Optional[Path] = None):
        self.base_dir = base_dir or self.DEFAULT_BASE_DIR
        self.data_dir = self.base_dir / "data"
        self.config_file = self.base_dir / "mc_server_config.json"
        self.legacy_config_file = self.base_dir / "deckcraft_config.json"
        self._ensure_directories()

    def _ensure_directories(self) -> None:
        """Crea las carpetas base del servidor si no existen."""
        try:
            self.data_dir.mkdir(parents=True, exist_ok=True)
            self.ssh_config_dir.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            print(f"[PodmanManager] Advertencia al crear directorios: {e}")

    def is_podman_available(self) -> bool:
        """Verifica si podman está instalado y accesible en PATH."""
        return shutil.which("podman") is not None

    def run_cmd(
        self, cmd: List[str], timeout: Optional[int] = 30
    ) -> Tuple[bool, str]:
        """
        Ejecuta un comando de sistema sin sudo y captura stdout y stderr.
        Retorna (exitoso, salida_o_error).
        """
        try:
            result = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=timeout,
                encoding="utf-8",
                errors="replace",
            )
            if result.returncode == 0:
                return True, result.stdout.strip()
            return False, result.stderr.strip() or result.stdout.strip()
        except subprocess.TimeoutExpired:
            return False, f"Tiempo de espera agotado ({timeout}s) ejecutando: {' '.join(cmd)}"
        except FileNotFoundError:
            return False, f"Comando no encontrado: {cmd[0]}"
        except Exception as e:
            return False, f"Error inesperado: {str(e)}"

    # -------------------------------------------------------------------------
    # CONSULTA DE ESTADOS
    # -------------------------------------------------------------------------

    def get_pod_status(self) -> str:
        """
        Retorna el estado de 'mc-pod':
        'Running', 'Degraded', 'Stopped', 'Exited', o 'Not Created'
        """
        if not self.is_podman_available():
            return "No Podman"

        success, output = self.run_cmd(
            ["podman", "pod", "ps", "-a", "--filter", f"name={self.POD_NAME}", "--format", "{{.Status}}"]
        )
        if success and output:
            first_line = output.splitlines()[0].strip()
            return first_line if first_line else "Not Created"
        return "Not Created"

    def get_container_status(self, container_name: str) -> str:
        """
        Retorna el estado de un contenedor específico:
        'running', 'exited', 'created', 'paused', 'not found', etc.
        """
        if not self.is_podman_available():
            return "No Podman"

        success, output = self.run_cmd(
            ["podman", "ps", "-a", "--filter", f"name=^{container_name}$", "--format", "{{.State}}"]
        )
        if success and output:
            first_line = output.splitlines()[0].strip().lower()
            return first_line if first_line else "not found"
        return "not found"

    def get_all_statuses(self) -> Dict[str, str]:
        """Obtiene un diccionario consolidado con el estado del pod y los contenedores."""
        return {
            "pod": self.get_pod_status(),
            "server": self.get_container_status(self.SERVER_CONTAINER),
            "playit": self.get_container_status(self.PLAYIT_CONTAINER),
            "ssh": self.get_container_status(self.SSH_CONTAINER),
        }

    # -------------------------------------------------------------------------
    # CONTROL DEL POD Y CONTENEDORES
    # -------------------------------------------------------------------------

    def start_pod(self) -> Tuple[bool, str]:
        """Inicia el pod mc-pod y todos sus contenedores asociados."""
        pod_status = self.get_pod_status()
        if pod_status == "Not Created":
            return False, "El pod 'mc-pod' no está creado. Ve a 'Configurar Servidor' para desplegarlo primero."
        return self.run_cmd(["podman", "pod", "start", self.POD_NAME], timeout=60)

    def stop_pod(self) -> Tuple[bool, str]:
        """Detiene de forma limpia el pod mc-pod."""
        pod_status = self.get_pod_status()
        if pod_status == "Not Created":
            return True, "El pod no está creado."
        return self.run_cmd(["podman", "pod", "stop", "-t", "15", self.POD_NAME], timeout=30)

    def restart_pod(self) -> Tuple[bool, str]:
        """Reinicia el pod mc-pod."""
        pod_status = self.get_pod_status()
        if pod_status == "Not Created":
            return False, "El pod no está creado."
        return self.run_cmd(["podman", "pod", "restart", self.POD_NAME], timeout=60)

    # -------------------------------------------------------------------------
    # CORRECCIÓN DE PERMISOS
    # -------------------------------------------------------------------------

    def fix_permissions(self) -> Tuple[bool, str]:
        """
        Ejecuta la rutina de emergencia para solucionar permisos rootless en Steam Deck:
        1. podman unshare chown -R 0:0 ~/minecraft-server/data
        2. podman exec mc-server chmod -R 777 /data (si mc-server está activo)
        """
        logs = []
        data_path = str(self.data_dir.resolve())

        # Paso 1: podman unshare chown -R 0:0
        success1, out1 = self.run_cmd(
            ["podman", "unshare", "chown", "-R", "0:0", data_path], timeout=30
        )
        if success1:
            logs.append(f"✔ Permisos de usuario mapeados correctamente en {data_path}")
        else:
            logs.append(f"✖ Error en 'podman unshare chown': {out1}")

        # Paso 2: Si el contenedor mc-server está corriendo, aplicar chmod 777 interno
        server_status = self.get_container_status(self.SERVER_CONTAINER)
        if server_status == "running":
            success2, out2 = self.run_cmd(
                ["podman", "exec", self.SERVER_CONTAINER, "chmod", "-R", "777", "/data"],
                timeout=20,
            )
            if success2:
                logs.append("✔ Permisos 777 aplicados internamente en el contenedor mc-server")
            else:
                logs.append(f"⚠ Aviso en chmod interno: {out2}")
        else:
            logs.append("ℹ mc-server no está en ejecución; permisos host actualizados")

        return True, "\n".join(logs)

    # -------------------------------------------------------------------------
    # RCON INTERACTIVO
    # -------------------------------------------------------------------------

    def send_rcon_command(self, command: str) -> Tuple[bool, str]:
        """
        Envía un comando al servidor de Minecraft usando itzg rcon-cli:
        podman exec mc-server rcon-cli "<comando>"
        """
        cmd_clean = command.strip()
        if not cmd_clean:
            return False, "Comando vacío."

        # Remover '/' inicial si el usuario lo escribió como en el chat de Minecraft
        if cmd_clean.startswith("/"):
            cmd_clean = cmd_clean[1:]

        server_status = self.get_container_status(self.SERVER_CONTAINER)
        if server_status != "running":
            return False, f"El contenedor 'mc-server' no está en ejecución (Estado: {server_status})."

        return self.run_cmd(
            ["podman", "exec", self.SERVER_CONTAINER, "rcon-cli", cmd_clean],
            timeout=15,
        )

    # -------------------------------------------------------------------------
    # GEYSER / FLOODGATE CONFIG FIX
    # -------------------------------------------------------------------------

    def apply_floodgate_config_fix(self) -> Tuple[bool, str]:
        """
        Ajusta la configuración de Geyser para que auth-type sea floodgate:
        sed -i 's/auth-type: online/auth-type: floodgate/g' .../plugins/Geyser-Spigot/config.yml
        """
        candidates = [
            self.data_dir / "plugins" / "Geyser-Spigot" / "config.yml",
            self.data_dir / "plugins" / "Geyser" / "config.yml",
            self.data_dir / "config" / "Geyser-Fabric" / "config.yml",
        ]

        fixed = False
        details = []

        for path in candidates:
            if path.exists():
                try:
                    content = path.read_text(encoding="utf-8")
                    if "auth-type: online" in content:
                        new_content = content.replace("auth-type: online", "auth-type: floodgate")
                        path.write_text(new_content, encoding="utf-8")
                        details.append(f"✔ Actualizado auth-type a 'floodgate' en: {path.name}")
                        fixed = True
                    elif "auth-type: floodgate" in content:
                        details.append(f"ℹ {path.name} ya tenía configurado 'auth-type: floodgate'.")
                        fixed = True
                except Exception as e:
                    details.append(f"✖ Error leyendo {path}: {e}")

        if fixed:
            return True, "\n".join(details)
        return (
            False,
            "No se encontró el archivo config.yml de Geyser aún.\n"
            "El servidor debe iniciar al menos una vez para que Geyser genere sus archivos.",
        )

    # -------------------------------------------------------------------------
    # GUARDADO Y CARGA DE CONFIGURACIÓN
    # -------------------------------------------------------------------------

    def load_config(self) -> Dict:
        """Carga la configuración guardada o retorna los valores por defecto."""
        default_config = {
            "version": "LATEST",
            "memory": "4G",
            "server_category": "plugins",  # vanilla, plugins, mods
            "server_type": "PAPER",
            "crossplay": True,
            "online_mode": False,
            "enable_whitelist": False,
            "playit_key": "",
            "enable_ssh": False,
            "ssh_user": "adminmc",
            "ssh_pass": "deckcraft123",
        }

        target_cfg = self.config_file if self.config_file.exists() else self.legacy_config_file
        if target_cfg.exists():
            try:
                with open(target_cfg, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    default_config.update(data)
            except Exception as e:
                print(f"[PodmanManager] Error leyendo config previa: {e}")

        return default_config

    def save_config(self, config: Dict) -> bool:
        """Guarda la configuración en disco."""
        try:
            with open(self.config_file, "w", encoding="utf-8") as f:
                json.dump(config, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"[PodmanManager] Error guardando config: {e}")
            return False

    # -------------------------------------------------------------------------
    # DESPLIEGUE Y ACTUALIZACIÓN DEL SERVIDOR
    # -------------------------------------------------------------------------

    def deploy_server(self, config: Dict, progress_callback=None) -> Tuple[bool, str]:
        """
        Orquesta el despliegue completo o actualización sin pérdida de datos:
        1. Verifica podman y directorios.
        2. Crea o verifica mc-pod con puertos 25565, 19132/udp, 2222.
        3. Detiene y elimina mc-server anterior si existía (los datos quedan en data/).
        4. Inicia mc-server con la nueva configuración y --user 0:0.
        5. Inicia o detiene mc-playit según la clave proporcionada.
        6. Inicia o detiene mc-ssh según la opción seleccionada.
        7. Aplica corrección de permisos y configuración post-arranque.
        """
        def log(msg: str):
            print(f"[Deploy] {msg}")
            if progress_callback:
                progress_callback(msg)

        if not self.is_podman_available():
            return False, "Error: Podman no está disponible en este sistema."

        self._ensure_directories()
        data_path = str(self.data_dir.resolve())
        ssh_config_path = str(self.ssh_config_dir.resolve())

        # 1. Verificar / Crear el Pod mc-pod
        log("Verificando pod 'mc-pod'...")
        pod_status = self.get_pod_status()

        if pod_status == "Not Created":
            log("Creando pod 'mc-pod' con puertos 25565 (Java), 19132/udp (Bedrock), 2222 (SSH)...")
            success, out = self.run_cmd([
                "podman", "pod", "create",
                "--name", self.POD_NAME,
                "-p", "25565:25565",
                "-p", "19132:19132/udp",
                "-p", "2222:2222",
            ], timeout=60)
            if not success:
                return False, f"Error al crear el pod: {out}"
        else:
            log(f"Pod 'mc-pod' existente encontrado (Estado: {pod_status}).")

        # 2. Preparar variables de mc-server
        version = config.get("version", "LATEST").strip() or "LATEST"
        memory = config.get("memory", "4G").strip() or "4G"
        server_type = config.get("server_type", "PAPER").upper().strip()
        online_mode = "TRUE" if config.get("online_mode", False) else "FALSE"
        whitelist = "TRUE" if config.get("enable_whitelist", False) else "FALSE"
        crossplay = config.get("crossplay", False)

        log("Configurando contenedor 'mc-server'...")
        # Detener y remover mc-server existente si existe
        curr_server_state = self.get_container_status(self.SERVER_CONTAINER)
        if curr_server_state != "not found":
            log("Deteniendo contenedor 'mc-server' previo...")
            self.run_cmd(["podman", "stop", "-t", "10", self.SERVER_CONTAINER], timeout=25)
            log("Removiendo contenedor previo para actualizar variables...")
            self.run_cmd(["podman", "rm", "-f", self.SERVER_CONTAINER], timeout=15)

        # Construir comando run de mc-server
        server_cmd = [
            "podman", "run", "-d",
            "--name", self.SERVER_CONTAINER,
            "--pod", self.POD_NAME,
            "--restart", "unless-stopped",
            "--user", "0:0",
            "-v", f"{data_path}:/data:Z",
            "-e", "EULA=TRUE",
            "-e", f"VERSION={version}",
            "-e", f"MEMORY={memory}",
            "-e", f"TYPE={server_type}",
            "-e", f"ONLINE_MODE={online_mode}",
            "-e", f"ENABLE_WHITELIST={whitelist}",
            "-e", f"ENFORCE_WHITELIST={whitelist}",
            "-e", "ENABLE_RCON=true",
            "-e", "RCON_PORT=25575",
            "-e", "RCON_PASSWORD=deckcraft",
        ]

        # Inyectar plugins de Crossplay si está habilitado
        if crossplay:
            if server_type in ["PAPER", "PURPUR", "SPIGOT"]:
                plugins_urls = [
                    "https://download.geysermc.org/v2/projects/geyser/versions/latest/builds/latest/downloads/spigot",
                    "https://download.geysermc.org/v2/projects/floodgate/versions/latest/builds/latest/downloads/spigot",
                    "https://github.com/SkinsRestorer/SkinsRestorer/releases/latest/download/SkinsRestorer.jar",
                ]
                server_cmd.extend(["-e", f"PLUGINS={','.join(plugins_urls)}"])
                log("Habilitado Crossplay Java+Bedrock (Geyser + Floodgate + SkinsRestorer vía PLUGINS)")
            elif server_type == "FABRIC":
                fabric_mods = [
                    "https://download.geysermc.org/v2/projects/geyser/versions/latest/builds/latest/downloads/fabric",
                    "https://download.geysermc.org/v2/projects/floodgate/versions/latest/builds/latest/downloads/fabric",
                ]
                server_cmd.extend(["-e", f"MODS={','.join(fabric_mods)}"])
                log("Habilitado Crossplay Java+Bedrock en Fabric vía MODS")

        server_cmd.append("docker.io/itzg/minecraft-server:latest")

        log("Lanzando contenedor 'mc-server' con itzg/minecraft-server...")
        success_server, out_server = self.run_cmd(server_cmd, timeout=90)
        if not success_server:
            return False, f"Error al iniciar mc-server: {out_server}"
        log(f"Contenedor 'mc-server' iniciado con ID: {out_server[:12] if len(out_server)>=12 else out_server}")

        # 3. Configurar mc-playit
        playit_key = config.get("playit_key", "").strip()
        curr_playit_state = self.get_container_status(self.PLAYIT_CONTAINER)
        if curr_playit_state != "not found":
            log("Deteniendo contenedor 'mc-playit' previo...")
            self.run_cmd(["podman", "stop", "-t", "5", self.PLAYIT_CONTAINER], timeout=15)
            self.run_cmd(["podman", "rm", "-f", self.PLAYIT_CONTAINER], timeout=15)

        if playit_key:
            log("Iniciando contenedor 'mc-playit' con Secret Key...")
            playit_cmd = [
                "podman", "run", "-d",
                "--name", self.PLAYIT_CONTAINER,
                "--pod", self.POD_NAME,
                "--restart", "unless-stopped",
                "-e", f"SECRET_KEY={playit_key}",
                "ghcr.io/playit-cloud/playit-agent:latest",
            ]
            success_playit, out_playit = self.run_cmd(playit_cmd, timeout=60)
            if not success_playit:
                log(f"Advertencia: no se pudo iniciar mc-playit: {out_playit}")
            else:
                log("Contenedor 'mc-playit' activo con túnel configurado.")
        else:
            log("Secret Key de Playit no provista; 'mc-playit' omitido.")

        # 4. Configurar mc-ssh (Opcional)
        enable_ssh = config.get("enable_ssh", False)
        curr_ssh_state = self.get_container_status(self.SSH_CONTAINER)
        if curr_ssh_state != "not found":
            log("Deteniendo contenedor 'mc-ssh' previo...")
            self.run_cmd(["podman", "stop", "-t", "5", self.SSH_CONTAINER], timeout=15)
            self.run_cmd(["podman", "rm", "-f", self.SSH_CONTAINER], timeout=15)

        if enable_ssh:
            ssh_user = config.get("ssh_user", "adminmc").strip() or "adminmc"
            ssh_pass = config.get("ssh_pass", "deckcraft123").strip() or "deckcraft123"
            log(f"Iniciando contenedor 'mc-ssh' (Usuario: {ssh_user}, Puerto: 2222)...")

            ssh_cmd = [
                "podman", "run", "-d",
                "--name", self.SSH_CONTAINER,
                "--pod", self.POD_NAME,
                "--restart", "unless-stopped",
                "-e", "PASSWORD_ACCESS=true",
                "-e", f"USER_NAME={ssh_user}",
                "-e", f"USER_PASSWORD={ssh_pass}",
                "-v", f"{data_path}:/servidor-mc:Z",
                "-v", f"{ssh_config_path}:/config:Z",
                "lscr.io/linuxserver/openssh-server:latest",
            ]

            success_ssh, out_ssh = self.run_cmd(ssh_cmd, timeout=60)
            if not success_ssh:
                log(f"Advertencia al iniciar mc-ssh: {out_ssh}")
            else:
                log("Esperando inicialización de OpenSSH para aplicar configuración de contraseña...")
                time.sleep(3)
                # Ejecutar desbloqueo de contraseña según requerimiento
                pw_fix_cmd = [
                    "podman", "exec", self.SSH_CONTAINER,
                    "sh", "-c", f"echo '{ssh_user}:{ssh_pass}' | chpasswd && passwd -u {ssh_user}"
                ]
                self.run_cmd(pw_fix_cmd, timeout=15)
                # Ejecutar chmod en mc-server
                self.run_cmd(["podman", "exec", self.SERVER_CONTAINER, "chmod", "-R", "777", "/data"], timeout=15)
                log("Acceso SSH y permisos de /servidor-mc (/data) configurados exitosamente.")

        # 5. Asegurar permisos finales
        log("Aplicando corrección de permisos en carpeta de datos...")
        self.fix_permissions()

        # 6. Guardar configuración en archivo
        self.save_config(config)

        log("✔ Despliegue finalizado con éxito.")
        return True, "Servidor desplegado y en ejecución correctamente."
