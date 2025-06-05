# 📄 Pro OCR - Screenshot & Text Extraction Tool

**Version:** 1.0
**Author:** Shiboshree Roy
**Release Date:** 2025-06-05
**Icon:** 🧠 (Brain emoji to represent advanced OCR intelligence)

---

## Overview

**Pro OCR** is a modern, user-friendly desktop application built with Python and Tkinter for extracting text from images or screenshots. It leverages the powerful EasyOCR engine to provide accurate text recognition from uploaded images or live screen captures. The tool is designed with a sleek dark-themed UI and responsive layout to enhance usability and productivity.

---

## Features

* 📁 **Upload Image**: Open and load various image formats including PNG, JPG, JPEG, BMP, TIFF.
* 📷 **Capture Screen**: Instantly capture the current screen for OCR processing.
* 🔍 **Extract Text**: Use EasyOCR to detect and extract text from the loaded image.
* 📋 **Copy Text**: Copy extracted text to clipboard for quick pasting.
* 💾 **Save Text**: Save extracted text to a `.txt` file.
* 🧹 **Clear**: Reset the application to clear image and text.
* 🔍 **Zoom In/Out**: Zoom the loaded image for better view and inspection.
* 🖥️ **Responsive UI**: Adjusts layout to window resizing with scrollable text area and image display.
* ⚡ **Keyboard Shortcuts**: Ctrl+O to upload, Ctrl+S to save text for quick access.
* 🛠️ **Cross-Platform**: Works on Windows, macOS, and Linux (Python & dependencies required).

---

## System Requirements

* Python 3.7 or higher
* Tkinter (usually bundled with Python)
* PIL (Pillow)
* OpenCV (`cv2`)
* numpy
* easyocr
* pyperclip
* pyautogui

---

## Installation

Install dependencies using pip:

```bash
pip install pillow opencv-python numpy easyocr pyperclip pyautogui
```

---

## Usage

1. Run the application:

```bash
python main.py
```

2. Use the **File > Upload Image** menu or click **📁 Upload Image** to select an image file.
3. Use **📷 Capture Screen** to take a screenshot instantly.
4. Click **🔍 Extract Text** to process and extract text from the image.
5. Extracted text will display in the scrollable text box.
6. Use **📋 Copy Text** to copy text to clipboard or **💾 Save Text** to save it to a file.
7. Zoom in/out the image with **🔍 Zoom In** / **🔎 Zoom Out** buttons for better visualization.
8. Clear all content using **🧹 Clear**.

---

## Keyboard Shortcuts

* **Ctrl + O** — Upload Image
* **Ctrl + S** — Save Text

---

## Code Snippet Example

```python
# Initialize and run OCR application
if __name__ == "__main__":
    root = tk.Tk()
    app = OCRApp(root)
    root.mainloop()
```

---

## License

MIT License

---

## Contact

For feedback, suggestions, or issues, please contact:
**Shiboshree Roy**
Email: [shiboshreeroycse@gmail.com](mailto:shiboshreecseroy@gmail.com)

---

**Pro OCR** | Version 1.0 | © 2025 Shiboshree Roy

