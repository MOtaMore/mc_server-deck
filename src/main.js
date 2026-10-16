import { invoke } from "@tauri-apps/api/core";

// State Management
let currentConfig = {
  version: "1.21.4",
  server_type: "PAPER",
  memory: "4G",
  online_mode: false,
  enable_whitelist: false,
  crossplay: true,
  connection_mode: "public_ip",
  playit_key: "",
  enable_ssh: true,
  ssh_user: "adminmc",
  ssh_pass: "deckcraft123",
  motd: "Servidor Minecraft en Steam Deck",
  difficulty: "normal",
  max_players: 10,
  custom_env: {}
};

let networkInfo = null;
let lastLogText = "";
let isScreensaverActive = false;
let screensaverAnimId = null;
let idleTimer = null;
const IDLE_TIMEOUT_MS = 5 * 60 * 1000; // 5 minutos de inactividad para OLED

// DOM Elements
const elements = {
  // Tabs
  navTabs: document.querySelectorAll(".nav-tab"),
  tabContents: document.querySelectorAll(".tab-content"),
  
  // Header & Badges
  podGlobalBadge: document.getElementById("pod-global-badge"),
  podGlobalText: document.getElementById("pod-global-text"),
  btnScreensaver: document.getElementById("btn-screensaver"),
  
  // Desync Alert
  desyncAlert: document.getElementById("desync-alert"),
  desyncReasonText: document.getElementById("desync-reason-text"),
  btnAutoRepair: document.getElementById("btn-auto-repair"),
  
  // Dashboard Status Cards
  cardPodBadge: document.getElementById("card-pod-badge"),
  podSyncVal: document.getElementById("pod-sync-val"),
  cardServerBadge: document.getElementById("card-server-badge"),
  dashboardVersionVal: document.getElementById("dashboard-version-val"),
  dashboardRamVal: document.getElementById("dashboard-ram-val"),
  cardTunnelBadge: document.getElementById("card-tunnel-badge"),
  dashboardLocalIp: document.getElementById("dashboard-local-ip"),
  dashboardPublicIp: document.getElementById("dashboard-public-ip"),
  cardSshBadge: document.getElementById("card-ssh-badge"),
  dashboardSshUser: document.getElementById("dashboard-ssh-user"),
  
  // Controls
  btnStartServer: document.getElementById("btn-start-server"),
  btnStopServer: document.getElementById("btn-stop-server"),
  btnRestartServer: document.getElementById("btn-restart-server"),
  btnDashboardRepair: document.getElementById("btn-dashboard-repair"),
  
  // Terminal
  terminalBody: document.getElementById("terminal-body"),
  chkAutoscroll: document.getElementById("chk-autoscroll"),
  btnClearLogs: document.getElementById("btn-clear-logs"),
  rconInput: document.getElementById("rcon-input"),
  btnSendRcon: document.getElementById("btn-send-rcon"),
  
  // Config Form
  configForm: document.getElementById("config-form"),
  cfgVersion: document.getElementById("cfg-version"),
  btnRefreshVersions: document.getElementById("btn-refresh-versions"),
  cfgRamSlider: document.getElementById("cfg-ram-slider"),
  ramSliderVal: document.getElementById("ram-slider-val"),
  cfgMotd: document.getElementById("cfg-motd"),
  cfgDifficulty: document.getElementById("cfg-difficulty"),
  cfgMaxPlayers: document.getElementById("cfg-max-players"),
  cfgOnlineMode: document.getElementById("cfg-online-mode"),
  cfgWhitelist: document.getElementById("cfg-whitelist"),
  cfgCrossplay: document.getElementById("cfg-crossplay"),
  
  // Network
  connTabs: document.querySelectorAll(".conn-tab"),
  connPanePublic: document.getElementById("conn-pane-public"),
  connPanePlayit: document.getElementById("conn-pane-playit"),
  netLocalIpFull: document.getElementById("net-local-ip-full"),
  netPublicIpFull: document.getElementById("net-public-ip-full"),
  btnTestUpnp: document.getElementById("btn-test-upnp"),
  upnpResultBox: document.getElementById("upnp-result-box"),
  upnpResultText: document.getElementById("upnp-result-text"),
  guideLocalIp: document.getElementById("guide-local-ip"),
  cfgPlayitKey: document.getElementById("cfg-playit-key"),
  btnSavePlayit: document.getElementById("btn-save-playit"),
  cfgEnableSsh: document.getElementById("cfg-enable-ssh"),
  cfgSshUser: document.getElementById("cfg-ssh-user"),
  cfgSshPass: document.getElementById("cfg-ssh-pass"),
  sftpLocalUrl: document.getElementById("sftp-local-url"),
  
  // Tools
  btnDeepRepair: document.getElementById("btn-deep-repair"),
  btnFixPerms: document.getElementById("btn-fix-perms"),
  btnInstallShortcuts: document.getElementById("btn-install-shortcuts"),
  
  // Dialog Modal
  touchDialog: document.getElementById("touch-dialog"),
  dialogTitle: document.getElementById("dialog-title"),
  dialogMessage: document.getElementById("dialog-message"),
  dialogInput: document.getElementById("dialog-input"),
  dialogBtnCancel: document.getElementById("dialog-btn-cancel"),
  dialogBtnOk: document.getElementById("dialog-btn-ok"),
  
  // Screensaver
  oledScreensaver: document.getElementById("oled-screensaver"),
  bouncingLogo: document.getElementById("bouncing-logo"),
  screensaverStatusBadge: document.getElementById("screensaver-status-badge"),
  
  // Toast
  toastContainer: document.getElementById("toast-container")
};

// ==========================================
// TOAST NOTIFICATIONS
// ==========================================
function showToast(message, type = "info") {
  const toast = document.createElement("div");
  toast.className = `toast toast-${type}`;
  toast.textContent = message;
  elements.toastContainer.appendChild(toast);
  setTimeout(() => {
    toast.style.opacity = "0";
    toast.style.transform = "translateX(40px)";
    toast.style.transition = "all 0.3s ease";
    setTimeout(() => toast.remove(), 300);
  }, 4000);
}

// ==========================================
// TAB NAVIGATION
// ==========================================
elements.navTabs.forEach(tab => {
  tab.addEventListener("click", () => {
    const target = tab.dataset.tab;
    elements.navTabs.forEach(t => t.classList.remove("active"));
    elements.tabContents.forEach(tc => tc.classList.remove("active"));
    
    tab.classList.add("active");
    const activeSection = document.getElementById(`tab-${target}`);
    if (activeSection) activeSection.classList.add("active");
  });
});

// Network sub-tabs
elements.connTabs.forEach(tab => {
  tab.addEventListener("click", () => {
    const mode = tab.dataset.mode;
    elements.connTabs.forEach(t => t.classList.remove("active"));
    tab.classList.add("active");
    
    if (mode === "public_ip") {
      elements.connPanePublic.classList.add("active");
      elements.connPanePlayit.classList.remove("active");
      currentConfig.connection_mode = "public_ip";
    } else {
      elements.connPanePublic.classList.remove("active");
      elements.connPanePlayit.classList.add("active");
      currentConfig.connection_mode = "playit";
    }
  });
});

// ==========================================
// STATUS POLLING & ANTI-DESYNC
// ==========================================
async function refreshStatus() {
  try {
    const status = await invoke("get_status");
    updateStatusUI(status);
  } catch (err) {
    console.error("Error al obtener estado:", err);
  }
}

function updateStatusUI(status) {
  const podState = (status.status || "Unknown").toLowerCase();
  
  // Global Header Badge
  elements.podGlobalBadge.className = "status-pill";
  if (podState === "running" && status.is_healthy) {
    elements.podGlobalBadge.classList.add("status-running");
    elements.podGlobalText.textContent = "Servidor Activo";
    elements.screensaverStatusBadge.textContent = "Servidor Activo";
    elements.screensaverStatusBadge.style.color = "var(--status-green)";
  } else if (podState === "degraded" || status.desync_detected) {
    elements.podGlobalBadge.classList.add("status-degraded");
    elements.podGlobalText.textContent = "Desincronizado";
    elements.screensaverStatusBadge.textContent = "Atención requerida";
    elements.screensaverStatusBadge.style.color = "var(--status-amber)";
  } else if (podState === "not created") {
    elements.podGlobalBadge.classList.add("status-stopped");
    elements.podGlobalText.textContent = "No Creado";
    elements.screensaverStatusBadge.textContent = "Servidor No Creado";
    elements.screensaverStatusBadge.style.color = "var(--text-muted)";
  } else {
    elements.podGlobalBadge.classList.add("status-stopped");
    elements.podGlobalText.textContent = "Detenido";
    elements.screensaverStatusBadge.textContent = "Servidor Detenido";
    elements.screensaverStatusBadge.style.color = "var(--text-muted)";
  }

  // Anti-Desync Alert Banner
  if (status.desync_detected) {
    elements.desyncAlert.classList.remove("hidden");
    elements.desyncReasonText.textContent = status.desync_reason || "Estado del pod inconsistente.";
    elements.podSyncVal.textContent = "Desincronizado";
    elements.podSyncVal.className = "val text-highlight";
  } else {
    elements.desyncAlert.classList.add("hidden");
    elements.podSyncVal.textContent = "Sincronizado";
    elements.podSyncVal.className = "val text-green";
  }

  // Card: mc-pod
  elements.cardPodBadge.textContent = status.status;
  elements.cardPodBadge.className = "badge";
  if (podState === "running") elements.cardPodBadge.classList.add("badge-green");
  else if (podState === "degraded") elements.cardPodBadge.classList.add("badge-amber");
  else elements.cardPodBadge.classList.add("badge-gray");

  // Card: mc-server
  const serverContainer = status.containers ? status.containers["mc-server"] : null;
  if (serverContainer) {
    elements.cardServerBadge.textContent = serverContainer.status;
    elements.cardServerBadge.className = "badge";
    if (serverContainer.status === "running") {
      elements.cardServerBadge.classList.add("badge-green");
    } else {
      elements.cardServerBadge.classList.add("badge-red");
    }
  } else {
    elements.cardServerBadge.textContent = "No Creado";
    elements.cardServerBadge.className = "badge badge-gray";
  }

  // Card: mc-ssh
  const sshContainer = status.containers ? status.containers["mc-ssh"] : null;
  if (sshContainer && sshContainer.status === "running") {
    elements.cardSshBadge.textContent = "Activo";
    elements.cardSshBadge.className = "badge badge-green";
  } else {
    elements.cardSshBadge.textContent = "Detenido";
    elements.cardSshBadge.className = "badge badge-gray";
  }

  // Tunnel Card
  if (currentConfig.connection_mode === "playit") {
    elements.cardTunnelBadge.textContent = "Playit.gg";
    elements.cardTunnelBadge.className = "badge badge-blue";
  } else {
    elements.cardTunnelBadge.textContent = "IP Pública";
    elements.cardTunnelBadge.className = "badge badge-blue";
  }
}

// ==========================================
// TERMINAL LOGS & RCON CONSOLE
// ==========================================
async function refreshLogs() {
  try {
    const logs = await invoke("get_logs", { tail: 80 });
    if (logs && logs !== lastLogText) {
      lastLogText = logs;
      renderLogs(logs);
    }
  } catch (_) {
    // Silencioso si el servidor aún no ha sido lanzado
  }
}

function renderLogs(rawLogs) {
  const lines = rawLogs.split("\n");
  elements.terminalBody.innerHTML = "";
  
  lines.forEach(line => {
    if (!line.trim()) return;
    const div = document.createElement("div");
    div.className = "log-line";
    if (line.includes("WARN") || line.includes("WARNING")) {
      div.style.color = "var(--status-amber)";
    } else if (line.includes("ERROR") || line.includes("Exception")) {
      div.style.color = "var(--status-red)";
    }
    div.textContent = line;
    elements.terminalBody.appendChild(div);
  });

  if (elements.chkAutoscroll.checked) {
    elements.terminalBody.scrollTop = elements.terminalBody.scrollHeight;
  }
}

async function sendRcon(cmd) {
  if (!cmd || !cmd.trim()) return;
  const command = cmd.trim();
  
  // Agregar al terminal local inmediatamente
  const div = document.createElement("div");
  div.className = "log-line cmd-sent";
  div.textContent = `> ${command}`;
  elements.terminalBody.appendChild(div);
  elements.terminalBody.scrollTop = elements.terminalBody.scrollHeight;
  
  try {
    const res = await invoke("send_rcon", { command });
    if (res && res.trim()) {
      const respDiv = document.createElement("div");
      respDiv.className = "log-line";
      respDiv.style.color = "var(--accent-cyan)";
      respDiv.textContent = res.trim();
      elements.terminalBody.appendChild(respDiv);
      elements.terminalBody.scrollTop = elements.terminalBody.scrollHeight;
    }
  } catch (err) {
    showToast(`Error RCON: ${err}`, "error");
  }
}

elements.btnSendRcon.addEventListener("click", () => {
  sendRcon(elements.rconInput.value);
  elements.rconInput.value = "";
});

elements.rconInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter") {
    sendRcon(elements.rconInput.value);
    elements.rconInput.value = "";
  }
});

elements.btnClearLogs.addEventListener("click", () => {
  elements.terminalBody.innerHTML = '<div class="log-line text-muted">[Consola limpiada localmente]</div>';
});

// Quick command macro buttons
document.querySelectorAll(".btn-chip").forEach(chip => {
  chip.addEventListener("click", () => {
    const cmd = chip.dataset.cmd;
    const macro = chip.dataset.macro;
    
    if (cmd) {
      sendRcon(cmd);
    } else if (macro === "op") {
      openTouchDialog("Hacer Administrador (OP)", "Nombre de usuario del jugador de Minecraft:", (user) => {
        if (user) sendRcon(`op ${user}`);
      });
    } else if (macro === "whitelist") {
      openTouchDialog("Agregar a Whitelist", "Nombre de usuario a autorizar:", (user) => {
        if (user) sendRcon(`whitelist add ${user}`);
      });
    }
  });
});

// ==========================================
// SERVER CONTROLS & ACTIONS
// ==========================================
elements.btnStartServer.addEventListener("click", async () => {
  showToast("Iniciando mc-pod...", "info");
  try {
    const res = await invoke("start_server");
    showToast(res, "success");
    await refreshStatus();
  } catch (err) {
    showToast(`Fallo al iniciar: ${err}`, "error");
  }
});

elements.btnStopServer.addEventListener("click", async () => {
  showToast("Deteniendo mc-pod...", "info");
  try {
    const res = await invoke("stop_server");
    showToast(res, "info");
    await refreshStatus();
  } catch (err) {
    showToast(`Error: ${err}`, "error");
  }
});

elements.btnRestartServer.addEventListener("click", async () => {
  showToast("Reiniciando mc-pod...", "info");
  try {
    const res = await invoke("restart_server");
    showToast(res, "success");
    await refreshStatus();
  } catch (err) {
    showToast(`Error: ${err}`, "error");
  }
});

// Anti-Desync Repair Routine
async function triggerRepair() {
  showToast("Ejecutando reconciliación y reparación profunda de Podman...", "info");
  try {
    const res = await invoke("repair_pod");
    showToast(res, "success");
    await refreshStatus();
  } catch (err) {
    showToast(`Error en reconciliación: ${err}`, "error");
  }
}

elements.btnAutoRepair.addEventListener("click", triggerRepair);
elements.btnDashboardRepair.addEventListener("click", triggerRepair);
elements.btnDeepRepair.addEventListener("click", triggerRepair);

// Fix Permissions
elements.btnFixPerms.addEventListener("click", async () => {
  showToast("Aplicando corrección de permisos rootless...", "info");
  try {
    await invoke("repair_pod"); // Ejecuta unshare chown -R 0:0 y chmod
    showToast("Permisos corregidos exitosamente en ~/minecraft-server/data.", "success");
  } catch (err) {
    showToast(`Error: ${err}`, "error");
  }
});

// Install Shortcuts
elements.btnInstallShortcuts.addEventListener("click", async () => {
  try {
    const res = await invoke("install_shortcuts");
    showToast(res, "success");
  } catch (err) {
    showToast(`Error: ${err}`, "error");
  }
});

// ==========================================
// CONFIGURATION WIZARD
// ==========================================
async function loadConfigData() {
  try {
    const cfg = await invoke("load_config");
    currentConfig = { ...currentConfig, ...cfg };
    populateConfigForm();
  } catch (err) {
    console.error("Error al cargar config:", err);
  }
}

function populateConfigForm() {
  if (currentConfig.version) elements.cfgVersion.value = currentConfig.version;
  
  // Server Type Radios
  const typeRadios = document.querySelectorAll('input[name="server_type"]');
  typeRadios.forEach(r => {
    r.checked = (r.value === currentConfig.server_type);
    const card = r.closest(".type-card");
    if (card) {
      if (r.checked) card.classList.add("active");
      else card.classList.remove("active");
    }
  });

  // RAM Slider
  const ramNum = parseInt(currentConfig.memory) || 4;
  elements.cfgRamSlider.value = ramNum;
  elements.ramSliderVal.textContent = `${ramNum} GB`;
  elements.dashboardRamVal.textContent = `${ramNum}G`;
  
  // Inputs
  elements.cfgMotd.value = currentConfig.motd || "";
  elements.cfgDifficulty.value = currentConfig.difficulty || "normal";
  elements.cfgMaxPlayers.value = currentConfig.max_players || 10;
  elements.cfgOnlineMode.checked = currentConfig.online_mode || false;
  elements.cfgWhitelist.checked = currentConfig.enable_whitelist || false;
  elements.cfgCrossplay.checked = currentConfig.crossplay !== false;
  
  // SSH & Playit
  elements.cfgPlayitKey.value = currentConfig.playit_key || "";
  elements.cfgEnableSsh.checked = currentConfig.enable_ssh !== false;
  elements.cfgSshUser.value = currentConfig.ssh_user || "adminmc";
  elements.cfgSshPass.value = currentConfig.ssh_pass || "deckcraft123";
  elements.dashboardSshUser.textContent = elements.cfgSshUser.value;

  // Connection mode tab
  if (currentConfig.connection_mode === "playit") {
    elements.connTabs[1].click();
  } else {
    elements.connTabs[0].click();
  }

  // Update summary badge
  elements.dashboardVersionVal.textContent = `${currentConfig.version} (${currentConfig.server_type})`;
}

// Server Type Card Click Handler
document.querySelectorAll(".type-card").forEach(card => {
  card.addEventListener("click", () => {
    document.querySelectorAll(".type-card").forEach(c => c.classList.remove("active"));
    card.classList.add("active");
    const radio = card.querySelector('input[type="radio"]');
    if (radio) {
      radio.checked = true;
      currentConfig.server_type = radio.value;
    }
  });
});

// RAM Slider change
elements.cfgRamSlider.addEventListener("input", (e) => {
  const val = e.target.value;
  elements.ramSliderVal.textContent = `${val} GB`;
  currentConfig.memory = `${val}G`;
});

// Load Versions from Mojang API
async function loadMinecraftVersions() {
  try {
    const res = await invoke("get_minecraft_versions");
    if (res && res.versions && res.versions.length > 0) {
      elements.cfgVersion.innerHTML = "";
      res.versions.forEach(v => {
        const opt = document.createElement("option");
        opt.value = v.id;
        opt.textContent = `${v.id} ${v.id === res.latest_release ? "(Última versión estable)" : ""}`;
        if (v.id === currentConfig.version) opt.selected = true;
        elements.cfgVersion.appendChild(opt);
      });
      showToast("Versiones de Mojang actualizadas.", "info");
    }
  } catch (err) {
    console.warn("Fallo al consultar versiones en vivo:", err);
  }
}

elements.btnRefreshVersions.addEventListener("click", loadMinecraftVersions);

// Deploy Server Config
elements.configForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  
  const selectedType = document.querySelector('input[name="server_type"]:checked');
  const typeVal = selectedType ? selectedType.value : "PAPER";
  
  const deployConfig = {
    version: elements.cfgVersion.value || "1.21.4",
    server_type: typeVal,
    memory: `${elements.cfgRamSlider.value}G`,
    online_mode: elements.cfgOnlineMode.checked,
    enable_whitelist: elements.cfgWhitelist.checked,
    crossplay: elements.cfgCrossplay.checked,
    connection_mode: currentConfig.connection_mode || "public_ip",
    playit_key: elements.cfgPlayitKey.value.trim(),
    enable_ssh: elements.cfgEnableSsh.checked,
    ssh_user: elements.cfgSshUser.value.trim() || "adminmc",
    ssh_pass: elements.cfgSshPass.value.trim() || "deckcraft123",
    motd: elements.cfgMotd.value.trim(),
    difficulty: elements.cfgDifficulty.value,
    max_players: parseInt(elements.cfgMaxPlayers.value) || 10,
    custom_env: {}
  };

  currentConfig = deployConfig;
  showToast("Desplegando servidor en mc-pod... Esto puede tomar unos segundos.", "info");
  
  try {
    const res = await invoke("deploy_server", { config: deployConfig });
    showToast(res, "success");
    await refreshStatus();
    // Volver al dashboard
    elements.navTabs[0].click();
  } catch (err) {
    showToast(`Error al desplegar: ${err}`, "error");
  }
});

// Save Playit Secret Key
elements.btnSavePlayit.addEventListener("click", async () => {
  const key = elements.cfgPlayitKey.value.trim();
  currentConfig.playit_key = key;
  currentConfig.connection_mode = "playit";
  showToast("Guardando clave de Playit.gg y actualizando contenedor...", "info");
  try {
    await invoke("save_config", { config: currentConfig });
    await invoke("deploy_server", { config: currentConfig });
    showToast("Túnel Playit.gg configurado y activo.", "success");
  } catch (err) {
    showToast(`Error: ${err}`, "error");
  }
});

// ==========================================
// NETWORK & IP ADDRESSES
// ==========================================
async function loadNetworkInfo() {
  try {
    networkInfo = await invoke("get_network_info");
    
    // Local IP
    elements.dashboardLocalIp.textContent = networkInfo.local_ip;
    elements.guideLocalIp.textContent = networkInfo.local_ip;
    elements.netLocalIpFull.textContent = `${networkInfo.local_ip}:${networkInfo.mc_java_port}`;
    elements.sftpLocalUrl.textContent = `sftp://${currentConfig.ssh_user || 'adminmc'}@${networkInfo.local_ip}:${networkInfo.ssh_port}`;
    
    // Public IP
    if (networkInfo.public_ip) {
      elements.dashboardPublicIp.textContent = networkInfo.public_ip;
      elements.netPublicIpFull.textContent = `${networkInfo.public_ip}:${networkInfo.mc_java_port}`;
    } else {
      elements.dashboardPublicIp.textContent = "No disponible";
      elements.netPublicIpFull.textContent = "No se detectó IP Pública";
    }
  } catch (err) {
    console.error("Error al cargar datos de red:", err);
  }
}

// UPnP Button
elements.btnTestUpnp.addEventListener("click", async () => {
  elements.upnpResultText.textContent = "Sondeando soporte UPnP en tu router WiFi...";
  try {
    const [ok, msg] = await invoke("test_upnp");
    elements.upnpResultText.textContent = msg;
    if (ok) {
      showToast("¡Puertos abiertos automáticamente vía UPnP!", "success");
    }
  } catch (err) {
    elements.upnpResultText.textContent = `Error: ${err}`;
  }
});

// Copy Buttons
document.querySelectorAll(".btn-copy").forEach(btn => {
  btn.addEventListener("click", () => {
    const targetId = btn.dataset.copy;
    const el = document.getElementById(targetId);
    if (el) {
      navigator.clipboard.writeText(el.textContent.trim());
      showToast("¡Copiado al portapapeles!", "success");
    }
  });
});

// ==========================================
// TOUCH DIALOG MODAL
// ==========================================
let dialogCallback = null;

function openTouchDialog(title, message, callback) {
  elements.dialogTitle.textContent = title;
  elements.dialogMessage.textContent = message;
  elements.dialogInput.value = "";
  dialogCallback = callback;
  elements.touchDialog.classList.remove("hidden");
  elements.dialogInput.focus();
}

elements.dialogBtnCancel.addEventListener("click", () => {
  elements.touchDialog.classList.add("hidden");
  dialogCallback = null;
});

elements.dialogBtnOk.addEventListener("click", () => {
  const val = elements.dialogInput.value.trim();
  elements.touchDialog.classList.add("hidden");
  if (dialogCallback) dialogCallback(val);
  dialogCallback = null;
});

elements.dialogInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter") elements.dialogBtnOk.click();
});

// ==========================================
// OLED SCREENSAVER (ANTI-BURN-IN CRT/DVD STYLE)
// ==========================================
let posX = 100, posY = 100;
let velX = 1.6, velY = 1.2;

function startScreensaver() {
  isScreensaverActive = true;
  elements.oledScreensaver.classList.remove("hidden");
  
  // Random start
  posX = Math.random() * (window.innerWidth - 300);
  posY = Math.random() * (window.innerHeight - 150);
  
  function bounce() {
    if (!isScreensaverActive) return;
    
    const logoW = elements.bouncingLogo.offsetWidth || 260;
    const logoH = elements.bouncingLogo.offsetHeight || 90;
    const maxW = window.innerWidth - logoW;
    const maxH = window.innerHeight - logoH;
    
    posX += velX;
    posY += velY;
    
    if (posX >= maxW) { posX = maxW; velX = -Math.abs(velX); }
    if (posX <= 0) { posX = 0; velX = Math.abs(velX); }
    if (posY >= maxH) { posY = maxH; velY = -Math.abs(velY); }
    if (posY <= 0) { posY = 0; velY = Math.abs(velY); }
    
    elements.bouncingLogo.style.transform = `translate3d(${posX}px, ${posY}px, 0)`;
    screensaverAnimId = requestAnimationFrame(bounce);
  }
  
  screensaverAnimId = requestAnimationFrame(bounce);
}

function stopScreensaver() {
  if (!isScreensaverActive) return;
  isScreensaverActive = false;
  elements.oledScreensaver.classList.add("hidden");
  if (screensaverAnimId) {
    cancelAnimationFrame(screensaverAnimId);
    screensaverAnimId = null;
  }
  resetIdleTimer();
}

elements.btnScreensaver.addEventListener("click", startScreensaver);
elements.oledScreensaver.addEventListener("click", stopScreensaver);

function resetIdleTimer() {
  if (idleTimer) clearTimeout(idleTimer);
  if (!isScreensaverActive) {
    idleTimer = setTimeout(startScreensaver, IDLE_TIMEOUT_MS);
  }
}

// User activity listener to dismiss screensaver & reset idle timer
["touchstart", "mousedown", "keydown"].forEach(evt => {
  window.addEventListener(evt, () => {
    if (isScreensaverActive) stopScreensaver();
    resetIdleTimer();
  }, { passive: true });
});

// ==========================================
// INITIALIZATION
// ==========================================
async function init() {
  resetIdleTimer();
  await loadConfigData();
  await loadMinecraftVersions();
  await loadNetworkInfo();
  await refreshStatus();
  await refreshLogs();
  
  // Interval loops for real-time monitoring
  setInterval(refreshStatus, 3000);
  setInterval(refreshLogs, 2500);
}

window.addEventListener("DOMContentLoaded", init);
