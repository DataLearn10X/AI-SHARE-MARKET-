"""LLM service (provider-agnostic, optional)."""

from __future__ import annotations

import json
import logging
import os
from typing import Optional

import requests

logger = logging.getLogger(__name__)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")


def _post_json(url, headers, payload, timeout=30):
    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=timeout)
        resp.raise_for_status()
        return resp.json()
    except Exception as exc:
        logger.warning("LLM request failed: %s", exc)
        return None


def generate_text(prompt: str, system: Optional[str] = None) -> Optional[str]:
    """Try OpenAI, then Groq, then Ollama. Return text or None."""
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    # OpenAI
    if OPENAI_API_KEY:
        data = _post_json(
            "https://api.openai.com/v1/chat/completions",
            {"Authorization": f"Bearer {OPENAI_API_KEY}", "Content-Type": "application/json"},
            {"model": "gpt-4o-mini", "messages": messages, "temperature": 0.2},
        )
        if data and "choices" in data:
            return data["choices"][0]["message"]["content"]

    # Groq
    if GROQ_API_KEY:
        data = _post_json(
            "https://api.groq.com/openai/v1/chat/completions",
            {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"},
            {"model": "llama-3.1-8b-instant", "messages": messages, "temperature": 0.2},
        )
        if data and "choices" in data:
            return data["choices"][0]["message"]["content"]

    # Ollama
    try:
        data = _post_json(
            f"{OLLAMA_BASE_URL}/api/chat",
            {"Content-Type": "application/json"},
            {"model": "llama3", "messages": messages, "stream": False},
        )
        if data and "message" in data:
            return data["message"].get("content")
    except Exception:
        pass

    return None
