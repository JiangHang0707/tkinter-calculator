"""
Tkinter Calculator
==================
A clean, modern calculator with dark theme, keyboard support, and error handling.
Run: python calculator.py
Requires: Python 3.x (Tkinter is built-in)
"""

import tkinter as tk
import tkinter.font as tk_font  # noqa: F401 — activates tk.font namespace


class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculator")
        self.root.resizable(True, True)  # Allow resizing
        self.root.configure(bg="#1a1a1a")
        self.root.minsize(280, 420)      # Minimum size so it never gets too small

        # Center the window on screen
        window_width, window_height = 340, 520
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        x = (screen_w - window_width) // 2
        y = (screen_h - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # State
        self.expression = ""
        self.just_evaluated = False

        # Colors
        self.colors = {
            "bg":            "#1a1a1a",
            "display_bg":    "#111111",
            "display_fg":    "#f5f5f5",
            "expr_fg":       "#888888",
            "btn_number":    "#2c2c2c",
            "btn_operator":  "#3a3a3a",
            "btn_equals":    "#e88c00",
            "btn_clear":     "#c0392b",
            "btn_fg":        "#f5f5f5",
            "btn_hover_num": "#3f3f3f",
            "btn_hover_op":  "#4a4a4a",
            "btn_hover_eq":  "#f5a623",
            "btn_hover_cl":  "#e74c3c",
        }

        self._build_ui()
        self._bind_keyboard()
        self._bind_resize()

    # ─── UI CONSTRUCTION ──────────────────────────────────────────────────────

    def _build_ui(self):
        # Make root grid responsive
        self.root.rowconfigure(0, weight=0)  # display — fixed
        self.root.rowconfigure(1, weight=1)  # buttons — expands
        self.root.columnconfigure(0, weight=1)

        # ── Display area ──
        display_frame = tk.Frame(self.root, bg=self.colors["display_bg"], pady=16)
        display_frame.grid(row=0, column=0, sticky="ew", padx=12, pady=(16, 8))
        display_frame.columnconfigure(0, weight=1)

        # Expression label (small, shows what's being typed)
        self.expr_label = tk.Label(
            display_frame,
            text="",
            font=("Courier", 13),
            bg=self.colors["display_bg"],
            fg=self.colors["expr_fg"],
            anchor="e",
            padx=12,
        )
        self.expr_label.grid(row=0, column=0, sticky="ew")

        # Main result display — font size will scale on resize
        self.display_var = tk.StringVar(value="0")
        self.display = tk.Label(
            display_frame,
            textvariable=self.display_var,
            font=("Courier", 38, "bold"),
            bg=self.colors["display_bg"],
            fg=self.colors["display_fg"],
            anchor="e",
            padx=12,
        )
        self.display.grid(row=1, column=0, sticky="ew")

        # ── Button grid ──
        self.btn_frame = tk.Frame(self.root, bg=self.colors["bg"])
        self.btn_frame.grid(row=1, column=0, sticky="nsew", padx=12, pady=(0, 12))

        buttons = [
            ("C",   0, 0, 1, "clear"),
            ("+/-", 0, 1, 1, "operator"),
            ("%",   0, 2, 1, "operator"),
            ("÷",   0, 3, 1, "operator"),
            ("7",   1, 0, 1, "number"),
            ("8",   1, 1, 1, "number"),
            ("9",   1, 2, 1, "number"),
            ("×",   1, 3, 1, "operator"),
            ("4",   2, 0, 1, "number"),
            ("5",   2, 1, 1, "number"),
            ("6",   2, 2, 1, "number"),
            ("−",   2, 3, 1, "operator"),
            ("1",   3, 0, 1, "number"),
            ("2",   3, 1, 1, "number"),
            ("3",   3, 2, 1, "number"),
            ("+",   3, 3, 1, "operator"),
            ("0",   4, 0, 2, "number"),
            (".",   4, 2, 1, "number"),
            ("=",   4, 3, 1, "equals"),
        ]

        for col in range(4):
            self.btn_frame.columnconfigure(col, weight=1, uniform="col")
        for row in range(5):
            self.btn_frame.rowconfigure(row, weight=1, uniform="row")

        self.buttons = {}  # store button refs for font scaling
        for (label, row, col, colspan, style) in buttons:
            btn = self._make_button(self.btn_frame, label, row, col, colspan, style)
            self.buttons[label] = btn

    def _make_button(self, parent, label, row, col, colspan, style):
        color_map = {
            "number":   (self.colors["btn_number"],   self.colors["btn_hover_num"]),
            "operator": (self.colors["btn_operator"], self.colors["btn_hover_op"]),
            "equals":   (self.colors["btn_equals"],   self.colors["btn_hover_eq"]),
            "clear":    (self.colors["btn_clear"],    self.colors["btn_hover_cl"]),
        }
        bg, hover_bg = color_map[style]

        btn = tk.Button(
            parent,
            text=label,
            font=("Courier", 18, "bold"),
            bg=bg,
            fg=self.colors["btn_fg"],
            activebackground=hover_bg,
            activeforeground=self.colors["btn_fg"],
            relief="flat",
            bd=0,
            cursor="hand2",
            command=lambda l=label: self._on_button(l),
        )
        btn.grid(row=row, column=col, columnspan=colspan, sticky="nsew", padx=4, pady=4)
        btn.bind("<Enter>", lambda e, b=btn, c=hover_bg: b.config(bg=c))
        btn.bind("<Leave>", lambda e, b=btn, c=bg: b.config(bg=c))
        return btn

    # ─── RESPONSIVE FONT SCALING ──────────────────────────────────────────────

    def _bind_resize(self):
        """Scale fonts when window is resized."""
        self.root.bind("<Configure>", self._on_resize)

    def _on_resize(self, event):
        if event.widget != self.root:
            return
        w = event.width
        expr_size = max(10, min(16, w // 26))
        btn_size  = max(12, min(22, w // 20))
        self.expr_label.config(font=("Courier", expr_size))
        for btn in self.buttons.values():
            btn.config(font=("Courier", btn_size, "bold"))
        # Re-fit display font to current text
        self._fit_display_font()

    def _fit_display_font(self):
        """Shrink display font so the current number always fits within window width."""
        text = self.display_var.get()
        # Available width with generous padding buffer to prevent overflow
        available = max(100, self.root.winfo_width() - 80)
        # Start from a max size and shrink until text fits
        max_size = max(20, min(48, available // 9))
        size = max_size
        while size > 8:
            # Use tk's actual font measurement for pixel-perfect accuracy
            test_font = tk.font.Font(family="Courier", size=size, weight="bold")
            actual_width = test_font.measure(text)
            if actual_width <= available:
                break
            size -= 1
        self.display.config(font=("Courier", size, "bold"))

    # ─── KEYBOARD SUPPORT ─────────────────────────────────────────────────────

    def _bind_keyboard(self):
        for char in "0123456789.":
            self.root.bind(char, lambda e, c=char: self._on_button(c))
        self.root.bind("+",          lambda e: self._on_button("+"))
        self.root.bind("-",          lambda e: self._on_button("−"))
        self.root.bind("*",          lambda e: self._on_button("×"))
        self.root.bind("/",          lambda e: self._on_button("÷"))
        self.root.bind("<Return>",   lambda e: self._on_button("="))
        self.root.bind("<KP_Enter>", lambda e: self._on_button("="))
        self.root.bind("<BackSpace>",lambda e: self._on_button("C"))
        self.root.bind("<Escape>",   lambda e: self._on_button("C"))

    # ─── LOGIC ────────────────────────────────────────────────────────────────

    def _on_button(self, label):
        if label == "C":
            self._clear()
        elif label == "=":
            self._evaluate()
        elif label == "+/-":
            self._toggle_sign()
        elif label == "%":
            self._percent()
        else:
            self._append(label)

    def _append(self, value):
        op_map = {"×": "*", "÷": "/", "−": "-"}
        actual = op_map.get(value, value)

        if self.just_evaluated and value.isdigit():
            self.expression = ""
        self.just_evaluated = False

        if actual in "*/+-" and self.expression and self.expression[-1] in "*/+-":
            self.expression = self.expression[:-1]

        if actual in "*/+" and not self.expression:
            return

        if actual == ".":
            parts = self.expression.replace("*", "+").replace("/", "+").replace("-", "+").split("+")
            if parts and "." in parts[-1]:
                return

        self.expression += actual

        display_expr = self.expression.replace("*", "×").replace("/", "÷").replace("-", "−")
        self.expr_label.config(text=display_expr)
        parts = self.expression.replace("*", " ").replace("/", " ").replace("+", " ").replace("-", " ").split()
        self.display_var.set(parts[-1] if parts else "0")
        self._fit_display_font()

    def _evaluate(self):
        if not self.expression:
            return
        try:
            result = eval(self.expression)
            if isinstance(result, float):
                result = round(result, 10)
                if result == int(result):
                    result = int(result)
            display_expr = self.expression.replace("*", "×").replace("/", "÷").replace("-", "−")
            self.expr_label.config(text=display_expr + " =")
            self.display_var.set(str(result))
            self.expression = str(result)
            self.just_evaluated = True
            self._fit_display_font()
        except ZeroDivisionError:
            self.display_var.set("÷ by zero!")
            self.expr_label.config(text="")
            self.expression = ""
            self.just_evaluated = True
        except Exception:
            self.display_var.set("Error")
            self.expr_label.config(text="")
            self.expression = ""
            self.just_evaluated = True

    def _clear(self):
        self.expression = ""
        self.just_evaluated = False
        self.display_var.set("0")
        self.expr_label.config(text="")
        self._fit_display_font()

    def _toggle_sign(self):
        if not self.expression:
            return
        try:
            result = -eval(self.expression)
            self.expression = str(result)
            self.display_var.set(str(result))
            self.expr_label.config(text=self.expression)
        except Exception:
            pass

    def _percent(self):
        if not self.expression:
            return
        try:
            result = eval(self.expression) / 100
            result = round(result, 10)
            if result == int(result):
                result = int(result)
            self.expression = str(result)
            self.display_var.set(str(result))
            self.expr_label.config(text=self.expression)
        except Exception:
            pass


# ─── ENTRY POINT ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    root = tk.Tk()
    app = Calculator(root)
    root.mainloop()