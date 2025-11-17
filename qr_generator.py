import tkinter as tk
from tkinter import filedialog, messagebox, colorchooser
import qrcode
from qrcode.image.pil import PilImage
from urllib.parse import urlparse


# Default colors
qr_color = "#000000"
bg_color = "#FFFFFF"


def is_valid_url(url: str) -> bool:
    """Check if the given string is a valid URL."""
    parsed = urlparse(url)
    return all([parsed.scheme in ("http", "https"), parsed.netloc])


def choose_qr_color():
    global qr_color
    color = colorchooser.askcolor(title="Choose QR Code Color")
    if color[1] is not None:
        qr_color = color[1]
        qr_color_preview.config(bg=qr_color)


def choose_bg_color():
    global bg_color
    color = colorchooser.askcolor(title="Choose Background Color")
    if color[1] is not None:
        bg_color = color[1]
        bg_color_preview.config(bg=bg_color)


def generate_qr():
    data = entry_data.get().strip()

    if not is_valid_url(data):
        messagebox.showerror("Invalid URL", "Please enter a valid URL starting with http:// or https://")
        return

    file_path = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("PNG File", "*.png")],
        title="Save QR Code As"
    )

    if not file_path:
        return

    try:
        qr = qrcode.QRCode(
            version=None,
            error_correction=0,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)

        img = qr.make_image(
            image_factory=PilImage,
            fill_color=qr_color,
            back_color=bg_color
        )

        img.save(file_path)
        messagebox.showinfo("Success", f"QR Code has been saved:\n{file_path}")

    except Exception as e:
        messagebox.showerror("Error", str(e))


# --- GUI ---
root = tk.Tk()
root.title("QR Code Generator")
root.geometry("480x300")
root.resizable(False, False)

frame = tk.Frame(root, padx=20, pady=20)
frame.pack(fill="both", expand=True)


# URL input
tk.Label(frame, text="Enter URL:").pack(anchor="w")
entry_data = tk.Entry(frame, width=45)
entry_data.pack(fill="x", pady=5)


# COLOR SECTION
color_frame = tk.Frame(frame)
color_frame.pack(pady=15)


### QR COLOR ROW ###
tk.Label(color_frame, text="QR Code Color:").grid(row=0, column=0, padx=5, sticky="w")

btn_qr_color = tk.Button(color_frame, text="Pick", width=10, command=choose_qr_color)
btn_qr_color.grid(row=0, column=1, padx=5)

qr_color_preview = tk.Label(color_frame, bg=qr_color, width=10, height=1, relief="groove")
qr_color_preview.grid(row=0, column=2, padx=5)


### BACKGROUND COLOR ROW ###
tk.Label(color_frame, text="Background Color:").grid(row=1, column=0, padx=5, sticky="w")

btn_bg_color = tk.Button(color_frame, text="Pick", width=10, command=choose_bg_color)
btn_bg_color.grid(row=1, column=1, padx=5)

bg_color_preview = tk.Label(color_frame, bg=bg_color, width=10, height=1, relief="groove")
bg_color_preview.grid(row=1, column=2, padx=5)


# Generate Button
tk.Button(frame, text="Generate & Save QR Code", command=generate_qr).pack(pady=15)


root.mainloop()
