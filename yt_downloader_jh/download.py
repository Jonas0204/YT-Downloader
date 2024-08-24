from pathlib import Path
from pytubefix import YouTube
from tkinter import StringVar

DOWNLOADS_DIR = Path.home() / "Downloads"

def download_video(url_var: StringVar, status_label, title_label, progress_label, progress_bar, update_file_list):
    url = url_var.get()
    if not url:
        status_label.configure(text="No URL provided", text_color="red")
        return

    try:
        yt = YouTube(url, on_progress_callback=lambda s, c, r: on_progress_update(s, c, r, progress_label, progress_bar))
        audio_stream = yt.streams.filter(only_audio=True).get_by_itag(251)

        title_label.configure(text=yt.title, text_color="white")
        status_label.configure(text="")

        audio_stream.download(output_path=str(DOWNLOADS_DIR), skip_existing=True, mp3=True)

        status_label.configure(text="Download Complete")

        update_file_list()
    except Exception as e:
        status_label.configure(text=str(e), text_color="red")
        print(e)

def on_progress_update(stream, chunk, bytes_remaining, progress_label, progress_bar):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percent_complete = round(bytes_downloaded / total_size * 100, 2)

    progress_label.configure(text=f"{percent_complete}%")
    progress_label.update()
    progress_bar.set(percent_complete / 100)
    progress_bar.update()
