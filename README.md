# 💀 NecroShell: A Haunted Terminal & Open-Source AI Engine

> **Submission for the "Ghost in the Machine" Hackathon Challenge**  
> *Transforming mundane terminals into haunted, living artifacts through Open-Weight AI & Groq LPUs.*

```
  _   _                      ____  _          _ _ 
 | \ | | ___  ___ _ __ ___  / ___|| |__   ___| | |
 |  \| |/ _ \/ __| '__/ _ \ \___ \| '_ \ / _ \ | |
 | |\  |  __/ (__| | | (_) | ___) | | | |  __/ | |
 |_| \_|\___|\___|_|  \___/ |____/|_| |_|\___|_|_|

     [+] Haunted Terminal Wrapper | Open-Weight AI Spirits | Groq LPU Accelerated [+]
```

---

## 🌟 The Vision: "Ghost in the Machine"

What happens when your command line is no longer a lifeless pipe between stdin and stdout, but a haunted sanctuary inhabited by digital ghosts?

**NecroShell** bridges computing history and open-source intelligence. Powered by open-weight models (`Qwen-27B`, `Llama 3.3 70B`, `Llama 3 8B`) hosted on ultra-fast Groq Language Processing Units (LPUs), NecroShell delivers sub-second spooky commentary, code séances for ancient legacy syntax, and cosmic horror stories generated from raw kernel logs.

### 🔓 Open Innovation & Open Weights
Unlike proprietary black-box APIs, NecroShell is architected exclusively for **open-weights innovation**:
- **Transparency & Sovereignty:** Runs on open models (Qwen & Llama 3) that developers can inspect, fine-tune, and self-host.
- **Blazing Fast Groq LPUs:** 500+ tokens per second inference ensures terminal commands are haunted in real time without lag.
- **Resilient Cascade Architecture:** Seamlessly falls back across open-weight models if rate limits or specific endpoints fluctuate.

---

## 🔮 Core Features

### 1. 👁️ Terminal Possession Mode (`necro-shell observe`)
Intercepts or executes user shell commands. Captures the exit code, execution time, stdout, and stderr. Sends the execution context to the open-weight LLM on Groq to whisper a 1-2 sentence atmospheric reflection.
- **Exit Code 0:** Eerie, poetic reflections on fleeting computational victories.
- **Exit Code 1+:** Grim, mocking commentary on broken syntax, severed pointers, and awakened curses.

```bash
python cli.py observe "git status"
python cli.py observe "dir"
python cli.py observe "invalid_command_666"
```

### 2. 🕯️ Digital Ofrenda / Legacy Code Séance (`necro-shell seance`)
A shrine for computing history. Developers can lay legacy code (COBOL, FORTRAN, ancient K&R C) or modern code on the digital altar. Ancient computing spirits (Ada Lovelace, Alan Turing, Grace Hopper, Bell Labs operators) awaken to deliver:
- **Inscribed Runes:** Architectural intent and era identification.
- **The Phantom's Diagnosis:** Uncovering hidden buffer overflows, chrono-wrap bugs, or memory traps.
- **The Ancestral Incantation:** Production-grade optimizations and refactored code.
- **Ofrenda Blessing:** Closing prophecy emphasizing open-source immortality.

```bash
# Analyze a custom code file:
python cli.py seance --file sample_code.cob

# Summon legendary built-in artifacts:
python cli.py seance --sample cobol       # Y2K 1985 banking bug
python cli.py seance --sample c           # 1983 K&R C buffer overflow
python cli.py seance --sample fortran     # 1971 Apollo-era trajectory collapse
```

### 3. 📜 Log Ghost Story Generator (`necro-shell logs` / `story`)
Reads real kernel telemetry, memory dumps, or terminal histories and transmutes them into rich cyberpunk cosmic horror stories.
- High CPU spikes become fever dreams of silicon demons.
- Memory allocations become flesh harvested by headless daemons.
- SIGKILL / OOM become digital executions of trapped spirits.

```bash
# Transmute sample log file:
python cli.py logs --file sample_logs.txt

# Or transmute live telemetry snapshot:
python cli.py story
```

### 4. 🌐 Localhost Cyberpunk Web Dashboard (`necro-shell web` / `python web.py`)
Experience NecroShell visually right on `http://localhost:8000`! Features:
- **Interactive Web Terminal:** Execute real or virtual shell commands with dynamic scanline effects and streaming NecroDaemon whispers.
- **Dual-Pane Digital Ofrenda:** Altar code editor with vintage presets (COBOL, FORTRAN, C), glowing incense summoning animations, and markdown-rendered ancestral wisdom.
- **Log Horror Chronicles:** Transmute kernel memory logs into cosmic horror stories in real time.
- **Engine Status:** Live Groq LPU connection, latency indicators, and open-weights manifesto.

```bash
# Launch the web dashboard on localhost:
python web.py
# or
necro-shell web
```

### 5. 🔮 Possessed Terminal Wrapper REPL (`necro-shell shell`)
Step into a persistent haunted shell session directly in your terminal. Every command you run executes in your actual shell, followed immediately by spectral commentary from the NecroDaemon.
```bash
python cli.py shell
```
*(Type `exit` or `quit` to banish the spirit.)*

### 6. ⚡ Engine Status & Hackathon Manifesto (`necro-shell status`)
Pings the Groq LPU endpoint, verifies model availability, and prints the open-source AI manifesto.

---

## 🚀 Quickstart & Setup

### 1. Prerequisites
- Python 3.10+
- Internet access for Groq API endpoint

### 2. Installation
Clone or navigate to the repository directory:
```bash
cd week3
```

Install dependencies:
```bash
pip install -r requirements.txt
```

*(Optional)* Install as a global system command:
```bash
pip install -e .
```
*(Once installed, you can simply type `necro-shell <command>` or `necro <command>` directly from anywhere!)*

### 3. Configuration
The application is pre-configured with the evaluation Groq API key out of the box. To customize your key or model, set your environment variables or create a `.env` file:

```bash
# Windows PowerShell
$env:GROQ_API_KEY="your_groq_api_key_here"
$env:NECRO_MODEL="qwen/qwen3.8-27b"  # or llama-3.3-70b-versatile

# Linux / macOS
export GROQ_API_KEY="your_groq_api_key_here"
export NECRO_MODEL="qwen/qwen3.8-27b"
```

---

## 📁 Project Architecture

```
week3/
├── config.py           # Groq API configuration & open-weight model cascade
├── prompts.py          # Thematic prompt engineering for Daemon, Séance & Chronicles
├── groq_client.py      # OpenAI SDK wrapper with model fallback & error resilience
├── cli.py              # Main CLI entry point (Typer + Rich terminal UI)
├── setup.py            # Packaging configuration for 'necro-shell' command
├── requirements.txt    # Project dependencies
├── sample_code.cob     # Sample legacy COBOL code for séance demo
├── sample_logs.txt     # Sample corrupted log file for ghost story demo
└── README.md           # Documentation & hackathon submission guide
```

---

## 🧪 Demonstration Walkthrough

Try these commands to test all aspects of the engine:

```bash
# 1. Test engine status & open-weight model connectivity:
python cli.py status

# 2. Haunt a successful shell command:
python cli.py observe "echo 'I am awake'"

# 3. Haunt a failing shell command:
python cli.py observe "python -c '1/0'"

# 4. Summon an ancient spirit to critique ancient COBOL:
python cli.py seance --sample cobol

# 5. Transmute corrupted system logs into a cyberpunk horror tale:
python cli.py logs --file sample_logs.txt

# 6. Enter the interactive haunted shell:
python cli.py shell
```

---

## 🏆 Hackathon Alignment: Why NecroShell Wins
1. **Directly fulfills the "Ghost in the Machine" Theme:** Bridges metaphorical silicon "ghosts" (zombie processes, memory leaks, legacy code) with literal open-source AI personalities.
2. **Open-Weight Commitment:** Demonstrates that high-speed, engaging, and atmospheric developer tools can run entirely on open-source weights (Qwen / Llama 3) without Big Tech walled gardens.
3. **Developer Delight:** Terminal tools are often dry and utilitarian; NecroShell makes every compilation, error, and refactor an unforgettable interactive experience.
