#!/usr/bin/env python3
"""Entrypoint for nanobot gateway in Docker.

Resolves environment variables into config.json at runtime,
then execs nanobot gateway with the resolved config.
"""

import json
import os
import sys
from pathlib import Path


def resolve_config() -> str:
    """Read config.json, inject env vars, write resolved config, return path."""
    config_dir = Path(__file__).parent
    config_path = config_dir / "config.json"
    resolved_path = config_dir / "config.resolved.json"
    workspace_dir = config_dir / "workspace"

    # Load base config
    with open(config_path) as f:
        config = json.load(f)

    # Resolve provider API key and base URL from env vars
    if "providers" in config and "custom" in config["providers"]:
        if api_key := os.environ.get("LLM_API_KEY", ""):
            config["providers"]["custom"]["apiKey"] = api_key
        if api_base := os.environ.get("LLM_API_BASE_URL", ""):
            config["providers"]["custom"]["apiBase"] = api_base
        if model := os.environ.get("LLM_API_MODEL", ""):
            config["agents"]["defaults"]["model"] = model

    # Resolve gateway host/port from env vars
    if "gateway" not in config:
        config["gateway"] = {}
    if host := os.environ.get("NANOBOT_GATEWAY_CONTAINER_ADDRESS", ""):
        config["gateway"]["host"] = host
    if port := os.environ.get("NANOBOT_GATEWAY_CONTAINER_PORT", ""):
        config["gateway"]["port"] = int(port)

    # Resolve webchat host/port from env vars (channel config)
    if "channels" not in config:
        config["channels"] = {}
    if "webchat" not in config["channels"]:
        config["channels"]["webchat"] = {"enabled": True, "allow_from": ["*"]}
    if host := os.environ.get("NANOBOT_WEBCHAT_CONTAINER_ADDRESS", ""):
        config["channels"]["webchat"]["host"] = host
    if port := os.environ.get("NANOBOT_WEBCHAT_CONTAINER_PORT", ""):
        config["channels"]["webchat"]["port"] = int(port)
    # Note: NANOBOT_ACCESS_KEY is read by the webchat channel from env directly

    # Resolve MCP server env vars (for lms MCP server)
    if "tools" in config and "mcpServers" in config["tools"]:
        if "lms" in config["tools"]["mcpServers"]:
            lms_server = config["tools"]["mcpServers"]["lms"]
            if backend_url := os.environ.get("NANOBOT_LMS_BACKEND_URL", ""):
                lms_server["env"]["NANOBOT_LMS_BACKEND_URL"] = backend_url
            if api_key := os.environ.get("NANOBOT_LMS_API_KEY", ""):
                lms_server["env"]["NANOBOT_LMS_API_KEY"] = api_key

    # Write resolved config
    with open(resolved_path, "w") as f:
        json.dump(config, f, indent=2)

    return str(resolved_path)


def main() -> None:
    """Resolve config and exec nanobot gateway."""
    resolved_config = resolve_config()
    workspace = str(Path(__file__).parent / "workspace")

    # Exec nanobot gateway with resolved config
    os.execvp(
        "nanobot",
        [
            "nanobot",
            "gateway",
            "--config",
            resolved_config,
            "--workspace",
            workspace,
        ],
    )


if __name__ == "__main__":
    main()
