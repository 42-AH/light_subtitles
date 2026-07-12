import os
import tkinter as tk
from tkinter import messagebox

from pynput import keyboard

import config
from transcriber import Transcriber
from audio_capture import AudioCapture
from overlay import Overlay
from settings_window import SettingsWindow


class App:
    def __init__(self):
        self.cfg = config.load()
        self.root = tk.Tk()
        self.root.withdraw()
        self.overlay = Overlay(self.root, self.cfg)
        self.capture = None
        self.transcriber = None
        self.settings = None
        self.visible = True
        self.start_pipeline()
        self.setup_hotkeys()

    def start_pipeline(self):
        model_path = self.cfg["model_path"]
        if not os.path.isdir(model_path):
            self.prompt_missing_model(model_path)
            return
        self.transcriber = Transcriber(model_path, self.cfg["samplerate"])
        self.capture = AudioCapture(self.transcriber, self.on_text,
                                    samplerate=self.cfg["samplerate"])
        self.capture.start()

    def stop_pipeline(self):
        if self.capture:
            self.capture.stop()
            self.capture.join(timeout=2)
            self.capture = None
        self.transcriber = None

    def on_text(self, text, is_final):
        if is_final:
            self.root.after(0, lambda: self.overlay.show(final_text=text))
        else:
            self.root.after(0, lambda: self.overlay.show(partial_text=text))

    def apply_config(self, new_cfg):
        restart = (new_cfg["model_path"] != self.cfg["model_path"]
                   or new_cfg["samplerate"] != self.cfg["samplerate"])
        self.cfg = new_cfg
        config.save(new_cfg)
        self.overlay.update_config(new_cfg)
        if restart:
            self.stop_pipeline()
            self.start_pipeline()

    def open_settings(self):
        if self.settings and self.settings.top.winfo_exists():
            self.settings.top.lift()
            return
        self.settings = SettingsWindow(self.root, self.cfg, self.apply_config)

    def toggle(self):
        self.visible = not self.visible
        (self.overlay.win.deiconify if self.visible
         else self.overlay.win.withdraw)()

    def prompt_missing_model(self, model_path):
        messagebox.showwarning(
            "Model not found",
            f"No Vosk model at:\n{model_path}\n\n"
            "Download one from alphacephei.com/vosk/models, unzip it into the "
            "'models' folder, then pick it in Settings (Ctrl+Alt+S).")
        self.root.after(300, self.open_settings)

    def setup_hotkeys(self):
        def marshal(fn):
            return lambda: self.root.after(0, fn)

        self.hotkeys = keyboard.GlobalHotKeys({
            self.cfg["hotkey_settings"]: marshal(self.open_settings),
            self.cfg["hotkey_toggle"]: marshal(self.toggle),
        })
        self.hotkeys.start()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    App().run()
