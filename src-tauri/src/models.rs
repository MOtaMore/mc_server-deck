use serde::{Deserialize, Serialize};
use std::collections::HashMap;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ServerConfig {
    #[serde(default = "default_version")]
    pub version: String,
    #[serde(default = "default_server_type")]
    pub server_type: String,
    #[serde(default = "default_memory")]
    pub memory: String,
    #[serde(default)]
    pub online_mode: bool,
    #[serde(default)]
    pub enable_whitelist: bool,
    #[serde(default = "default_true")]
    pub crossplay: bool,
    #[serde(default = "default_connection_mode")]
    pub connection_mode: String, // "public_ip" or "playit"
    #[serde(default)]
    pub playit_key: String,
    #[serde(default = "default_true")]
    pub enable_ssh: bool,
    #[serde(default = "default_ssh_user")]
    pub ssh_user: String,
    #[serde(default = "default_ssh_pass")]
    pub ssh_pass: String,
    #[serde(default = "default_motd")]
    pub motd: String,
    #[serde(default = "default_difficulty")]
    pub difficulty: String,
    #[serde(default = "default_max_players")]
    pub max_players: u32,
    #[serde(default)]
    pub custom_env: HashMap<String, String>,
}

fn default_version() -> String { "1.21.4".to_string() }
fn default_server_type() -> String { "PAPER".to_string() }
fn default_memory() -> String { "4G".to_string() }
fn default_true() -> bool { true }
fn default_connection_mode() -> String { "public_ip".to_string() }
fn default_ssh_user() -> String { "adminmc".to_string() }
fn default_ssh_pass() -> String { "deckcraft123".to_string() }
fn default_motd() -> String { "Servidor Minecraft en Steam Deck".to_string() }
fn default_difficulty() -> String { "normal".to_string() }
fn default_max_players() -> u32 { 10 }

impl Default for ServerConfig {
    fn default() -> Self {
        Self {
            version: default_version(),
            server_type: default_server_type(),
            memory: default_memory(),
            online_mode: false,
            enable_whitelist: false,
            crossplay: true,
            connection_mode: default_connection_mode(),
            playit_key: String::new(),
            enable_ssh: true,
            ssh_user: default_ssh_user(),
            ssh_pass: default_ssh_pass(),
            motd: default_motd(),
            difficulty: default_difficulty(),
            max_players: default_max_players(),
            custom_env: HashMap::new(),
        }
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ContainerState {
    pub name: String,
    pub status: String, // "running", "exited", "created", "dead", "not found"
    pub exit_code: Option<i64>,
    pub uptime: Option<String>,
    pub id: Option<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct PodStatus {
    pub status: String, // "Running", "Degraded", "Stopped", "Exited", "Not Created", "No Podman"
    pub containers: HashMap<String, ContainerState>,
    pub is_healthy: bool,
    pub desync_detected: bool,
    pub desync_reason: Option<String>,
    pub last_checked: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SystemNetworkInfo {
    pub local_ip: String,
    pub public_ip: Option<String>,
    pub mc_java_port: u16,
    pub mc_bedrock_port: u16,
    pub ssh_port: u16,
    pub upnp_status: String,
    pub upnp_active: bool,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct MinecraftVersionItem {
    pub id: String,
    pub version_type: String, // "release", "snapshot"
    pub release_time: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct MinecraftVersionsResponse {
    pub latest_release: String,
    pub latest_snapshot: String,
    pub versions: Vec<MinecraftVersionItem>,
}
