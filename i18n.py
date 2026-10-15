"""
MC Server-Deck - Motor de Internacionalización (i18n)
Soporte multilenguaje para Español (ES), English (EN), Português (PT) y Français (FR).
"""

from typing import Dict, Any

LANGUAGES = {
    "es": "Español",
    "en": "English",
    "pt": "Português",
    "fr": "Français",
}

# Diccionario completo de traducciones
TRANSLATIONS: Dict[str, Dict[str, str]] = {
    # -------------------------------------------------------------------------
    # ESPAÑOL
    # -------------------------------------------------------------------------
    "es": {
        # General / Header
        "app_title": "🎮 MC Server-Deck",
        "edition_badge": "STEAM DECK EDITION",
        "podman_active": "PODMAN ROOTLESS: ACTIVO",
        "podman_missing": "PODMAN: NO ENCONTRADO",
        "btn_oled_mode": "🌙 Modo OLED",
        "btn_oled_tooltip": "Activa el protector de pantalla rebotante anti-quemado OLED sobre negro puro.\nMantiene el servidor activo y la pantalla protegida sin apagar la consola.",
        "btn_add_steam": "➕ Añadir a Steam",
        "btn_add_steam_tooltip": "Registra MC Server-Deck con icono y carátulas en tu biblioteca de Steam\npara que aparezca en el Modo Juego (Gaming Mode).",
        "tab_dashboard": "🎮 Panel de Control y Consola",
        "tab_setup": "⚙️ Configurar Servidor (Asistente)",
        "tab_guide": "📖 Guía de Conexión & Red",
        "status_footer": "Directorio de datos: {data_dir}  |  Espacio de usuario: /home/deck  |  Puertos: 25565 (Java), 19132 (Bedrock)",
        "server_deployed_msg": "✔ Servidor desplegado. Mostrando registros en vivo...",
        
        # Dashboard - Estados
        "status_pod_title": "Pod (Red y Contenedores):",
        "status_server_title": "Servidor Minecraft (itzg):",
        "status_playit_title": "Túnel Playit.gg:",
        "status_ssh_title": "Acceso SFTP / SSH:",
        "status_checking": "Comprobando...",
        "st_active": "ACTIVO",
        "st_stopped": "DETENIDO",
        "st_degraded": "DEGRADADO",
        "st_online": "ONLINE",
        "st_offline": "OFFLINE",
        "st_connected": "CONECTADO",
        "st_inactive": "NO ACTIVO",
        "st_disabled": "DESACTIVADO",
        "st_not_created": "NO CREADO",
        "st_unknown": "DESCONOCIDO",
        
        # Dashboard - Acciones
        "btn_start_server": "▶ Iniciar Servidor",
        "btn_stop_server": "⏹ Detener Servidor",
        "btn_restart_server": "🔄 Reiniciar Servidor",
        "btn_fix_perms": "🔧 Corregir Permisos",
        "btn_fix_perms_tooltip": "Ejecuta podman unshare chown -R 0:0 y chmod 777 para reparar errores de permisos en /home/deck",
        
        # Dashboard - Consola
        "console_title": "🖥 Salida de Consola en Vivo (itzg mc-server)",
        "chk_autoscroll": "Auto-scroll",
        "btn_clear_console": "Limpiar Vista",
        "console_placeholder": "Escribe un comando de Minecraft (ej: list, time set day, weather clear, say ¡Hola!)...",
        "btn_keyboard": "⌨️ Teclado",
        "btn_keyboard_tooltip": "Abre el teclado virtual en pantalla de Steam Deck (o pulsa STEAM + X)",
        "btn_send_cmd": "Enviar Comando ↵",
        
        # Dashboard - Botones rápidos
        "btn_quick_op": "👑 Hacer OP",
        "btn_quick_op_tooltip": "Otorga permisos de operador a un jugador con 'op <nombre>'",
        "btn_quick_wl_java": "📋 Whitelist Add (Java)",
        "btn_quick_wl_java_tooltip": "Añade un jugador de Java a la lista blanca",
        "btn_quick_wl_bedrock": "🎮 Bedrock Whitelist (Floodgate)",
        "btn_quick_wl_bedrock_tooltip": "Añade un jugador de Bedrock con 'fwhitelist add <Gamertag>'",
        "btn_quick_save": "💾 Guardar Mundo",
        "btn_quick_save_tooltip": "Fuerza el guardado de los datos del mundo en disco con 'save-all'",
        "btn_quick_list": "👥 Ver Jugadores",
        "btn_quick_list_tooltip": "Muestra los jugadores conectados en la consola con 'list'",
        
        # Asistente (Setup Wizard)
        "wizard_banner_title": "Asistente de Servidor y Opciones de Despliegue",
        "wizard_banner_desc": "Crea un servidor nuevo o actualiza las opciones del actual. Tus mundos y archivos guardados en /home/deck/minecraft-server/data NUNCA se borrarán.",
        "lbl_version_title": "1. Versión de Minecraft (-e VERSION):",
        "custom_version_placeholder": "Ej: 1.21.1 ó snapshot...",
        "lbl_ram_title": "2. Memoria RAM Asignada (-e MEMORY):",
        "ram_recommended": "4G (Recomendado)",
        "ram_warning": "⚠️ Nota Steam Deck: Cuenta con 16 GB compartidos entre RAM y GPU. Se aconseja asignar 4G (Vanilla / Plugins) o 6G (Modpacks pesados) para evitar micro-tirones en Gaming Mode.",
        "lbl_type_title": "3. Motor del Servidor y Tipo de Software (-e TYPE):",
        "type_vanilla": "Vanilla (Mojang Oficial)",
        "type_plugins": "Plugins (Paper / Purpur / Spigot)",
        "type_mods": "Mods (Fabric / Forge / NeoForge / Quilt)",
        "lbl_specific_software": "Software específico:",
        "lbl_connectivity_title": "4. Conectividad, Crossplay y Reglas de Jugador:",
        "chk_crossplay": "Permitir Crossplay Java + Bedrock (GeyserMC + Floodgate + SkinsRestorer)",
        "crossplay_info": "ℹ Permite que amigos en Android, iOS, Xbox, PlayStation, Switch o Windows Bedrock se conecten directamente al mismo mundo que los de PC Java (Puerto 19132 UDP).",
        "btn_apply_floodgate": "🔄 Aplicar corrección 'auth-type: floodgate' en Geyser config",
        "lbl_auth_mode": "Modo de Autenticación:",
        "auth_premium": "Solo Cuentas Premium (ONLINE_MODE=TRUE)",
        "auth_offline": "Premium + No Premium / Offline (ONLINE_MODE=FALSE)",
        "chk_whitelist": "Activar Whitelist obligatoria (ENABLE_WHITELIST & ENFORCE_WHITELIST)",
        "lbl_playit_title": "5. Túnel Playit.gg (Jugar por Internet sin abrir puertos en el router):",
        "lbl_playit_key": "Playit Secret Key:",
        "playit_key_placeholder": "Pega aquí tu clave secreta de agente playit (opcional)",
        "btn_open_playit": "🌐 Panel Playit.gg",
        "playit_card_info": "📋 Puertos para configurar en la web de Playit.gg:\n  • Minecraft Java: Añade un túnel TCP apuntando al puerto local 25565\n  • Minecraft Bedrock: Añade un túnel UDP apuntando al puerto local 19132\n  • Servidor SFTP: Añade un túnel TCP apuntando al puerto local 2222",
        "chk_enable_ssh": "6. Habilitar contenedor SSH / SFTP (Para subir mods y mundos con FileZilla / WinSCP)",
        "lbl_ssh_mode": "Modo de Acceso SFTP / SSH:",
        "ssh_mode_local": "🏠 Red Local / WiFi (IP directa de tu Steam Deck)",
        "ssh_mode_playit": "🌐 Por Internet vía Playit.gg (Túnel TCP puerto 2222 sin abrir puertos)",
        "lbl_ssh_user": "Usuario SSH:",
        "lbl_ssh_pass": "Contraseña SSH:",
        "ssh_info_local": "💡 Conexión SFTP local: Host: {ip} | Puerto: 2222 | Ruta remota: /servidor-mc",
        "ssh_info_playit": "💡 Conexión SFTP por Internet: Host: <tu-dominio-playit> | Puerto: <puerto-asignado-playit> | Ruta remota: /servidor-mc",
        "btn_deploy": "💾 Guardar y Desplegar Servidor en Steam Deck",
        
        # Guía de Conexión
        "guide_ip_title": "IP Local de tu Steam Deck en la Red:",
        "btn_refresh_ip": "Refrescar IP",
        "guide_java_title": "☕ Conectar desde Minecraft Java (PC / Mac / Linux)",
        "guide_java_body": "<b>En la misma red WiFi/Cable:</b><br>1. Abre Minecraft Java Edition.<br>2. Ve a <i>Multijugador -> Añadir Servidor</i>.<br>3. Dirección del servidor: <code>{ip}:25565</code>.<br>4. ¡Haz clic en Unirse al Servidor!",
        "guide_bedrock_title": "🎮 Conectar desde Bedrock (Xbox, Switch, PS4/5, Celular)",
        "guide_bedrock_body": "<b>Gracias a GeyserMC + Floodgate:</b><br>1. Abre Minecraft Bedrock.<br>2. Ve a la pestaña <i>Servidores -> Añadir Servidor</i>.<br>3. IP del Servidor: <code>{ip}</code>.<br>4. Puerto: <code>19132</code> (Puerto estándar de Bedrock).<br><i>(Nota: En consolas como Xbox o Switch puedes usar apps como BedrockTogether o DNS).</i>",
        "guide_playit_title": "🌐 Jugar por Internet con amigos (Sin abrir puertos)",
        "guide_playit_body": "1. Consigue tu <i>Secret Key</i> registrándote en <a style='color:#38bdf8;' href='https://playit.gg'>playit.gg</a>.<br>2. Pégala en la pestaña <b>Configurar Servidor</b> y guarda.<br>3. En tu panel de playit.gg crea un túnel:<br>   • TCP en puerto 25565 para Java.<br>   • UDP en puerto 19132 para Bedrock.<br>4. Comparte la dirección pública asignada (ej: <code>algo.craft.ply.gg</code>) a tus amigos.",
        "guide_sftp_title": "📁 Transferir Mods, Plugins y Mundos (SFTP)",
        "guide_sftp_body": "<b>Opciones de Conexión:</b><br>• <b>Opción A (Red Local WiFi):</b> Servidor: <code>{ip}</code> | Puerto: <code>2222</code> | Usuario: <code>{user}</code> | Carpeta: <code>/servidor-mc</code><br>• <b>Opción B (Internet vía Playit.gg):</b> Si configuraste un túnel TCP al puerto 2222 en playit, usa el dominio y puerto público de playit.<br>Compatible con <b>FileZilla</b>, <b>WinSCP</b> y <b>Cyberduck</b>.",
        "guide_tips_title": "🔋 Consejos para el Servidor en Steam Deck:",
        "guide_tips_body": "• <b>Protector de Pantalla OLED (Anti-Burn):</b> Para proteger la pantalla OLED de la Steam Deck contra quemados sin apagar el servidor, activa el <b>Modo OLED</b> (botón 🌙 superior). Utiliza fondo negro absoluto (0% emisión OLED con píxeles apagados) e icono rebotante tipo monitor CRT / DVD. Además, el sistema inhibe la suspensión de SteamOS para que nadie se desconecte.<br>• <b>Añadir a la Biblioteca de Steam:</b> Puedes registrar MC Server-Deck en tu biblioteca de Steam para el Modo Juego en un solo clic usando el botón <b>➕ Añadir a Steam</b> de la barra superior.<br>• <b>Modo de Energía:</b> Conecta el cargador oficial de 45W si vas a hospedar partidas largas con muchos amigos.<br>• <b>Teclado en Gaming Mode:</b> Pulsa el botón ⌨️ en la consola o el atajo <b>STEAM + X</b> para abrir el teclado virtual en pantalla.",

        # Diálogos y Modales
        "dlg_op_title": "Hacer Operador",
        "dlg_op_prompt": "Introduce el nombre del jugador para hacer OP:",
        "dlg_wl_java_title": "Añadir a Whitelist (Java)",
        "dlg_wl_java_prompt": "Nombre de usuario de Minecraft Java:",
        "dlg_wl_bedrock_title": "Añadir a Whitelist (Bedrock)",
        "dlg_wl_bedrock_prompt": "Gamertag del jugador de Bedrock (Xbox / Consola / Móvil):",
        "dlg_stop_title": "Detener Servidor",
        "dlg_stop_msg": "¿Deseas detener el servidor de Minecraft y todos sus servicios asociados?",
        "dlg_stop_btn": "Detener",
        "dlg_restart_title": "Reiniciar Servidor",
        "dlg_restart_msg": "¿Deseas reiniciar todos los contenedores de Minecraft?",
        "dlg_restart_btn": "Reiniciar",
        "dlg_confirm": "Confirmar",
        "dlg_cancel": "Cancelar",
        "dlg_close": "Finalizar",
        "dlg_deploy_title": "Desplegando Servidor de Minecraft...",
        "dlg_deploy_preparing": "Preparando contenedores en espacio de usuario...",
        "dlg_deploy_success": "✔ Despliegue completado con éxito",
        "dlg_deploy_error": "✖ Ocurrió un error en el despliegue",
        "screensaver_wake_hud": "MC Server-Deck  •  mc-server: {srv_st}  •  mc-pod: {pod_st}  •  (Toca para despertar)",
    },

    # -------------------------------------------------------------------------
    # ENGLISH
    # -------------------------------------------------------------------------
    "en": {
        # General / Header
        "app_title": "🎮 MC Server-Deck",
        "edition_badge": "STEAM DECK EDITION",
        "podman_active": "PODMAN ROOTLESS: ACTIVE",
        "podman_missing": "PODMAN: NOT FOUND",
        "btn_oled_mode": "🌙 OLED Mode",
        "btn_oled_tooltip": "Activates the CRT-style bouncing OLED anti-burn screensaver on pure black.\nKeeps the server running and screen protected without putting the console to sleep.",
        "btn_add_steam": "➕ Add to Steam",
        "btn_add_steam_tooltip": "Registers MC Server-Deck with icons and grid art in your Steam library\nso it appears in Gaming Mode.",
        "tab_dashboard": "🎮 Control Panel & Console",
        "tab_setup": "⚙️ Server Setup (Wizard)",
        "tab_guide": "📖 Connection & Network Guide",
        "status_footer": "Data directory: {data_dir}  |  User space: /home/deck  |  Ports: 25565 (Java), 19132 (Bedrock)",
        "server_deployed_msg": "✔ Server deployed. Streaming live logs...",

        # Dashboard - Statuses
        "status_pod_title": "Pod (Network & Containers):",
        "status_server_title": "Minecraft Server (itzg):",
        "status_playit_title": "Playit.gg Tunnel:",
        "status_ssh_title": "SFTP / SSH Access:",
        "status_checking": "Checking...",
        "st_active": "ACTIVE",
        "st_stopped": "STOPPED",
        "st_degraded": "DEGRADED",
        "st_online": "ONLINE",
        "st_offline": "OFFLINE",
        "st_connected": "CONNECTED",
        "st_inactive": "INACTIVE",
        "st_disabled": "DISABLED",
        "st_not_created": "NOT CREATED",
        "st_unknown": "UNKNOWN",

        # Dashboard - Actions
        "btn_start_server": "▶ Start Server",
        "btn_stop_server": "⏹ Stop Server",
        "btn_restart_server": "🔄 Restart Server",
        "btn_fix_perms": "🔧 Fix Permissions",
        "btn_fix_perms_tooltip": "Runs podman unshare chown -R 0:0 and chmod 777 to fix user permissions in /home/deck",

        # Dashboard - Console
        "console_title": "🖥 Live Console Output (itzg mc-server)",
        "chk_autoscroll": "Auto-scroll",
        "btn_clear_console": "Clear Output",
        "console_placeholder": "Type a Minecraft command (e.g. list, time set day, weather clear, say Hello!)...",
        "btn_keyboard": "⌨️ Keyboard",
        "btn_keyboard_tooltip": "Opens Steam Deck on-screen virtual keyboard (or press STEAM + X)",
        "btn_send_cmd": "Send Command ↵",

        # Dashboard - Quick Buttons
        "btn_quick_op": "👑 Make OP",
        "btn_quick_op_tooltip": "Grants operator permissions with 'op <player>'",
        "btn_quick_wl_java": "📋 Whitelist Add (Java)",
        "btn_quick_wl_java_tooltip": "Adds a Java player to whitelist",
        "btn_quick_wl_bedrock": "🎮 Bedrock Whitelist (Floodgate)",
        "btn_quick_wl_bedrock_tooltip": "Adds a Bedrock player with 'fwhitelist add <Gamertag>'",
        "btn_quick_save": "💾 Save World",
        "btn_quick_save_tooltip": "Forces disk chunk write with 'save-all'",
        "btn_quick_list": "👥 List Players",
        "btn_quick_list_tooltip": "Shows online players in console with 'list'",

        # Setup Wizard
        "wizard_banner_title": "Server Setup & Deployment Wizard",
        "wizard_banner_desc": "Create a new server or update current settings. Your worlds and saved files in /home/deck/minecraft-server/data will NEVER be erased.",
        "lbl_version_title": "1. Minecraft Version (-e VERSION):",
        "custom_version_placeholder": "E.g. 1.21.1 or snapshot...",
        "lbl_ram_title": "2. Allocated RAM Memory (-e MEMORY):",
        "ram_recommended": "4G (Recommended)",
        "ram_warning": "⚠️ Steam Deck Note: Features 16 GB shared between RAM and GPU. 4G (Vanilla/Plugins) or 6G (heavy Modpacks) is recommended to avoid stutter in Gaming Mode.",
        "lbl_type_title": "3. Server Engine & Software Type (-e TYPE):",
        "type_vanilla": "Vanilla (Official Mojang)",
        "type_plugins": "Plugins (Paper / Purpur / Spigot)",
        "type_mods": "Mods (Fabric / Forge / NeoForge / Quilt)",
        "lbl_specific_software": "Specific software:",
        "lbl_connectivity_title": "4. Connectivity, Crossplay & Player Rules:",
        "chk_crossplay": "Enable Java + Bedrock Crossplay (GeyserMC + Floodgate + SkinsRestorer)",
        "crossplay_info": "ℹ Allows friends on Android, iOS, Xbox, PlayStation, Switch or Windows Bedrock to join the same world as PC Java players (Port 19132 UDP).",
        "btn_apply_floodgate": "🔄 Apply 'auth-type: floodgate' fix in Geyser config",
        "lbl_auth_mode": "Authentication Mode:",
        "auth_premium": "Premium Accounts Only (ONLINE_MODE=TRUE)",
        "auth_offline": "Premium + Non-Premium / Offline (ONLINE_MODE=FALSE)",
        "chk_whitelist": "Enforce Whitelist (ENABLE_WHITELIST & ENFORCE_WHITELIST)",
        "lbl_playit_title": "5. Playit.gg Tunnel (Play over the Internet without port forwarding):",
        "lbl_playit_key": "Playit Secret Key:",
        "playit_key_placeholder": "Paste your Playit agent secret key here (optional)",
        "btn_open_playit": "🌐 Playit.gg Dashboard",
        "playit_card_info": "📋 Ports to configure on Playit.gg web dashboard:\n  • Minecraft Java: Add a TCP tunnel pointing to local port 25565\n  • Minecraft Bedrock: Add a UDP tunnel pointing to local port 19132\n  • SFTP Server: Add a TCP tunnel pointing to local port 2222",
        "chk_enable_ssh": "6. Enable SSH / SFTP container (To upload mods & worlds with FileZilla / WinSCP)",
        "lbl_ssh_mode": "SFTP / SSH Access Mode:",
        "ssh_mode_local": "🏠 Local Network / WiFi (Direct Steam Deck IP)",
        "ssh_mode_playit": "🌐 Over Internet via Playit.gg (Port 2222 TCP tunnel without port forwarding)",
        "lbl_ssh_user": "SSH User:",
        "lbl_ssh_pass": "SSH Password:",
        "ssh_info_local": "💡 Local SFTP Connection: Host: {ip} | Port: 2222 | Remote path: /servidor-mc",
        "ssh_info_playit": "💡 Internet SFTP Connection: Host: <your-playit-domain> | Port: <assigned-playit-port> | Remote path: /servidor-mc",
        "btn_deploy": "💾 Save & Deploy Server on Steam Deck",

        # Connection Guide
        "guide_ip_title": "Local IP Address of your Steam Deck on the Network:",
        "btn_refresh_ip": "Refresh IP",
        "guide_java_title": "☕ Connecting from Minecraft Java (PC / Mac / Linux)",
        "guide_java_body": "<b>On the same WiFi/Ethernet network:</b><br>1. Open Minecraft Java Edition.<br>2. Go to <i>Multiplayer -> Add Server</i>.<br>3. Server Address: <code>{ip}:25565</code>.<br>4. Click Join Server!",
        "guide_bedrock_title": "🎮 Connecting from Bedrock (Xbox, Switch, PS4/5, Mobile)",
        "guide_bedrock_body": "<b>Powered by GeyserMC + Floodgate:</b><br>1. Open Minecraft Bedrock.<br>2. Go to <i>Servers -> Add Server</i>.<br>3. Server IP: <code>{ip}</code>.<br>4. Port: <code>19132</code> (Standard Bedrock port).<br><i>(Note: On consoles like Xbox or Switch you can use BedrockTogether or DNS).</i>",
        "guide_playit_title": "🌐 Playing over the Internet with friends (No port forwarding)",
        "guide_playit_body": "1. Get your <i>Secret Key</i> by registering at <a style='color:#38bdf8;' href='https://playit.gg'>playit.gg</a>.<br>2. Paste it in <b>Server Setup</b> tab and save.<br>3. In your playit.gg panel create tunnels:<br>   • TCP on port 25565 for Java.<br>   • UDP on port 19132 for Bedrock.<br>4. Share the assigned public address (e.g.: <code>something.craft.ply.gg</code>) with friends.",
        "guide_sftp_title": "📁 Transferring Mods, Plugins & Worlds (SFTP)",
        "guide_sftp_body": "<b>Connection Options:</b><br>• <b>Option A (Local WiFi Network):</b> Server: <code>{ip}</code> | Port: <code>2222</code> | User: <code>{user}</code> | Directory: <code>/servidor-mc</code><br>• <b>Option B (Internet via Playit.gg):</b> If you set up a TCP tunnel for port 2222 on Playit, use Playit's public address and port.<br>Compatible with <b>FileZilla</b>, <b>WinSCP</b> and <b>Cyberduck</b>.",
        "guide_tips_title": "🔋 Steam Deck Server Tips:",
        "guide_tips_body": "• <b>OLED Screen Saver (Anti-Burn):</b> To protect Steam Deck OLED screen against burn-in without turning off the server, activate <b>OLED Mode</b> (🌙 top button). Uses pure black (0% emission with OLED pixels turned off) and bouncing CRT / DVD logo. System sleep is inhibited so nobody disconnects.<br>• <b>Add to Steam Library:</b> Register MC Server-Deck in your Steam library for Gaming Mode in one click using the <b>➕ Add to Steam</b> top button.<br>• <b>Power Mode:</b> Connect the official 45W charger for long gaming sessions.<br>• <b>Gaming Mode Keyboard:</b> Tap the ⌨️ button in console or press <b>STEAM + X</b> to bring up the on-screen keyboard.",

        # Dialogs & Modals
        "dlg_op_title": "Make Operator",
        "dlg_op_prompt": "Enter player name to give OP permissions:",
        "dlg_wl_java_title": "Add to Whitelist (Java)",
        "dlg_wl_java_prompt": "Minecraft Java username:",
        "dlg_wl_bedrock_title": "Add to Whitelist (Bedrock)",
        "dlg_wl_bedrock_prompt": "Bedrock player Gamertag (Xbox / Console / Mobile):",
        "dlg_stop_title": "Stop Server",
        "dlg_stop_msg": "Do you want to stop the Minecraft server and its associated services?",
        "dlg_stop_btn": "Stop",
        "dlg_restart_title": "Restart Server",
        "dlg_restart_msg": "Do you want to restart all Minecraft containers?",
        "dlg_restart_btn": "Restart",
        "dlg_confirm": "Confirm",
        "dlg_cancel": "Cancel",
        "dlg_close": "Finish",
        "dlg_deploy_title": "Deploying Minecraft Server...",
        "dlg_deploy_preparing": "Preparing user-space containers...",
        "dlg_deploy_success": "✔ Deployment completed successfully",
        "dlg_deploy_error": "✖ An error occurred during deployment",
        "screensaver_wake_hud": "MC Server-Deck  •  mc-server: {srv_st}  •  mc-pod: {pod_st}  •  (Touch to wake)",
    },

    # -------------------------------------------------------------------------
    # PORTUGUÊS
    # -------------------------------------------------------------------------
    "pt": {
        # General / Header
        "app_title": "🎮 MC Server-Deck",
        "edition_badge": "STEAM DECK EDITION",
        "podman_active": "PODMAN ROOTLESS: ATIVO",
        "podman_missing": "PODMAN: NÃO ENCONTRADO",
        "btn_oled_mode": "🌙 Modo OLED",
        "btn_oled_tooltip": "Ativa o protetor de tela saltitante anti-burn OLED sobre preto puro.\nMantém o servidor ativo e a tela protegida sem desligar o console.",
        "btn_add_steam": "➕ Adicionar à Steam",
        "btn_add_steam_tooltip": "Registra o MC Server-Deck com ícones e capas na sua biblioteca da Steam\npara que apareça no Modo Jogo (Gaming Mode).",
        "tab_dashboard": "🎮 Painel de Controle e Console",
        "tab_setup": "⚙️ Configurar Servidor (Assistente)",
        "tab_guide": "📖 Guia de Conexão e Rede",
        "status_footer": "Diretório de dados: {data_dir}  |  Espaço de usuário: /home/deck  |  Portas: 25565 (Java), 19132 (Bedrock)",
        "server_deployed_msg": "✔ Servidor implantado. Transmitindo registros ao vivo...",

        # Dashboard - Estados
        "status_pod_title": "Pod (Rede e Contêineres):",
        "status_server_title": "Servidor Minecraft (itzg):",
        "status_playit_title": "Túnel Playit.gg:",
        "status_ssh_title": "Acesso SFTP / SSH:",
        "status_checking": "Verificando...",
        "st_active": "ATIVO",
        "st_stopped": "PARADO",
        "st_degraded": "DEGRADADO",
        "st_online": "ONLINE",
        "st_offline": "OFFLINE",
        "st_connected": "CONECTADO",
        "st_inactive": "INATIVO",
        "st_disabled": "DESATIVADO",
        "st_not_created": "NÃO CRIADO",
        "st_unknown": "DESCONHECIDO",

        # Dashboard - Ações
        "btn_start_server": "▶ Iniciar Servidor",
        "btn_stop_server": "⏹ Parar Servidor",
        "btn_restart_server": "🔄 Reiniciar Servidor",
        "btn_fix_perms": "🔧 Corrigir Permissões",
        "btn_fix_perms_tooltip": "Executa podman unshare chown -R 0:0 e chmod 777 para corrigir permissões em /home/deck",

        # Dashboard - Console
        "console_title": "🖥 Saída do Console ao Vivo (itzg mc-server)",
        "chk_autoscroll": "Rolagem automática",
        "btn_clear_console": "Limpar Vista",
        "console_placeholder": "Digite um comando do Minecraft (ex: list, time set day, weather clear, say Olá!)...",
        "btn_keyboard": "⌨️ Teclado",
        "btn_keyboard_tooltip": "Abre o teclado virtual na tela do Steam Deck (ou pressione STEAM + X)",
        "btn_send_cmd": "Enviar Comando ↵",

        # Dashboard - Botões rápidos
        "btn_quick_op": "👑 Tornar OP",
        "btn_quick_op_tooltip": "Concede permissões de operador com 'op <nome>'",
        "btn_quick_wl_java": "📋 Whitelist Add (Java)",
        "btn_quick_wl_java_tooltip": "Adiciona jogador Java à lista branca",
        "btn_quick_wl_bedrock": "🎮 Bedrock Whitelist (Floodgate)",
        "btn_quick_wl_bedrock_tooltip": "Adiciona jogador Bedrock com 'fwhitelist add <Gamertag>'",
        "btn_quick_save": "💾 Salvar Mundo",
        "btn_quick_save_tooltip": "Força gravação do mundo no disco com 'save-all'",
        "btn_quick_list": "👥 Ver Jogadores",
        "btn_quick_list_tooltip": "Mostra jogadores conectados no console com 'list'",

        # Assistente (Setup Wizard)
        "wizard_banner_title": "Assistente de Configuração do Servidor",
        "wizard_banner_desc": "Crie um novo servidor ou atualize as opções atuais. Seus mundos e arquivos em /home/deck/minecraft-server/data NUNCA serão apagados.",
        "lbl_version_title": "1. Versão do Minecraft (-e VERSION):",
        "custom_version_placeholder": "Ex: 1.21.1 ou snapshot...",
        "lbl_ram_title": "2. Memória RAM Alocada (-e MEMORY):",
        "ram_recommended": "4G (Recomendado)",
        "ram_warning": "⚠️ Nota Steam Deck: Possui 16 GB compartilhados entre RAM e GPU. Recomenda-se 4G (Vanilla/Plugins) ou 6G (Modpacks pesados) para evitar travamentos no Modo Jogo.",
        "lbl_type_title": "3. Motor do Servidor e Tipo de Software (-e TYPE):",
        "type_vanilla": "Vanilla (Oficial Mojang)",
        "type_plugins": "Plugins (Paper / Purpur / Spigot)",
        "type_mods": "Mods (Fabric / Forge / NeoForge / Quilt)",
        "lbl_specific_software": "Software específico:",
        "lbl_connectivity_title": "4. Conectividade, Crossplay e Regras de Jogador:",
        "chk_crossplay": "Permitir Crossplay Java + Bedrock (GeyserMC + Floodgate + SkinsRestorer)",
        "crossplay_info": "ℹ Permite que amigos no Android, iOS, Xbox, PlayStation, Switch ou Windows Bedrock entrem no mesmo mundo que jogadores de PC Java (Porta 19132 UDP).",
        "btn_apply_floodgate": "🔄 Aplicar correção 'auth-type: floodgate' no Geyser config",
        "lbl_auth_mode": "Modo de Autenticação:",
        "auth_premium": "Apenas Contas Premium (ONLINE_MODE=TRUE)",
        "auth_offline": "Premium + Não-Premium / Offline (ONLINE_MODE=FALSE)",
        "chk_whitelist": "Ativar Whitelist obrigatória (ENABLE_WHITELIST & ENFORCE_WHITELIST)",
        "lbl_playit_title": "5. Túnel Playit.gg (Jogar pela Internet sem abrir portas no roteador):",
        "lbl_playit_key": "Playit Secret Key:",
        "playit_key_placeholder": "Cole sua chave secreta de agente playit aqui (opcional)",
        "btn_open_playit": "🌐 Painel Playit.gg",
        "playit_card_info": "📋 Portas para configurar no painel web do Playit.gg:\n  • Minecraft Java: Adicione um túnel TCP apontando para a porta local 25565\n  • Minecraft Bedrock: Adicione um túnel UDP apontando para a porta local 19132\n  • Servidor SFTP: Adicione um túnel TCP apontando para a porta local 2222",
        "chk_enable_ssh": "6. Habilitar contêiner SSH / SFTP (Para enviar mods e mundos com FileZilla / WinSCP)",
        "lbl_ssh_mode": "Modo de Acesso SFTP / SSH:",
        "ssh_mode_local": "🏠 Rede Local / Wi-Fi (IP direto do seu Steam Deck)",
        "ssh_mode_playit": "🌐 Pela Internet via Playit.gg (Túnel TCP porta 2222 sem abrir portas)",
        "lbl_ssh_user": "Usuário SSH:",
        "lbl_ssh_pass": "Senha SSH:",
        "ssh_info_local": "💡 Conexão SFTP local: Host: {ip} | Porta: 2222 | Caminho remoto: /servidor-mc",
        "ssh_info_playit": "💡 Conexão SFTP Internet: Host: <seu-dominio-playit> | Porta: <porta-designada-playit> | Caminho remoto: /servidor-mc",
        "btn_deploy": "💾 Salvar e Implantar Servidor no Steam Deck",

        # Guia de Conexão
        "guide_ip_title": "IP Local do seu Steam Deck na Rede:",
        "btn_refresh_ip": "Atualizar IP",
        "guide_java_title": "☕ Conectar pelo Minecraft Java (PC / Mac / Linux)",
        "guide_java_body": "<b>Na mesma rede Wi-Fi/Cabo:</b><br>1. Abra o Minecraft Java Edition.<br>2. Vá em <i>Multijogador -> Adicionar Servidor</i>.<br>3. Endereço do servidor: <code>{ip}:25565</code>.<br>4. Clique em Entrar no Servidor!",
        "guide_bedrock_title": "🎮 Conectar pelo Bedrock (Xbox, Switch, PS4/5, Celular)",
        "guide_bedrock_body": "<b>Com GeyserMC + Floodgate:</b><br>1. Abra o Minecraft Bedrock.<br>2. Vá na aba <i>Servidores -> Adicionar Servidor</i>.<br>3. IP do Servidor: <code>{ip}</code>.<br>4. Porta: <code>19132</code> (Porta padrão do Bedrock).<br><i>(Nota: Em consoles como Xbox ou Switch você pode usar apps como BedrockTogether ou DNS).</i>",
        "guide_playit_title": "🌐 Jogar pela Internet com amigos (Sem abrir portas)",
        "guide_playit_body": "1. Obtenha sua <i>Secret Key</i> registrando-se em <a style='color:#38bdf8;' href='https://playit.gg'>playit.gg</a>.<br>2. Cole na aba <b>Configurar Servidor</b> e salve.<br>3. No painel do playit crie os túneis:<br>   • TCP na porta 25565 para Java.<br>   • UDP na porta 19132 para Bedrock.<br>4. Compartilhe o endereço público com seus amigos.",
        "guide_sftp_title": "📁 Transferir Mods, Plugins e Mundos (SFTP)",
        "guide_sftp_body": "<b>Opções de Conexão:</b><br>• <b>Opção A (Rede Local Wi-Fi):</b> Servidor: <code>{ip}</code> | Porta: <code>2222</code> | Usuário: <code>{user}</code> | Pasta: <code>/servidor-mc</code><br>• <b>Opção B (Internet via Playit.gg):</b> Se configurou um túnel TCP para a porta 2222 no Playit, use o domínio e porta pública do Playit.<br>Compatível com <b>FileZilla</b>, <b>WinSCP</b> e <b>Cyberduck</b>.",
        "guide_tips_title": "🔋 Dicas para o Servidor no Steam Deck:",
        "guide_tips_body": "• <b>Protetor de Tela OLED (Anti-Burn):</b> Para proteger a tela OLED do Steam Deck contra queima sem desligar o servidor, ative o <b>Modo OLED</b> (botão 🌙 superior). Usa fundo preto puro (0% emissão com pixels desligados) e ícone saltitante tipo monitor CRT / DVD. A suspensão é inibida para ninguém ser desconectado.<br>• <b>Adicionar à Biblioteca da Steam:</b> Registre o MC Server-Deck no Modo Jogo em um clique usando o botão <b>➕ Adicionar à Steam</b>.<br>• <b>Modo de Energia:</b> Conecte o carregador oficial de 45W para sessões longas.<br>• <b>Teclado no Gaming Mode:</b> Toque no botão ⌨️ no console ou pressione <b>STEAM + X</b> para abrir o teclado virtual.",

        # Diálogos
        "dlg_op_title": "Tornar Operador",
        "dlg_op_prompt": "Digite o nome do jogador para dar OP:",
        "dlg_wl_java_title": "Adicionar à Whitelist (Java)",
        "dlg_wl_java_prompt": "Nome de usuário do Minecraft Java:",
        "dlg_wl_bedrock_title": "Adicionar à Whitelist (Bedrock)",
        "dlg_wl_bedrock_prompt": "Gamertag do jogador Bedrock (Xbox / Console / Celular):",
        "dlg_stop_title": "Parar Servidor",
        "dlg_stop_msg": "Deseja parar o servidor de Minecraft e todos os serviços associados?",
        "dlg_stop_btn": "Parar",
        "dlg_restart_title": "Reiniciar Servidor",
        "dlg_restart_msg": "Deseja reiniciar todos os contêineres do Minecraft?",
        "dlg_restart_btn": "Reiniciar",
        "dlg_confirm": "Confirmar",
        "dlg_cancel": "Cancelar",
        "dlg_close": "Finalizar",
        "dlg_deploy_title": "Implantando Servidor Minecraft...",
        "dlg_deploy_preparing": "Preparando contêineres em espaço de usuário...",
        "dlg_deploy_success": "✔ Implantação concluída com sucesso",
        "dlg_deploy_error": "✖ Ocorreu um erro na implantação",
        "screensaver_wake_hud": "MC Server-Deck  •  mc-server: {srv_st}  •  mc-pod: {pod_st}  •  (Toque para acordar)",
    },

    # -------------------------------------------------------------------------
    # FRANÇAIS
    # -------------------------------------------------------------------------
    "fr": {
        # General / Header
        "app_title": "🎮 MC Server-Deck",
        "edition_badge": "STEAM DECK EDITION",
        "podman_active": "PODMAN ROOTLESS : ACTIF",
        "podman_missing": "PODMAN : INTROUVABLE",
        "btn_oled_mode": "🌙 Mode OLED",
        "btn_oled_tooltip": "Active l'économiseur d'écran OLED anti-marquage style écran cathodique sur noir absolu.\nConserve le serveur actif et protège l'écran sans mettre la console en veille.",
        "btn_add_steam": "➕ Ajouter à Steam",
        "btn_add_steam_tooltip": "Enregistre MC Server-Deck avec ses jaquettes dans votre bibliothèque Steam\npour qu'il apparaisse dans le Mode Jeu (Gaming Mode).",
        "tab_dashboard": "🎮 Panneau de Contrôle & Console",
        "tab_setup": "⚙️ Configuration du Serveur (Assistant)",
        "tab_guide": "📖 Guide de Connexion & Réseau",
        "status_footer": "Dossier de données : {data_dir}  |  Espace utilisateur : /home/deck  |  Ports : 25565 (Java), 19132 (Bedrock)",
        "server_deployed_msg": "✔ Serveur déployé. Diffusion des journaux en direct...",

        # Dashboard - États
        "status_pod_title": "Pod (Réseau et Conteneurs) :",
        "status_server_title": "Serveur Minecraft (itzg) :",
        "status_playit_title": "Tunnel Playit.gg :",
        "status_ssh_title": "Accès SFTP / SSH :",
        "status_checking": "Vérification...",
        "st_active": "ACTIF",
        "st_stopped": "ARRÊTÉ",
        "st_degraded": "DÉGRADÉ",
        "st_online": "EN LIGNE",
        "st_offline": "HORS LIGNE",
        "st_connected": "CONNECTÉ",
        "st_inactive": "INACTIF",
        "st_disabled": "DÉSACTIVÉ",
        "st_not_created": "NON CRÉÉ",
        "st_unknown": "INCONNU",

        # Dashboard - Actions
        "btn_start_server": "▶ Démarrer Serveur",
        "btn_stop_server": "⏹ Arrêter Serveur",
        "btn_restart_server": "🔄 Redémarrer Serveur",
        "btn_fix_perms": "🔧 Réparer Permissions",
        "btn_fix_perms_tooltip": "Exécute podman unshare chown -R 0:0 et chmod 777 pour réparer les permissions dans /home/deck",

        # Dashboard - Console
        "console_title": "🖥 Console en direct (itzg mc-server)",
        "chk_autoscroll": "Défilement auto",
        "btn_clear_console": "Effacer",
        "console_placeholder": "Entrez une commande Minecraft (ex: list, time set day, weather clear, say Bonjour !)...",
        "btn_keyboard": "⌨️ Clavier",
        "btn_keyboard_tooltip": "Ouvre le clavier virtuel de la Steam Deck (ou appuyez sur STEAM + X)",
        "btn_send_cmd": "Envoyer Commande ↵",

        # Dashboard - Boutons rapides
        "btn_quick_op": "👑 Nommer OP",
        "btn_quick_op_tooltip": "Accorde les privilèges d'opérateur avec 'op <pseudo>'",
        "btn_quick_wl_java": "📋 Whitelist Add (Java)",
        "btn_quick_wl_java_tooltip": "Ajoute un joueur Java à la liste blanche",
        "btn_quick_wl_bedrock": "🎮 Bedrock Whitelist (Floodgate)",
        "btn_quick_wl_bedrock_tooltip": "Ajoute un joueur Bedrock avec 'fwhitelist add <Gamertag>'",
        "btn_quick_save": "💾 Sauvegarder Monde",
        "btn_quick_save_tooltip": "Force l'écriture du monde sur disque avec 'save-all'",
        "btn_quick_list": "👥 Voir Joueurs",
        "btn_quick_list_tooltip": "Affiche les joueurs connectés avec 'list'",

        # Assistant de configuration
        "wizard_banner_title": "Assistant de Déploiement et Configuration",
        "wizard_banner_desc": "Créez un nouveau serveur ou mettez à jour la configuration actuelle. Vos mondes et fichiers dans /home/deck/minecraft-server/data ne seront JAMAIS effacés.",
        "lbl_version_title": "1. Version de Minecraft (-e VERSION) :",
        "custom_version_placeholder": "Ex: 1.21.1 ou snapshot...",
        "lbl_ram_title": "2. Mémoire RAM Allouée (-e MEMORY) :",
        "ram_recommended": "4G (Recommandé)",
        "ram_warning": "⚠️ Note Steam Deck : Partage 16 Go entre RAM et GPU. Il est recommandé d'allouer 4G (Vanilla/Plugins) ou 6G (Modpacks lourds) pour éviter les ralentissements.",
        "lbl_type_title": "3. Moteur de Serveur & Logiciel (-e TYPE) :",
        "type_vanilla": "Vanilla (Officiel Mojang)",
        "type_plugins": "Plugins (Paper / Purpur / Spigot)",
        "type_mods": "Mods (Fabric / Forge / NeoForge / Quilt)",
        "lbl_specific_software": "Logiciel spécifique :",
        "lbl_connectivity_title": "4. Connectivité, Crossplay & Règles de Jeu :",
        "chk_crossplay": "Autoriser Crossplay Java + Bedrock (GeyserMC + Floodgate + SkinsRestorer)",
        "crossplay_info": "ℹ Permet aux amis sur Android, iOS, Xbox, PlayStation, Switch ou Windows Bedrock de rejoindre le même monde que les joueurs PC Java (Port 19132 UDP).",
        "btn_apply_floodgate": "🔄 Appliquer le correctif 'auth-type: floodgate' dans Geyser config",
        "lbl_auth_mode": "Mode d'Authentification :",
        "auth_premium": "Comptes Premium Uniquement (ONLINE_MODE=TRUE)",
        "auth_offline": "Premium + Non-Premium / Hors-ligne (ONLINE_MODE=FALSE)",
        "chk_whitelist": "Activer la Whitelist obligatoire (ENABLE_WHITELIST & ENFORCE_WHITELIST)",
        "lbl_playit_title": "5. Tunnel Playit.gg (Jouer en ligne sans ouvrir les ports de la box) :",
        "lbl_playit_key": "Playit Secret Key :",
        "playit_key_placeholder": "Collez votre clé secrète Playit ici (facultatif)",
        "btn_open_playit": "🌐 Tableau de bord Playit.gg",
        "playit_card_info": "📋 Ports à configurer sur Playit.gg :\n  • Minecraft Java : Ajoutez un tunnel TCP vers le port local 25565\n  • Minecraft Bedrock : Ajoutez un tunnel UDP vers le port local 19132\n  • Serveur SFTP : Ajoutez un tunnel TCP vers le port local 2222",
        "chk_enable_ssh": "6. Activer le conteneur SSH / SFTP (Pour transférer mods et mondes via FileZilla / WinSCP)",
        "lbl_ssh_mode": "Mode d'Accès SFTP / SSH :",
        "ssh_mode_local": "🏠 Réseau Local / Wi-Fi (IP directe de votre Steam Deck)",
        "ssh_mode_playit": "🌐 Via Internet avec Playit.gg (Tunnel TCP port 2222 sans redirection de port)",
        "lbl_ssh_user": "Utilisateur SSH :",
        "lbl_ssh_pass": "Mot de passe SSH :",
        "ssh_info_local": "💡 Connexion SFTP locale : Hôte : {ip} | Port : 2222 | Dossier distant : /servidor-mc",
        "ssh_info_playit": "💡 Connexion SFTP Internet : Hôte : <votre-domaine-playit> | Port : <port-playit> | Dossier distant : /servidor-mc",
        "btn_deploy": "💾 Sauvegarder et Déployer le Serveur sur Steam Deck",

        # Guide de Connexion
        "guide_ip_title": "Adresse IP Locale de votre Steam Deck sur le Réseau :",
        "btn_refresh_ip": "Rafraîchir IP",
        "guide_java_title": "☕ Connexion depuis Minecraft Java (PC / Mac / Linux)",
        "guide_java_body": "<b>Sur le même réseau Wi-Fi/Câble :</b><br>1. Ouvrez Minecraft Java Edition.<br>2. Allez dans <i>Multijoueur -> Nouveau Serveur</i>.<br>3. Adresse du serveur : <code>{ip}:25565</code>.<br>4. Cliquez sur Rejoindre !",
        "guide_bedrock_title": "🎮 Connexion depuis Bedrock (Xbox, Switch, PS4/5, Mobile)",
        "guide_bedrock_body": "<b>Grâce à GeyserMC + Floodgate :</b><br>1. Ouvrez Minecraft Bedrock.<br>2. Allez dans l'onglet <i>Serveurs -> Ajouter un serveur</i>.<br>3. IP du serveur : <code>{ip}</code>.<br>4. Port : <code>19132</code> (Port standard Bedrock).<br><i>(Note : Sur console Xbox ou Switch, utilisez BedrockTogether ou DNS).</i>",
        "guide_playit_title": "🌐 Jouer par Internet avec des amis (Sans ouvrir de ports)",
        "guide_playit_body": "1. Obtenez votre <i>Secret Key</i> sur <a style='color:#38bdf8;' href='https://playit.gg'>playit.gg</a>.<br>2. Collez-la dans l'onglet <b>Configuration du Serveur</b> et sauvegardez.<br>3. Dans Playit créez les tunnels :<br>   • TCP port 25565 pour Java.<br>   • UDP port 19132 pour Bedrock.<br>4. Partagez l'adresse publique avec vos amis.",
        "guide_sftp_title": "📁 Transférer Mods, Plugins & Mondes (SFTP)",
        "guide_sftp_body": "<b>Options de Connexion :</b><br>• <b>Option A (Réseau Local Wi-Fi) :</b> Serveur : <code>{ip}</code> | Port : <code>2222</code> | Utilisateur : <code>{user}</code> | Dossier : <code>/servidor-mc</code><br>• <b>Option B (Internet via Playit.gg) :</b> Si vous avez créé un tunnel TCP vers le port 2222 sur Playit, utilisez l'adresse et le port attribués.<br>Compatible avec <b>FileZilla</b>, <b>WinSCP</b> et <b>Cyberduck</b>.",
        "guide_tips_title": "🔋 Conseils pour le Serveur sur Steam Deck :",
        "guide_tips_body": "• <b>Économiseur d'Écran OLED (Anti-Burn) :</b> Pour protéger l'écran OLED sans couper le serveur, activez le <b>Mode OLED</b> (bouton 🌙 supérieur). Fond noir absolu (pixels éteints) et logo rebondissant CRT / DVD. La mise en veille est inhibée.<br>• <b>Ajouter à la Bibliothèque Steam :</b> Ajoutez MC Server-Deck au Gaming Mode en un clic via le bouton <b>➕ Ajouter à Steam</b>.<br>• <b>Alimentation :</b> Branchez le chargeur 45W pour les longues sessions.<br>• <b>Clavier en Gaming Mode :</b> Appuyez sur le bouton ⌨️ de la console ou <b>STEAM + X</b> pour afficher le clavier virtuel.",

        # Dialogues
        "dlg_op_title": "Nommer Opérateur",
        "dlg_op_prompt": "Entrez le pseudo du joueur à promouvoir OP :",
        "dlg_wl_java_title": "Ajouter à la Whitelist (Java)",
        "dlg_wl_java_prompt": "Pseudo Minecraft Java :",
        "dlg_wl_bedrock_title": "Ajouter à la Whitelist (Bedrock)",
        "dlg_wl_bedrock_prompt": "Gamertag Bedrock (Xbox / Console / Mobile) :",
        "dlg_stop_title": "Arrêter le Serveur",
        "dlg_stop_msg": "Voulez-vous arrêter le serveur Minecraft et ses services associés ?",
        "dlg_stop_btn": "Arrêter",
        "dlg_restart_title": "Redémarrer le Serveur",
        "dlg_restart_msg": "Voulez-vous redémarrer tous les conteneurs Minecraft ?",
        "dlg_restart_btn": "Redémarrer",
        "dlg_confirm": "Confirmer",
        "dlg_cancel": "Annuler",
        "dlg_close": "Terminer",
        "dlg_deploy_title": "Déploiement du Serveur Minecraft...",
        "dlg_deploy_preparing": "Préparation des conteneurs en espace utilisateur...",
        "dlg_deploy_success": "✔ Déploiement terminé avec succès",
        "dlg_deploy_error": "✖ Une erreur est survenue lors du déploiement",
        "screensaver_wake_hud": "MC Server-Deck  •  mc-server: {srv_st}  •  mc-pod: {pod_st}  •  (Touchez pour réveiller)",
    },
}

# Idioma activo actual por defecto
CURRENT_LANGUAGE = "es"


def get_language() -> str:
    """Retorna el código de idioma activo."""
    return CURRENT_LANGUAGE


def set_language(lang_code: str):
    """Establece el idioma activo si es válido."""
    global CURRENT_LANGUAGE
    if lang_code in TRANSLATIONS:
        CURRENT_LANGUAGE = lang_code


def t(key: str, **kwargs: Any) -> str:
    """
    Retorna la traducción correspondiente a la clave para el idioma actual.
    Soporta formateo con argumentos posicionales/nombrados.
    Si la clave no existe en el idioma activo, intenta en inglés o español como fallback.
    """
    lang_dict = TRANSLATIONS.get(CURRENT_LANGUAGE, TRANSLATIONS["es"])
    text = lang_dict.get(key)

    if text is None:
        # Fallback a español o inglés
        text = TRANSLATIONS["es"].get(key, TRANSLATIONS["en"].get(key, key))

    if kwargs:
        try:
            return text.format(**kwargs)
        except Exception:
            return text
    return text
