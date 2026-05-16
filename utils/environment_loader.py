from pathlib import Path
import json


CONFIG_DIR = Path(__file__).resolve().parent.parent / "config"


def load_env_config(env: str = "dev") -> dict:
    """
    Load environment-specific configuration.
    """

    config_file = CONFIG_DIR / f"{env}.json"

    if not config_file.exists():
        raise FileNotFoundError(
            f"Environment config file not found: {config_file}"
        )

    with config_file.open("r", encoding="utf-8") as file:
        return json.load(file)