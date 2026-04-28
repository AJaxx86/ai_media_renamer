import json
from pathlib import Path
from typing import Any

CONFIG_PATH = Path("config.json")

DEFAULT_CONFIG: dict[str, Any] = {
	"openrouter_key": "",
	"ollama_port": "11434",
	"cloud_enabled": False,
	"cloud_model": "google/gemini-3-flash-preview",
}


def load_config() -> dict[str, Any]:
	if not CONFIG_PATH.exists():
		save_config(DEFAULT_CONFIG)
		return DEFAULT_CONFIG.copy()

	try:
		with CONFIG_PATH.open("r", encoding="utf-8") as file:
			loaded = json.load(file)
	except json.JSONDecodeError:
		return DEFAULT_CONFIG.copy()

	config = DEFAULT_CONFIG.copy()
	config.update(loaded)
	return config


def save_config(config: dict[str, Any]) -> None:
	with CONFIG_PATH.open("w", encoding="utf-8") as file:
		json.dump(config, file, indent=4)


def get_setting(key: str) -> Any:
	return load_config().get(key, DEFAULT_CONFIG.get(key))


def set_setting(key: str, value: Any) -> None:
	config = load_config()
	config[key] = value
	save_config(config)
