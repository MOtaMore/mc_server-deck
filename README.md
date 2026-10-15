# 🎮 MC Server-Deck

**MC Server-Deck** es una aplicación de escritorio nativa con interfaz gráfica (GUI) diseñada específicamente para la **Steam Deck (SteamOS / Arch Linux)** en resolución nativa **1280x800**, totalmente compatible con la pantalla táctil y el trackpad/ratón.

Permite alojar y administrar servidores de Minecraft de alto rendimiento de forma autónoma utilizando contenedores **Podman en espacio de usuario (rootless)**, sin requerir permisos de superusuario (`sudo`) ni alterar el sistema de archivos inmutable de SteamOS.

---

## 🌟 Características Principales

- **Diseñado para Steam Deck (1280x800):** Interfaz oscura moderna basada en el diseño de SteamOS con botones táctiles grandes, fuentes de alta legibilidad y controles optimizados.
- **Protector de Pantalla OLED (Anti-Quemado CRT):** Modo salvapantallas con fondo negro 100% puro (`#000000`, píxeles OLED completamente apagados) y el icono de la aplicación rebotando estilo monitor de tubo CRT / logo DVD. Permite que la pantalla no sufra desgaste y el servidor continúe en ejecución sin que la consola se suspenda ni se apague.
- **Integración con Steam en 1 Clic:** Registra automáticamente la aplicación en `shortcuts.vdf` con portadas para la cuadrícula de Steam (Steam Grid Poster, Banner y Logo) para iniciarla directamente desde el Modo Juego (Gaming Mode).
- **Inhibición de Suspensión (Anti-Sleep):** Utiliza `systemd-inhibit` para que SteamOS no suspenda el sistema ni corte la conexión WiFi mientras el servidor esté activo.
- **Soporte de Teclado Virtual Steam:** Botón directo en la consola para invocar el teclado en pantalla oficial de Steam Deck sin necesidad de teclado físico.
- **Podman Rootless (`mc-pod`):** Todo se ejecuta en el espacio de usuario `/home/deck`. Cero permisos `sudo` requeridos.
- **Persistencia Segura de Datos:** Los mundos, configuraciones, mods y plugins se guardan de forma permanente en `/home/deck/minecraft-server/data`.
- **Actualización sin Pérdida de Mundos:** Puedes cambiar la versión de Minecraft, la memoria RAM asignada o el motor de servidor en cualquier momento desde el Asistente sin borrar tu progreso ni tu mapa.
- **Crossplay Java + Bedrock:** Compatible con GeyserMC, Floodgate y SkinsRestorer para que amigos en consolas (Xbox, PlayStation, Nintendo Switch), celulares (iOS, Android) y PC Windows 10/11 Bedrock jueguen en el mismo servidor junto a jugadores de Java.
- **Túnel Playit.gg Integrado:** Juega con tus amigos a través de Internet sin abrir puertos en el router WiFi de tu casa ni exponer tu IP pública.
- **Servidor SFTP / SSH Integrado:** Sube y descarga mods, mundos, datapacks y plugins de forma inalámbrica desde tu PC principal usando FileZilla, WinSCP o Cyberduck.
- **Consola RCON en Vivo:** Visualización fluida de logs del servidor en tiempo real y envío instantáneo de comandos de Minecraft (`op`, `whitelist`, `save-all`, `list`, etc.).
- **Botón de Emergencia para Permisos:** Corrección automática de permisos de archivo rootless (`podman unshare chown -R 0:0` y `chmod 777`).

---

## 🏗 Arquitectura de Contenedores

La aplicación gestiona un único Pod de Podman llamado `mc-pod` que mapea los puertos:
- `25565:25565` (Minecraft Java Edition TCP)
- `19132:19132/udp` (Minecraft Bedrock Edition UDP)
- `2222:2222` (Acceso SFTP / SSH TCP)

### Contenedores dentro de `mc-pod`:
1. **`mc-server` (`docker.io/itzg/minecraft-server:latest`):**
   - Corre con `--user 0:0` para garantizar que los archivos en `/home/deck/minecraft-server/data` pertenezcan al usuario `deck`.
   - Soporta Vanilla, Paper, Purpur, Spigot, Fabric, Forge, NeoForge y Quilt.
2. **`mc-playit` (`ghcr.io/playit-cloud/playit-agent:latest`):**
   - Agente oficial de Playit.gg configurado mediante la variable `SECRET_KEY`.
3. **`mc-ssh` (`lscr.io/linuxserver/openssh-server:latest`):**
   - Servidor SFTP para gestión de archivos con montaje de `/home/deck/minecraft-server/data:/servidor-mc:Z`.

---

## 🚀 Instalación en Steam Deck

### Paso 1: Ir al Modo Escritorio
1. Presiona el botón físico **STEAM** en tu Steam Deck.
2. Ve a **Encendido/Apagar (Power)** -> **Cambiar al Modo Escritorio (Switch to Desktop)**.

### Paso 2: Clonar y Ejecutar el Instalador
Abre **Konsole** (la terminal de SteamOS) y ejecuta los siguientes comandos:

```bash
git clone https://github.com/MOtaMore/mc_server-deck.git
cd mc_server-deck
chmod +x install.sh
./install.sh
```

El instalador automáticamente:
1. Comprueba la presencia de Python 3 y Podman.
2. Crea el entorno virtual en `~/.local/share/mc-server-deck/venv` e instala PyQt6.
3. Configura los permisos y la estructura de carpetas en `/home/deck/minecraft-server/`.
4. Crea los accesos directos en tu Escritorio (`~/Desktop/MC-Server-Deck.desktop`) y en el menú de aplicaciones.

---

## 🎮 Añadir a Steam (Gaming Mode)

Para ejecutar **MC Server-Deck** con los controles de la consola y la pantalla táctil en el Modo Juego:

1. En el Modo Escritorio, abre la aplicación de **Steam**.
2. En la barra superior, haz clic en **Juegos (Games)** -> **Añadir un producto que no es de Steam a mi biblioteca... (Add a Non-Steam Game...)**.
3. En la lista desplegable, busca y marca **MC Server-Deck**.
   *(Si no aparece, haz clic en "Buscar..." y selecciona `/home/deck/.local/share/mc-server-deck/run.sh`)*.
4. Haz clic en **Añadir seleccionados**.
5. Regresa al **Modo Juego (Return to Gaming Mode)** desde el acceso directo del escritorio.
6. ¡Encontrarás MC Server-Deck en tu biblioteca de Steam listo para ejecutarse a 1280x800!

---

## 📱 Pantallas y Uso de la Aplicación

### 1. Panel de Control y Consola en Vivo (Dashboard)
- **Monitoreo en Tiempo Real:** Indicadores visuales (Verde = Activo, Rojo = Detenido) para el Pod y cada uno de los contenedores.
- **Acciones Rápidas:**
  - `Iniciar Servidor`: Inicia el pod `mc-pod`.
  - `Detener Servidor`: Detención limpia y segura del pod.
  - `Reiniciar Servidor`: Reinicia los contenedores activos.
  - `Corregir Permisos`: Ejecuta la rutina `podman unshare chown -R 0:0` y `chmod 777` ante bloqueos de lectura/escritura.
- **Consola Interactiva:** Transmisión en vivo de los registros del servidor con casilla de auto-scroll.
- **Envío de Comandos RCON:** Campo de entrada con tecla Enter o botón de envío que ejecuta comandos directamente mediante `podman exec mc-server rcon-cli`.
- **Botones de Atajo:**
  - `Hacer OP`: Abre un diálogo táctil para ascender a un jugador.
  - `Whitelist Add (Java)`: Registra jugadores de Java en la lista blanca.
  - `Bedrock Whitelist`: Ejecuta `fwhitelist add <Gamertag>` para jugadores de consolas/móviles.
  - `Guardar Mundo`: Fuerza el guardado inmediato de chunks en disco (`save-all`).
  - `Ver Jugadores`: Muestra la lista de jugadores conectados (`list`).

### 2. Asistente de Configuración (Setup Wizard)
- **Versión de Minecraft:** Selector con versiones populares (`LATEST`, `1.21.4`, `1.20.4`, etc.) o entrada personalizada.
- **Memoria RAM:** Slider de 2G a 8G con indicador recomendado de 4G a 6G para respetar los 16 GB de RAM unificada de la Steam Deck.
- **Tipo de Servidor:**
  - **Vanilla:** Servidor oficial de Mojang.
  - **Plugins:** Paper (Recomendado), Purpur o Spigot.
  - **Mods:** Fabric, Forge, NeoForge o Quilt.
- **Crossplay Bedrock (Geyser + Floodgate):** Inyecta automáticamente los plugins oficiales de Geyser, Floodgate y SkinsRestorer.
- **Modo Online:** Alterna entre cuentas oficiales Premium o modo mixto (offline).
- **Túnel Playit.gg:** Campo para pegar la `SECRET_KEY` de tu agente de playit.
- **Servidor SFTP/SSH:** Permite activar el acceso remoto, configurar el usuario y la contraseña.
- **Guardar y Desplegar:** Recrea el contenedor `mc-server` con las nuevas configuraciones preservando al 100% tus mundos en la carpeta de datos.

### 3. Guía de Conexión y Red
- Muestra la dirección IP local de tu Steam Deck (`192.168.x.x`) para conectarse fácilmente dentro del hogar.
- Tarjetas con instrucciones paso a paso para Java, Bedrock, Playit y FileZilla.

---

## 🛠 Comandos Útiles de Podman (Terminal)

Si deseas inspeccionar el servidor manualmente desde la consola:

```bash
# Ver estado del pod y contenedores
podman pod ps
podman ps -a

# Ver registros en vivo del servidor
podman logs -f mc-server

# Entrar a la consola RCON manualmente
podman exec -it mc-server rcon-cli

# Iniciar o detener todo el pod
podman pod start mc-pod
podman pod stop mc-pod
```

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más detalles.
