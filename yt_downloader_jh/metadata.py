from mutagen.id3 import ID3, APIC, TIT2, TPE1, TALB, ID3NoHeaderError
from tkinter import messagebox
import tkinter as tk

def save_metadata(current_file_path, metadata_title, metadata_artist, metadata_album, cover_image_path):
    if not current_file_path:
        messagebox.showerror("Error", "No MP3 file selected")
        return

    try:
        audio = ID3(current_file_path)

        audio[TIT2] = TIT2(encoding=3, text=metadata_title.get())
        audio[TPE1] = TPE1(encoding=3, text=metadata_artist.get())
        audio[TALB] = TALB(encoding=3, text=metadata_album.get())

        if cover_image_path:
            with open(cover_image_path, 'rb') as img_file:
                cover_data = img_file.read()
            audio['APIC'] = APIC(encoding=3, mime='image/jpeg', type=3, desc='Cover', data=cover_data)

        audio.save()
        messagebox.showinfo("Success", "Metadata saved successfully!")
    except ID3NoHeaderError:
        audio = ID3()
        save_metadata(current_file_path, metadata_title, metadata_artist, metadata_album, cover_image_path)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def load_metadata(current_file_path, metadata_title, metadata_artist, metadata_album):
    try:
        audio = ID3(current_file_path)
        metadata_title.delete(0, tk.END)
        metadata_artist.delete(0, tk.END)
        metadata_album.delete(0, tk.END)

        metadata_title.insert(0, audio.get(TIT2, "").text[0])
        metadata_artist.insert(0, audio.get(TPE1, "").text[0])
        metadata_album.insert(0, audio.get(TALB, "").text[0])

    except ID3NoHeaderError:
        pass
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while loading metadata: {e}")
