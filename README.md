# 🎮 MC Server-Deck (Rust Edition)

**English** • [Español](README.es.md)

High-performance native application written in **Rust** (with Tauri v2 frontend) built specifically for the **Steam Deck** (SteamOS / Arch Linux). Easily deploy, manage, and orchestrate Minecraft servers using native **rootless Podman** on SteamOS, with zero external Python dependencies and an advanced anti-desynchronization engine.

---

## 🌟 Key Features

- **Built 100% in Rust + Tauri v2:**
  - Instant startup speed, minimal RAM overhead, and native compiled execution.
  - Completely eliminates Python virtual environment (`venv`) issues, `PyQt6` dependencies, and UI thread lockups.
- **Multi-Language Support (i18n):**
  - Seamless real-time language switcher supporting **English (default)**, **Spanish**, **French**, and **Portuguese**, with automatic fallback.
- **Podman Anti-Desynchronization Engine:**
  - **Mutex Serialization:** All state-mutating operations (`deploy`, `start`, `stop`, `restart`, `repair`) are sequentially queued through an asynchronous Rust actor (`tokio::sync::Mutex`), preventing Podman database and storage locks (`storage.db`).
  - **Structured JSON Inspection:** Queries Podman container states directly using `--format json` with deep inspection of the infra-container, `mc-server`, `mc-playit`, and `mc-ssh`.
  - **Automatic Reconciliation & Healing:** Detects when the primary Minecraft container has failed or when the pod enters a `Degraded` state, providing an automated 1-click healing routine to remove orphaned containers and cleanly resync the pod.
- **Minecraft Version Control:**
  - Connects directly to the official Mojang API (`piston-meta.mojang.com`) to dynamically fetch latest releases (1.21.4, 1.20.4, 1.19.2, etc.) and snapshots.
- **Flexible Connectivity (Public IP vs Playit.gg):**
  - **Public IP:** Automatic detection of Local LAN and Public Internet IP. Includes automatic UPnP port-forwarding probing and an interactive step-by-step router guide (TCP 25565, UDP 19132, TCP 2222).
  - **Playit.gg Tunnels:** Integrated `mc-playit` agent container with `SECRET_KEY` support, allowing you to play with friends over the Internet without port forwarding or exposing your home IP.
- **Multiple Server Engines:**
  - **Official Vanilla:** Pure unmodified Mojang server.
  - **Plugins:** Paper (Recommended), Purpur, or Spigot.
  - **Mods:** Fabric, Forge, NeoForge, or Quilt.
- **Built-in Java + Bedrock Crossplay:**
  - Automated integration of GeyserMC, Floodgate, and SkinsRestorer, enabling console (Xbox, PlayStation, Nintendo Switch), mobile (iOS, Android), and Windows Bedrock players to play together with Java users.
- **Remote SFTP / SSH Access:**
  - Dedicated `mc-ssh` container mapped to `/servidor-mc` (`~/minecraft-server/data`) for uploading mods, worlds, datapacks, and plugins wirelessly from your main PC using FileZilla or WinSCP.
- **Interactive Live RCON Console & Log Streaming:**
  - Send live Minecraft commands (`op`, `whitelist`, `save-all`, `list`, `say`, etc.) with convenient touch-friendly quick action macros.
- **OLED Anti-Burn-In Screensaver:**
  - Built-in screensaver with pure black background (`#000000` to turn off OLED pixels on the Steam Deck OLED panel) and a DVD/CRT bouncing logo to keep your server running continuously without panel wear.

---

## 🏗 Container Architecture in Podman

The application manages a single rootless user-space Pod named `mc-pod` mapping:
- `25565:25565` (Minecraft Java Edition TCP)
- `19132:19132/udp` (Minecraft Bedrock Edition UDP)
- `2222:2222` (SFTP / SSH Access TCP)

### Containers inside `mc-pod`:
1. **`mc-server` (`docker.io/itzg/minecraft-server:latest`):**
   - Runs the Minecraft server engine with `--user 0:0` and persistent data volume at `~/minecraft-server/data:/data:Z`.
2. **`mc-playit` (`ghcr.io/playit-cloud/playit-agent:latest`):**
   - Official Playit.gg tunnel agent container activated when a secret key is provided or tunnel mode is selected.
3. **`mc-ssh` (`lscr.io/linuxserver/openssh-server:latest`):**
   - SFTP server for remote wireless file management.

---

## 🚀 Installation on Steam Deck

### Step 1: Switch to Desktop Mode
1. Press the physical **STEAM** button on your Steam Deck.
2. Go to **Power** -> **Switch to Desktop**.

### Step 2: Clone and Run Installer
Open **Konsole** (SteamOS terminal) and run:

```bash
git clone https://github.com/MOtaMore/mc_server-deck.git
cd mc_server-deck
chmod +x install.sh
./install.sh
```

The script will install the optimized pre-compiled Linux binary and create desktop shortcuts in both `~/Desktop/MC-Server-Deck.desktop` and your SteamOS application launcher.

---

## 🎮 Add to Steam (Gaming Mode)

1. In Desktop Mode, open the **Steam** desktop client.
2. In the top menu, click **Games** -> **Add a Non-Steam Game to My Library...**.
3. Select **MC Server-Deck** (or browse to `~/.local/share/mc-server-deck/mc-server-deck`).
4. Click **Add Selected Programs**.
5. Switch back to **Gaming Mode**. The application is ready to launch with full 1280x800 touch screen and controller support!

---

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
