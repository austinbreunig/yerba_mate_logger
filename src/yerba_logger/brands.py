import json
from pathlib import Path
from typing import Dict, Any

class BrandRegistry:
    def __init__(self, path="yerbas.json"):
        self.path = Path(path)
        self.brands = self._load()

    def _load(self):
        if self.path.exists():
            with open(self.path) as f:
                return json.load(f)
        return {}

    def save(self):
        with open(self.path, "w") as f:
            json.dump(self.brands, f, indent=2)

    def add_brand(self, name: str, location: str):
        self.brands[name] = location
        self.save()

    def get_location(self, name: str):
        return self.brands.get(name)
