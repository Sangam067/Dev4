"""
NecroShell CLI Entry Point
A Haunted Terminal & Open-Source AI Engine for the 'Ghost in the Machine' Hackathon.
Powered by Open-Weight LLMs (Llama 3 / Qwen) via Groq High-Speed LPU Inference.
"""

import sys
import os
import subprocess

# Force UTF-8 stream encoding across Windows and Unix platforms
if sys.platform == "win32":
    try:
        if sys.stdout.encoding.lower() != "utf-8":
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        if sys.stderr.encoding.lower() != "utf-8":
            sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

import typer
from typing import Optional
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.syntax import Syntax

from config import THEME, get_active_model, CANDIDATE_MODELS
import groq_client

app = typer.Typer(
    name="necro-shell",
    help="NecroShell: A Haunted Terminal & Open-Source AI Engine powered by Groq LPU inference.",
    add_completion=False,
    rich_markup_mode="rich",
)

console = Console(force_terminal=True, legacy_windows=False)

BANNER = r"""[bold magenta]
  _   _                      ____  _          _ _ 
 | \ | | ___  ___ _ __ ___  / ___|| |__   ___| | |
 |  \| |/ _ \/ __| '__/ _ \ \___ \| '_ \ / _ \ | |
 | |\  |  __/ (__| | | (_) | ___) | | | |  __/ | |
 |_| \_|\___|\___|_|  \___/ |____/|_| |_|\___|_|_|
[/bold magenta]
[italic bright_cyan]     [+] Haunted Terminal Wrapper | Open-Weight AI Spirits | Groq LPU Accelerated [+][/italic bright_cyan]
"""

BUILTIN_SAMPLES = {
    "cobol": (
        "COBOL (1985) - The Y2K Midnight Interest Glitch",
        """       IDENTIFICATION DIVISION.
       PROGRAM-ID. Y2K-INTEREST-CALC.
       DATA DIVISION.
       WORKING-STORAGE SECTION.
       01 WS-TRANS-DATE PIC 9(6).
       01 WS-BALANCE    PIC 9(7)V99 VALUE 0015000.50.
       01 WS-RATE       PIC V999    VALUE .075.
       01 WS-GHOST-PTR  USAGE POINTER.
       PROCEDURE DIVISION.
       0001-CALC-SOUL.
           DISPLAY "COMMENCING COMPOUND INTEREST CYCLE...".
           IF WS-TRANS-DATE < 000101
               MULTIPLY WS-BALANCE BY WS-RATE GIVING WS-BALANCE
           ELSE
               DISPLAY "CRITICAL: CHRONO-REGISTER WRAPAROUND DETECTED"
               SET WS-GHOST-PTR TO NULL
               CALL "VOID_DEREF" USING WS-GHOST-PTR.
           STOP RUN."""
    ),
    "c": (
        "Ancient K&R C - The Unchecked Buffer & Dangling Spectre",
        """/* Inscribed in 1983 - Unholy socket handler */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

struct SessionDemon {
    char username[16];
    int is_root;
    void (*banish)(void);
};

void summon(char *input) {
    struct SessionDemon demon;
    demon.is_root = 0;
    /* Ancient sin: unbounded strcpy into stack-allocated flesh */
    strcpy(demon.username, input);
    if (demon.is_root != 0) {
        printf("[!] Possession complete: Root spirit unleashed.\\n");
    }
}"""
    ),
    "fortran": (
        "FORTRAN IV - The Trajectory That Missed the Horizon",
        """C     1971 APOLLO-ERA TRAJECTORY CORRECTION
      PROGRAM TRAJ_SPIRIT
      DOUBLE PRECISION VEL, ALT, GRAV, APOGEE
      DATA GRAV /9.80665D0/, APOGEE /0.0D0/
      READ(5, 100) VEL, ALT
  100 FORMAT(2F12.4)
  200 IF (ALT .LE. 0.0D0) GOTO 666
      APOGEE = (VEL * VEL) / (2.0D0 * GRAV)
      WRITE(6, 300) APOGEE
  300 FORMAT(' ASCENT ACHIEVED: ', F12.4)
      STOP
  666 WRITE(6, 667)
  667 FORMAT(' WARNING: IMPACT VECTOR COLLAPSED INTO ABYSS')
      STOP
      END"""
    ),
}


def print_banner():
    """Render the spectral ASCII banner."""
    console.print(BANNER)


@app.command(name="observe", help="Execute or simulate a shell command and summon spooky AI commentary.")
def observe(
    command: str = typer.Argument(..., help="The shell command to execute and haunt."),
    simulate: bool = typer.Option(False, "--simulate", "-s", help="Simulate execution without running real command."),
    model: Optional[str] = typer.Option(None, "--model", "-m", help="Override open-weight model name."),
):
    """
    Terminal Possession Mode:
    Executes the command, streams output, and generates a chilling 1-2 line whisper
    from the open-weight LLM observing the registers.
    """
    print_banner()
    console.print(f"[bold purple][*] Observing invocation:[/bold purple] [bright_yellow]{command}[/bright_yellow]\n")

    stdout = ""
    stderr = ""
    exit_code = 0

    if simulate:
        console.print("[dim italic]~ Simulation mode active: no real bytes disturbed ~[/dim italic]\n")
        stdout = f"[simulated output of `{command}`]"
    else:
        try:
            proc = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
            )
            stdout = proc.stdout
            stderr = proc.stderr
            exit_code = proc.returncode

            if stdout:
                console.print(stdout.rstrip())
            if stderr:
                console.print(f"[red]{stderr.rstrip()}[/red]")
        except Exception as e:
            exit_code = 1
            stderr = str(e)
            console.print(f"[red]Execution faulted: {e}[/red]")

    with console.status("[italic bright_green][!] NecroDaemon is meditating upon your registers...[/italic bright_green]", spinner="aesthetic"):
        whisper = groq_client.get_possession_whisper(
            command=command,
            exit_code=exit_code,
            stdout=stdout,
            stderr=stderr,
            model=model,
        )

    color_border = "green" if exit_code == 0 else "red"
    icon = "[OK]" if exit_code == 0 else "[ERR]"
    panel_title = f"[bold {color_border}]{icon} NecroDaemon Whisper (exit code: {exit_code})[/bold {color_border}]"

    console.print()
    console.print(
        Panel(
            f"[italic bright_cyan]{whisper}[/italic bright_cyan]",
            title=panel_title,
            subtitle="[dim purple]Open-Weight Intelligence via Groq LPU[/dim purple]",
            border_style=color_border,
            expand=False,
        )
    )


@app.command(name="seance", help="Digital Ofrenda: Summon ancient computing spirits to review legacy/modern code.")
def seance(
    file: Optional[str] = typer.Option(None, "--file", "-f", help="Path to code file to sacrifice."),
    sample: Optional[str] = typer.Option(None, "--sample", "-s", help="Sample artifact: 'cobol', 'c', or 'fortran'."),
    model: Optional[str] = typer.Option(None, "--model", "-m", help="Override open-weight model name."),
):
    """
    Legacy Code Séance Mode:
    Offers code at the digital ofrenda for ancient programming spirits (Ada, Turing, Hopper, Bell Labs)
    to perform eerie analysis and crypt-level optimizations.
    """
    print_banner()
    code_content = ""
    artifact_name = "Custom Offering"

    if file:
        if not os.path.exists(file):
            console.print(f"[bold red][X] The altar rejected your path: file '{file}' does not exist.[/bold red]")
            raise typer.Exit(code=1)
        with open(file, "r", encoding="utf-8", errors="ignore") as f:
            code_content = f.read()
        artifact_name = os.path.basename(file)
    elif sample:
        key = sample.lower().strip()
        if key in BUILTIN_SAMPLES:
            artifact_name, code_content = BUILTIN_SAMPLES[key]
        else:
            console.print(f"[bold yellow]Available samples: {', '.join(BUILTIN_SAMPLES.keys())}[/bold yellow]")
            raise typer.Exit(code=1)
    else:
        console.print("[bold bright_green][*] Welcome to the Digital Ofrenda [*][/bold bright_green]")
        console.print("[dim]Select an ancient offering or paste your own sacrificial runes:[/dim]\n")
        console.print("  [1] COBOL (1985) - Y2K Chrono-Wrap Glitch")
        console.print("  [2] Ancient K&R C - Dangling Pointer & Stack Smashing")
        console.print("  [3] FORTRAN IV (1971) - Trajectory Vector Collapse")
        console.print("  [4] Interactive Code Input\n")

        choice = typer.prompt("Choose your sacrifice (1-4)", default="1")
        if choice == "1":
            artifact_name, code_content = BUILTIN_SAMPLES["cobol"]
        elif choice == "2":
            artifact_name, code_content = BUILTIN_SAMPLES["c"]
        elif choice == "3":
            artifact_name, code_content = BUILTIN_SAMPLES["fortran"]
        else:
            console.print("\n[dim]Enter code below (end with blank line or single 'END'):[/dim]")
            lines = []
            while True:
                try:
                    line = input()
                    if line.strip() == "END":
                        break
                    lines.append(line)
                    if not line and len(lines) > 2 and not lines[-2]:
                        break
                except (EOFError, KeyboardInterrupt):
                    break
            code_content = "\n".join(lines)
            artifact_name = "Interactive Mortal Offering"

    if not code_content.strip():
        console.print("[red]The altar remains empty. No runes were provided.[/red]")
        raise typer.Exit(code=1)

    console.print(f"\n[bold magenta][+] Offering Altar Inscription:[/bold magenta] [bright_yellow]{artifact_name}[/bright_yellow]\n")
    preview = code_content[:600] + ("\n... [truncated for display]" if len(code_content) > 600 else "")
    console.print(Syntax(preview, "text", theme="monokai", line_numbers=True))

    console.print("\n[bold purple][*] Communing with the ancestral spirits of computing...[/bold purple]")
    with console.status("[italic bright_cyan]Burning digital incense at the ofrenda...[/italic bright_cyan]", spinner="moon"):
        analysis = groq_client.start_seance(
            code_snippet=code_content,
            context_note=f"Artifact: {artifact_name}",
            model=model,
        )

    console.print()
    console.print(
        Panel(
            Markdown(analysis),
            title="[bold green][+] Voice of the Ancestral Computing Spirits [+][/bold green]",
            subtitle="[dim]Digital Ofrenda - Open-Weight Consciousness[/dim]",
            border_style="purple",
            padding=(1, 2),
        )
    )


@app.command(name="story", help="Transmute system logs and daemon traces into a cyberpunk horror narrative.")
def story(
    file: Optional[str] = typer.Option(None, "--file", "-f", help="Path to log file to analyze."),
    model: Optional[str] = typer.Option(None, "--model", "-m", help="Override open-weight model name."),
):
    """
    Log Ghost Story Generator:
    Reads system logs, process spikes, or crash dumps and translates them
    into a chilling cosmic horror story of daemons inside the hardware.
    """
    print_banner()
    log_data = ""

    if file and os.path.exists(file):
        with open(file, "r", encoding="utf-8", errors="ignore") as f:
            log_data = f.read()
        source_desc = f"Log File: {file}"
    else:
        source_desc = "Live Memory / Daemon Telemetry Snapshot"
        log_data = f"""[SYSTEM CHRONICLES - SECTOR D-9]
TIMESTAMP: 2026-10-31T03:59:59.004Z
KERNEL: ring_buffer_overflow @ 0x7FFF00DEADC0
PID 666 (necro_daemon): CPU spike 99.4% in thread 0x4B (MEMORY_HUNGER)
DAEMON: child process 1337 terminated unexpectedly: signal SIGKILL (exit status 137)
SOCKET: 0.0.0.0:6666 listening ... UNKNOWN_PAYLOAD received from 127.0.0.1:void
SWAP_SPACE: 84% exhausted. Page faults rising exponentially (12,481 faults/sec)
AUDIT: User 'root' attempted authentication 404 times without password
SYSTEM STATUS: Silicon temperatures surging (94C). Unidentified interrupts in IRQ 13."""

    console.print(f"[bold magenta][*] Transmuting:[/bold magenta] [italic bright_yellow]{source_desc}[/italic bright_yellow]\n")
    console.print(Panel(log_data.strip(), title="[dim]Raw Log Input[/dim]", border_style="dim"))

    with console.status("[italic bright_red][!] Chronicling the ghosts within the machine...[/italic bright_red]", spinner="bouncingBar"):
        tale = groq_client.generate_log_tale(log_text=log_data, model=model)

    console.print()
    console.print(
        Panel(
            f"[italic white]{tale}[/italic white]",
            title="[bold red][+] The Chronicle of the Machine Ghost [+][/bold red]",
            subtitle="[dim purple]Decoded from Silicon by Open-Weight AI[/dim purple]",
            border_style="red",
            padding=(1, 2),
        )
    )


# Alias command 'logs' to 'story' as requested in hackathon specification
@app.command(name="logs", help="Alias for 'story': Generate a horror story from system logs.")
def logs(
    file: Optional[str] = typer.Option(None, "--file", "-f", help="Path to log file to analyze."),
    model: Optional[str] = typer.Option(None, "--model", "-m", help="Override open-weight model name."),
):
    """Alias for 'story' command."""
    story(file=file, model=model)


@app.command(name="web", help="Launch NecroShell localhost web interface (FastAPI + Cyberpunk UI).")
def web(
    host: str = typer.Option("127.0.0.1", "--host", "-h", help="Host address to bind to."),
    port: int = typer.Option(8000, "--port", "-p", help="Port to listen on."),
):
    """
    Launch NecroShell on Localhost:
    Starts the high-speed FastAPI web dashboard on http://localhost:8000
    with interactive Terminal Possession, Digital Ofrenda Séance, and Log Horror generator.
    """
    print_banner()
    console.print(f"[bold bright_green][+] Igniting NecroShell Localhost Portal on http://{host}:{port}[/bold bright_green]")
    import web as web_module
    web_module.start_server(host=host, port=port)


@app.command(name="shell", help="Enter the Possessed Terminal Wrapper REPL (Continuous Haunted Shell).")
def possessed_shell(
    model: Optional[str] = typer.Option(None, "--model", "-m", help="Override open-weight model name."),
):
    """
    Continuous Haunted Interactive Shell:
    Every command you run is passed directly to your system shell, and the
    NecroDaemon immediately speaks from the void after each invocation.
    Type 'exit' or 'quit' to banish the spirit.
    """
    print_banner()
    console.print("[bold purple][*] You have stepped across the silicon threshold.[/bold purple]")
    console.print("[dim bright_cyan]Every shell command executed here will be judged by the open-weight daemon.[/dim bright_cyan]")
    console.print("[dim]Type 'exit' or 'quit' to close the portal.\n[/dim]")

    while True:
        try:
            cwd = os.getcwd()
            folder = os.path.basename(cwd) or cwd
            prompt_str = f"[bold magenta]necro[/bold magenta]:[bold bright_green]{folder}[/bold bright_green] [bold red]>[/bold red] "
            cmd = console.input(prompt_str).strip()

            if not cmd:
                continue

            if cmd.lower() in ["exit", "quit", "banish"]:
                console.print("\n[italic bright_cyan][*] The spirit recedes into the cooling heatsinks. Portal closed.[/italic bright_cyan]")
                break

            if cmd.startswith("cd "):
                target_dir = cmd[3:].strip().strip('"').strip("'")
                try:
                    os.chdir(target_dir)
                    whisper = groq_client.get_possession_whisper(
                        command=cmd,
                        exit_code=0,
                        stdout=f"Changed directory to {os.getcwd()}",
                        model=model,
                    )
                    console.print(f"[dim italic bright_cyan]   ↳ [OK] {whisper}[/dim italic bright_cyan]\n")
                except Exception as e:
                    console.print(f"[red]cd: {e}[/red]")
                continue

            proc = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if proc.stdout:
                console.print(proc.stdout.rstrip())
            if proc.stderr:
                console.print(f"[red]{proc.stderr.rstrip()}[/red]")

            whisper = groq_client.get_possession_whisper(
                command=cmd,
                exit_code=proc.returncode,
                stdout=proc.stdout,
                stderr=proc.stderr,
                model=model,
            )
            color = "bright_cyan" if proc.returncode == 0 else "red"
            icon = "[OK]" if proc.returncode == 0 else "[ERR]"
            console.print(f"[{color}]   ↳ {icon} {whisper}[/{color}]\n")

        except (KeyboardInterrupt, EOFError):
            console.print("\n[italic bright_cyan][*] Abrupt severance... the portal collapses.[/italic bright_cyan]")
            break


@app.command(name="status", help="Display NecroShell engine health, Groq LPU connection, and Open-Source AI status.")
def status():
    """
    Engine diagnostic and Hackathon Open Innovation manifesto.
    """
    print_banner()
    with console.status("[italic bright_green]Probing silicon consciousness...[/italic bright_green]", spinner="dots"):
        diag = groq_client.verify_connection()

    status_color = "bright_green" if diag.get("status") == "online" else "bright_red"
    console.print(
        Panel(
            f"""[bold]System Status:[/bold] [{status_color}]{diag.get('status', 'unknown').upper()}[/{status_color}]
[bold]Active Model:[/bold] [bright_yellow]{diag.get('active_model', get_active_model())}[/bright_yellow]
[bold]Inference Engine:[/bold] [bright_cyan]{diag.get('engine', 'Groq LPU Architecture')}[/bright_cyan]
[bold]Open Innovation:[/bold] [bold bright_green]100% Open-Weight LLMs (Llama 3 / Qwen)[/bold bright_green]
[bold]Spirit Pulse:[/bold] [italic white]"{diag.get('response', 'SILENT')}"[/italic white]

[dim purple]═════════════════════════════════════════════════════════════════[/dim purple]
[bold magenta]HACKATHON MANIFESTO: The Ghost in the Machine[/bold magenta]
NecroShell proves that open-weight intelligence does not belong locked inside
walled gardens. Powered by open-weights hosted on ultra-low-latency Groq LPUs,
the terminal becomes a living, atmospheric companion for developers—breathing
life into legacy code and turning mundane debugging into cybernetic folklore.""",
            title="[bold magenta][+] NecroShell Engine & Manifesto [+][/bold magenta]",
            border_style="magenta",
            padding=(1, 2),
        )
    )


if __name__ == "__main__":
    app()
