# api/config/api_config.py

from typing import Dict
import yaml
from pathlib import Path


class APIConfig:
    """API Configuration management."""

    def __init__(self, config_path: str = "config/default/api_config.yaml"):
        self.config_path = Path(config_path)
        self.config = self._load_config()

    def _load_config(self) -> Dict:
        """Load API configuration from YAML file."""
        if not self.config_path.exists():
            raise FileNotFoundError(f"Config file not found: {self.config_path}")

        with open(self.config_path, 'r') as f:
            return yaml.safe_load(f)

    @property
    def rate_limits(self) -> Dict:
        """Get rate limiting configuration."""
        return self.config.get('rate_limits', {})

    @property
    def endpoints(self) -> Dict:
        """Get endpoint configuration."""
        return self.config.get('endpoints', {})

    @property
    def auth(self) -> Dict:
        """Get authentication configuration."""
        return self.config.get('auth', {})

    @property
    def cors(self) -> Dict:
        """Get CORS configuration."""
        return self.config.get('cors', {})