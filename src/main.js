import { invoke } from "@tauri-apps/api/core";
import { initLanguage, setLanguage, getLanguage, t, applyTranslations } from "./i18n.js";

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
  motd: "Minecraft Server on Steam Deck",
  difficulty: "normal",
  max_players: 10,
  custom_env: {}
};

let networkInfo = null;
let lastLogText = "";
let lastStatus = null;
let isScreensaverActive = false;
let screensaverAnimId = null;
let idleTimer = null;
const IDLE_TIMEOUT_MS = 5 * 60 * 1000; // 5 min idle timer for OLED

// DOM Elements
const elements = {
  // Language Selector
  langSelect: document.getElementById("lang-select"),

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
    lastStatus = status;
    updateStatusUI(status);
  } catch (err) {
    console.error("Error fetching status:", err);
  }
}

function updateStatusUI(status) {
  if (!status) return;
  const podState = (status.status || "Unknown").toLowerCase();
  
  // Global Header Badge
  elements.podGlobalBadge.className = "status-pill";
  if (podState === "running" && status.is_healthy) {
    elements.podGlobalBadge.classList.add("status-running");
    elements.podGlobalText.textContent = t("status.running");
    elements.screensaverStatusBadge.textContent = t("status.running");
    elements.screensaverStatusBadge.style.color = "var(--status-green)";
  } else if (podState === "degraded" || status.desync_detected) {
    elements.podGlobalBadge.classList.add("status-degraded");
    elements.podGlobalText.textContent = t("status.degraded");
    elements.screensaverStatusBadge.textContent = t("status.attention_required");
    elements.screensaverStatusBadge.style.color = "var(--status-amber)";
  } else if (podState === "not created") {
    elements.podGlobalBadge.classList.add("status-stopped");
    elements.podGlobalText.textContent = t("status.not_created");
    elements.screensaverStatusBadge.textContent = t("status.server_not_created");
    elements.screensaverStatusBadge.style.color = "var(--text-muted)";
  } else {
    elements.podGlobalBadge.classList.add("status-stopped");
    elements.podGlobalText.textContent = t("status.stopped");
    elements.screensaverStatusBadge.textContent = t("status.server_stopped");
    elements.screensaverStatusBadge.style.color = "var(--text-muted)";
  }

  // Anti-Desync Alert Banner
  if (status.desync_detected) {
    elements.desyncAlert.classList.remove("hidden");
    elements.desyncReasonText.textContent = status.desync_reason || t("alert.desync_default_reason");
    elements.podSyncVal.textContent = t("status.degraded");
    elements.podSyncVal.className = "val text-highlight";
  } else {
    elements.desyncAlert.classList.add("hidden");
    elements.podSyncVal.textContent = t("status.optimal");
    elements.podSyncVal.className = "val text-green";
  }

  // Card: mc-pod
  elements.cardPodBadge.className = "badge";
  if (podState === "running") {
    elements.cardPodBadge.textContent = t("status.running");
    elements.cardPodBadge.classList.add("badge-green");
  } else if (podState === "degraded") {
    elements.cardPodBadge.textContent = t("status.degraded");
    elements.cardPodBadge.classList.add("badge-amber");
  } else if (podState === "not created") {
    elements.cardPodBadge.textContent = t("status.not_created");
    elements.cardPodBadge.classList.add("badge-gray");
  } else {
    elements.cardPodBadge.textContent = status.status || t("status.stopped");
    elements.cardPodBadge.classList.add("badge-gray");
  }

  // Card: mc-server
  const serverContainer = status.containers ? status.containers["mc-server"] : null;
  if (serverContainer) {
    elements.cardServerBadge.className = "badge";
    if (serverContainer.status === "running") {
      elements.cardServerBadge.textContent = t("status.running");
      elements.cardServerBadge.classList.add("badge-green");
    } else {
      elements.cardServerBadge.textContent = serverContainer.status;
      elements.cardServerBadge.classList.add("badge-red");
    }
  } else {
    elements.cardServerBadge.textContent = t("status.not_found");
    elements.cardServerBadge.className = "badge badge-gray";
  }

  // Card: mc-ssh
  const sshContainer = status.containers ? status.containers["mc-ssh"] : null;
  if (sshContainer && sshContainer.status === "running") {
    elements.cardSshBadge.textContent = t("status.active");
    elements.cardSshBadge.className = "badge badge-green";
  } else {
    elements.cardSshBadge.textContent = t("status.stopped");
    elements.cardSshBadge.className = "badge badge-gray";
  }

  // Tunnel Card
  if (currentConfig.connection_mode === "playit") {
    elements.cardTunnelBadge.textContent = "Playit.gg";
    elements.cardTunnelBadge.className = "badge badge-blue";
  } else {
    elements.cardTunnelBadge.textContent = t("status.public_ip");
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
    // Silent before server launched
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
  
  // Add to local terminal immediately
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
    showToast(t("toast.rcon_error", { err }), "error");
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
  elements.terminalBody.innerHTML = `<div class="log-line text-muted">${t("terminal.cleared_locally")}</div>`;
});

// Quick command macro buttons
document.querySelectorAll(".btn-chip").forEach(chip => {
  chip.addEventListener("click", () => {
    const cmd = chip.dataset.cmd;
    const macro = chip.dataset.macro;
    
    if (cmd) {
      sendRcon(cmd);
    } else if (macro === "op") {
      openTouchDialog(t("dialog.op_title"), t("dialog.op_prompt"), (user) => {
        if (user) sendRcon(`op ${user}`);
      });
    } else if (macro === "whitelist_java" || macro === "whitelist") {
      openTouchDialog(t("dialog.whitelist_java_title"), t("dialog.whitelist_java_prompt"), (user) => {
        if (user) sendRcon(`whitelist add ${user}`);
      });
    } else if (macro === "whitelist_bedrock") {
      openTouchDialog(t("dialog.whitelist_bedrock_title"), t("dialog.whitelist_bedrock_prompt"), (user) => {
        if (user) {
          const formattedUser = (user.includes(" ") && !user.startsWith('"')) ? `"${user}"` : user;
          sendRcon(`fwhitelist add ${formattedUser}`);
        }
      });
    }
  });
});

// ==========================================
// SERVER CONTROLS & ACTIONS
// ==========================================
elements.btnStartServer.addEventListener("click", async () => {
  showToast(t("toast.starting"), "info");
  try {
    const res = await invoke("start_server");
    showToast(res, "success");
    await refreshStatus();
  } catch (err) {
    showToast(t("toast.start_error", { err }), "error");
  }
});

elements.btnStopServer.addEventListener("click", async () => {
  showToast(t("toast.stopping"), "info");
  try {
    const res = await invoke("stop_server");
    showToast(res, "info");
    await refreshStatus();
  } catch (err) {
    showToast(t("toast.error", { err }), "error");
  }
});

elements.btnRestartServer.addEventListener("click", async () => {
  showToast(t("toast.restarting"), "info");
  try {
    const res = await invoke("restart_server");
    showToast(res, "success");
    await refreshStatus();
  } catch (err) {
    showToast(t("toast.error", { err }), "error");
  }
});

// Anti-Desync Repair Routine
async function triggerRepair() {
  showToast(t("toast.repairing"), "info");
  try {
    const res = await invoke("repair_pod");
    showToast(res, "success");
    await refreshStatus();
  } catch (err) {
    showToast(t("toast.repair_error", { err }), "error");
  }
}

elements.btnAutoRepair.addEventListener("click", triggerRepair);
elements.btnDashboardRepair.addEventListener("click", triggerRepair);
elements.btnDeepRepair.addEventListener("click", triggerRepair);

// Fix Permissions
elements.btnFixPerms.addEventListener("click", async () => {
  showToast(t("toast.fixing_perms"), "info");
  try {
    await invoke("repair_pod"); // Executes unshare chown -R 0:0 and fixes permissions
    showToast(t("toast.perms_fixed"), "success");
  } catch (err) {
    showToast(t("toast.error", { err }), "error");
  }
});

// Install Shortcuts
elements.btnInstallShortcuts.addEventListener("click", async () => {
  try {
    const res = await invoke("install_shortcuts");
    showToast(res, "success");
  } catch (err) {
    showToast(t("toast.error", { err }), "error");
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
    console.error("Error loading config:", err);
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
        opt.textContent = `${v.id} ${v.id === res.latest_release ? t("config.latest_stable") : ""}`;
        if (v.id === currentConfig.version) opt.selected = true;
        elements.cfgVersion.appendChild(opt);
      });
      showToast(t("toast.mojang_updated"), "info");
    }
  } catch (err) {
    console.warn("Failed to fetch Mojang versions in real-time:", err);
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
  showToast(t("toast.deploying"), "info");
  
  try {
    const res = await invoke("deploy_server", { config: deployConfig });
    showToast(res, "success");
    await refreshStatus();
    // Return to dashboard
    elements.navTabs[0].click();
  } catch (err) {
    showToast(t("toast.deploy_error", { err }), "error");
  }
});

// Save Playit Secret Key
elements.btnSavePlayit.addEventListener("click", async () => {
  const key = elements.cfgPlayitKey.value.trim();
  currentConfig.playit_key = key;
  currentConfig.connection_mode = "playit";
  showToast(t("toast.saving_playit"), "info");
  try {
    await invoke("save_config", { config: currentConfig });
    await invoke("deploy_server", { config: currentConfig });
    showToast(t("toast.playit_active"), "success");
  } catch (err) {
    showToast(t("toast.error", { err }), "error");
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
      elements.dashboardPublicIp.textContent = t("status.not_available");
      elements.netPublicIpFull.textContent = t("status.no_public_ip");
    }
  } catch (err) {
    console.error("Error loading network info:", err);
  }
}

// UPnP Button
elements.btnTestUpnp.addEventListener("click", async () => {
  elements.upnpResultText.textContent = t("toast.upnp_probing");
  try {
    const [ok, msg] = await invoke("test_upnp");
    elements.upnpResultText.textContent = msg;
    if (ok) {
      showToast(t("toast.upnp_success"), "success");
    }
  } catch (err) {
    showToast(t("toast.error", { err }), "error");
  }
});

// Copy Buttons
document.querySelectorAll(".btn-copy").forEach(btn => {
  btn.addEventListener("click", () => {
    const targetId = btn.dataset.copy;
    const el = document.getElementById(targetId);
    if (el) {
      navigator.clipboard.writeText(el.textContent.trim());
      showToast(t("toast.copied"), "success");
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
  // Initialize internationalization (defaults to English 'en')
  const activeLang = initLanguage();
  if (elements.langSelect) {
    elements.langSelect.value = activeLang;
    elements.langSelect.addEventListener("change", (e) => {
      const newLang = e.target.value;
      setLanguage(newLang);
      if (lastStatus) updateStatusUI(lastStatus);
      if (networkInfo) loadNetworkInfo();
    });
  }

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
