# 🧮 Tkinter Calculator

A clean, modern desktop calculator built with **Python** and **Tkinter**. Features a dark theme, responsive layout, keyboard support, and smart display scaling.

---

## 📸 Preview

> A fully functional calculator with a dark UI, color-coded buttons, and a responsive display that scales with the window size.

---

## ✨ Features

- **Basic Operations** — Addition, Subtraction, Multiplication, Division
- **Extra Functions** — Percentage (`%`) and Toggle Sign (`+/-`)
- **Smart Display** — Font auto-scales to fit any number without overflow
- **Resizable Window** — UI adapts fully when window is resized
- **Keyboard Support** — Type numbers and operators directly from your keyboard
- **Error Handling** — Gracefully handles division by zero and invalid inputs
- **Dark Theme** — Clean, modern dark UI with color-coded buttons

---

## 🖥️ Requirements

- Python 3.x
- Tkinter *(built-in with Python — no installation needed)*

---

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/tkinter-calculator.git
cd tkinter-calculator
```

### 2. Run the calculator
```bash
python calculator.py
```

That's it — no dependencies to install!

---

## ⌨️ Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `0` – `9` | Input digits |
| `+` | Addition |
| `-` | Subtraction |
| `*` | Multiplication |
| `/` | Division |
| `.` | Decimal point |
| `Enter` | Calculate result (`=`) |
| `Backspace` / `Esc` | Clear display (`C`) |

---

## 🗂️ Project Structure

```
tkinter-calculator/
├── calculator.py        # Main application
├── test_calculator.py   # Unit tests for calculator logic
└── README.md            # Project documentation
```

---

## 🧪 Running Tests

To verify the calculator logic is working correctly:

```bash
python test_calculator.py
```

Expected output:
```
All tests passed! ✅
```

---

## 🎨 UI Overview

| Button | Color | Function |
|--------|-------|----------|
| `C` | 🔴 Red | Clears the display |
| `÷ × − +` | ⬛ Dark grey | Operators |
| `=` | 🟠 Orange | Evaluates result |
| `0–9`, `.` | ⬛ Grey | Number input |

---

## 🔧 Customisation

You can tweak the display font size limits inside `_fit_display_font()` in `calculator.py`:

```python
# Line 178 — Maximum font size (raise for bigger text)
max_size = max(20, min(48, available // 9))

# Line 180 — Minimum font size (lower to fit more digits)
while size > 8:
```

To change button or background colors, edit the `self.colors` dictionary at the top of the `Calculator` class.

---

## 📋 Version History

| Version | Description |
|---------|-------------|
| v1.0 | Initial release — basic calculator with dark theme |

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

## 🙋 Author

Built with ❤️ using Python and Tkinter.
