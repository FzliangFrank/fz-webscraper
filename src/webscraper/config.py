import toml
import os
from pathlib import Path
from typing import Dict, Any

def load_config() -> Dict[str, Any]:
    """
    Load configuration from config.toml file.
    
    Returns:
        Dict[str, Any]: Configuration dictionary
    """
    config_path = Path(__file__).parent.parent.parent / 'config' / 'scrapers.toml'
    
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file not found at {config_path}")
    
    with open(config_path, 'r') as f:
        config = toml.load(f)
    
    return config 