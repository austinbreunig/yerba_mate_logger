import os
import json
from pathlib import Path
from typing import Dict, Any
import json
from importlib.resources import files
from appdirs import user_data_dir

APP_NAME = "yerba_mate_logger"

def get_user_file(filename: str) -> Path:
    return Path(user_data_dir(APP_NAME)) / filename

def get_default_resource(filename: str):
    return files("yerba_logger.data") / filename

def ensure_user_copy(filename: str) -> Path:
    user_path = get_user_file(filename)
    user_path.parent.mkdir(parents=True, exist_ok=True)
    if not user_path.exists():
        default_data = json.loads(get_default_resource(filename).read_text())
        with user_path.open("w") as f:
            json.dump(default_data, f, indent=2)
    return user_path

class BrandRegistry:
    def __init__(self):
        self.path = ensure_user_copy("yerbas.json")
        self.brands = self._load()
    
    def _load(self):
        if os.path.exists(self.path):
            return json.loads(self.path.read_text())
        else:
            raise FileNotFoundError(f"File {self.path} not found.")
        
    def save(self):
        with open(self.path, "w") as f:
            json.dump(self.brands, f, indent=2)

    def add_brand(self, name: str, location: str):
        self.brands[name] = location
        self.save()

    def get_location(self, name: str):
        return self.brands.get(name)

    def list_brands(self):
        return self.brands.keys()
    
class ProfileRegistry:
    def __init__(self):
        self.path = ensure_user_copy("profiles.json")
        self.profiles = self._load()


    def _load(self):
        if os.path.exists(self.path):
            return json.loads(self.path.read_text())
        else:
            raise FileNotFoundError(f"File {self.path} not found.")
        
    def save(self):
        with open(self.path, "w") as f:
            json.dump(self.profiles, f, indent=2)

    def add_profile(self, name: str, data: str):
        self.profiles[name].append(data)
        self.save()

    def remove_profile(self, name: str, data: str):
        if name in self.profiles:
            self.profiles[name].remove(data)
            self.save()
        else:
            raise KeyError(f"Profile '{name}' not found.")

    def get_profile(self, name: str):
        # return json
        return self.profiles.get(name)
    
    def list_profiles(self):
        return self.profiles.keys()
    
class WeightRegistry:
    def __init__(self):
        self.path = ensure_user_copy("weights.json")
        self.weights = self._load()

    def _load(self):
        if os.path.exists(self.path):
            return json.loads(self.path.read_text())
        else:
            raise FileNotFoundError(f"File {self.path} not found.")
        
    def save(self):
        with open(self.path, "w") as f:
            json.dump(self.weights, f, indent=2)

    def add_weight(self, name: str, data: str): # in-development
        self.weights[name] = data
        self.save()

    def get_weight(self, name: str): # in-development
        return self.weights.get(name)