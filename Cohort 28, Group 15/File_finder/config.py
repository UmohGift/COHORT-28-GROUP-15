from pathlib import Path
from typing import Dict

# dictionary
config: Dict[str, object] = {
    "root_path": str(Path.home() ), 
    "case_sensitive": True,
    "display_size": 10
}


def set_root_path(new_path: str) -> None:
    """Update root path if valid directory"""
    path = Path(new_path)
    if path.exists() and path.is_dir():
        config["root_path"] = str(path)
    else:
        print("Invalid path. Keeping old root_path.")


def toggle_case_sensitive() -> None:
    """Switch case sensitivity"""
    config["case_sensitive"] = not config["case_sensitive"]


def set_display_size(size: int) -> None:
    """Update display size between 3–20"""
    if 3 <= size <= 20:
        config["display_size"] = size
    else:
        print("Display size must be between 3 and 20.")
