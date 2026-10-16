pub mod commands;
pub mod minecraft;
pub mod models;
pub mod network;
pub mod podman;
pub mod steamos;

use podman::{PodmanEngine, SharedPodmanEngine};
use std::sync::Arc;

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    let podman_engine: SharedPodmanEngine = Arc::new(PodmanEngine::new());

    tauri::Builder::default()
        .manage(podman_engine)
        .plugin(
            tauri_plugin_log::Builder::default()
                .level(log::LevelFilter::Info)
                .build(),
        )
        .invoke_handler(tauri::generate_handler![
            commands::get_status,
            commands::deploy_server,
            commands::start_server,
            commands::stop_server,
            commands::restart_server,
            commands::repair_pod,
            commands::send_rcon,
            commands::get_logs,
            commands::get_minecraft_versions,
            commands::get_network_info,
            commands::test_upnp,
            commands::load_config,
            commands::save_config,
            commands::install_shortcuts,
        ])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
