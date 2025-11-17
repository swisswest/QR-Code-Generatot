import tkinter as tk
from tkinter import filedialog, messagebox
import qrcode
from qrcode.image.pil import PilImage
from urllib.parse import urlparse


def is_valid_url(url: str) -> bool:
    parsed = urlparse(url)
    return all([parsed.scheme in ("http", "https"), parsed.netloc])


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
            fill_color="black",
            back_color="white"
        )

        img.save(file_path)
        messagebox.showinfo("Success", f"QR Code has been saved:\n{file_path}")

    except Exception as e:
        messagebox.showerror("Error", str(e))


root = tk.Tk()
root.title("QR Code Generator")
root.geometry("400x200")
root.resizable(False, False)

frame = tk.Frame(root, padx=20, pady=20)
frame.pack(fill="both", expand=True)

tk.Label(frame, text="Enter URL:").pack(anchor="w")

entry_data = tk.Entry(frame, width=40)
entry_data.pack(fill="x", pady=5)

tk.Button(frame, text="Generate & Save QR Code", command=generate_qr).pack(pady=10)

root.mainloop()
