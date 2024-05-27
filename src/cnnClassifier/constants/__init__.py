"""
    Here we read the config.yaml, params.yaml file ,
    because CONFIG_FILE_PATH, PARAMS_FILE_PATH are constants which are never be changed.
"""

from pathlib import Path

CONFIG_FILE_PATH = Path("config\config.yaml")
PARAMS_FILE_PATH = Path("params.yaml")