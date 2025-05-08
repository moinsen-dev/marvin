"""Konfiguration für Marvin."""

import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import yaml
from pydantic import BaseModel, Field


class AgentConfig(BaseModel):
    """Konfiguration für einen Agenten."""
    
    name: str
    enabled: bool = True
    model: str = "gemini-pro"  # Standard-Modell für Google ADK
    temperature: float = 0.2
    max_tokens: int = 1024
    top_p: float = 0.95
    extra_params: Dict[str, Any] = Field(default_factory=dict)


class APIConfig(BaseModel):
    """Konfiguration für die API."""
    
    host: str = "127.0.0.1"
    port: int = 8000
    ssl_cert: Optional[str] = None
    ssl_key: Optional[str] = None
    debug: bool = False
    cors_origins: List[str] = Field(default_factory=lambda: ["*"])
    token_expiration: int = 3600  # in Sekunden


class MCPConfig(BaseModel):
    """Konfiguration für den MCP-Server."""
    
    host: str = "127.0.0.1"
    port: int = 9000
    ssl_cert: Optional[str] = None
    ssl_key: Optional[str] = None
    max_clients: int = 100
    heartbeat_interval: int = 30  # in Sekunden


class Context7Config(BaseModel):
    """Konfiguration für Context 7."""
    
    api_key: Optional[str] = None
    endpoint: str = "https://api.context7.com/v1"
    timeout: int = 60  # in Sekunden
    max_tokens: int = 8192


class PathConfig(BaseModel):
    """Konfiguration für Pfade."""
    
    templates_dir: str = "./templates"
    output_dir: str = "./output"
    cache_dir: str = "./cache"
    logs_dir: str = "./logs"


class MarvinConfig(BaseModel):
    """Hauptkonfiguration für Marvin."""
    
    agents: Dict[str, AgentConfig] = Field(default_factory=dict)
    api: APIConfig = Field(default_factory=APIConfig)
    mcp: MCPConfig = Field(default_factory=MCPConfig)
    context7: Context7Config = Field(default_factory=Context7Config)
    paths: PathConfig = Field(default_factory=PathConfig)
    log_level: str = "INFO"
    environment: str = "development"


def load_config(config_path: Optional[Union[str, Path]] = None) -> MarvinConfig:
    """Lädt die Konfiguration aus einer YAML-Datei.
    
    Args:
        config_path: Pfad zur Konfigurationsdatei. Wenn None, werden Standardwerte verwendet.
        
    Returns:
        Die geladene Konfiguration
        
    Raises:
        FileNotFoundError: Wenn die angegebene Konfigurationsdatei nicht gefunden wurde
        yaml.YAMLError: Wenn die YAML-Datei ungültig ist
    """
    config = {}
    
    if config_path:
        config_path = Path(config_path)
        if not config_path.exists():
            raise FileNotFoundError(f"Konfigurationsdatei nicht gefunden: {config_path}")
        
        with open(config_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
    
    # Standard-Agent-Konfigurationen
    if "agents" not in config:
        config["agents"] = {
            "document_analysis": {
                "name": "document_analysis",
                "enabled": True,
                "model": "gemini-pro",
                "temperature": 0.2,
            },
            "codebase_analysis": {
                "name": "codebase_analysis",
                "enabled": True,
                "model": "gemini-pro",
                "temperature": 0.1,
            },
            "template_generation": {
                "name": "template_generation",
                "enabled": True,
                "model": "gemini-pro",
                "temperature": 0.3,
            },
            "sequence_planner": {
                "name": "sequence_planner",
                "enabled": True,
                "model": "gemini-pro",
                "temperature": 0.1,
            },
        }
    
    # Umgebungsvariablen überschreiben Konfiguration
    if os.environ.get("MARVIN_API_HOST"):
        if "api" not in config:
            config["api"] = {}
        config["api"]["host"] = os.environ["MARVIN_API_HOST"]
    
    if os.environ.get("MARVIN_API_PORT"):
        if "api" not in config:
            config["api"] = {}
        config["api"]["port"] = int(os.environ["MARVIN_API_PORT"])
    
    if os.environ.get("MARVIN_MCP_HOST"):
        if "mcp" not in config:
            config["mcp"] = {}
        config["mcp"]["host"] = os.environ["MARVIN_MCP_HOST"]
    
    if os.environ.get("MARVIN_MCP_PORT"):
        if "mcp" not in config:
            config["mcp"] = {}
        config["mcp"]["port"] = int(os.environ["MARVIN_MCP_PORT"])
    
    if os.environ.get("MARVIN_CONTEXT7_API_KEY"):
        if "context7" not in config:
            config["context7"] = {}
        config["context7"]["api_key"] = os.environ["MARVIN_CONTEXT7_API_KEY"]
    
    if os.environ.get("MARVIN_LOG_LEVEL"):
        config["log_level"] = os.environ["MARVIN_LOG_LEVEL"]
    
    if os.environ.get("MARVIN_ENVIRONMENT"):
        config["environment"] = os.environ["MARVIN_ENVIRONMENT"]
    
    # Config-Objekt erstellen
    return MarvinConfig(**config)


# Globale Konfiguration
config = load_config()
