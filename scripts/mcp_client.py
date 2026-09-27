#!/usr/bin/env python3
"""Small mcporter client shared by the Zoho Expense helper CLIs."""

from __future__ import annotations

import json
import subprocess


class McporterError(RuntimeError):
    """Raised when mcporter cannot return a usable tool result."""


def _redact(text, secret):
    return str(text or "").replace(secret, "<MCP_URL>").strip()


def _unwrap_content(payload):
    """Unwrap raw MCP content when mcporter returns the complete envelope."""
    if not isinstance(payload, dict):
        return payload
    result = payload.get("result")
    if not isinstance(result, dict):
        return payload
    content = result.get("content")
    if not isinstance(content, list) or not content:
        return payload
    first = content[0]
    if not isinstance(first, dict) or "text" not in first:
        return payload
    text = first["text"]
    if not isinstance(text, str):
        return text
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {"text": text}


def call_tool(mcp_url, tool, arguments, timeout=30):
    """Call one MCP tool without invoking a shell or printing the endpoint."""
    command = [
        "mcporter",
        "call",
        f"{mcp_url}.{tool}",
        "--args",
        json.dumps(arguments, ensure_ascii=False),
    ]
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except FileNotFoundError as exc:
        raise McporterError("mcporter executable not found") from exc
    except subprocess.TimeoutExpired as exc:
        raise McporterError("mcporter call timed out") from exc

    if result.returncode != 0:
        detail = _redact(result.stderr or result.stdout, mcp_url)
        raise McporterError(detail or "mcporter call failed")

    try:
        payload = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        detail = _redact(result.stderr, mcp_url)
        raise McporterError(detail or "mcporter returned invalid JSON") from exc

    payload = _unwrap_content(payload)
    if isinstance(payload, dict) and payload.get("status") in {"error", "failure"}:
        detail = payload.get("error") or payload.get("message") or payload.get("data")
        raise McporterError(_redact(detail, mcp_url) or "Zoho Expense request failed")
    if isinstance(payload, dict) and payload.get("error"):
        raise McporterError(_redact(payload["error"], mcp_url))
    return payload
