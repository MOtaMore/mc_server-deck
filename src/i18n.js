// Internationalization (i18n) Module for MC Server Deck
// Primary / Default language: English (en)
// Fallback / Supported languages: Spanish (es), French (fr), Portuguese (pt)

export const translations = {
  en: {
    // Nav & Header
    "nav.dashboard": "Dashboard",
    "nav.config": "Configuration",
    "nav.network": "Network & Access",
    "nav.tools": "Tools & Steam",
    "header.subtitle": "Podman Native • SteamOS",
    "header.screensaver_title": "OLED Screensaver Mode (Anti-Burn-In)",

    // Status Badges & Labels
    "status.checking": "Checking...",
    "status.running": "Server Active",
    "status.degraded": "Desynchronized",
    "status.stopped": "Stopped",
    "status.not_created": "Not Created",
    "status.not_found": "Not Found",
    "status.attention_required": "Attention required",
    "status.server_stopped": "Server Stopped",
    "status.server_not_created": "Server Not Created",
    "status.synchronized": "Synchronized",
    "status.optimal": "Optimal",
    "status.active": "Active",
    "status.public_ip": "Public IP",
    "status.not_available": "Not available",
    "status.no_public_ip": "No Public IP detected",

    // Anti-Desync Banner
    "alert.desync_title": "Desynchronization detected in Pod:",
    "alert.desync_default_reason": "The Minecraft container is not responding within the pod.",
    "alert.reconcile_repair": "Reconcile & Repair Pod",

    // Dashboard Cards
    "card.pod_title": "Podman Pod (`mc-pod`)",
    "card.pod_ports": "Mapped ports:",
    "card.pod_sync": "Synchronization:",
    "card.server_title": "Minecraft Server (`mc-server`)",
    "card.server_version": "Version / Engine:",
    "card.server_ram": "Allocated RAM:",
    "card.conn_title": "Connection Mode",
    "card.conn_local_ip": "Local IP (WiFi):",
    "card.conn_public_ip": "Public IP:",
    "card.conn_detecting": "Detecting...",
    "card.ssh_title": "SFTP Access (`mc-ssh`)",
    "card.ssh_port": "SFTP Port:",
    "card.ssh_user": "User:",

    // Controls & Macros
    "controls.start": "Start Server",
    "controls.stop": "Stop Server",
    "controls.restart": "Restart",
    "controls.repair": "Repair Pod",
    "controls.repair_tooltip": "Reconcile container and reset Podman desyncs",
    "macros.label": "Quick Commands:",
    "macros.save": "💾 Save World",
    "macros.players": "👥 View Players",
    "macros.op": "⭐ Make OP",
    "macros.whitelist": "📋 Whitelist",
    "macros.whitelist_java": "📋 Whitelist Java",
    "macros.whitelist_bedrock": "🎮 Whitelist Bedrock (Floodgate)",
    "macros.weather": "☀️ Clear Weather",

    // Terminal / Console
    "terminal.title": "Server Console (Live Logs & RCON)",
    "terminal.autoscroll": "Auto-Scroll",
    "terminal.clear": "Clear",
    "terminal.initial_ready": "[MC Server Deck] Ready. Click 'Start Server' to begin.",
    "terminal.cleared_locally": "[Console cleared locally]",
    "terminal.input_placeholder": "Type a Minecraft command (e.g. list, op Steve, say Hello)...",
    "terminal.send": "Send",

    // Config Tab - Banner
    "config.header_title": "Server Configuration Wizard",
    "config.header_desc": "Configure Minecraft version, engine type, RAM and gameplay options. Your worlds in ~/minecraft-server/data will remain 100% safe.",

    // Config Tab - Section 1
    "config.section1_title": "1. Version Control and Engine",
    "config.version_label": "Official Minecraft Version:",
    "config.refresh_btn": "🔄 Refresh",
    "config.refresh_tooltip": "Query versions from Mojang API",
    "config.version_helper": "Automatically updated from Mojang API.",
    "config.latest_stable": "(Latest stable version)",
    "config.engine_label": "Server Engine Type (Vanilla / Plugins / Mods):",
    "engine.paper_name": "Paper (Recommended)",
    "engine.paper_desc": "Spigot/Paper plugins, optimized for Steam Deck",
    "engine.vanilla_name": "Vanilla Official",
    "engine.vanilla_desc": "Pure official Mojang server, unmodified",
    "engine.purpur_name": "Purpur",
    "engine.purpur_desc": "Maximum performance and configurable options",
    "engine.fabric_name": "Fabric (Mods)",
    "engine.fabric_desc": "Fast loading and modern high-performance mods",
    "engine.forge_name": "Forge (Mods)",
    "engine.forge_desc": "The classic heavy mods ecosystem",
    "engine.neoforge_name": "NeoForge (Mods)",
    "engine.neoforge_desc": "The new generation of the Forge ecosystem",
    "config.crossplay_title": "Crossplay Java + Bedrock (Geyser + Floodgate)",
    "config.crossplay_desc": "Allows Nintendo Switch, Xbox, PlayStation, Mobile and Windows Bedrock players to join this server.",

    // Config Tab - Section 2
    "config.section2_title": "2. Performance and Parameters",
    "config.ram_label": "Allocated RAM:",
    "config.ram_recommended": "4G - 6G (Recommended for Steam Deck)",
    "config.motd_label": "Server Message (MOTD):",
    "config.difficulty_label": "Difficulty:",
    "diff.peaceful": "Peaceful",
    "diff.easy": "Easy",
    "diff.normal": "Normal",
    "diff.hard": "Hard",
    "config.max_players_label": "Max Players:",
    "config.online_mode_title": "Online Mode (Premium Accounts)",
    "config.online_mode_desc": "Disable to allow non-premium / offline accounts",
    "config.whitelist_title": "Whitelist",
    "config.whitelist_desc": "Only authorized players will be able to join",
    "config.save_deploy": "Save & Deploy Server in Pod",

    // Network Tab
    "network.tab_public_ip": "Option 1: Direct Connection via Public IP",
    "network.tab_playit": "Option 2: Playit.gg Tunnels (No port forwarding)",
    "network.addresses_title": "Server Connection Addresses",
    "network.local_friends": "For friends in your home (Local WiFi Network):",
    "network.internet_friends": "For friends on the Internet (Public IP):",
    "network.copy": "Copy",
    "network.fetching_public_ip": "Querying Public IP...",
    "network.ports_title": "Ports Used on your Steam Deck:",
    "network.port_java": "Minecraft Java Edition",
    "network.port_bedrock": "Minecraft Bedrock Edition (Crossplay)",
    "network.port_sftp": "SFTP / SSH Access (Worlds & Mods)",
    "network.upnp_title": "Port Forwarding (WiFi Router)",
    "network.upnp_btn": "⚡ Try Automatic UPnP",
    "network.upnp_default": "You can test if your router allows automatic port forwarding via UPnP or configure it manually in the router web interface.",
    "network.router_guide_title": "How to forward ports on your Router (Step by Step):",
    "network.router_step1": "Open a browser on your PC or phone and access your router (usually <code>http://192.168.1.1</code> or <code>http://192.168.0.1</code>).",
    "network.router_step2": "Look for the section named <strong>Port Forwarding</strong>, <strong>Virtual Server</strong> or <strong>NAT</strong>.",
    "network.router_step3": "Add a rule for your Steam Deck's Local IP (<strong id=\"guide-local-ip\">192.168.x.x</strong>):<br>External & Internal Port: <strong>25565</strong> &bull; Protocol: <strong>TCP</strong>",
    "network.router_step4": "(Optional for Bedrock): Add a rule for port <strong>19132</strong> with protocol <strong>UDP</strong>.",
    "network.router_step5": "Save changes on the router. Your friends can now connect using your Public IP!",
    "network.playit_title": "Secure Playit.gg Tunnel (Zero Router Setup)",
    "network.playit_desc": "With Playit.gg you don't need to forward router ports or expose your public IP. The agent creates a secure tunnel directly to Playit servers.",
    "network.playit_key_label": "Playit.gg Secret Key:",
    "network.playit_placeholder": "Paste your Playit.gg secret key here",
    "network.playit_helper_pre": "Don't have an account or tunnel? Sign up for free at",
    "network.playit_helper_post": "and create a tunnel for Minecraft (25565).",
    "network.save_playit_btn": "Save & Activate Playit.gg Tunnel",
    "network.ssh_title": "Remote SFTP / SSH Access (FileZilla / WinSCP)",
    "network.ssh_desc": "Wirelessly transfer worlds, mods, datapacks and plugins from your main PC to the <code>/servidor-mc</code> directory on your Steam Deck.",
    "network.ssh_user_label": "SFTP User:",
    "network.ssh_pass_label": "SFTP Password:",
    "network.ssh_port_label": "SFTP Port:",
    "network.sftp_url_label": "URL for FileZilla / WinSCP (Local Network):",

    // Tools Tab
    "tools.repair_title": "Anti-Desync Management & Reconciliation",
    "tools.repair_desc": "If Podman reports corrupted states, storage locks, crashed containers or socket errors, this tool resets orphan states and restores clean pod synchronization.",
    "tools.repair_btn": "Run Deep Reconciliation",
    "tools.perms_title": "Fix File Permissions",
    "tools.perms_desc": "Runs the rootless routine <code>podman unshare chown -R 0:0</code> and fixes read/write permissions on the worlds and data folder to avoid lockouts.",
    "tools.perms_btn": "Fix Data Permissions",
    "tools.shortcuts_title": "Steam Integration (Gaming Mode)",
    "tools.shortcuts_desc": "Installs shortcuts on your Desktop and SteamOS applications list so you can easily launch the app in Gaming Mode with controller support.",
    "tools.shortcuts_btn": "Install Shortcuts",
    "tools.paths_title": "File Paths on Steam Deck",
    "tools.path_data": "Minecraft Data:",
    "tools.path_ssh": "SSH Config:",
    "tools.path_app": "App Config:",

    // Modals & Screensaver
    "dialog.cancel": "Cancel",
    "dialog.ok": "Accept",
    "dialog.op_title": "Make Administrator (OP)",
    "dialog.op_prompt": "Minecraft player username:",
    "dialog.whitelist_title": "Add to Whitelist",
    "dialog.whitelist_prompt": "Username to authorize:",
    "dialog.whitelist_java_title": "Add to Java Whitelist",
    "dialog.whitelist_java_prompt": "Minecraft Java player username (runs 'whitelist add <username>'):",
    "dialog.whitelist_bedrock_title": "Add to Bedrock Whitelist (Floodgate)",
    "dialog.whitelist_bedrock_prompt": "Bedrock Gamertag or Floodgate UUID (Tip: If player never joined before, turn off whitelist temporarily with 'whitelist off' so they connect once, or enter their Floodgate UUID):",
    "screensaver.hint": "Tap any button or touch the screen to return to the panel",

    // Toast Notifications
    "toast.deploying": "Deploying server to mc-pod... This may take a few seconds.",
    "toast.deploy_error": "Deployment error: {err}",
    "toast.starting": "Starting mc-pod...",
    "toast.start_error": "Failed to start: {err}",
    "toast.stopping": "Stopping mc-pod...",
    "toast.restarting": "Restarting mc-pod...",
    "toast.repairing": "Running deep reconciliation and repair in Podman...",
    "toast.repair_error": "Reconciliation error: {err}",
    "toast.fixing_perms": "Applying rootless permission fix...",
    "toast.perms_fixed": "Permissions successfully fixed in ~/minecraft-server/data.",
    "toast.saving_playit": "Saving Playit.gg key and updating container...",
    "toast.playit_active": "Playit.gg tunnel configured and active.",
    "toast.mojang_updated": "Mojang versions updated.",
    "toast.copied": "Copied to clipboard!",
    "toast.upnp_probing": "Probing UPnP support on your WiFi router...",
    "toast.upnp_success": "Ports opened automatically via UPnP!",
    "toast.rcon_error": "RCON Error: {err}",
    "toast.error": "Error: {err}"
  },

  es: {
    // Nav & Header
    "nav.dashboard": "Dashboard",
    "nav.config": "Configuración",
    "nav.network": "Red & Acceso",
    "nav.tools": "Herramientas & Steam",
    "header.subtitle": "Podman Native • SteamOS",
    "header.screensaver_title": "Modo Salvapantallas OLED (Anti-Quemado)",

    // Status Badges & Labels
    "status.checking": "Comprobando...",
    "status.running": "Servidor Activo",
    "status.degraded": "Desincronizado",
    "status.stopped": "Detenido",
    "status.not_created": "No Creado",
    "status.not_found": "No Encontrado",
    "status.attention_required": "Atención requerida",
    "status.server_stopped": "Servidor Detenido",
    "status.server_not_created": "Servidor No Creado",
    "status.synchronized": "Sincronizado",
    "status.optimal": "Óptima",
    "status.active": "Activo",
    "status.public_ip": "IP Pública",
    "status.not_available": "No disponible",
    "status.no_public_ip": "No se detectó IP Pública",

    // Anti-Desync Banner
    "alert.desync_title": "Desincronización detectada en el Pod:",
    "alert.desync_default_reason": "El contenedor de Minecraft no responde con el pod.",
    "alert.reconcile_repair": "Reconciliar & Reparar Pod",

    // Dashboard Cards
    "card.pod_title": "Podman Pod (`mc-pod`)",
    "card.pod_ports": "Puertos mapeados:",
    "card.pod_sync": "Sincronización:",
    "card.server_title": "Servidor Minecraft (`mc-server`)",
    "card.server_version": "Versión / Motor:",
    "card.server_ram": "RAM Asignada:",
    "card.conn_title": "Modo de Conexión",
    "card.conn_local_ip": "IP Local (WiFi):",
    "card.conn_public_ip": "IP Pública:",
    "card.conn_detecting": "Detectando...",
    "card.ssh_title": "Acceso SFTP (`mc-ssh`)",
    "card.ssh_port": "Puerto SFTP:",
    "card.ssh_user": "Usuario:",

    // Controls & Macros
    "controls.start": "Iniciar Servidor",
    "controls.stop": "Detener Servidor",
    "controls.restart": "Reiniciar",
    "controls.repair": "Reparar Pod",
    "controls.repair_tooltip": "Reconciliar contenedor y resetear desincronizaciones de podman",
    "macros.label": "Comandos Rápidos:",
    "macros.save": "💾 Guardar Mundo",
    "macros.players": "👥 Ver Jugadores",
    "macros.op": "⭐ Hacer OP",
    "macros.whitelist": "📋 Whitelist",
    "macros.whitelist_java": "📋 Whitelist Java",
    "macros.whitelist_bedrock": "🎮 Whitelist Bedrock (Floodgate)",
    "macros.weather": "☀️ Despejar Clima",

    // Terminal / Console
    "terminal.title": "Consola del Servidor (Logs & RCON en Vivo)",
    "terminal.autoscroll": "Auto-Scroll",
    "terminal.clear": "Limpiar",
    "terminal.initial_ready": "[MC Server Deck] Listo. Presiona 'Iniciar Servidor' para comenzar.",
    "terminal.cleared_locally": "[Consola limpiada localmente]",
    "terminal.input_placeholder": "Escribe un comando de Minecraft (ej: list, op Steve, say ¡Hola!)...",
    "terminal.send": "Enviar",

    // Config Tab - Banner
    "config.header_title": "Asistente de Configuración del Servidor",
    "config.header_desc": "Configura la versión de Minecraft, tipo de motor, memoria RAM y opciones de juego. Tus mundos en ~/minecraft-server/data se mantendrán 100% a salvo.",

    // Config Tab - Section 1
    "config.section1_title": "1. Control de Versionado y Motor",
    "config.version_label": "Versión Oficial de Minecraft:",
    "config.refresh_btn": "🔄 Actualizar",
    "config.refresh_tooltip": "Consultar versiones desde Mojang API",
    "config.version_helper": "Se actualizan automáticamente desde la API de Mojang.",
    "config.latest_stable": "(Última versión estable)",
    "config.engine_label": "Tipo de Servidor (Vanilla / Plugins / Mods):",
    "engine.paper_name": "Paper (Recomendado)",
    "engine.paper_desc": "Plugins Spigot/Paper, optimizado para Steam Deck",
    "engine.vanilla_name": "Vanilla Oficial",
    "engine.vanilla_desc": "Servidor oficial Mojang puro, sin modificaciones",
    "engine.purpur_name": "Purpur",
    "engine.purpur_desc": "Máximo rendimiento y opciones configurables",
    "engine.fabric_name": "Fabric (Mods)",
    "engine.fabric_desc": "Carga rápida y mods modernos de alto rendimiento",
    "engine.forge_name": "Forge (Mods)",
    "engine.forge_desc": "El clásico ecosistema de mods pesados",
    "engine.neoforge_name": "NeoForge (Mods)",
    "engine.neoforge_desc": "La nueva generación del ecosistema Forge",
    "config.crossplay_title": "Crossplay Java + Bedrock (Geyser + Floodgate)",
    "config.crossplay_desc": "Permite que jugadores de Nintendo Switch, Xbox, PlayStation, Celulares y Windows Bedrock jueguen en este servidor.",

    // Config Tab - Section 2
    "config.section2_title": "2. Rendimiento y Parámetros",
    "config.ram_label": "Memoria RAM Asignada:",
    "config.ram_recommended": "4G - 6G (Recomendado Steam Deck)",
    "config.motd_label": "Mensaje del Servidor (MOTD):",
    "config.difficulty_label": "Dificultad:",
    "diff.peaceful": "Pacífico",
    "diff.easy": "Fácil",
    "diff.normal": "Normal",
    "diff.hard": "Difícil",
    "config.max_players_label": "Jugadores Máximos:",
    "config.online_mode_title": "Modo Online (Cuentas Premium)",
    "config.online_mode_desc": "Desactivar para permitir cuentas No-Premium / mixtas",
    "config.whitelist_title": "Lista Blanca (Whitelist)",
    "config.whitelist_desc": "Solo los jugadores autorizados podrán ingresar",
    "config.save_deploy": "Guardar y Desplegar Servidor en Pod",

    // Network Tab
    "network.tab_public_ip": "Opción 1: Conexión por IP Pública (Directo)",
    "network.tab_playit": "Opción 2: Túneles Playit.gg (Sin abrir puertos)",
    "network.addresses_title": "Direcciones de Conexión del Servidor",
    "network.local_friends": "Para amigos en tu misma casa (Red Local WiFi):",
    "network.internet_friends": "Para amigos en Internet (IP Pública):",
    "network.copy": "Copiar",
    "network.fetching_public_ip": "Consultando IP Pública...",
    "network.ports_title": "Puertos Utilizados en tu Steam Deck:",
    "network.port_java": "Minecraft Java Edition",
    "network.port_bedrock": "Minecraft Bedrock Edition (Crossplay)",
    "network.port_sftp": "Acceso SFTP / SSH (Mundos y Mods)",
    "network.upnp_title": "Apertura de Puertos (Router WiFi)",
    "network.upnp_btn": "⚡ Intentar UPnP Automático",
    "network.upnp_default": "Puedes probar si tu router permite apertura automática mediante UPnP o configurarlo manualmente en la web del router.",
    "network.router_guide_title": "Cómo abrir los puertos en tu Router (Paso a Paso):",
    "network.router_step1": "Abre el navegador en tu PC o móvil y entra a tu router (usualmente <code>http://192.168.1.1</code> o <code>http://192.168.0.1</code>).",
    "network.router_step2": "Busca la sección <strong>Port Forwarding</strong>, <strong>Reenvío de Puertos</strong> o <strong>Servidores Virtuales</strong>.",
    "network.router_step3": "Agrega una regla para la IP Local de tu Steam Deck (<strong id=\"guide-local-ip\">192.168.x.x</strong>):<br>Puerto Externo e Interno: <strong>25565</strong> &bull; Protocolo: <strong>TCP</strong>",
    "network.router_step4": "(Opcional para Bedrock): Agrega regla para puerto <strong>19132</strong> con protocolo <strong>UDP</strong>.",
    "network.router_step5": "Guarda los cambios en el router. ¡Tus amigos ya podrán conectarse a tu IP Pública!",
    "network.playit_title": "Túnel Seguro Playit.gg (Cero Configuración de Router)",
    "network.playit_desc": "Con Playit.gg no necesitas abrir puertos en tu router ni exponer tu IP pública. El agente crea un túnel seguro directo a los servidores de Playit.",
    "network.playit_key_label": "Secret Key de Playit.gg:",
    "network.playit_placeholder": "Pega aquí tu secret key de Playit.gg",
    "network.playit_helper_pre": "¿No tienes una cuenta o túnel? Entra gratis en",
    "network.playit_helper_post": "y crea un túnel para Minecraft (25565).",
    "network.save_playit_btn": "Guardar y Activar Túnel Playit.gg",
    "network.ssh_title": "Acceso Remoto SFTP / SSH (FileZilla / WinSCP)",
    "network.ssh_desc": "Transfiere mundos, mods, datapacks y plugins de forma inalámbrica desde tu PC principal a la carpeta <code>/servidor-mc</code> de la Steam Deck.",
    "network.ssh_user_label": "Usuario SFTP:",
    "network.ssh_pass_label": "Contraseña SFTP:",
    "network.ssh_port_label": "Puerto SFTP:",
    "network.sftp_url_label": "URL para FileZilla / WinSCP (Red Local):",

    // Tools Tab
    "tools.repair_title": "Gestión y Reconciliación Anti-Desincronización",
    "tools.repair_desc": "Si Podman reporta estados corruptos, locks de almacenamiento, contenedores caídos o errores de socket, esta herramienta resetea los estados huérfanos y restaura la sincronización limpia del pod.",
    "tools.repair_btn": "Ejecutar Reconciliación Profunda",
    "tools.perms_title": "Corregir Permisos de Archivos",
    "tools.perms_desc": "Ejecuta la rutina rootless <code>podman unshare chown -R 0:0</code> y corrige los permisos de lectura y escritura en la carpeta de mundos y datos para evitar bloqueos.",
    "tools.perms_btn": "Corregir Permisos de Datos",
    "tools.shortcuts_title": "Integración con Steam (Gaming Mode)",
    "tools.shortcuts_desc": "Instala accesos directos en tu Escritorio y en la lista de aplicaciones de SteamOS para poder añadir y abrir la aplicación directamente con los controles de la consola en el Modo Juego.",
    "tools.shortcuts_btn": "Instalar Accesos Directos",
    "tools.paths_title": "Rutas de Archivos en Steam Deck",
    "tools.path_data": "Datos de Minecraft:",
    "tools.path_ssh": "Configuración SSH:",
    "tools.path_app": "Configuración App:",

    // Modals & Screensaver
    "dialog.cancel": "Cancelar",
    "dialog.ok": "Aceptar",
    "dialog.op_title": "Hacer Administrador (OP)",
    "dialog.op_prompt": "Nombre de usuario del jugador de Minecraft:",
    "dialog.whitelist_title": "Agregar a Whitelist",
    "dialog.whitelist_prompt": "Nombre de usuario a autorizar:",
    "dialog.whitelist_java_title": "Agregar a Whitelist (Java)",
    "dialog.whitelist_java_prompt": "Nombre de usuario Java (ejecuta 'whitelist add <usuario>'):",
    "dialog.whitelist_bedrock_title": "Agregar a Whitelist Bedrock (Floodgate)",
    "dialog.whitelist_bedrock_prompt": "Gamertag de Bedrock/Xbox o UUID de Floodgate (Consejo: Si nunca ha entrado a tu servidor, desactiva la whitelist un momento con 'whitelist off' para que entre una vez, o usa su UUID de Floodgate):",
    "screensaver.hint": "Toca cualquier botón o la pantalla táctil para volver al panel",

    // Toast Notifications
    "toast.deploying": "Desplegando servidor en mc-pod... Esto puede tomar unos segundos.",
    "toast.deploy_error": "Error al desplegar: {err}",
    "toast.starting": "Iniciando mc-pod...",
    "toast.start_error": "Fallo al iniciar: {err}",
    "toast.stopping": "Deteniendo mc-pod...",
    "toast.restarting": "Reiniciando mc-pod...",
    "toast.repairing": "Ejecutando reconciliación y reparación profunda de Podman...",
    "toast.repair_error": "Error en reconciliación: {err}",
    "toast.fixing_perms": "Aplicando corrección de permisos rootless...",
    "toast.perms_fixed": "Permisos corregidos exitosamente en ~/minecraft-server/data.",
    "toast.saving_playit": "Guardando clave de Playit.gg y actualizando contenedor...",
    "toast.playit_active": "Túnel Playit.gg configurado y activo.",
    "toast.mojang_updated": "Versiones de Mojang actualizadas.",
    "toast.copied": "¡Copiado al portapapeles!",
    "toast.upnp_probing": "Sondeando soporte UPnP en tu router WiFi...",
    "toast.upnp_success": "¡Puertos abiertos automáticamente vía UPnP!",
    "toast.rcon_error": "Error RCON: {err}",
    "toast.error": "Error: {err}"
  },

  fr: {
    // Nav & Header
    "nav.dashboard": "Tableau de bord",
    "nav.config": "Configuration",
    "nav.network": "Réseau & Accès",
    "nav.tools": "Outils & Steam",
    "header.subtitle": "Podman Native • SteamOS",
    "header.screensaver_title": "Économiseur d'écran OLED (Anti-brûlure)",

    // Status Badges & Labels
    "status.checking": "Vérification...",
    "status.running": "Serveur Actif",
    "status.degraded": "Désynchronisé",
    "status.stopped": "Arrêté",
    "status.not_created": "Non Créé",
    "status.not_found": "Non Trouvé",
    "status.attention_required": "Attention requise",
    "status.server_stopped": "Serveur Arrêté",
    "status.server_not_created": "Serveur Non Créé",
    "status.synchronized": "Synchronisé",
    "status.optimal": "Optimale",
    "status.active": "Actif",
    "status.public_ip": "IP Publique",
    "status.not_available": "Non disponible",
    "status.no_public_ip": "Aucune IP Publique détectée",

    // Anti-Desync Banner
    "alert.desync_title": "Désynchronisation détectée dans le Pod :",
    "alert.desync_default_reason": "Le conteneur Minecraft ne répond pas dans le pod.",
    "alert.reconcile_repair": "Réconcilier & Réparer le Pod",

    // Dashboard Cards
    "card.pod_title": "Podman Pod (`mc-pod`)",
    "card.pod_ports": "Ports mappés :",
    "card.pod_sync": "Synchronisation :",
    "card.server_title": "Serveur Minecraft (`mc-server`)",
    "card.server_version": "Version / Moteur :",
    "card.server_ram": "RAM Allouée :",
    "card.conn_title": "Mode de Connexion",
    "card.conn_local_ip": "IP Locale (WiFi) :",
    "card.conn_public_ip": "IP Publique :",
    "card.conn_detecting": "Détection...",
    "card.ssh_title": "Accès SFTP (`mc-ssh`)",
    "card.ssh_port": "Port SFTP :",
    "card.ssh_user": "Utilisateur :",

    // Controls & Macros
    "controls.start": "Démarrer le Serveur",
    "controls.stop": "Arrêter le Serveur",
    "controls.restart": "Redémarrer",
    "controls.repair": "Réparer le Pod",
    "controls.repair_tooltip": "Réconcilier le conteneur et réinitialiser les désynchronisations de Podman",
    "macros.label": "Commandes Rapides :",
    "macros.save": "💾 Sauvegarder Monde",
    "macros.players": "👥 Voir Joueurs",
    "macros.op": "⭐ Donner OP",
    "macros.whitelist": "📋 Liste Blanche",
    "macros.whitelist_java": "📋 Liste Blanche Java",
    "macros.whitelist_bedrock": "🎮 Liste Blanche Bedrock (Floodgate)",
    "macros.weather": "☀️ Météo Dégagée",

    // Terminal / Console
    "terminal.title": "Console du Serveur (Logs & RCON en direct)",
    "terminal.autoscroll": "Défilement Auto",
    "terminal.clear": "Effacer",
    "terminal.initial_ready": "[MC Server Deck] Prêt. Cliquez sur 'Démarrer le Serveur' pour commencer.",
    "terminal.cleared_locally": "[Console effacée localement]",
    "terminal.input_placeholder": "Entrez une commande Minecraft (ex: list, op Steve, say Bonjour)...",
    "terminal.send": "Envoyer",

    // Config Tab - Banner
    "config.header_title": "Assistant de Configuration du Serveur",
    "config.header_desc": "Configurez la version de Minecraft, le moteur, la RAM et les options de jeu. Vos mondes dans ~/minecraft-server/data resteront 100% en sécurité.",

    // Config Tab - Section 1
    "config.section1_title": "1. Contrôle de Version et Moteur",
    "config.version_label": "Version Officielle de Minecraft :",
    "config.refresh_btn": "🔄 Actualiser",
    "config.refresh_tooltip": "Interroger les versions depuis l'API Mojang",
    "config.version_helper": "Mises à jour automatiquement depuis l'API Mojang.",
    "config.latest_stable": "(Dernière version stable)",
    "config.engine_label": "Type de Serveur (Vanilla / Plugins / Mods) :",
    "engine.paper_name": "Paper (Recommandé)",
    "engine.paper_desc": "Plugins Spigot/Paper, optimisé pour Steam Deck",
    "engine.vanilla_name": "Vanilla Officiel",
    "engine.vanilla_desc": "Serveur officiel Mojang pur, sans modifications",
    "engine.purpur_name": "Purpur",
    "engine.purpur_desc": "Performances maximales et options configurables",
    "engine.fabric_name": "Fabric (Mods)",
    "engine.fabric_desc": "Chargement rapide et mods modernes haute performance",
    "engine.forge_name": "Forge (Mods)",
    "engine.forge_desc": "L'écosystème classique de mods lourds",
    "engine.neoforge_name": "NeoForge (Mods)",
    "engine.neoforge_desc": "La nouvelle génération de l'écosystème Forge",
    "config.crossplay_title": "Crossplay Java + Bedrock (Geyser + Floodgate)",
    "config.crossplay_desc": "Permet aux joueurs Nintendo Switch, Xbox, PlayStation, Mobiles et Windows Bedrock de rejoindre ce serveur.",

    // Config Tab - Section 2
    "config.section2_title": "2. Performances et Paramètres",
    "config.ram_label": "Mémoire RAM Allouée :",
    "config.ram_recommended": "4G - 6G (Recommandé Steam Deck)",
    "config.motd_label": "Message du Serveur (MOTD) :",
    "config.difficulty_label": "Difficulté :",
    "diff.peaceful": "Paisible",
    "diff.easy": "Facile",
    "diff.normal": "Normale",
    "diff.hard": "Difficile",
    "config.max_players_label": "Joueurs Max :",
    "config.online_mode_title": "Mode En Ligne (Comptes Premium)",
    "config.online_mode_desc": "Désactiver pour autoriser les comptes non-premium / mixtes",
    "config.whitelist_title": "Liste Blanche (Whitelist)",
    "config.whitelist_desc": "Seuls les joueurs autorisés pourront se connecter",
    "config.save_deploy": "Sauvegarder & Déployer le Serveur dans le Pod",

    // Network Tab
    "network.tab_public_ip": "Option 1 : Connexion Directe par IP Publique",
    "network.tab_playit": "Option 2 : Tunnels Playit.gg (Sans ouverture de ports)",
    "network.addresses_title": "Adresses de Connexion du Serveur",
    "network.local_friends": "Pour les amis chez vous (Réseau Local WiFi) :",
    "network.internet_friends": "Pour les amis sur Internet (IP Publique) :",
    "network.copy": "Copier",
    "network.fetching_public_ip": "Interrogation de l'IP Publique...",
    "network.ports_title": "Ports Utilisés sur votre Steam Deck :",
    "network.port_java": "Minecraft Java Edition",
    "network.port_bedrock": "Minecraft Bedrock Edition (Crossplay)",
    "network.port_sftp": "Accès SFTP / SSH (Mondes & Mods)",
    "network.upnp_title": "Ouverture des Ports (Routeur WiFi)",
    "network.upnp_btn": "⚡ Essayer UPnP Automatique",
    "network.upnp_default": "Vous pouvez tester si votre routeur permet l'ouverture automatique via UPnP ou le configurer manuellement.",
    "network.router_guide_title": "Comment ouvrir les ports sur votre Routeur (Étape par étape) :",
    "network.router_step1": "Ouvrez le navigateur sur votre PC ou mobile et accédez à votre routeur (généralement <code>http://192.168.1.1</code> ou <code>http://192.168.0.1</code>).",
    "network.router_step2": "Recherchez la section nommée <strong>Redirection de Ports</strong>, <strong>Serveurs Virtuels</strong> ou <strong>NAT</strong>.",
    "network.router_step3": "Ajoutez une règle pour l'IP Locale de votre Steam Deck (<strong id=\"guide-local-ip\">192.168.x.x</strong>) :<br>Port Externe et Interne : <strong>25565</strong> &bull; Protocole : <strong>TCP</strong>",
    "network.router_step4": "(Optionnel pour Bedrock) : Ajoutez une règle pour le port <strong>19132</strong> en protocole <strong>UDP</strong>.",
    "network.router_step5": "Enregistrez les modifications sur le routeur. Vos amis peuvent maintenant se connecter avec votre IP Publique !",
    "network.playit_title": "Tunnel Sécurisé Playit.gg (Zéro Configuration Routeur)",
    "network.playit_desc": "Avec Playit.gg, vous n'avez pas besoin d'ouvrir des ports ni d'exposer votre IP publique. L'agent crée un tunnel sécurisé direct vers les serveurs Playit.",
    "network.playit_key_label": "Clé Secrète Playit.gg :",
    "network.playit_placeholder": "Collez votre clé secrète Playit.gg ici",
    "network.playit_helper_pre": "Pas de compte ou de tunnel ? Inscrivez-vous gratuitement sur",
    "network.playit_helper_post": "et créez un tunnel pour Minecraft (25565).",
    "network.save_playit_btn": "Sauvegarder & Activer le Tunnel Playit.gg",
    "network.ssh_title": "Accès distant SFTP / SSH (FileZilla / WinSCP)",
    "network.ssh_desc": "Transférez des mondes, mods, datapacks et plugins sans fil depuis votre PC vers le dossier <code>/servidor-mc</code> du Steam Deck.",
    "network.ssh_user_label": "Utilisateur SFTP :",
    "network.ssh_pass_label": "Mot de passe SFTP :",
    "network.ssh_port_label": "Port SFTP :",
    "network.sftp_url_label": "URL pour FileZilla / WinSCP (Réseau Local) :",

    // Tools Tab
    "tools.repair_title": "Gestion et Réconciliation Anti-Désynchronisation",
    "tools.repair_desc": "Si Podman signale des états corrompus, des verrous de stockage ou des erreurs de socket, cet outil nettoie les états orphelins et restaure une synchronisation propre.",
    "tools.repair_btn": "Exécuter la Réconciliation Profonde",
    "tools.perms_title": "Corriger les Permissions de Fichiers",
    "tools.perms_desc": "Exécute la routine sans racine <code>podman unshare chown -R 0:0</code> et corrige les permissions de lecture/écriture pour éviter tout blocage.",
    "tools.perms_btn": "Corriger les Permissions des Données",
    "tools.shortcuts_title": "Intégration Steam (Gaming Mode)",
    "tools.shortcuts_desc": "Installe des raccourcis sur votre Bureau et dans la liste des applications SteamOS pour ouvrir l'application directement avec les commandes en mode jeu.",
    "tools.shortcuts_btn": "Installer les Raccourcis",
    "tools.paths_title": "Chemins des Fichiers sur Steam Deck",
    "tools.path_data": "Données Minecraft :",
    "tools.path_ssh": "Configuration SSH :",
    "tools.path_app": "Configuration App :",

    // Modals & Screensaver
    "dialog.cancel": "Annuler",
    "dialog.ok": "Accepter",
    "dialog.op_title": "Nommer Administrateur (OP)",
    "dialog.op_prompt": "Nom d'utilisateur du joueur Minecraft :",
    "dialog.whitelist_title": "Ajouter à la Liste Blanche",
    "dialog.whitelist_prompt": "Nom d'utilisateur à autoriser :",
    "dialog.whitelist_java_title": "Ajouter à la Liste Blanche Java",
    "dialog.whitelist_java_prompt": "Nom d'utilisateur Java (exécute 'whitelist add <joueur>') :",
    "dialog.whitelist_bedrock_title": "Ajouter à la Liste Blanche Bedrock (Floodgate)",
    "dialog.whitelist_bedrock_prompt": "Gamertag Bedrock ou UUID Floodgate (Astuce : Si le joueur n'a jamais rejoint votre serveur, désactivez temporairement la liste blanche avec 'whitelist off' pour qu'il se connecte une fois, ou entrez son UUID Floodgate) :",
    "screensaver.hint": "Touchez n'importe quel bouton ou l'écran pour revenir au panneau",

    // Toast Notifications
    "toast.deploying": "Déploiement du serveur sur mc-pod... Cela peut prendre quelques secondes.",
    "toast.deploy_error": "Erreur de déploiement : {err}",
    "toast.starting": "Démarrage de mc-pod...",
    "toast.start_error": "Échec du démarrage : {err}",
    "toast.stopping": "Arrêt de mc-pod...",
    "toast.restarting": "Redémarrage de mc-pod...",
    "toast.repairing": "Exécution de la réconciliation approfondie de Podman...",
    "toast.repair_error": "Erreur de réconciliation : {err}",
    "toast.fixing_perms": "Application de la correction des permissions rootless...",
    "toast.perms_fixed": "Permissions corrigées avec succès dans ~/minecraft-server/data.",
    "toast.saving_playit": "Sauvegarde de la clé Playit.gg et mise à jour du conteneur...",
    "toast.playit_active": "Tunnel Playit.gg configuré et actif.",
    "toast.mojang_updated": "Versions Mojang mises à jour.",
    "toast.copied": "Copié dans le presse-papiers !",
    "toast.upnp_probing": "Vérification du support UPnP sur votre routeur WiFi...",
    "toast.upnp_success": "Ports ouverts automatiquement via UPnP !",
    "toast.rcon_error": "Erreur RCON : {err}",
    "toast.error": "Erreur : {err}"
  },

  pt: {
    // Nav & Header
    "nav.dashboard": "Painel",
    "nav.config": "Configurações",
    "nav.network": "Rede & Acesso",
    "nav.tools": "Ferramentas & Steam",
    "header.subtitle": "Podman Native • SteamOS",
    "header.screensaver_title": "Protetor de Tela OLED (Anti-Burn-in)",

    // Status Badges & Labels
    "status.checking": "Verificando...",
    "status.running": "Servidor Ativo",
    "status.degraded": "Dessincronizado",
    "status.stopped": "Parado",
    "status.not_created": "Não Criado",
    "status.not_found": "Não Encontrado",
    "status.attention_required": "Atenção necessária",
    "status.server_stopped": "Servidor Parado",
    "status.server_not_created": "Servidor Não Criado",
    "status.synchronized": "Sincronizado",
    "status.optimal": "Ótima",
    "status.active": "Ativo",
    "status.public_ip": "IP Pública",
    "status.not_available": "Não disponível",
    "status.no_public_ip": "Nenhum IP Público detectado",

    // Anti-Desync Banner
    "alert.desync_title": "Dessincronização detectada no Pod:",
    "alert.desync_default_reason": "O contêiner do Minecraft não responde dentro do pod.",
    "alert.reconcile_repair": "Reconciliar & Reparar Pod",

    // Dashboard Cards
    "card.pod_title": "Podman Pod (`mc-pod`)",
    "card.pod_ports": "Portas mapeadas:",
    "card.pod_sync": "Sincronização:",
    "card.server_title": "Servidor Minecraft (`mc-server`)",
    "card.server_version": "Versão / Motor:",
    "card.server_ram": "RAM Alocada:",
    "card.conn_title": "Modo de Conexão",
    "card.conn_local_ip": "IP Local (WiFi):",
    "card.conn_public_ip": "IP Público:",
    "card.conn_detecting": "Detectando...",
    "card.ssh_title": "Acesso SFTP (`mc-ssh`)",
    "card.ssh_port": "Porta SFTP:",
    "card.ssh_user": "Usuário:",

    // Controls & Macros
    "controls.start": "Iniciar Servidor",
    "controls.stop": "Parar Servidor",
    "controls.restart": "Reiniciar",
    "controls.repair": "Reparar Pod",
    "controls.repair_tooltip": "Reconciliar contêiner e redefinir dessincronizações do Podman",
    "macros.label": "Comandos Rápidos:",
    "macros.save": "💾 Salvar Mundo",
    "macros.players": "👥 Ver Jogadores",
    "macros.op": "⭐ Tornar OP",
    "macros.whitelist": "📋 Whitelist",
    "macros.whitelist_java": "📋 Whitelist Java",
    "macros.whitelist_bedrock": "🎮 Whitelist Bedrock (Floodgate)",
    "macros.weather": "☀️ Limpar Clima",

    // Terminal / Console
    "terminal.title": "Console do Servidor (Logs & RCON em Tempo Real)",
    "terminal.autoscroll": "Auto-Rolagem",
    "terminal.clear": "Limpar",
    "terminal.initial_ready": "[MC Server Deck] Pronto. Clique em 'Iniciar Servidor' para começar.",
    "terminal.cleared_locally": "[Console limpo localmente]",
    "terminal.input_placeholder": "Digite um comando do Minecraft (ex: list, op Steve, say Olá)...",
    "terminal.send": "Enviar",

    // Config Tab - Banner
    "config.header_title": "Assistente de Configuração do Servidor",
    "config.header_desc": "Configure a versão do Minecraft, tipo de motor, memória RAM e opções de jogo. Seus mundos em ~/minecraft-server/data permanecerão 100% seguros.",

    // Config Tab - Section 1
    "config.section1_title": "1. Controle de Versão e Motor",
    "config.version_label": "Versão Oficial do Minecraft:",
    "config.refresh_btn": "🔄 Atualizar",
    "config.refresh_tooltip": "Consultar versões da API da Mojang",
    "config.version_helper": "Atualizadas automaticamente da API da Mojang.",
    "config.latest_stable": "(Última versão estável)",
    "config.engine_label": "Tipo de Servidor (Vanilla / Plugins / Mods):",
    "engine.paper_name": "Paper (Recomendado)",
    "engine.paper_desc": "Plugins Spigot/Paper, otimizado para Steam Deck",
    "engine.vanilla_name": "Vanilla Oficial",
    "engine.vanilla_desc": "Servidor oficial Mojang puro, sem modificações",
    "engine.purpur_name": "Purpur",
    "engine.purpur_desc": "Desempenho máximo e opções configuráveis",
    "engine.fabric_name": "Fabric (Mods)",
    "engine.fabric_desc": "Carregamento rápido e mods modernos de alto desempenho",
    "engine.forge_name": "Forge (Mods)",
    "engine.forge_desc": "O ecossistema clássico de mods pesados",
    "engine.neoforge_name": "NeoForge (Mods)",
    "engine.neoforge_desc": "A nova geração do ecossistema Forge",
    "config.crossplay_title": "Crossplay Java + Bedrock (Geyser + Floodgate)",
    "config.crossplay_desc": "Permite que jogadores de Nintendo Switch, Xbox, PlayStation, Celular e Windows Bedrock joguem neste servidor.",

    // Config Tab - Section 2
    "config.section2_title": "2. Desempenho e Parâmetros",
    "config.ram_label": "Memória RAM Alocada:",
    "config.ram_recommended": "4G - 6G (Recomendado para Steam Deck)",
    "config.motd_label": "Mensagem do Servidor (MOTD):",
    "config.difficulty_label": "Dificuldade:",
    "diff.peaceful": "Pacífico",
    "diff.easy": "Fácil",
    "diff.normal": "Normal",
    "diff.hard": "Difícil",
    "config.max_players_label": "Máximo de Jogadores:",
    "config.online_mode_title": "Modo Online (Contas Premium)",
    "config.online_mode_desc": "Desative para permitir contas não premium / mistas",
    "config.whitelist_title": "Lista Branca (Whitelist)",
    "config.whitelist_desc": "Apenas jogadores autorizados poderão entrar",
    "config.save_deploy": "Salvar e Implantar Servidor no Pod",

    // Network Tab
    "network.tab_public_ip": "Opção 1: Conexão por IP Pública (Direta)",
    "network.tab_playit": "Opção 2: Túneis Playit.gg (Sem abrir portas)",
    "network.addresses_title": "Endereços de Conexão do Servidor",
    "network.local_friends": "Para amigos na mesma casa (Rede Local WiFi):",
    "network.internet_friends": "Para amigos na Internet (IP Pública):",
    "network.copy": "Copiar",
    "network.fetching_public_ip": "Consultando IP Público...",
    "network.ports_title": "Portas Utilizadas no seu Steam Deck:",
    "network.port_java": "Minecraft Java Edition",
    "network.port_bedrock": "Minecraft Bedrock Edition (Crossplay)",
    "network.port_sftp": "Acesso SFTP / SSH (Mundos e Mods)",
    "network.upnp_title": "Abertura de Portas (Roteador WiFi)",
    "network.upnp_btn": "⚡ Tentar UPnP Automático",
    "network.upnp_default": "Você pode testar se seu roteador permite abertura automática via UPnP ou configurá-lo manualmente no roteador.",
    "network.router_guide_title": "Como abrir as portas no seu Roteador (Passo a Passo):",
    "network.router_step1": "Abra o navegador no seu PC ou celular e acesse seu roteador (geralmente <code>http://192.168.1.1</code> ou <code>http://192.168.0.1</code>).",
    "network.router_step2": "Procure a seção <strong>Redirecionamento de Portas</strong>, <strong>Servidores Virtuais</strong> ou <strong>NAT</strong>.",
    "network.router_step3": "Adicione uma regra para o IP Local do seu Steam Deck (<strong id=\"guide-local-ip\">192.168.x.x</strong>):<br>Porta Externa e Interna: <strong>25565</strong> &bull; Protocolo: <strong>TCP</strong>",
    "network.router_step4": "(Opcional para Bedrock): Adicione uma regra para a porta <strong>19132</strong> com protocolo <strong>UDP</strong>.",
    "network.router_step5": "Salve as alterações no roteador. Seus amigos já poderão se conectar usando seu IP Público!",
    "network.playit_title": "Túnel Seguro Playit.gg (Zero Configuração de Roteador)",
    "network.playit_desc": "Com o Playit.gg você não precisa abrir portas no roteador nem expor seu IP público. O agente cria um túnel seguro direto para os servidores da Playit.",
    "network.playit_key_label": "Chave Secreta do Playit.gg:",
    "network.playit_placeholder": "Cole aqui sua chave secreta do Playit.gg",
    "network.playit_helper_pre": "Não tem uma conta ou túnel? Crie gratuitamente em",
    "network.playit_helper_post": "e configure um túnel para Minecraft (25565).",
    "network.save_playit_btn": "Salvar e Ativar Túnel Playit.gg",
    "network.ssh_title": "Acesso Remoto SFTP / SSH (FileZilla / WinSCP)",
    "network.ssh_desc": "Transfira mundos, mods, datapacks e plugins sem fio do seu PC para a pasta <code>/servidor-mc</code> do Steam Deck.",
    "network.ssh_user_label": "Usuário SFTP:",
    "network.ssh_pass_label": "Senha SFTP:",
    "network.ssh_port_label": "Porta SFTP:",
    "network.sftp_url_label": "URL para FileZilla / WinSCP (Rede Local):",

    // Tools Tab
    "tools.repair_title": "Gerenciamento e Reconciliação Anti-Dessincronização",
    "tools.repair_desc": "Se o Podman relatar estados corrompidos, bloqueios de armazenamento ou erros de socket, esta ferramenta redefine estados órfãos e restaura a sincronização limpa do pod.",
    "tools.repair_btn": "Executar Reconciliação Profunda",
    "tools.perms_title": "Corrigir Permissões de Arquivos",
    "tools.perms_desc": "Executa a rotina rootless <code>podman unshare chown -R 0:0</code> e corrige as permissões de leitura/escrita na pasta de dados para evitar bloqueios.",
    "tools.perms_btn": "Corrigir Permissões de Dados",
    "tools.shortcuts_title": "Integração com a Steam (Gaming Mode)",
    "tools.shortcuts_desc": "Instala atalhos na Área de Trabalho e no menu de aplicativos do SteamOS para abrir o app diretamente no Modo Jogo com suporte a controles.",
    "tools.shortcuts_btn": "Instalar Atalhos",
    "tools.paths_title": "Caminhos de Arquivos no Steam Deck",
    "tools.path_data": "Dados do Minecraft:",
    "tools.path_ssh": "Configuração SSH:",
    "tools.path_app": "Configuração do App:",

    // Modals & Screensaver
    "dialog.cancel": "Cancelar",
    "dialog.ok": "Aceitar",
    "dialog.op_title": "Tornar Administrador (OP)",
    "dialog.op_prompt": "Nome de usuário do jogador de Minecraft:",
    "dialog.whitelist_title": "Adicionar à Whitelist",
    "dialog.whitelist_prompt": "Nome de usuário a autorizar:",
    "dialog.whitelist_java_title": "Adicionar à Whitelist Java",
    "dialog.whitelist_java_prompt": "Nome de usuário Java (executa 'whitelist add <usuário>'):",
    "dialog.whitelist_bedrock_title": "Adicionar à Whitelist Bedrock (Floodgate)",
    "dialog.whitelist_bedrock_prompt": "Gamertag Bedrock/Xbox ou UUID do Floodgate (Dica: Se o jogador nunca entrou no seu servidor, desative temporariamente a whitelist com 'whitelist off' para ele conectar uma vez, ou digite o UUID do Floodgate):",
    "screensaver.hint": "Toque em qualquer botão ou na tela para voltar ao painel",

    // Toast Notifications
    "toast.deploying": "Implantando servidor no mc-pod... Isso pode levar alguns segundos.",
    "toast.deploy_error": "Erro na implantação: {err}",
    "toast.starting": "Iniciando mc-pod...",
    "toast.start_error": "Falha ao iniciar: {err}",
    "toast.stopping": "Parando mc-pod...",
    "toast.restarting": "Reiniciando mc-pod...",
    "toast.repairing": "Executando reconciliação profunda do Podman...",
    "toast.repair_error": "Erro na reconciliação: {err}",
    "toast.fixing_perms": "Aplicando correção de permissões rootless...",
    "toast.perms_fixed": "Permissões corrigidas com sucesso em ~/minecraft-server/data.",
    "toast.saving_playit": "Salvando chave do Playit.gg e atualizando contêiner...",
    "toast.playit_active": "Túnel Playit.gg configurado e ativo.",
    "toast.mojang_updated": "Versões da Mojang atualizadas.",
    "toast.copied": "Copiado para a área de transferência!",
    "toast.upnp_probing": "Verificando suporte a UPnP no roteador WiFi...",
    "toast.upnp_success": "Portas abertas automaticamente via UPnP!",
    "toast.rcon_error": "Erro de RCON: {err}",
    "toast.error": "Erro: {err}"
  }
};

// Supported languages list
export const SUPPORTED_LANGUAGES = [
  { code: "en", name: "English", flag: "🇺🇸" },
  { code: "es", name: "Español", flag: "🇪🇸" },
  { code: "fr", name: "Français", flag: "🇫🇷" },
  { code: "pt", name: "Português", flag: "🇧🇷" }
];

// Current active language (Default is English 'en')
let currentLang = "en";

export function getLanguage() {
  return currentLang;
}

export function setLanguage(lang) {
  if (translations[lang]) {
    currentLang = lang;
  } else {
    currentLang = "en";
  }
  try {
    localStorage.setItem("mc_deck_lang", currentLang);
  } catch (_) {}
  applyTranslations();
  return currentLang;
}

export function initLanguage() {
  let saved = "en";
  try {
    saved = localStorage.getItem("mc_deck_lang");
  } catch (_) {}
  
  if (saved && translations[saved]) {
    currentLang = saved;
  } else {
    currentLang = "en"; // Default primary
  }
  applyTranslations();
  return currentLang;
}

export function t(key, params = {}) {
  const dict = translations[currentLang] || translations.en;
  let text = dict[key] || translations.en[key] || key;
  
  for (const [k, v] of Object.entries(params)) {
    text = text.replace(new RegExp(`\\{${k}\\}`, "g"), v);
  }
  return text;
}

export function applyTranslations() {
  // Translate innerText or textContent for elements with data-i18n
  document.querySelectorAll("[data-i18n]").forEach(el => {
    const key = el.getAttribute("data-i18n");
    if (key) {
      el.textContent = t(key);
    }
  });

  // Translate innerHTML for rich text elements with data-i18n-html
  document.querySelectorAll("[data-i18n-html]").forEach(el => {
    const key = el.getAttribute("data-i18n-html");
    if (key) {
      el.innerHTML = t(key);
    }
  });

  // Translate placeholders
  document.querySelectorAll("[data-i18n-placeholder]").forEach(el => {
    const key = el.getAttribute("data-i18n-placeholder");
    if (key) {
      el.setAttribute("placeholder", t(key));
    }
  });

  // Translate titles / tooltips
  document.querySelectorAll("[data-i18n-title]").forEach(el => {
    const key = el.getAttribute("data-i18n-title");
    if (key) {
      el.setAttribute("title", t(key));
    }
  });

  // Update HTML lang attribute
  document.documentElement.lang = currentLang;
}
