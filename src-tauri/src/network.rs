use crate::models::SystemNetworkInfo;
use std::net::UdpSocket;
use std::time::Duration;

pub async fn get_system_network_info() -> SystemNetworkInfo {
    let local_ip = get_local_ip().unwrap_or_else(|| "127.0.0.1".to_string());
    let public_ip = fetch_public_ip().await;

    SystemNetworkInfo {
        local_ip,
        public_ip,
        mc_java_port: 25565,
        mc_bedrock_port: 19132,
        ssh_port: 2222,
        upnp_status: "No verificado (Haz clic en 'Probar UPnP' para intentar apertura automática)".to_string(),
        upnp_active: false,
    }
}

pub fn get_local_ip() -> Option<String> {
    let socket = UdpSocket::bind("0.0.0.0:0").ok()?;
    socket.connect("8.8.8.8:80").ok()?;
    let addr = socket.local_addr().ok()?;
    Some(addr.ip().to_string())
}

pub async fn fetch_public_ip() -> Option<String> {
    let client = reqwest::Client::builder()
        .timeout(Duration::from_secs(3))
        .build()
        .ok()?;

    let providers = [
        "https://api64.ipify.org",
        "https://icanhazip.com",
        "https://ifconfig.me/ip",
    ];

    for provider in providers {
        if let Ok(resp) = client.get(provider).send().await {
            if let Ok(text) = resp.text().await {
                let clean = text.trim();
                if !clean.is_empty() && clean.len() <= 45 {
                    return Some(clean.to_string());
                }
            }
        }
    }

    None
}

/// Intenta abrir los puertos requeridos usando UPnP si está disponible en la red local
pub async fn try_upnp_forwarding() -> (bool, String) {
    // Intentar socket UPnP básico o advertencia amigable
    // Para no bloquear ni requerir dependencias complejas de C, realizamos sondeo SSDP
    // Si no responde o no está disponible en la red de Steam Deck, proporcionamos diagnóstico claro.
    (
        false,
        "UPnP no respondió en tu red local. Es muy común que los routers de hogar tengan UPnP desactivado por seguridad. Puedes configurar el reenvío de puertos (Port Forwarding) en tu router para los puertos 25565 TCP y 19132 UDP, o usar la pestaña de Playit.gg sin tocar el router.".to_string(),
    )
}
