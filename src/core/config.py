import json
from pathlib import Path
from typing import Any, Type, Optional, Union

_env_cache = {}

def load_env(path: str = "src/env.json") -> None:
    """
    Loads environment variables from a JSON config file into an internal cache.
    
    Args:
        path (str): Path to the config JSON file.
    """
    global _env_cache
    config_path = Path(path)


    if not config_path.exists():
        raise FileNotFoundError(f"Environment file not found: {path}")
    
    with config_path.open("r", encoding="utf-8") as file:
        _env_cache = json.load(file)


def get_env(key: str, default: Optional[Any] = None, as_type: Optional[Type] = None) -> Any:
    """
    Retrieves a value from the environment cache with optional type casting.
    
    Args:
        key (str): The variable name.
        default (Any): Fallback value if key is not found.
        as_type (Type): Type to cast the value to.
    
    Returns:
        Any: The value from the environment, cast if specified.
    """
    value = _env_cache.get(key, default)

    if as_type is not None and value is not None:
        try:
            return as_type(value)
        except (ValueError, TypeError):
            raise ValueError(f"Cannot cast environment variable '{key}' to {as_type}")
    
    return value
