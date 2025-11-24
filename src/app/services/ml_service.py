import json
from pathlib import Path

class MlService:

    def __init__(self):
        app_root = Path(__file__).resolve().parents[1]
        self.base_path = app_root / "assets" / "plots" / "fase5"

    def load_ml_data(self):
        json_file = self.base_path / "results.json"

        print("DEBUG PATH:", json_file, json_file.exists())

        if not json_file.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {json_file}")

        with open(json_file, "r", encoding="utf-8") as f:
            return json.load(f)
