import customtkinter as ctk
import os
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox
from mutagen.id3 import ID3, ID3NoHeaderError, APIC, TIT2, TPE1, TALB
from pytubefix import YouTube

# Constants
DOWNLOADS_DIR = Path.home() / "Downloads"

# Initialize main window
root = ctk.CTk()
root.title("MP3 Metadata Editor")
root.geometry("700x450")

# Grid layout setup
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

# Navigation frame
navigation_frame = ctk.CTkFrame(root, corner_radius=0)
navigation_frame.grid(row=0, column=0, sticky="nsew")
navigation_frame.grid_rowconfigure(4, weight=1)

def select_frame_by_name(name):
    if name == "home":
        home_frame.grid(row=0, column=1, sticky="nsew")
    else:
        home_frame.grid_forget()
    if name == "frame_3":
        third_frame.grid(row=0, column=1, sticky="nsew")
    else:
        third_frame.grid_forget()

def home_button_event():
    select_frame_by_name("home")

def frame_3_button_event():
    select_frame_by_name("frame_3")

def change_appearance_mode_event(new_appearance_mode):
    ctk.set_appearance_mode(new_appearance_mode)

home_button = ctk.CTkButton(navigation_frame, corner_radius=0, height=40, border_spacing=10,
                            text="Home", command=home_button_event)
home_button.grid(row=1, column=0, sticky="ew")

frame_3_button = ctk.CTkButton(navigation_frame, corner_radius=0, height=40, border_spacing=10,
                               text="Frame 3", command=frame_3_button_event)
frame_3_button.grid(row=2, column=0, sticky="ew")
frame_3_button.grid_forget()

appearance_mode_menu = ctk.CTkOptionMenu(navigation_frame, values=["Light", "Dark", "System"],
                                         command=change_appearance_mode_event)
appearance_mode_menu.grid(row=6, column=0, padx=20, pady=20, sticky="s")
appearance_mode_menu.set("System")

# Home frame
home_frame = ctk.CTkFrame(root, corner_radius=0, fg_color="transparent")
home_frame.grid_columnconfigure(0, weight=1)

title_label = ctk.CTkLabel(home_frame, text="YouTube-Link eingeben:")
title_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

url_var = tk.StringVar()
url_entry = ctk.CTkEntry(home_frame, width=350, height=40, textvariable=url_var)
url_entry.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

status_label = ctk.CTkLabel(home_frame, text="")
status_label.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

progress_label = ctk.CTkLabel(home_frame, text="0%")
progress_label.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

progress_bar = ctk.CTkProgressBar(home_frame, width=400)
progress_bar.set(0)
progress_bar.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

def download_video():
    url = url_var.get()
    if not url:
        status_label.configure(text="No URL provided", text_color="red")
        return

    try:
        yt = YouTube(url, on_progress_callback=on_progress_update)
        audio_stream = yt.streams.filter(only_audio=True).get_by_itag(251)

        title_label.configure(text=yt.title, text_color="white")
        status_label.configure(text="")

        audio_stream.download(output_path=str(DOWNLOADS_DIR), skip_existing=True, mp3=True)

        status_label.configure(text="Download Complete")
        update_file_list()
    except Exception as e:
        status_label.configure(text=str(e), text_color="red")
        print(e)

def on_progress_update(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percent_complete = round(bytes_downloaded / total_size * 100, 2)

    progress_label.configure(text=f"{percent_complete}%")
    progress_label.update()
    progress_bar.set(percent_complete / 100)
    progress_bar.update()

download_button = ctk.CTkButton(home_frame, text="Download", command=download_video)
download_button.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

# Third frame
third_frame = ctk.CTkFrame(root, corner_radius=0, fg_color="transparent")

metadata_title_label = ctk.CTkLabel(third_frame, text="Title:")
metadata_title_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")
metadata_title_entry = ctk.CTkEntry(third_frame, width=300)
metadata_title_entry.grid(row=0, column=1, padx=10, pady=10)

metadata_artist_label = ctk.CTkLabel(third_frame, text="Artist:")
metadata_artist_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")
metadata_artist_entry = ctk.CTkEntry(third_frame, width=300)
metadata_artist_entry.grid(row=1, column=1, padx=10, pady=10)

metadata_album_label = ctk.CTkLabel(third_frame, text="Album:")
metadata_album_label.grid(row=2, column=0, padx=10, pady=10, sticky="e")
metadata_album_entry = ctk.CTkEntry(third_frame, width=300)
metadata_album_entry.grid(row=2, column=1, padx=10, pady=10)

def choose_cover_image():
    global cover_image_path
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    if file_path:
        cover_image_path = file_path

cover_image_button = ctk.CTkButton(third_frame, text="Choose Cover Image", command=choose_cover_image)
cover_image_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

def save_metadata():
    global current_file_path
    if not current_file_path:
        messagebox.showerror("Error", "No MP3 file selected")
        return

    try:
        audio = ID3(current_file_path)

        audio[TIT2] = TIT2(encoding=3, text=metadata_title_entry.get())
        audio[TPE1] = TPE1(encoding=3, text=metadata_artist_entry.get())
        audio[TALB] = TALB(encoding=3, text=metadata_album_entry.get())

        if cover_image_path:
            with open(cover_image_path, 'rb') as img_file:
                cover_data = img_file.read()
            audio['APIC'] = APIC(encoding=3, mime='image/jpeg', type=3, desc='Cover', data=cover_data)

        audio.save()
        messagebox.showinfo("Success", "Metadata saved successfully!")

    except ID3NoHeaderError:
        audio = ID3()
        save_metadata()
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

save_metadata_button = ctk.CTkButton(third_frame, text="Save Metadata", command=save_metadata)
save_metadata_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

# Listbox for displaying files
file_listbox = tk.Listbox(third_frame, selectmode=tk.SINGLE)
file_listbox.grid(row=6, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

def update_file_list():
    file_listbox.delete(0, tk.END)
    for file in os.listdir(DOWNLOADS_DIR):
        if file.lower().endswith(".mp3"):
            file_listbox.insert(tk.END, file)

def on_listbox_select(event):
    global current_file_path
    selection = file_listbox.curselection()
    if selection:
        selected_file = file_listbox.get(selection[0])
        current_file_path = os.path.join(DOWNLOADS_DIR, selected_file)
        load_metadata()
        select_frame_by_name("frame_3")

file_listbox.bind("<<ListboxSelect>>", on_listbox_select)

def load_metadata():
    try:
        audio = ID3(current_file_path)
        metadata_title_entry.delete(0, tk.END)
        metadata_artist_entry.delete(0, tk.END)
        metadata_album_entry.delete(0, tk.END)

        metadata_title_entry.insert(0, audio.get(TIT2, "").text[0])
        metadata_artist_entry.insert(0, audio.get(TPE1, "").text[0])
        metadata_album_entry.insert(0, audio.get(TALB, "").text[0])

    except ID3NoHeaderError:
        pass
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while loading metadata: {e}")

# Select default frame
select_frame_by_name("home")

# Start main loop
root.mainloop()
