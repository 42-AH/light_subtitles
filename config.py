import json
import os

CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")

DEFAULTS = {
    "model_path": "models/vosk-model-small-en-us-0.15",
    "samplerate": 16000,
    "font_family": "Segoe UI",
    "font_size": 30,
    "font_color": "#FFFFFF",
    "box_color": "#000000",
    "box_padding": 10,
    "position": "bottom",
    "margin": 90,
    "max_chars": 20,
    "max_lines": 1,
    "clear_after": 4,
    "click_through": True,
    "hotkey_settings": "<ctrl>+<alt>+s",
    "hotkey_toggle": "<ctrl>+<alt>+h",
}


def load():
    cfg = dict(DEFAULTS)
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                cfg.update(json.load(f))
        except (json.JSONDecodeError, OSError):
            pass
    return cfg


def save(cfg):
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2)
