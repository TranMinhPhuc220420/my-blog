import os
from pathlib import Path

def get_root_path_project() -> Path:
    """
    Get the root path of the project.

    Returns:
        Path: The root path of the project.
    """
    return Path(__file__).resolve().parent.parent