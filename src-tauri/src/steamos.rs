use std::fs;

pub struct SteamOSHelper;

impl SteamOSHelper {
    /// Crea el acceso directo .desktop en el Escritorio y en el menú de aplicaciones de SteamOS
    pub fn install_desktop_shortcuts(app_exe: Option<String>) -> Result<String, String> {
        let home = match dirs::home_dir() {
            Some(h) => h,
            None => return Err("No se pudo obtener el directorio personal (HOME)".to_string()),
        };

        let current_exe = app_exe.unwrap_or_else(|| {
            std::env::current_exe()
                .map(|p| p.to_string_lossy().to_string())
                .unwrap_or_else(|_| "mc-server-deck".to_string())
        });

        let icon_path = home
            .join(".local/share/mc-server-deck/assets/icon.png")
            .to_string_lossy()
            .to_string();

        let desktop_content = format!(
            r#"[Desktop Entry]
Name=MC Server-Deck
Comment=Servidor de Minecraft nativo en Podman para Steam Deck
Exec="{}"
Icon={}
Terminal=false
Type=Application
Categories=Game;Utility;
StartupNotify=true
"#,
            current_exe, icon_path
        );

        let desktop_dir = home.join("Desktop");
        let app_dir = home.join(".local/share/applications");

        let _ = fs::create_dir_all(&desktop_dir);
        let _ = fs::create_dir_all(&app_dir);

        let desktop_file = desktop_dir.join("MC-Server-Deck.desktop");
        let app_file = app_dir.join("MC-Server-Deck.desktop");

        let res1 = fs::write(&desktop_file, &desktop_content);
        let res2 = fs::write(&app_file, &desktop_content);

        // Intentar dar permisos de ejecución en Linux
        #[cfg(unix)]
        {
            use std::os::unix::fs::PermissionsExt;
            if let Ok(meta) = fs::metadata(&desktop_file) {
                let mut perms = meta.permissions();
                perms.set_mode(0o755);
                let _ = fs::set_permissions(&desktop_file, perms);
            }
            if let Ok(meta) = fs::metadata(&app_file) {
                let mut perms = meta.permissions();
                perms.set_mode(0o755);
                let _ = fs::set_permissions(&app_file, perms);
            }
        }

        if res1.is_ok() || res2.is_ok() {
            Ok("Acceso directo instalado correctamente en el Escritorio y menú de aplicaciones.".to_string())
        } else {
            Err("No se pudieron escribir los accesos directos.".to_string())
        }
    }
}
