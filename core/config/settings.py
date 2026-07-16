from pathlib import Path

import yaml


CONFIG_FILE = Path(__file__).resolve().parent / "environments.yaml"


class Settings:
    def __init__(self, env: str = "local"):
        with CONFIG_FILE.open("r", encoding="utf-8") as file:
            environments = yaml.safe_load(file)

        if env not in environments:
            raise ValueError(f"Unknown environment: {env}")

        self.env = env
        self.base_url = environments[env]["base_url"]