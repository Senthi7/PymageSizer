import os
from PIL import Image
import pillow_heif
import tkinter as tk
from tkinter import filedialog, messagebox

# Ensure HEIF format is registered with Pillow
pillow_heif.register_heif_opener()

def resize_image(image_path, output_folder, prefix, max_width=1200, max_size_kb=400, count=1):
    try:
        with Image.open(image_path) as img:
            original_size = os.path.getsize(image_path) / 1024

            # Calculate the new height to maintain aspect ratio
            width_percent = max_width / float(img.size[0])
            new_height = int((float(img.size[1]) * float(width_percent)))

            img = img.resize((max_width, new_height), Image.LANCZOS)
            output_filename = f"{prefix}-{count}.jpg"
            output_path = os.path.join(output_folder, output_filename)
            
            # Save image with different quality settings to meet the max size requirement
            quality = 85
            img.save(output_path, optimize=True, quality=quality)
            
            resized_size = os.path.getsize(output_path) / 1024

            while os.path.getsize(output_path) > max_size_kb * 1024 and quality > 10:
                quality -= 5
                img.save(output_path, optimize=True, quality=quality)
                resized_size = os.path.getsize(output_path) / 1024
            
    except Exception as e:
        print(f"Error processing image {image_path}: {e}")

def bulk_resize_images(folder_path, output_folder, prefix, max_width=1200, max_size_kb=400):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    count = 1
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.jpg', '.jpeg', '.heic')):
            file_path = os.path.join(folder_path, filename)
            try:
                if os.path.getsize(file_path) > max_size_kb * 1024 or Image.open(file_path).size[0] > max_width:
                    resize_image(file_path, output_folder, prefix, max_width, max_size_kb, count)
                    count += 1
            except Exception as e:
                print(f"Error checking file {file_path}: {e}")

def select_input_folder():
    folder_path = filedialog.askdirectory()
    input_folder_var.set(folder_path)

def select_output_folder():
    folder_path = filedialog.askdirectory()
    output_folder_var.set(folder_path)

def start_resize():
    input_folder = input_folder_var.get()
    output_folder = output_folder_var.get()
    prefix = prefix_var.get()
    max_width = int(max_width_var.get())
    max_size_kb = int(max_size_var.get())
    
    if not input_folder or not output_folder:
        messagebox.showwarning("Warning", "Please select both input and output folders")
        return
    
    bulk_resize_images(input_folder, output_folder, prefix, max_width, max_size_kb)
    messagebox.showinfo("Info", "Image resizing completed")

app = tk.Tk()
app.title("Image Resizer")

input_folder_var = tk.StringVar()
output_folder_var = tk.StringVar()
prefix_var = tk.StringVar(value="karumari2024-canon")
max_width_var = tk.StringVar(value="1200")
max_size_var = tk.StringVar(value="400")

tk.Label(app, text="Input Folder:").grid(row=0, column=0, padx=10, pady=10)
tk.Entry(app, textvariable=input_folder_var, width=50).grid(row=0, column=1, padx=10, pady=10)
tk.Button(app, text="Browse", command=select_input_folder).grid(row=0, column=2, padx=10, pady=10)

tk.Label(app, text="Output Folder:").grid(row=1, column=0, padx=10, pady=10)
tk.Entry(app, textvariable=output_folder_var, width=50).grid(row=1, column=1, padx=10, pady=10)
tk.Button(app, text="Browse", command=select_output_folder).grid(row=1, column=2, padx=10, pady=10)

tk.Label(app, text="Filename Prefix:").grid(row=2, column=0, padx=10, pady=10)
tk.Entry(app, textvariable=prefix_var, width=50).grid(row=2, column=1, padx=10, pady=10)

tk.Label(app, text="Max Width:").grid(row=3, column=0, padx=10, pady=10)
tk.Entry(app, textvariable=max_width_var, width=10).grid(row=3, column=1, padx=10, pady=10, sticky="w")

tk.Label(app, text="Max Size (KB):").grid(row=4, column=0, padx=10, pady=10)
tk.Entry(app, textvariable=max_size_var, width=10).grid(row=4, column=1, padx=10, pady=10, sticky="w")

tk.Button(app, text="Start Resizing", command=start_resize).grid(row=5, column=0, columnspan=3, pady=20)

app.mainloop()
