"""This file contains all utility related code.

UTILITY : The functionality which is used frequently in our code is called utility related functionality.

Like importing the packages directly from here to any files.
"""
import os
from box.exceptions import BoxValueError    # For handling exceptions
import yaml
from cnnClassifier import logger
import json
import joblib
from ensure import ensure_annotations    # It is used to make the data types are given correctly in the function if we mention
from box import ConfigBox    # The Configbox is same as dictionary.
from pathlib import Path
from typing import Any
import base64

@ensure_annotations
def read_yaml(path_to_yaml: Path)-> ConfigBox:
    """reads yaml file and returns 

        Args:
            path_to_yaml(str): path like input

        Raises:
            ValueError: if yaml file is empty
            e : empty file

        Returns:
            ConfigBox: ConfigBox type
    """
    try:
        with open(path_to_yaml) as yaml_file:
            content = yaml.safe_load(yaml_file)
            logger.info(f"yaml file: {path_to_yaml} loaded successfully")
            return ConfigBox(content)
    except BoxValueError:
        raise ValueError("yaml file is empty")
    except Exception as e:
        raise e
    
@ensure_annotations
def create_directories(path_to_directories,verbose=True):
    """create list of directories

        Args:
            path_to_directories(list) : list of path of directories
            ignore_log(bool,optional): ignores if multiple directories are created.
    """
    for path in path_to_directories:
        os.makedirs(path,exist_ok=True)
        if verbose:
            logger.info(f"Created directory at : {path}")

@ensure_annotations
def load_json(path):
    """load json files data

        Args:
            path (Path): path to json file

        Returns:
            ConfigBox: data as class attributes instead of dicts
    """
    with open(path) as f:
        content=json.load(f)
    
    logger.info(f"json file loaded successfully from : {path}")
    return ConfigBox(content)

@ensure_annotations
def save_json(path: Path, data: dict):
    """save json data

    Args:
        path (Path): path to json file
        data (dict): data to be saved in json file
    """
    with open(path, "w") as f:
        json.dump(data, f, indent=4)

    logger.info(f"json file saved at: {path}")

@ensure_annotations
def save_bin(data,path):
    """save binary file

        Args:
            data (Any) : data to be saved as binary
            path (Path) : path to binary file 
    """
    joblib.dump(value=data, filename=path)
    logger.info(f"binary file saved at : {path}")

@ensure_annotations
def load_bin(path):
    """Load binary file

        Args:
            path (Path) : path to binary file

        Returns:
            Any : object stored in a file 
    """
    data=joblib.load(filename=path)
    logger.info(f"binary file loaded from : {path}")
    return data

@ensure_annotations
def get_size(path):
    """get size in kb

        Args:
            path (Path) : path of the file

        Returns:
            str: size in kb
    """
    size_in_kb=round(os.path.getsize(path)/1024)
    return f"~{size_in_kb} KB"

def decodeImage(imgstring,filename):
    """This function is used to decode image from base64 format after uploading into frontend.
    """
    imgdata = base64.b64decode(imgstring)
    with open(filename,"wb") as f:
        f.write(imgdata)
        f.close()

def encodeImageIntoBase64(croppedImagePath):
    """
        This function is used to encode image to a base64 format
            while uploading to frontend.
    """
    with open(croppedImagePath, "rb") as f:
        return base64.b64decode(f.read())