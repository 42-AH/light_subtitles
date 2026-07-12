import os
import glob
import tkinter as tk
from tkinter import ttk, colorchooser

FONTS = ["Segoe UI", "Arial", "Calibri", "Verdana", "Tahoma", "Consolas", "Georgia"]


class SettingsWindow:
    def __init__(self, root, cfg, on_apply):
        self.on_apply = on_apply
        self.cfg = dict(cfg)
        self.top = tk.Toplevel(root)
        self.top.title("Subtitle Settings")
        self.top.attributes("-topmost", True)
        self.top.resizable(False, False)
        self.vars = {}
        self._build()

    def _label(self, parent, r, text):
        tk.Label(parent, text=text, anchor="w").grid(
            row=r, column=0, sticky="w", padx=8, pady=5)

    def _build(self):
        f = ttk.Frame(self.top, padding=12)
        f.grid()
        r = 0

        self._label(f, r, "Model (language)")
        models = sorted(os.path.basename(p) for p in glob.glob("models/*")
                        if os.path.isdir(p))
        current = os.path.basename(self.cfg["model_path"])
        if current and current not in models:
            models = [current] + models
        self.vars["model"] = tk.StringVar(value=current)
        ttk.Combobox(f, textvariable=self.vars["model"], values=models,
                     width=34).grid(row=r, column=1, sticky="w")
        r += 1

        self._label(f, r, "Font")
        self.vars["font_family"] = tk.StringVar(value=self.cfg["font_family"])
        ttk.Combobox(f, textvariable=self.vars["font_family"], values=FONTS,
                     width=34).grid(row=r, column=1, sticky="w")
        r += 1

        self._label(f, r, "Font size")
        self.vars["font_size"] = tk.IntVar(value=self.cfg["font_size"])
        tk.Spinbox(f, from_=10, to=120, textvariable=self.vars["font_size"],
                   width=8).grid(row=r, column=1, sticky="w")
        r += 1

        self._label(f, r, "Text color")
        self.vars["font_color"] = tk.StringVar(value=self.cfg["font_color"])
        self._color_picker(f, r, self.vars["font_color"])
        r += 1

        self._label(f, r, "Box color")
        self.vars["box_color"] = tk.StringVar(value=self.cfg.get("box_color", "#000000"))
        self._color_picker(f, r, self.vars["box_color"])
        r += 1

        self._label(f, r, "Box padding")
        self.vars["box_padding"] = tk.IntVar(value=self.cfg.get("box_padding", 10))
        tk.Spinbox(f, from_=0, to=60, textvariable=self.vars["box_padding"],
                   width=8).grid(row=r, column=1, sticky="w")
        r += 1

        self._label(f, r, "Position")
        self.vars["position"] = tk.StringVar(value=self.cfg["position"])
        ttk.Combobox(f, textvariable=self.vars["position"],
                     values=["top", "middle", "bottom"], state="readonly",
                     width=34).grid(row=r, column=1, sticky="w")
        r += 1

        self._label(f, r, "Edge margin (px)")
        self.vars["margin"] = tk.IntVar(value=self.cfg["margin"])
        tk.Spinbox(f, from_=0, to=600, textvariable=self.vars["margin"],
                   width=8).grid(row=r, column=1, sticky="w")
        r += 1

        self._label(f, r, "Max lines")
        self.vars["max_lines"] = tk.IntVar(value=self.cfg["max_lines"])
        tk.Spinbox(f, from_=1, to=5, textvariable=self.vars["max_lines"],
                   width=8).grid(row=r, column=1, sticky="w")
        r += 1

        self._label(f, r, "Max chars/line")
        self.vars["max_chars"] = tk.IntVar(value=self.cfg["max_chars"])
        tk.Spinbox(f, from_=20, to=160, textvariable=self.vars["max_chars"],
                   width=8).grid(row=r, column=1, sticky="w")
        r += 1

        self._label(f, r, "Clear after (s)")
        self.vars["clear_after"] = tk.IntVar(value=self.cfg["clear_after"])
        tk.Spinbox(f, from_=1, to=30, textvariable=self.vars["clear_after"],
                   width=8).grid(row=r, column=1, sticky="w")
        r += 1

        self.vars["click_through"] = tk.BooleanVar(value=self.cfg["click_through"])
        tk.Checkbutton(f, text="Click-through overlay",
                       variable=self.vars["click_through"]).grid(
            row=r, column=1, sticky="w")
        r += 1

        tk.Label(f, text="Download more language models: alphacephei.com/vosk/models",
                 fg="#666").grid(row=r, column=0, columnspan=2, sticky="w",
                                 pady=(8, 2))
        r += 1

        btns = ttk.Frame(f)
        btns.grid(row=r, column=0, columnspan=2, pady=(10, 0))
        ttk.Button(btns, text="Apply", command=self._apply).grid(
            row=0, column=0, padx=6)
        ttk.Button(btns, text="Save & Close", command=self._save_close).grid(
            row=0, column=1, padx=6)

    def _color_picker(self, parent, r, var):
        frame = ttk.Frame(parent)
        frame.grid(row=r, column=1, sticky="w")
        tk.Entry(frame, textvariable=var, width=12).grid(row=0, column=0)

        def pick():
            chosen = colorchooser.askcolor(color=var.get())[1]
            if chosen:
                var.set(chosen)

        ttk.Button(frame, text="Pick", command=pick, width=6).grid(
            row=0, column=1, padx=4)

    def _collect(self):
        cfg = dict(self.cfg)
        model = self.vars["model"].get()
        if model:
            cfg["model_path"] = os.path.join("models", model)
        cfg["font_family"] = self.vars["font_family"].get()
        cfg["font_size"] = int(self.vars["font_size"].get())
        cfg["font_color"] = self.vars["font_color"].get()
        cfg["box_color"] = self.vars["box_color"].get()
        cfg["box_padding"] = int(self.vars["box_padding"].get())
        cfg["position"] = self.vars["position"].get()
        cfg["margin"] = int(self.vars["margin"].get())
        cfg["max_lines"] = int(self.vars["max_lines"].get())
        cfg["max_chars"] = int(self.vars["max_chars"].get())
        cfg["clear_after"] = int(self.vars["clear_after"].get())
        cfg["click_through"] = bool(self.vars["click_through"].get())
        return cfg

    def _apply(self):
        self.cfg = self._collect()
        self.on_apply(self.cfg)

    def _save_close(self):
        self._apply()
        self.top.destroy()
