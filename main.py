import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, Menu, Frame, Canvas
from PIL import Image, ImageTk
import easyocr
import pyperclip
import pyautogui

class OCRApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pro OCR - Screenshot & Text Extraction Tool")
        self.root.geometry("1200x800")
        self.root.configure(bg="#1e1e1e")
        self.root.minsize(900, 600)

        self.reader = easyocr.Reader(['en'], gpu=False)
        self.image_path = None
        self.original_image = None
        self.zoom_level = 1.0

        self.setup_menu()
        self.setup_ui()
        self.bind_shortcuts()

    def setup_menu(self):
        menu_bar = Menu(self.root)
        file_menu = Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Upload Image (Ctrl+O)", command=self.upload_image)
        file_menu.add_command(label="Capture Screen", command=self.capture_screen)
        file_menu.add_command(label="Save Text (Ctrl+S)", command=self.save_text)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        menu_bar.add_cascade(label="File", menu=file_menu)

        help_menu = Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="About", command=lambda: messagebox.showinfo("About", "Pro OCR Tool v1.0\nBy Shiboshree Roy"))
        menu_bar.add_cascade(label="Help", menu=help_menu)

        self.root.config(menu=menu_bar)

    def setup_ui(self):
        # Title Label
        title = tk.Label(self.root, text="🧠 Advanced OCR Tool", font=("Segoe UI", 20, "bold"),
                         bg="#1e1e1e", fg="#00ffae")
        title.grid(row=0, column=0, columnspan=3, pady=10, sticky="n")

        # Toolbar Frame with buttons
        toolbar = tk.Frame(self.root, bg="#2e2e2e")
        toolbar.grid(row=1, column=0, columnspan=3, sticky="ew", padx=10, pady=5)
        toolbar.columnconfigure(0, weight=1)

        buttons = [
            ("📁 Upload Image", self.upload_image, "#0078D7"),
            ("📷 Capture Screen", self.capture_screen, "#FF9500"),
            ("🔍 Extract Text", self.extract_text, "#28A745"),
            ("📋 Copy Text", self.copy_text, "#17A2B8"),
            ("💾 Save Text", self.save_text, "#6C63FF"),
            ("🧹 Clear", self.clear_all, "#DC3545"),
            ("🔍 Zoom In", self.zoom_in, "#8A2BE2"),
            ("🔎 Zoom Out", self.zoom_out, "#20B2AA")
        ]

        for i, (text, cmd, color) in enumerate(buttons):
            btn = tk.Button(toolbar, text=text, command=cmd, bg=color, fg="white",
                            font=("Segoe UI", 10, "bold"), padx=10)
            btn.grid(row=0, column=i, padx=5, pady=2)

        # Scrollable Image Display Area
        self.image_frame = Frame(self.root, bg="#1e1e1e", relief=tk.SUNKEN, bd=1)
        self.image_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=5)

        # Configure grid weights for responsiveness
        self.root.grid_rowconfigure(2, weight=3)  # image area bigger vertical weight
        self.root.grid_columnconfigure(0, weight=1)

        # Canvas for image and scrollbars
        self.canvas = Canvas(self.image_frame, bg="#1e1e1e", highlightthickness=0)
        self.canvas.grid(row=0, column=0, sticky="nsew")

        self.v_scrollbar = tk.Scrollbar(self.image_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.v_scrollbar.grid(row=0, column=1, sticky="ns")

        self.h_scrollbar = tk.Scrollbar(self.image_frame, orient=tk.HORIZONTAL, command=self.canvas.xview)
        self.h_scrollbar.grid(row=1, column=0, sticky="ew")

        self.canvas.configure(yscrollcommand=self.v_scrollbar.set, xscrollcommand=self.h_scrollbar.set)

        self.image_frame.grid_rowconfigure(0, weight=1)
        self.image_frame.grid_columnconfigure(0, weight=1)

        # Create a frame inside canvas to hold the image label (needed for scroll region)
        self.canvas_frame = Frame(self.canvas, bg="#1e1e1e")
        self.canvas.create_window((0, 0), window=self.canvas_frame, anchor="nw")

        # Image label inside the canvas_frame
        self.image_label = tk.Label(self.canvas_frame, bg="#1e1e1e")
        self.image_label.pack()

        # Bind the canvas frame resize event to update scroll region
        self.canvas_frame.bind("<Configure>", self.on_canvas_frame_configure)

        # Text area for extracted text
        self.text_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, font=("Segoe UI", 11),
                                                   width=130, height=15, bg="#f0f0f0", fg="black")
        self.text_area.grid(row=3, column=0, columnspan=3, sticky="nsew", padx=10, pady=10)
        self.root.grid_rowconfigure(3, weight=1)

        # Configure columnspan 3 for full width for text area and buttons
        self.root.grid_columnconfigure(1, weight=0)
        self.root.grid_columnconfigure(2, weight=0)

    def on_canvas_frame_configure(self, event):
        # Update scroll region to encompass the inner frame
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def bind_shortcuts(self):
        self.root.bind('<Control-o>', lambda event: self.upload_image())
        self.root.bind('<Control-s>', lambda event: self.save_text())

    def upload_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.tiff")])
        if file_path:
            self.image_path = file_path
            self.load_image(file_path)

    def load_image(self, path):
        self.original_image = Image.open(path)
        self.zoom_level = 1.0  # reset zoom on new image
        self.display_image(self.original_image)

    def display_image(self, img):
        # Resize with zoom
        width, height = img.size
        new_size = (int(width * self.zoom_level), int(height * self.zoom_level))
        resized = img.resize(new_size, Image.ANTIALIAS)

        self.tk_image = ImageTk.PhotoImage(resized)
        self.image_label.config(image=self.tk_image)

        # Update canvas scroll region
        self.canvas.config(scrollregion=(0, 0, new_size[0], new_size[1]))

        # Update size of canvas_frame to fit image (to trigger scrollbar correctly)
        self.canvas_frame.config(width=new_size[0], height=new_size[1])

    def capture_screen(self):
        self.root.withdraw()
        pyautogui.sleep(1)
        screenshot = pyautogui.screenshot()
        screenshot.save("temp_capture.png")
        self.root.deiconify()
        self.image_path = "temp_capture.png"
        self.load_image("temp_capture.png")
        self.text_area.delete(1.0, tk.END)

    def extract_text(self):
        if self.image_path:
            result = self.reader.readtext(self.image_path)
            extracted_text = "\n".join([item[1] for item in result])
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(tk.END, extracted_text)
        else:
            messagebox.showwarning("No Image", "Please upload or capture an image first.")

    def copy_text(self):
        text = self.text_area.get(1.0, tk.END).strip()
        if text:
            pyperclip.copy(text)
            messagebox.showinfo("Copied", "Text copied to clipboard.")
        else:
            messagebox.showwarning("Empty", "There is no text to copy.")

    def save_text(self):
        text = self.text_area.get(1.0, tk.END).strip()
        if text:
            file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                     filetypes=[("Text Files", "*.txt")])
            if file_path:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(text)
                messagebox.showinfo("Saved", f"Text saved to {file_path}")
        else:
            messagebox.showwarning("No Text", "There is no text to save.")

    def clear_all(self):
        self.image_label.config(image='')
        self.text_area.delete(1.0, tk.END)
        self.image_path = None
        self.original_image = None
        self.zoom_level = 1.0
        self.canvas.config(scrollregion=(0,0,0,0))
        self.canvas_frame.config(width=0, height=0)

    def zoom_in(self):
        if self.original_image:
            self.zoom_level += 0.1
            self.display_image(self.original_image)

    def zoom_out(self):
        if self.original_image and self.zoom_level > 0.2:
            self.zoom_level -= 0.1
            self.display_image(self.original_image)

if __name__ == "__main__":
    root = tk.Tk()
    app = OCRApp(root)
    root.mainloop()
