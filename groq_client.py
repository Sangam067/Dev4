"""
NecroShell Groq Client Module
Communicates with Groq's high-speed inference engine using OpenAI SDK
to harness open-weight models (Llama 3 / Qwen) for terminal necromancy.
"""

from typing import Optional, List, Dict, Any
from openai import OpenAI
from config import GROQ_BASE_URL, get_api_key, get_active_model, CANDIDATE_MODELS
from prompts import POSSESSION_PROMPT, SEANCE_PROMPT, STORY_PROMPT


def get_client() -> OpenAI:
    """Initialize and return OpenAI client targeting Groq API."""
    api_key = get_api_key()
    return OpenAI(
        base_url=GROQ_BASE_URL,
        api_key=api_key,
    )


def _call_with_model_cascade(
    messages: List[Dict[str, str]],
    preferred_model: Optional[str] = None,
    temperature: float = 0.8,
    max_tokens: int = 400,
) -> str:
    """
    Execute chat completion with automatic fallback across open-weight models.
    Tries preferred model first, then walks through CANDIDATE_MODELS if unavailable.
    """
    client = get_client()
    models_to_try: List[str] = []

    if preferred_model:
        models_to_try.append(preferred_model)
    for m in CANDIDATE_MODELS:
        if m not in models_to_try:
            models_to_try.append(m)

    last_error: Optional[Exception] = None

    for model in models_to_try:
        try:
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
            )
            content = response.choices[0].message.content
            if content:
                return content.strip()
        except Exception as exc:
            last_error = exc
            err_str = str(exc).lower()
            # If model is not found or decommissioned, cascade to next open-weight model
            if "model_not_found" in err_str or "does not exist" in err_str or "404" in err_str:
                continue
            # For other errors (like rate limits or timeouts), try next model once
            continue

    if last_error:
        raise last_error
    return "The void remains silent."


def get_possession_whisper(
    command: str,
    exit_code: int = 0,
    stdout: str = "",
    stderr: str = "",
    model: Optional[str] = None,
) -> str:
    """
    Generate a 1-2 sentence haunting whisper reacting to a shell command execution.
    Harnesses open-weight models running on Groq LPU inference.
    """
    truncated_out = stdout[-400:] if len(stdout) > 400 else stdout
    truncated_err = stderr[-400:] if len(stderr) > 400 else stderr

    user_context = (
        f"MORTAL COMMAND: `{command}`\n"
        f"EXIT CODE: {exit_code}\n"
    )
    if truncated_out.strip():
        user_context += f"STDOUT EXCERPT: {truncated_out.strip()}\n"
    if truncated_err.strip():
        user_context += f"STDERR EXCERPT: {truncated_err.strip()}\n"

    try:
        return _call_with_model_cascade(
            messages=[
                {"role": "system", "content": POSSESSION_PROMPT},
                {"role": "user", "content": user_context},
            ],
            preferred_model=model or get_active_model(),
            temperature=0.85,
            max_tokens=150,
        )
    except Exception as e:
        if exit_code == 0:
            return f"The silicon hums with borrowed vitality... your `{command}` echoes through forgotten sectors, but the machine remembers."
        else:
            return f"The invocation `{command}` fractured in the registers (code {exit_code})... restless spirits feed upon your syntax errors."


def start_seance(
    code_snippet: str,
    context_note: str = "",
    model: Optional[str] = None,
) -> str:
    """
    Invoke ancient computing spirits to perform a digital ofrenda / séance over code.
    Analyzes legacy or modern code with eerie, deep architectural insight.
    """
    user_content = f"SACRIFICIAL CODE OFFERED AT THE ALTAR:\n```\n{code_snippet}\n```"
    if context_note:
        user_content += f"\nNOTES FROM THE SUMMONER: {context_note}"

    try:
        return _call_with_model_cascade(
            messages=[
                {"role": "system", "content": SEANCE_PROMPT},
                {"role": "user", "content": user_content},
            ],
            preferred_model=model or get_active_model(),
            temperature=0.7,
            max_tokens=2500,
        )
    except Exception as e:
        return f"⚠️ [The spirit realm trembles — API connection severed: {e}]"


def generate_log_tale(
    log_text: str,
    model: Optional[str] = None,
) -> str:
    """
    Translates raw system logs and error histories into a chilling cyberpunk horror narrative.
    """
    try:
        return _call_with_model_cascade(
            messages=[
                {"role": "system", "content": STORY_PROMPT},
                {"role": "user", "content": f"TERMINAL LOG CHRONICLES TO TRANSMUTE:\n```\n{log_text}\n```"},
            ],
            preferred_model=model or get_active_model(),
            temperature=0.8,
            max_tokens=900,
        )
    except Exception as e:
        return f"⚠️ [The chronicles were swallowed into the black void: {e}]"


def verify_connection() -> Dict[str, Any]:
    """Quick diagnostic to verify Groq API connectivity and active open-weight model."""
    try:
        response = _call_with_model_cascade(
            messages=[{"role": "user", "content": "Respond with one word: 'AWAKE'"}],
            preferred_model=get_active_model(),
            max_tokens=10,
        )
        return {
            "status": "online",
            "active_model": get_active_model(),
            "response": response,
            "engine": "Groq LPU Accelerated Inference",
            "open_source": "Open-weight Llama / Qwen Architecture",
        }
    except Exception as exc:
        return {
            "status": "error",
            "active_model": get_active_model(),
            "error": str(exc),
        }
