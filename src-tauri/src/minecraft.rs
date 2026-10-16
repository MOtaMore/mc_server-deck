use crate::models::{MinecraftVersionItem, MinecraftVersionsResponse};
use serde::Deserialize;
use std::time::Duration;

#[derive(Debug, Deserialize)]
struct MojangManifestLatest {
    release: String,
    snapshot: String,
}

#[derive(Debug, Deserialize)]
struct MojangManifestVersion {
    id: String,
    #[serde(rename = "type")]
    version_type: String,
    #[serde(rename = "releaseTime")]
    release_time: String,
}

#[derive(Debug, Deserialize)]
struct MojangManifest {
    latest: MojangManifestLatest,
    versions: Vec<MojangManifestVersion>,
}

pub async fn fetch_minecraft_versions() -> MinecraftVersionsResponse {
    let client = reqwest::Client::builder()
        .timeout(Duration::from_secs(4))
        .build();

    if let Ok(client) = client {
        let url = "https://piston-meta.mojang.com/mc/game/version_manifest_v2.json";
        if let Ok(resp) = client.get(url).send().await {
            if let Ok(manifest) = resp.json::<MojangManifest>().await {
                let items: Vec<MinecraftVersionItem> = manifest
                    .versions
                    .into_iter()
                    .filter(|v| v.version_type == "release" || v.id == manifest.latest.snapshot)
                    .take(60) // Top 60 releases
                    .map(|v| MinecraftVersionItem {
                        id: v.id,
                        version_type: v.version_type,
                        release_time: v.release_time,
                    })
                    .collect();

                return MinecraftVersionsResponse {
                    latest_release: manifest.latest.release,
                    latest_snapshot: manifest.latest.snapshot,
                    versions: items,
                };
            }
        }
    }

    // Fallback versions if network is unavailable
    get_fallback_versions()
}

pub fn get_fallback_versions() -> MinecraftVersionsResponse {
    let popular_releases = vec![
        "1.21.4", "1.21.3", "1.21.1", "1.21",
        "1.20.6", "1.20.4", "1.20.2", "1.20.1",
        "1.19.4", "1.19.2", "1.18.2", "1.16.5", "1.12.2"
    ];

    let items = popular_releases
        .into_iter()
        .map(|ver| MinecraftVersionItem {
            id: ver.to_string(),
            version_type: "release".to_string(),
            release_time: String::new(),
        })
        .collect();

    MinecraftVersionsResponse {
        latest_release: "1.21.4".to_string(),
        latest_snapshot: "24w46a".to_string(),
        versions: items,
    }
}
