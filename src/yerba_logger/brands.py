import os
import json
from pathlib import Path
from typing import Dict, Any
import json
from importlib.resources import files

class BrandRegistry:
    def __init__(self):
        self.path = files("yerba_logger.data") / "yerbas.json"
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