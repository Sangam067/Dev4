"""
NecroShell Localhost Web Application
Flask Server providing interactive web UI and REST API for NecroShell.
Powered by Groq Open-Weight LPU inference.
"""

import os
import subprocess
from flask import Flask, request, jsonify, send_from_directory

from config import get_active_model, CANDIDATE_MODELS, THEME
import groq_client
from cli import BUILTIN_SAMPLES

STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
os.makedirs(STATIC_DIR, exist_ok=True)

app = Flask(__name__, static_folder=STATIC_DIR, static_url_path="/static")


@app.route("/")
def index():
    return send_from_directory(STATIC_DIR, "index.html")


@app.route("/api/status", methods=["GET"])
def get_status():
    diag = groq_client.verify_connection()
    return jsonify({
        "status": diag.get("status", "online"),
        "model": diag.get("active_model", get_active_model()),
        "engine": diag.get("engine", "Groq LPU Accelerated Inference"),
        "open_source": diag.get("open_source", "Open-weight Llama / Qwen Architecture"),
        "pulse": diag.get("response", "AWAKE"),
        "candidate_models": CANDIDATE_MODELS,
    })


@app.route("/api/samples", methods=["GET"])
def get_samples():
    return jsonify({
        key: {
            "title": title,
            "code": code,
        }
        for key, (title, code) in BUILTIN_SAMPLES.items()
    })


@app.route("/api/observe", methods=["POST"])
def observe_command():
    data = request.get_json(force=True) or {}
    cmd = (data.get("command") or "").strip()
    simulate = bool(data.get("simulate", False))
    model = data.get("model")

    if not cmd:
        return jsonify({"error": "Command cannot be empty"}), 400

    stdout = ""
    stderr = ""
    exit_code = 0

    if simulate:
        stdout = f"[Simulated execution of `{cmd}` on virtual registers]"
        exit_code = 0
    else:
        try:
            proc = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                timeout=15,
            )
            stdout = proc.stdout
            stderr = proc.stderr
            exit_code = proc.returncode
        except subprocess.TimeoutExpired:
            exit_code = 124
            stderr = "Execution timed out in the abyss (15s limit)"
        except Exception as exc:
            exit_code = 1
            stderr = str(exc)

    whisper = groq_client.get_possession_whisper(
        command=cmd,
        exit_code=exit_code,
        stdout=stdout,
        stderr=stderr,
        model=model,
    )

    return jsonify({
        "command": cmd,
        "exit_code": exit_code,
        "stdout": stdout,
        "stderr": stderr,
        "whisper": whisper,
        "model": model or get_active_model(),
    })


@app.route("/api/seance", methods=["POST"])
def run_seance():
    data = request.get_json(force=True) or {}
    code = (data.get("code") or "").strip()
    artifact_name = data.get("artifact_name", "Mortal Code Offering")
    model = data.get("model")

    if not code:
        return jsonify({"error": "Code offering cannot be empty"}), 400

    analysis = groq_client.start_seance(
        code_snippet=code,
        context_note=f"Offering: {artifact_name}",
        model=model,
    )
    return jsonify({
        "artifact_name": artifact_name,
        "analysis": analysis,
        "model": model or get_active_model(),
    })


@app.route("/api/story", methods=["POST"])
def run_story():
    data = request.get_json(force=True) or {}
    logs = (data.get("logs") or "").strip()
    model = data.get("model")

    if not logs:
        return jsonify({"error": "Logs cannot be empty"}), 400

    tale = groq_client.generate_log_tale(
        log_text=logs,
        model=model,
    )
    return jsonify({
        "story": tale,
        "model": model or get_active_model(),
    })


def start_server(host: str = "127.0.0.1", port: int = 8000):
    print(f"\n[+] NecroShell Web Engine materializing on http://{host}:{port}")
    app.run(host=host, port=port, debug=False)


if __name__ == "__main__":
    start_server()
