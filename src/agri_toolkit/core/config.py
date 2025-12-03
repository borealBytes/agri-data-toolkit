"""Configuration management for agri-data-toolkit."""

from pathlib import Path
from typing import Any, Dict, Optional

import yaml


class Config:
    """Configuration manager for the toolkit.

    Loads configuration from YAML files and provides access to settings.
    """

    def __init__(self, config_path: Optional[str] = None):
        """Initialize configuration.

        Args:
            config_path: Path to configuration YAML file.
                        If None, uses default_config.yaml.
        """
        if config_path is None:
            # Use default config from package
            config_path = self._get_default_config_path()

        self.config_path = Path(config_path)
        self._config: Dict[str, Any] = {}
        self.load()

    def _get_default_config_path(self) -> str:
        """Get path to default configuration file."""
        # Look for config in repository root
        repo_root = Path(__file__).parent.parent.parent.parent
        default_config = repo_root / "config" / "default_config.yaml"

        if default_config.exists():
            return str(default_config)

        raise FileNotFoundError(
            f"Default configuration not found at {default_config}. "
            "Please provide a config_path or ensure config/default_config.yaml exists."
        )

    def load(self) -> None:
        """Load configuration from YAML file."""
        if not self.config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {self.config_path}")

        with open(self.config_path, "r") as f:
            self._config = yaml.safe_load(f)

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by key.

        Supports nested keys using dot notation (e.g., 'fields.count').

        Args:
            key: Configuration key (supports dot notation for nested values).
            default: Default value if key not found.

        Returns:
            Configuration value or default.
        """
        keys = key.split(".")
        value = self._config

        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default

        return value

    def get_field_config(self) -> Dict[str, Any]:
        """Get field boundaries configuration."""
        return self.get("fields", {})

    def get_download_config(self) -> Dict[str, Any]:
        """Get download settings."""
        return self.get("download", {})

    def get_paths(self) -> Dict[str, str]:
        """Get configured paths."""
        return self.get("paths", {})

    @property
    def data_root(self) -> Path:
        """Get root data directory."""
        return Path(self.get("paths.data_root", "data"))

    @property
    def raw_data_path(self) -> Path:
        """Get raw data directory."""
        return Path(self.get("paths.raw", "data/raw"))

    @property
    def processed_data_path(self) -> Path:
        """Get processed data directory."""
        return Path(self.get("paths.processed", "data/processed"))
