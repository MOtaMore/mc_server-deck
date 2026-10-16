use crate::models::{ContainerState, PodStatus, ServerConfig};
use chrono::Local;
use serde_json::Value;
use std::collections::HashMap;
use std::fs;
use std::path::PathBuf;
use std::process::Stdio;
use std::sync::Arc;
use tokio::process::Command;
use tokio::sync::Mutex;

pub struct PodmanEngine {
    pub base_dir: PathBuf,
    pub data_dir: PathBuf,
    pub ssh_config_dir: PathBuf,
    pub config_file: PathBuf,
    operation_lock: Mutex<()>,
}

pub type SharedPodmanEngine = Arc<PodmanEngine>;

impl PodmanEngine {
    pub fn new() -> Self {
        let base_dir = dirs::home_dir()
            .unwrap_or_else(|| PathBuf::from("."))
            .join("minecraft-server");

        let data_dir = base_dir.join("data");
        let ssh_config_dir = base_dir.join("ssh-config");
        let config_file = base_dir.join("mc_server_config.json");

        let _ = fs::create_dir_all(&data_dir);
        let _ = fs::create_dir_all(&ssh_config_dir);

        Self {
            base_dir,
            data_dir,
            ssh_config_dir,
            config_file,
            operation_lock: Mutex::new(()),
        }
    }

    /// Comprueba si podman está disponible en PATH
    pub async fn is_podman_available(&self) -> bool {
        let output = Command::new("podman")
            .arg("--version")
            .output()
            .await;
        output.map(|o| o.status.success()).unwrap_or(false)
    }

    /// Ejecuta un comando podman capturando stdout y stderr
    pub async fn run_podman(&self, args: &[&str]) -> (bool, String) {
        let mut cmd = Command::new("podman");
        cmd.args(args);
        cmd.stdout(Stdio::piped());
        cmd.stderr(Stdio::piped());

        match cmd.output().await {
            Ok(output) => {
                let stdout = String::from_utf8_lossy(&output.stdout).trim().to_string();
                let stderr = String::from_utf8_lossy(&output.stderr).trim().to_string();
                if output.status.success() {
                    (true, if stdout.is_empty() { stderr } else { stdout })
                } else {
                    let err = if !stderr.is_empty() { stderr } else { stdout };
                    (false, err)
                }
            }
            Err(e) => (false, format!("Error al ejecutar podman: {}", e)),
        }
    }

    /// Inspección profunda del pod y sus contenedores para detectar desincronizaciones
    pub async fn get_pod_status_detailed(&self) -> PodStatus {
        let now = Local::now().format("%H:%M:%S").to_string();

        if !self.is_podman_available().await {
            return PodStatus {
                status: "No Podman".to_string(),
                containers: HashMap::new(),
                is_healthy: false,
                desync_detected: true,
                desync_reason: Some("Podman no está instalado o no se encuentra en el PATH de SteamOS.".to_string()),
                last_checked: now,
            };
        }

        // Consultar estado de mc-pod vía JSON estructurado
        let (success, out) = self.run_podman(&["pod", "inspect", "mc-pod", "--format", "json"]).await;

        if !success {
            return PodStatus {
                status: "Not Created".to_string(),
                containers: HashMap::new(),
                is_healthy: false,
                desync_detected: false,
                desync_reason: None,
                last_checked: now,
            };
        }

        let mut containers_map = HashMap::new();
        let mut desync_detected = false;
        let mut desync_reason: Option<String> = None;
        let mut pod_status_str = "Unknown".to_string();

        if let Ok(json_val) = serde_json::from_str::<Value>(&out) {
            if let Some(status) = json_val.get("State").and_then(|s| s.as_str()) {
                pod_status_str = status.to_string();
            } else if let Some(status) = json_val.get("Status").and_then(|s| s.as_str()) {
                pod_status_str = status.to_string();
            }

            // Inspeccionar contenedores dentro del pod
            if let Some(containers) = json_val.get("Containers").and_then(|c| c.as_array()) {
                for c in containers {
                    let name = c.get("Name").and_then(|n| n.as_str()).unwrap_or("").to_string();
                    let state = c.get("State").and_then(|s| s.as_str()).unwrap_or("").to_string();
                    let id = c.get("Id").and_then(|i| i.as_str()).map(|s| s.to_string());

                    if !name.is_empty() && !name.ends_with("-infra") {
                        containers_map.insert(
                            name.clone(),
                            ContainerState {
                                name: name.clone(),
                                status: state.clone(),
                                exit_code: None,
                                uptime: None,
                                id,
                            },
                        );

                        // Si el contenedor del servidor de minecraft está detenido o falló
                        if name == "mc-server" && state != "running" {
                            desync_detected = true;
                            desync_reason = Some(format!(
                                "El contenedor principal 'mc-server' se encuentra en estado '{}'. El pod no está sirviendo Minecraft.",
                                state
                            ));
                        }
                    }
                }
            }
        }

        // Si el pod está en estado Degraded
        if pod_status_str.to_lowercase() == "degraded" && !desync_detected {
            desync_detected = true;
            desync_reason = Some("El pod 'mc-pod' está en estado 'Degraded': uno o más de sus contenedores fallaron o se detuvieron inesperadamente.".to_string());
        }

        let is_healthy = (pod_status_str.to_lowercase() == "running") && !desync_detected;

        PodStatus {
            status: pod_status_str,
            containers: containers_map,
            is_healthy,
            desync_detected,
            desync_reason,
            last_checked: now,
        }
    }

    /// Despliega o actualiza el servidor de Minecraft de forma atómica y sincronizada
    pub async fn deploy_server(&self, config: ServerConfig) -> Result<String, String> {
        let _guard = self.operation_lock.lock().await;

        if !self.is_podman_available().await {
            return Err("Podman no está disponible en este sistema.".to_string());
        }

        let data_path = self.data_dir.to_string_lossy().to_string();
        let ssh_config_path = self.ssh_config_dir.to_string_lossy().to_string();

        // 1. Asegurar o crear el Pod mc-pod
        let pod_status = self.get_pod_status_detailed().await;
        if pod_status.status == "Not Created" || pod_status.desync_detected {
            // Limpiar si había residuo desincronizado
            let _ = self.run_podman(&["pod", "rm", "-f", "mc-pod"]).await;

            let (created, out) = self.run_podman(&[
                "pod", "create",
                "--name", "mc-pod",
                "-p", "25565:25565",
                "-p", "19132:19132/udp",
                "-p", "2222:2222",
            ]).await;

            if !created {
                return Err(format!("Error al crear el pod 'mc-pod': {}", out));
            }
        }

        // 2. Limpiar mc-server previo
        let _ = self.run_podman(&["stop", "-t", "10", "mc-server"]).await;
        let _ = self.run_podman(&["rm", "-f", "mc-server"]).await;

        // 3. Preparar variables para itzg/minecraft-server
        let online_str = if config.online_mode { "TRUE" } else { "FALSE" };
        let whitelist_str = if config.enable_whitelist { "TRUE" } else { "FALSE" };
        let memory_str = if config.memory.is_empty() { "4G" } else { &config.memory };
        let max_players_str = config.max_players.to_string();

        let mut server_args = vec![
            "run", "-d",
            "--name", "mc-server",
            "--pod", "mc-pod",
            "--restart", "unless-stopped",
            "--user", "0:0",
            "-v",
        ];
        let volume_arg = format!("{}:/data:Z", data_path);
        server_args.push(&volume_arg);

        let eula_arg = "EULA=TRUE";
        let ver_env = format!("VERSION={}", config.version);
        let mem_env = format!("MEMORY={}", memory_str);
        let type_env = format!("TYPE={}", config.server_type.to_uppercase());
        let online_env = format!("ONLINE_MODE={}", online_str);
        let wl_env = format!("ENABLE_WHITELIST={}", whitelist_str);
        let enf_wl_env = format!("ENFORCE_WHITELIST={}", whitelist_str);
        let motd_env = format!("MOTD={}", config.motd);
        let diff_env = format!("DIFFICULTY={}", config.difficulty);
        let maxp_env = format!("MAX_PLAYERS={}", max_players_str);
        let rcon_en_env = "ENABLE_RCON=true";
        let rcon_p_env = "RCON_PORT=25575";
        let rcon_pwd_env = "RCON_PASSWORD=deckcraft";

        server_args.extend_from_slice(&[
            "-e", eula_arg,
            "-e", &ver_env,
            "-e", &mem_env,
            "-e", &type_env,
            "-e", &online_env,
            "-e", &wl_env,
            "-e", &enf_wl_env,
            "-e", &motd_env,
            "-e", &diff_env,
            "-e", &maxp_env,
            "-e", "-e", rcon_en_env,
            "-e", rcon_p_env,
            "-e", rcon_pwd_env,
        ]);

        // Crossplay Java + Bedrock (Geyser + Floodgate + SkinsRestorer)
        let plugins_arg;
        let mods_arg;
        if config.crossplay {
            let st = config.server_type.to_uppercase();
            if ["PAPER", "PURPUR", "SPIGOT"].contains(&st.as_str()) {
                plugins_arg = "PLUGINS=https://download.geysermc.org/v2/projects/geyser/versions/latest/builds/latest/downloads/spigot,https://download.geysermc.org/v2/projects/floodgate/versions/latest/builds/latest/downloads/spigot,https://github.com/SkinsRestorer/SkinsRestorer/releases/latest/download/SkinsRestorer.jar".to_string();
                server_args.extend_from_slice(&["-e", &plugins_arg]);
            } else if st == "FABRIC" {
                mods_arg = "MODS=https://download.geysermc.org/v2/projects/geyser/versions/latest/builds/latest/downloads/fabric,https://download.geysermc.org/v2/projects/floodgate/versions/latest/builds/latest/downloads/fabric".to_string();
                server_args.extend_from_slice(&["-e", &mods_arg]);
            }
        }

        server_args.push("docker.io/itzg/minecraft-server:latest");

        let (server_ok, server_out) = self.run_podman(&server_args).await;
        if !server_ok {
            return Err(format!("Error al iniciar mc-server: {}", server_out));
        }

        // 4. Configurar mc-playit (Túnel Playit.gg)
        let _ = self.run_podman(&["stop", "-t", "5", "mc-playit"]).await;
        let _ = self.run_podman(&["rm", "-f", "mc-playit"]).await;

        let playit_key_clean = config.playit_key.trim();
        if config.connection_mode == "playit" || !playit_key_clean.is_empty() {
            let secret_env = format!("SECRET_KEY={}", playit_key_clean);
            let playit_args = vec![
                "run", "-d",
                "--name", "mc-playit",
                "--pod", "mc-pod",
                "--restart", "unless-stopped",
                "-e", &secret_env,
                "ghcr.io/playit-cloud/playit-agent:latest",
            ];
            let _ = self.run_podman(&playit_args).await;
        }

        // 5. Configurar mc-ssh (Acceso SSH / SFTP)
        let _ = self.run_podman(&["stop", "-t", "5", "mc-ssh"]).await;
        let _ = self.run_podman(&["rm", "-f", "mc-ssh"]).await;

        if config.enable_ssh {
            let ssh_user = if config.ssh_user.is_empty() { "adminmc" } else { &config.ssh_user };
            let ssh_pass = if config.ssh_pass.is_empty() { "deckcraft123" } else { &config.ssh_pass };

            let u_env = format!("USER_NAME={}", ssh_user);
            let p_env = format!("USER_PASSWORD={}", ssh_pass);
            let ssh_vol_data = format!("{}:/servidor-mc:Z", data_path);
            let ssh_vol_conf = format!("{}:/config:Z", ssh_config_path);

            let ssh_args = vec![
                "run", "-d",
                "--name", "mc-ssh",
                "--pod", "mc-pod",
                "--restart", "unless-stopped",
                "-e", "PASSWORD_ACCESS=true",
                "-e", &u_env,
                "-e", &p_env,
                "-v", &ssh_vol_data,
                "-v", &ssh_vol_conf,
                "lscr.io/linuxserver/openssh-server:latest",
            ];
            let _ = self.run_podman(&ssh_args).await;
        }

        // 6. Guardar configuración en JSON
        self.save_config(&config);

        Ok("Servidor de Minecraft desplegado y sincronizado correctamente en mc-pod.".to_string())
    }

    /// Inicia el pod existente
    pub async fn start_pod(&self) -> Result<String, String> {
        let _guard = self.operation_lock.lock().await;
        let (ok, out) = self.run_podman(&["pod", "start", "mc-pod"]).await;
        if ok {
            Ok("Pod iniciado exitosamente.".to_string())
        } else {
            Err(format!("Error al iniciar el pod: {}", out))
        }
    }

    /// Detiene el pod de forma limpia y segura
    pub async fn stop_pod(&self) -> Result<String, String> {
        let _guard = self.operation_lock.lock().await;
        let (ok, out) = self.run_podman(&["pod", "stop", "-t", "15", "mc-pod"]).await;
        if ok {
            Ok("Pod detenido de forma segura.".to_string())
        } else {
            Err(format!("Error al detener el pod: {}", out))
        }
    }

    /// Reinicia los contenedores del pod
    pub async fn restart_pod(&self) -> Result<String, String> {
        let _guard = self.operation_lock.lock().await;
        let _ = self.run_podman(&["pod", "stop", "-t", "10", "mc-pod"]).await;
        let (ok, out) = self.run_podman(&["pod", "start", "mc-pod"]).await;
        if ok {
            Ok("Pod reiniciado exitosamente.".to_string())
        } else {
            Err(format!("Error al reiniciar el pod: {}", out))
        }
    }

    /// Motor de Reconciliación y Reparación Anti-Desincronización:
    /// Limpia contenedores bloqueados o corruptos, resetea locks y vuelve a sincronizar el pod
    pub async fn repair_and_reconcile(&self) -> Result<String, String> {
        let _guard = self.operation_lock.lock().await;

        // 1. Detener forzosamente contenedores
        let _ = self.run_podman(&["stop", "-t", "5", "mc-server", "mc-playit", "mc-ssh"]).await;
        let _ = self.run_podman(&["rm", "-f", "mc-server", "mc-playit", "mc-ssh"]).await;
        let _ = self.run_podman(&["pod", "rm", "-f", "mc-pod"]).await;

        // 2. Corregir permisos de datos si podman unshare está disponible
        let data_path = self.data_dir.to_string_lossy().to_string();
        let _ = self.run_podman(&["unshare", "chown", "-R", "0:0", &data_path]).await;

        // 3. Recrear el pod con los puertos canónicos
        let (created, out) = self.run_podman(&[
            "pod", "create",
            "--name", "mc-pod",
            "-p", "25565:25565",
            "-p", "19132:19132/udp",
            "-p", "2222:2222",
        ]).await;

        if !created {
            return Err(format!("Fallo al recrear el pod limpio: {}", out));
        }

        // 4. Si existe configuración guardada previa, re-desplegar de forma limpia
        let config = self.load_config();
        drop(_guard); // Soltar lock temporalmente para llamar a deploy_server
        self.deploy_server(config).await
    }

    /// Ejecuta un comando en la consola RCON del servidor de Minecraft
    pub async fn send_rcon(&self, command: &str) -> Result<String, String> {
        let clean_cmd = command.trim();
        if clean_cmd.is_empty() {
            return Ok(String::new());
        }

        let (ok, out) = self.run_podman(&["exec", "mc-server", "rcon-cli", clean_cmd]).await;
        if ok {
            Ok(out)
        } else {
            Err(format!("Error RCON: {}", out))
        }
    }

    /// Obtiene las últimas líneas de logs de mc-server
    pub async fn get_server_logs(&self, tail_lines: usize) -> Result<String, String> {
        let tail_str = tail_lines.to_string();
        let (ok, out) = self.run_podman(&["logs", "--tail", &tail_str, "mc-server"]).await;
        if ok {
            Ok(out)
        } else {
            Err(out)
        }
    }

    /// Guarda la configuración en disco
    pub fn save_config(&self, config: &ServerConfig) {
        if let Ok(json) = serde_json::to_string_pretty(config) {
            let _ = fs::write(&self.config_file, json);
        }
    }

    /// Carga la configuración guardada o retorna los valores por defecto
    pub fn load_config(&self) -> ServerConfig {
        if let Ok(content) = fs::read_to_string(&self.config_file) {
            if let Ok(cfg) = serde_json::from_str::<ServerConfig>(&content) {
                return cfg;
            }
        }
        ServerConfig::default()
    }
}
