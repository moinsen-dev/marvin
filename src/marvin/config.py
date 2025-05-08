"""Configuration for Marvin."""

import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import yaml
from pydantic import BaseModel, Field

from marvin.logging import get_logger, setup_logging

logger = get_logger("config")


class AgentConfig(BaseModel):
    """Configuration for an agent."""

    name: str
    enabled: bool = True
    model: str = "gemini-pro"  # Default model for Google ADK
    temperature: float = 0.2
    max_tokens: int = 1024
    top_p: float = 0.95
    extra_params: Dict[str, Any] = Field(default_factory=dict)


class APIConfig(BaseModel):
    """Configuration for the API."""

    host: str = "127.0.0.1"
    port: int = 8000
    ssl_cert: Optional[str] = None
    ssl_key: Optional[str] = None
    debug: bool = False
    cors_origins: List[str] = Field(default_factory=lambda: ["*"])
    token_expiration: int = 3600  # in seconds


class MCPConfig(BaseModel):
    """Configuration for the MCP server."""

    host: str = "127.0.0.1"
    port: int = 9000
    ssl_cert: Optional[str] = None
    ssl_key: Optional[str] = None
    max_clients: int = 100
    heartbeat_interval: int = 30  # in seconds


class Context7Config(BaseModel):
    """Configuration for Context 7."""

    api_key: Optional[str] = None
    endpoint: str = "https://api.context7.com/v1"
    timeout: int = 60  # in seconds
    max_tokens: int = 8192


class PathConfig(BaseModel):
    """Configuration for paths."""

    templates_dir: str = "./templates"
    output_dir: str = "./output"
    cache_dir: str = "./cache"
    logs_dir: str = "./logs"


class MarvinConfig(BaseModel):
    """Main configuration for Marvin."""

    agents: Dict[str, AgentConfig] = Field(default_factory=dict)
    api: APIConfig = Field(default_factory=APIConfig)
    mcp: MCPConfig = Field(default_factory=MCPConfig)
    context7: Context7Config = Field(default_factory=Context7Config)
    paths: PathConfig = Field(default_factory=PathConfig)
    log_level: str = "INFO"
    environment: str = "development"


def load_config(config_path: Optional[Union[str, Path]] = None) -> MarvinConfig:
    """Loads the configuration from a YAML file.

    Args:
        config_path: Path to the configuration file. If None, default values are used.

    Returns:
        The loaded configuration

    Raises:
        FileNotFoundError: If the specified configuration file was not found
        yaml.YAMLError: If the YAML file is invalid
    """
    config = {}

    if config_path:
        config_path = Path(config_path)
        if not config_path.exists():
            logger.error(f"Configuration file not found: {config_path}")
            raise FileNotFoundError(f"Configuration file not found: {config_path}")

        logger.info(f"Loading configuration from {config_path}")
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                config = yaml.safe_load(f)
            logger.debug("Configuration file loaded successfully")
        except yaml.YAMLError as e:
            logger.error(f"Error parsing YAML configuration: {e}")
            raise
    else:
        logger.info("No configuration file specified, using default values")

    # Default agent configurations
    if "agents" not in config:
        logger.debug("Adding default agent configurations")
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

    # Environment variables override configuration
    if os.environ.get("MARVIN_API_HOST"):
        if "api" not in config:
            config["api"] = {}
        config["api"]["host"] = os.environ["MARVIN_API_HOST"]
        logger.debug(f"Using API host from environment: {config['api']['host']}")

    if os.environ.get("MARVIN_API_PORT"):
        if "api" not in config:
            config["api"] = {}
        config["api"]["port"] = int(os.environ["MARVIN_API_PORT"])
        logger.debug(f"Using API port from environment: {config['api']['port']}")

    if os.environ.get("MARVIN_MCP_HOST"):
        if "mcp" not in config:
            config["mcp"] = {}
        config["mcp"]["host"] = os.environ["MARVIN_MCP_HOST"]
        logger.debug(f"Using MCP host from environment: {config['mcp']['host']}")

    if os.environ.get("MARVIN_MCP_PORT"):
        if "mcp" not in config:
            config["mcp"] = {}
        config["mcp"]["port"] = int(os.environ["MARVIN_MCP_PORT"])
        logger.debug(f"Using MCP port from environment: {config['mcp']['port']}")

    if os.environ.get("MARVIN_CONTEXT7_API_KEY"):
        if "context7" not in config:
            config["context7"] = {}
        config["context7"]["api_key"] = os.environ["MARVIN_CONTEXT7_API_KEY"]
        logger.debug("Using Context7 API key from environment")

    if os.environ.get("MARVIN_LOG_LEVEL"):
        config["log_level"] = os.environ["MARVIN_LOG_LEVEL"]
        logger.debug(f"Using log level from environment: {config['log_level']}")

    if os.environ.get("MARVIN_ENVIRONMENT"):
        config["environment"] = os.environ["MARVIN_ENVIRONMENT"]
        logger.debug(f"Using environment from environment: {config['environment']}")

    # Create config object
    marvin_config = MarvinConfig(**config)
    logger.info(
        f"Configuration loaded: environment={marvin_config.environment}, log_level={marvin_config.log_level}"
    )

    # Update logging level based on config
    setup_logging(marvin_config.log_level)

    return marvin_config


# Global configuration
config = load_config()
