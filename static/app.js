/* ==========================================================================
   NECROSHELL FRONTEND ENGINE JAVASCRIPT
   Connects UI to Localhost FastAPI Endpoints for Terminal Possession,
   Code Séances, and Log Horror Tales via Groq LPUs.
   ========================================================================== */

document.addEventListener("DOMContentLoaded", () => {
    initTabs();
    initStatus();
    initCrtToggle();
    initTerminal();
    initSeance();
    initStories();
});

/* --------------------------------------------------------------------------
   1. TAB NAVIGATION
   -------------------------------------------------------------------------- */
function initTabs() {
    const tabs = document.querySelectorAll(".nav-tab");
    const contents = document.querySelectorAll(".tab-content");

    tabs.forEach(tab => {
        tab.addEventListener("click", () => {
            const targetId = tab.dataset.tab;
            tabs.forEach(t => t.classList.remove("active"));
            contents.forEach(c => c.classList.remove("active"));

            tab.classList.add("active");
            const targetContent = document.getElementById(targetId);
            if (targetContent) targetContent.classList.add("active");
        });
    });
}

/* --------------------------------------------------------------------------
   2. SYSTEM STATUS & CONNECTION
   -------------------------------------------------------------------------- */
async function initStatus() {
    const statusText = document.getElementById("statusText");
    const activeModelTag = document.getElementById("activeModelTag");
    const specEngine = document.getElementById("specEngine");
    const specModel = document.getElementById("specModel");
    const specPulse = document.getElementById("specPulse");

    try {
        const res = await fetch("/api/status");
        if (res.ok) {
            const data = await res.json();
            statusText.textContent = `PULSE: ${data.status.toUpperCase()} (${data.pulse})`;
            activeModelTag.textContent = data.model;
            if (specEngine) specEngine.textContent = data.engine;
            if (specModel) specModel.textContent = data.model;
            if (specPulse) specPulse.textContent = `ONLINE: "${data.pulse}"`;
        } else {
            statusText.textContent = "VOID DEGRADED";
        }
    } catch (err) {
        statusText.textContent = "OFFLINE PORTAL";
    }
}

/* --------------------------------------------------------------------------
   3. CRT EFFECT TOGGLE
   -------------------------------------------------------------------------- */
function initCrtToggle() {
    const btn = document.getElementById("crtToggle");
    btn.addEventListener("click", () => {
        const isEnabled = document.body.classList.toggle("crt-enabled");
        btn.textContent = isEnabled ? "CRT: ON" : "CRT: OFF";
    });
}

/* --------------------------------------------------------------------------
   4. TERMINAL POSSESSION
   -------------------------------------------------------------------------- */
function initTerminal() {
    const input = document.getElementById("terminalInput");
    const btnExecute = document.getElementById("btnExecute");
    const terminalOutput = document.getElementById("terminalOutput");
    const chkSimulate = document.getElementById("chkSimulate");
    const btnClear = document.getElementById("btnClearTerminal");

    // Quick command buttons
    document.querySelectorAll(".quick-cmd").forEach(b => {
        b.addEventListener("click", () => {
            input.value = b.dataset.cmd;
            executeCommand();
        });
    });

    btnClear.addEventListener("click", () => {
        terminalOutput.innerHTML = "";
    });

    btnExecute.addEventListener("click", executeCommand);
    input.addEventListener("keydown", (e) => {
        if (e.key === "Enter") {
            e.preventDefault();
            executeCommand();
        }
    });

    async function executeCommand() {
        const cmd = input.value.trim();
        if (!cmd) return;

        input.value = "";
        const simulate = chkSimulate.checked;

        // Render command row
        const entry = document.createElement("div");
        entry.className = "term-entry";
        entry.innerHTML = `
            <div class="term-cmd-row">
                <span class="term-prompt-tag">necro:week3 ❯</span>
                <span class="term-cmd-text">${escapeHtml(cmd)}</span>
            </div>
            <div class="term-loading" style="color: var(--color-cyan); font-size: 0.8rem;">
                ⚡ Invocation reverberating in registers...
            </div>
        `;
        terminalOutput.appendChild(entry);
        terminalOutput.scrollTop = terminalOutput.scrollHeight;

        try {
            const res = await fetch("/api/observe", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ command: cmd, simulate })
            });

            const data = await res.json();
            const loadingEl = entry.querySelector(".term-loading");
            if (loadingEl) loadingEl.remove();

            let outHtml = "";
            if (data.stdout && data.stdout.trim()) {
                outHtml += `<pre class="term-output-raw">${escapeHtml(data.stdout)}</pre>`;
            }
            if (data.stderr && data.stderr.trim()) {
                outHtml += `<pre class="term-output-raw is-error">${escapeHtml(data.stderr)}</pre>`;
            }

            const isErr = data.exit_code !== 0;
            const whisperClass = isErr ? "daemon-whisper-box whisper-error" : "daemon-whisper-box";
            const icon = isErr ? "💀" : "👁️";

            outHtml += `
                <div class="${whisperClass}">
                    <span class="whisper-label">${icon} NecroDaemon Whisper (exit code: ${data.exit_code}) [${data.model}]</span>
                    <p>${escapeHtml(data.whisper)}</p>
                </div>
            `;
            entry.insertAdjacentHTML("beforeend", outHtml);
            terminalOutput.scrollTop = terminalOutput.scrollHeight;

        } catch (err) {
            entry.insertAdjacentHTML("beforeend", `
                <div class="daemon-whisper-box whisper-error">
                    <span class="whisper-label">💀 Portal Severed</span>
                    <p>Failed to commune with NecroDaemon: ${escapeHtml(err.message)}</p>
                </div>
            `);
        }
    }
}

/* --------------------------------------------------------------------------
   5. DIGITAL OFRENDA / SÉANCE
   -------------------------------------------------------------------------- */
let cachedSamples = {};

async function initSeance() {
    const codeEditor = document.getElementById("codeEditor");
    const artifactNameInput = document.getElementById("artifactNameInput");
    const btnSummon = document.getElementById("btnSummonSeance");
    const seanceOutput = document.getElementById("seanceOutput");

    // Fetch built-in samples
    try {
        const res = await fetch("/api/samples");
        if (res.ok) cachedSamples = await res.json();
    } catch (e) {
        console.error("Could not load samples:", e);
    }

    // Preset buttons
    document.querySelectorAll(".preset-btn[data-sample]").forEach(btn => {
        btn.addEventListener("click", () => {
            const sampleKey = btn.dataset.sample;
            if (cachedSamples[sampleKey]) {
                artifactNameInput.value = cachedSamples[sampleKey].title;
                codeEditor.value = cachedSamples[sampleKey].code;
            }
        });
    });

    // Default to cobol
    if (cachedSamples["cobol"]) {
        artifactNameInput.value = cachedSamples["cobol"].title;
        codeEditor.value = cachedSamples["cobol"].code;
    }

    btnSummon.addEventListener("click", async () => {
        const code = codeEditor.value.trim();
        const artifactName = artifactNameInput.value.trim() || "Sacrificial Offering";

        if (!code) {
            alert("The altar remains empty! Please paste code or select a preset.");
            return;
        }

        seanceOutput.innerHTML = `
            <div class="oracle-placeholder">
                <div class="placeholder-icon" style="animation: pulse-skull 1.5s infinite;">🕯️</div>
                <p>Burning digital incense at the altar...</p>
                <span class="placeholder-sub">Awakening Ada Lovelace, Alan Turing, and Grace Hopper...</span>
            </div>
        `;

        try {
            const res = await fetch("/api/seance", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ code, artifact_name: artifactName })
            });

            const data = await res.json();
            if (data.analysis) {
                const htmlContent = marked.parse(data.analysis);
                seanceOutput.innerHTML = `
                    <div class="seance-result">
                        <div style="font-size:0.75rem; color:var(--color-cyan); margin-bottom:1rem; font-family:var(--font-mono);">
                            Summoned via: ${data.model}
                        </div>
                        ${htmlContent}
                    </div>
                `;
            } else {
                seanceOutput.innerHTML = `<p style="color:var(--color-red);">The spirits refused to speak: ${escapeHtml(data.detail || "Unknown error")}</p>`;
            }
        } catch (err) {
            seanceOutput.innerHTML = `<p style="color:var(--color-red);">Séance interrupted: ${escapeHtml(err.message)}</p>`;
        }
    });
}

/* --------------------------------------------------------------------------
   6. LOG GHOST STORIES
   -------------------------------------------------------------------------- */
function initStories() {
    const logInput = document.getElementById("logInput");
    const btnLoadSample = document.getElementById("btnLoadSampleLogs");
    const btnGenerate = document.getElementById("btnGenerateStory");
    const storyOutput = document.getElementById("storyOutput");

    const sampleLogData = `[SYSTEM CHRONICLES - SECTOR D-9]
TIMESTAMP: 2026-10-31T03:59:59.004Z
KERNEL: ring_buffer_overflow @ 0x7FFF00DEADC0
PID 666 (necro_daemon): CPU spike 99.4% in thread 0x4B (MEMORY_HUNGER)
DAEMON: child process 1337 terminated unexpectedly: signal SIGKILL (exit status 137)
SOCKET: 0.0.0.0:6666 listening ... UNKNOWN_PAYLOAD received from 127.0.0.1:void
SWAP_SPACE: 84% exhausted. Page faults rising exponentially (12,481 faults/sec)
AUDIT: User 'root' attempted authentication 404 times without password
SYSTEM STATUS: Silicon temperatures surging (94C). Unidentified interrupts in IRQ 13.`;

    btnLoadSample.addEventListener("click", () => {
        logInput.value = sampleLogData;
    });

    btnGenerate.addEventListener("click", async () => {
        const logs = logInput.value.trim();
        if (!logs) {
            alert("Please paste logs or click 'Load Corrupted Kernel Logs' first.");
            return;
        }

        storyOutput.innerHTML = `
            <div class="oracle-placeholder">
                <div class="placeholder-icon" style="animation: pulse-skull 1.5s infinite;">🩸</div>
                <p>Chronicling the ghosts within the machine...</p>
                <span class="placeholder-sub">Transmuting stack frames and CPU heat into cosmic horror...</span>
            </div>
        `;

        try {
            const res = await fetch("/api/story", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ logs })
            });

            const data = await res.json();
            if (data.story) {
                const formatted = marked.parse(data.story);
                storyOutput.innerHTML = `
                    <div class="story-result">
                        <div style="font-size:0.75rem; color:var(--color-red); margin-bottom:1rem; font-family:var(--font-mono);">
                            Decoded by Open-Weight Intelligence (${data.model})
                        </div>
                        ${formatted}
                    </div>
                `;
            } else {
                storyOutput.innerHTML = `<p style="color:var(--color-red);">Void swallowed the chronicle: ${escapeHtml(data.detail || "Error")}</p>`;
            }
        } catch (err) {
            storyOutput.innerHTML = `<p style="color:var(--color-red);">Transmutation failed: ${escapeHtml(err.message)}</p>`;
        }
    });
}

function escapeHtml(str) {
    if (!str) return "";
    return str
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}
