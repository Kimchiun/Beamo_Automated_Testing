"""
Configuration loader for Beamo automated testing platform.
Supports dev, stage, and live environments.
"""

import os
import yaml
from pathlib import Path
from typing import Dict, Any, Optional
from pydantic import BaseModel


class BrowserConfig(BaseModel):
    """Browser configuration model."""
    headless: bool = True
    slow_mo: int = 0
    timeout: int = 30000


class TestDataConfig(BaseModel):
    """Test data configuration model."""
    valid_user: Dict[str, str]
    admin_user: Dict[str, str]


class TestConfig(BaseModel):
    """Test configuration model."""
    screenshot_on_failure: bool = True
    video_recording: bool = True
    trace_recording: bool = True
    retry_count: int = 2


class ReportingConfig(BaseModel):
    """Reporting configuration model."""
    output_dir: str
    html_report: bool = True
    console_output: bool = True


class EmailConfig(BaseModel):
    """Email configuration model."""
    smtp_server: str = "smtp.gmail.com"
    smtp_port: int = 587
    sender_email: Optional[str] = None
    sender_password: Optional[str] = None
    recipient_email: str = "steve.kim@3i.ai"
    send_on_completion: bool = True


class APIConfig(BaseModel):
    """API configuration model."""
    base_url: str
    timeout: int = 10000


class EnvironmentConfig(BaseModel):
    """Complete environment configuration model."""
    environment: str
    base_url: str
    browser: BrowserConfig
    test_data: TestDataConfig
    test_config: TestConfig
    reporting: ReportingConfig
    api: APIConfig
    email: Optional[EmailConfig] = None


class ConfigLoader:
    """Configuration loader for managing environment-specific settings."""
    
    def __init__(self, config_dir: str = "config"):
        self.config_dir = Path(config_dir)
        self._configs: Dict[str, EnvironmentConfig] = {}
    
    def load_config(self, environment: str) -> EnvironmentConfig:
        """
        Load configuration for specified environment.
        
        Args:
            environment: Environment name (dev, stage, live)
            
        Returns:
            EnvironmentConfig: Loaded configuration
            
        Raises:
            FileNotFoundError: If config file doesn't exist
            ValueError: If config is invalid
        """
        if environment in self._configs:
            return self._configs[environment]
        
        config_file = self.config_dir / f"{environment}.yaml"
        
        if not config_file.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_file}")
        
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config_data = yaml.safe_load(f)
            
            config = EnvironmentConfig(**config_data)
            self._configs[environment] = config
            return config
            
        except Exception as e:
            raise ValueError(f"Invalid configuration in {config_file}: {e}")
    
    def get_current_environment(self) -> str:
        """Get current environment from environment variable."""
        return os.getenv("BEAMO_ENV", "dev")
    
    def get_current_config(self) -> EnvironmentConfig:
        """Get configuration for current environment."""
        env = self.get_current_environment()
        return self.load_config(env)


# Global config loader instance
config_loader = ConfigLoader()


def get_config(environment: Optional[str] = None) -> EnvironmentConfig:
    """
    Get configuration for specified or current environment.
    
    Args:
        environment: Environment name (optional, uses BEAMO_ENV if not provided)
        
    Returns:
        EnvironmentConfig: Configuration for the environment
    """
    if environment:
        return config_loader.load_config(environment)
    return config_loader.get_current_config()
