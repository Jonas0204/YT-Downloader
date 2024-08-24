import os
import tkinter as tk
from tkinter import filedialog


def choose_cover_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    return file_path


def update_file_list(file_listbox, download_dir):
    file_listbox.delete(0, tk.END)
    for file in os.listdir(download_dir):
        if file.lower().endswith(".mp3"):
            file_listbox.insert(tk.END, file)
