import tkinter as tk
from pathlib import Path
import customtkinter as ctk
from pytubefix import YouTube
# from pytubefix.cli import on_progress

DOWNLOADS_DIR = Path.home() / "Downloads"

# System Settings
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


# https://github.com/JuanBindez/pytubefix/blob/main/docs/user/streams.rst#id5
def download_video():
    try:
        yt_link = url_var.get()
        yt_object = YouTube(yt_link, on_progress_callback=on_progress_update)

        # Retrieve video and audio streams
        video_stream = yt_object.streams.get_highest_resolution()
        audio_stream = yt_object.streams.filter(only_audio=True).get_by_itag(251)

        # Update UI with the video title
        title_label.configure(text=yt_object.title, text_color="white")
        status_label.configure(text="")

        # Download the audio file
        audio_stream.download(output_path=str(DOWNLOADS_DIR), skip_existing=True, mp3=True)
    except Exception as e:
        status_label.configure(text=str(e), text_color="red")
    else:
        status_label.configure(text="Download Complete")


def on_progress_update(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percent_complete = round(bytes_downloaded / total_size * 100, 0)

    # Update progress percentage and progress bar
    progress_label.configure(text=f"{percent_complete}%")
    progress_label.update()
    progress_bar.set(percent_complete / 100)


# Initialize app frame
app = ctk.CTk()
app.geometry("720x480")
app.title("YouTube Downloader")

# Create a frame to hold the UI elements
frame = ctk.CTkFrame(app)
frame.grid(row=0, column=0, padx=20, pady=20)

# UI Elements
title_label = ctk.CTkLabel(frame, text="YouTube-Link eingeben:")
title_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

# URL Entry
url_var = tk.StringVar()
url_entry = ctk.CTkEntry(frame, width=350, height=40, textvariable=url_var)
url_entry.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

# Status Label
status_label = ctk.CTkLabel(frame, text="")
status_label.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

# Progress Percentage Label
progress_label = ctk.CTkLabel(frame, text="0%")
progress_label.grid(row=3, column=0, padx=10, pady=10)

# Progress Bar
progress_bar = ctk.CTkProgressBar(frame, width=400)
progress_bar.set(0)
progress_bar.grid(row=3, column=1, padx=10, pady=10)

# Download Button
download_button = ctk.CTkButton(frame, text="Download", command=download_video)
download_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

# Run the app
app.mainloop()
