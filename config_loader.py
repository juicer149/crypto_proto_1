import json
import yaml
from pathlib import Path
from typing import Any, Dict


def load_config(file_path: str):
    """
    Loads YAML or JSON depending on file case.
    If the file ends with .json -> use json.load.
    Else use yaml.safe_load
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    with open(path, "r", encoding="utf-8") as file:
        if file_path.endswith(".json"):
            return json.load(file)
        else:
            return yaml.safe_load(file)
