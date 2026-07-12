import sys
import ctypes
import tkinter as tk

CHROMA = "#010203"


class Overlay:
    def __init__(self, root, cfg):
        self.root = root
        self.cfg = dict(cfg)
        self.sw = root.winfo_screenwidth()
        self.sh = root.winfo_screenheight()

        self.win = tk.Toplevel(root)
        self.win.overrideredirect(True)
        self.win.geometry(f"{self.sw}x{self.sh}+0+0")
        self.win.attributes("-topmost", True)
        self.win.configure(bg=CHROMA)
        try:
            self.win.attributes("-transparentcolor", CHROMA)
        except tk.TclError:
            self.win.attributes("-alpha", 0.85)

        self.canvas = tk.Canvas(self.win, width=self.sw, height=self.sh,
                                bg=CHROMA, highlightthickness=0, bd=0)
        self.canvas.pack(fill="both", expand=True)

        self._final = ""
        self._partial = ""
        self._clear_job = None

        self.win.after(200, lambda: self._set_click_through(
            self.cfg.get("click_through", True)))

    def update_config(self, cfg):
        self.cfg = dict(cfg)
        self._set_click_through(self.cfg.get("click_through", True))
        self.render()

    def show(self, final_text=None, partial_text=None):
        if final_text is not None:
            self._final, self._partial = final_text, ""
        if partial_text is not None:
            self._partial = partial_text
        self.render()
        self._schedule_clear()

    def _schedule_clear(self):
        if self._clear_job:
            self.root.after_cancel(self._clear_job)
        secs = int(self.cfg.get("clear_after", 4))
        self._clear_job = self.root.after(secs * 1000, self._clear)

    def _clear(self):
        self._final = self._partial = ""
        self.render()

    def _wrap(self, text):
        max_chars = int(self.cfg.get("max_chars", 80))
        lines, cur = [], ""
        for word in text.split():
            if len(cur) + len(word) + 1 <= max_chars:
                cur = (cur + " " + word).strip()
            else:
                lines.append(cur)
                cur = word
        if cur:
            lines.append(cur)
        return lines[-int(self.cfg.get("max_lines", 2)):]

    def render(self):
        self.canvas.delete("all")
        text = self._partial or self._final
        if not text:
            return

        cfg = self.cfg
        lines = self._wrap(text)
        font = (cfg["font_family"], int(cfg["font_size"]), "bold")
        line_h = int(cfg["font_size"]) + 12
        block_h = line_h * len(lines)
        margin = int(cfg.get("margin", 90))

        pos = cfg.get("position", "bottom")
        if pos == "top":
            y0 = margin
        elif pos == "middle":
            y0 = (self.sh - block_h) // 2
        else:
            y0 = self.sh - block_h - margin

        cx = self.sw // 2
        items = []
        for i, line in enumerate(lines):
            y = y0 + i * line_h + line_h // 2
            items.append(self.canvas.create_text(
                cx, y, text=line, font=font, fill=cfg["font_color"]))

        bbox = self.canvas.bbox(*items)
        if bbox:
            pad = int(cfg.get("box_padding", 10))
            x1, y1, x2, y2 = bbox
            rect = self.canvas.create_rectangle(
                x1 - pad, y1 - pad, x2 + pad, y2 + pad,
                fill=cfg.get("box_color", "#000000"), outline="")
            self.canvas.tag_lower(rect)

    def _set_click_through(self, enable):
        if sys.platform != "win32":
            return
        try:
            hwnd = ctypes.windll.user32.GetParent(self.win.winfo_id())
            GWL_EXSTYLE, WS_EX_LAYERED, WS_EX_TRANSPARENT = -20, 0x80000, 0x20
            style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
            if enable:
                style |= WS_EX_LAYERED | WS_EX_TRANSPARENT
            else:
                style &= ~WS_EX_TRANSPARENT
            ctypes.windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style)
        except Exception:
            pass
