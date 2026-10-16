# 🎮 MC Server-Deck (Edición Rust)

Aplicación nativa de alto rendimiento escrita en **Rust** (con interfaz Tauri v2) diseñada específicamente para la **Steam Deck** (SteamOS / Arch Linux). Permite desplegar, administrar y orquestar servidores de Minecraft utilizando el **Podman rootless** nativo del sistema operativo, con cero dependencias externas de Python y con un motor de gestión anti-desincronizaciones.

---

## 🌟 Características Principales

- **Desarrollado 100% en Rust + Tauri v2:**
  - Máxima velocidad de inicio, consumo mínimo de memoria RAM en la consola y binario compilado nativamente.
  - Elimina por completo los problemas de entornos virtuales de Python (`venv`), dependencias de `PyQt6` o bloqueos de threads.
- **Sistema Anti-Desincronizaciones de Podman:**
  - **Serialización Mutex:** Las operaciones mutativas (`deploy`, `start`, `stop`, `restart`, `repair`) se ejecutan secuencialmente mediante un actor asíncrono en Rust (`tokio::sync::Mutex`), evitando los bloqueos de base de datos de almacenamiento (`storage.db locks`) de Podman.
  - **Inspección JSON Estructurada:** Lee directamente los estados de Podman mediante `--format json` e inspección profunda del infra-contenedor y los contenedores `mc-server`, `mc-playit` y `mc-ssh`.
  - **Reconciliación y Auto-Reparación:** Detecta automáticamente si el contenedor principal de Minecraft falló o el pod entró en estado `Degraded`, alertando al usuario y proporcionando una rutina de recuperación en 1 clic que limpia contenedores zombi y resincroniza el pod.
- **Control de Versionado de Minecraft:**
  - Conexión directa con la API oficial de Mojang (`piston-meta.mojang.com`) para consultar dinámicamente las últimas versiones estables (1.21.4, 1.20.4, 1.19.2, etc.) y snapshots.
- **Conectividad Flexible (IP Pública vs Playit.gg):**
  - **IP Pública:** Detección automática de IP Local (LAN) e IP Pública de internet. Incluye prueba de apertura automática mediante UPnP y guía interactiva paso a paso para abrir puertos en el router WiFi (TCP 25565, UDP 19132, TCP 2222).
  - **Túneles Playit.gg:** Contenedor `mc-playit` integrado con `SECRET_KEY` para jugar con amigos a través de internet sin abrir ningún puerto ni exponer tu dirección IP.
- **Elección del Motor de Servidor:**
  - **Vanilla Oficial:** Servidor oficial de Mojang.
  - **Plugins:** Paper (Recomendado), Purpur o Spigot.
  - **Mods:** Fabric, Forge, NeoForge o Quilt.
- **Crossplay Java + Bedrock Integrado:**
  - Inyección automática de GeyserMC, Floodgate y SkinsRestorer para que jugadores de consolas (Xbox, PlayStation, Nintendo Switch), móviles (Android, iOS) y Windows Bedrock jueguen en el mismo servidor junto a usuarios de Java.
- **Acceso Remoto SFTP / SSH:**
  - Contenedor `mc-ssh` con mapeo a `/servidor-mc` (`~/minecraft-server/data`) para subir mods, mundos, datapacks y plugins de forma inalámbrica desde tu PC principal mediante FileZilla o WinSCP.
- **Consola RCON Interactiva y Streaming de Logs:**
  - Envío en vivo de comandos de Minecraft (`op`, `whitelist`, `save-all`, `list`, `say`, etc.) con macros táctiles rápidas.
- **Protector de Pantalla OLED Anti-Quemado:**
  - Modo salvapantallas con fondo negro puro (`#000000`, apagando píxeles en la pantalla OLED de la consola) y animación rebotante estilo DVD/CRT para mantener el servidor corriendo indefinidamente sin desgaste de panel.

---

## 🏗 Arquitectura de Contenedores en Podman

La aplicación gestiona un único Pod de Podman en espacio de usuario rootless llamado `mc-pod` que mapea:
- `25565:25565` (Minecraft Java Edition TCP)
- `19132:19132/udp` (Minecraft Bedrock Edition UDP)
- `2222:2222` (Acceso SFTP / SSH TCP)

### Contenedores dentro de `mc-pod`:
1. **`mc-server` (`docker.io/itzg/minecraft-server:latest`):**
   - Ejecuta el motor de Minecraft con `--user 0:0` y mapeo de volumen persistente en `~/minecraft-server/data:/data:Z`.
2. **`mc-playit` (`ghcr.io/playit-cloud/playit-agent:latest`):**
   - Agente oficial de túnel Playit.gg activado si se introduce la clave secreta o se elige el modo túnel.
3. **`mc-ssh` (`lscr.io/linuxserver/openssh-server:latest`):**
   - Servidor SFTP para gestión inalámbrica de archivos.

---

## 🚀 Instalación en Steam Deck

### Paso 1: Cambiar al Modo Escritorio
1. Presiona el botón físico **STEAM** en tu Steam Deck.
2. Ve a **Encendido/Apagar (Power)** -> **Cambiar al Modo Escritorio (Switch to Desktop)**.

### Paso 2: Clonar y Ejecutar el Instalador
Abre **Konsole** (la terminal de SteamOS) y ejecuta:

```bash
git clone https://github.com/MOtaMore/mc_server-deck.git
cd mc_server-deck
chmod +x install.sh
./install.sh
```

El script compilará el backend en Rust, el frontend web moderno y registrará el acceso directo en tu Escritorio (`~/Desktop/MC-Server-Deck.desktop`).

---

## 🎮 Añadir a Steam (Gaming Mode)

1. En el Modo Escritorio, abre la aplicación **Steam**.
2. Haz clic en la barra superior en **Juegos (Games)** -> **Añadir un producto que no es de Steam a mi biblioteca...**.
3. Selecciona **MC Server-Deck** (o navega hasta `~/.local/share/mc-server-deck/mc-server-deck`).
4. Haz clic en **Añadir seleccionados**.
5. Regresa al **Modo Juego (Gaming Mode)**. ¡Encontrarás la app lista para usar con pantalla táctil a 1280x800!

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más detalles.
