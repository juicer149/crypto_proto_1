import yaml
from pathlib import Path
from typing import Any, Dict


def load_yaml(file_path: str) -> Dict[str, Any]:
    """
    Loads a YAML file with pathlib - Path -.
    Casts an error if path dont exists().
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    with open(path, "r", encoding="utf-8") as file:
        return yaml.safe_load(file)
