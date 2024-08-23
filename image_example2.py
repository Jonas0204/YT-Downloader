import customtkinter as ctk
import os
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox
from mutagen.id3 import ID3, ID3NoHeaderError, APIC, TIT2, TPE1, TALB
from pytubefix import YouTube


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Constants
        self.DOWNLOADS_DIR = Path.home() / "Downloads"

        # Initialize UI
        self.title("MP3 Metadata Editor")
        self.geometry("700x450")

        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # create navigation frame
        self.navigation_frame = ctk.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        self.home_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10,
                                         text="Home", command=self.home_button_event)
        self.home_button.grid(row=1, column=0, sticky="ew")

        self.frame_3_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10,
                                            text="Frame 3", command=self.frame_3_button_event)
        self.frame_3_button.grid(row=2, column=0, sticky="ew")

        self.appearance_mode_menu = ctk.CTkOptionMenu(self.navigation_frame, values=["Light", "Dark", "System"],
                                                      command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=6, column=0, padx=20, pady=20, sticky="s")
        self.appearance_mode_menu.set("System")  # Set default to System

        # create home frame
        self.home_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.home_frame.grid_columnconfigure(0, weight=1)

        # UI Elements for home frame
        self.title_label = ctk.CTkLabel(self.home_frame, text="YouTube-Link eingeben:")
        self.title_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        self.url_var = tk.StringVar()
        self.url_entry = ctk.CTkEntry(self.home_frame, width=350, height=40, textvariable=self.url_var)
        self.url_entry.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        self.status_label = ctk.CTkLabel(self.home_frame, text="")
        self.status_label.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        self.progress_label = ctk.CTkLabel(self.home_frame, text="0%")
        self.progress_label.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        self.progress_bar = ctk.CTkProgressBar(self.home_frame, width=400)
        self.progress_bar.set(0)
        self.progress_bar.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

        self.download_button = ctk.CTkButton(self.home_frame, text="Download", command=self.download_video)
        self.download_button.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

        # create third frame
        self.third_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.create_frame_3_widgets()  # Initialize widgets for frame 3

        # select default frame
        self.select_frame_by_name("home")

    def select_frame_by_name(self, name):
        """Setzt die Ansicht auf das angegebene Frame"""
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.frame_3_button.configure(fg_color=("gray75", "gray25") if name == "frame_3" else "transparent")

        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()
        if name == "frame_3":
            self.third_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.third_frame.grid_forget()

    def home_button_event(self):
        """Wechselt zu Home Frame"""
        self.select_frame_by_name("home")

    def frame_3_button_event(self):
        """Wechselt zu Frame 3"""
        self.select_frame_by_name("frame_3")

    def change_appearance_mode_event(self, new_appearance_mode):
        """Ändert den Erscheinungsmodus und aktualisiert die Listbox-Farben"""
        ctk.set_appearance_mode(new_appearance_mode)

    def create_frame_3_widgets(self):
        """Erstellt die Widgets für Frame 3 zur Bearbeitung von Metadaten"""
        self.metadata_title_label = ctk.CTkLabel(self.third_frame, text="Title:")
        self.metadata_title_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.metadata_title_entry = ctk.CTkEntry(self.third_frame, width=300)
        self.metadata_title_entry.grid(row=0, column=1, padx=10, pady=10)

        self.metadata_artist_label = ctk.CTkLabel(self.third_frame, text="Artist:")
        self.metadata_artist_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.metadata_artist_entry = ctk.CTkEntry(self.third_frame, width=300)
        self.metadata_artist_entry.grid(row=1, column=1, padx=10, pady=10)

        self.metadata_album_label = ctk.CTkLabel(self.third_frame, text="Album:")
        self.metadata_album_label.grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.metadata_album_entry = ctk.CTkEntry(self.third_frame, width=300)
        self.metadata_album_entry.grid(row=2, column=1, padx=10, pady=10)

        self.cover_image_button = ctk.CTkButton(self.third_frame, text="Choose Cover Image",
                                                command=self.choose_cover_image)
        self.cover_image_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        self.save_metadata_button = ctk.CTkButton(self.third_frame, text="Save Metadata", command=self.save_metadata)
        self.save_metadata_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

        # Listbox for displaying files
        self.file_listbox = tk.Listbox(self.third_frame, selectmode=tk.SINGLE)
        self.file_listbox.grid(row=6, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        self.file_listbox.bind("<<ListboxSelect>>", self.on_listbox_select)

        self.cover_image_path = ""
        self.current_file_path = ""

    def choose_cover_image(self):
        """Öffnet einen Dateidialog, um ein Cover-Bild auszuwählen"""
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            self.cover_image_path = file_path

    def save_metadata(self):
        """Speichert die Metadaten in der MP3-Datei"""
        if not self.current_file_path:
            messagebox.showerror("Error", "No MP3 file selected")
            return

        try:
            audio = ID3(self.current_file_path)

            # Set metadata
            audio[TIT2] = TIT2(encoding=3, text=self.metadata_title_entry.get())
            audio[TPE1] = TPE1(encoding=3, text=self.metadata_artist_entry.get())
            audio[TALB] = TALB(encoding=3, text=self.metadata_album_entry.get())

            # Add cover image
            if self.cover_image_path:
                with open(self.cover_image_path, 'rb') as img_file:
                    cover_data = img_file.read()
                audio['APIC'] = APIC(encoding=3, mime='image/jpeg', type=3, desc='Cover', data=cover_data)

            audio.save()
            messagebox.showinfo("Success", "Metadata saved successfully!")

        except ID3NoHeaderError:
            # Create new ID3 tag if none exists
            audio = ID3()
            self.save_metadata()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def download_video(self):
        """Startet den Download eines MP3s von YouTube"""
        url = self.url_var.get()  # URL vom Entry-Feld holen
        if not url:
            self.status_label.configure(text="No URL provided", text_color="red")
            return

        try:
            yt = YouTube(url, on_progress_callback=self.on_progress_update)
            audio_stream = yt.streams.filter(only_audio=True).get_by_itag(251)

            # Update UI with the video title
            self.title_label.configure(text=yt.title, text_color="white")
            self.status_label.configure(text="")

            # Download audio file
            audio_stream.download(output_path=str(self.DOWNLOADS_DIR), skip_existing=True, mp3=True)

            self.status_label.configure(text="Download Complete")
            self.update_file_list()  # Update the file list
        except Exception as e:
            self.status_label.configure(text=str(e), text_color="red")
            print(e)

    def on_progress_update(self, stream, chunk, bytes_remaining):
        """Callback zur Fortschrittsaktualisierung"""
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        percent_complete = round(bytes_downloaded / total_size * 100, 2)

        # Update progress percentage and progress bar
        self.progress_label.configure(text=f"{percent_complete}%")
        self.progress_label.update()
        self.progress_bar.set(percent_complete / 100)
        self.progress_bar.update()


    def update_file_list(self):
        """Aktualisiert die Liste der MP3-Dateien im Download-Verzeichnis"""
        self.file_listbox.delete(0, tk.END)
        for file in os.listdir(self.DOWNLOADS_DIR):
            if file.lower().endswith(".mp3"):
                self.file_listbox.insert(tk.END, file)

    def on_listbox_select(self, event):
        """Wird aufgerufen, wenn eine Datei in der Listbox ausgewählt wird"""
        selection = self.file_listbox.curselection()
        if selection:
            selected_file = self.file_listbox.get(selection[0])
            self.current_file_path = os.path.join(self.DOWNLOADS_DIR, selected_file)
            self.load_metadata()
            self.select_frame_by_name("frame_3")  # Wechsel zu Frame 3

    def load_metadata(self):
        """Lädt die Metadaten der ausgewählten MP3-Datei"""
        try:
            audio = ID3(self.current_file_path)
            self.metadata_title_entry.delete(0, tk.END)
            self.metadata_artist_entry.delete(0, tk.END)
            self.metadata_album_entry.delete(0, tk.END)

            self.metadata_title_entry.insert(0, audio.get(TIT2, "").text[0])
            self.metadata_artist_entry.insert(0, audio.get(TPE1, "").text[0])
            self.metadata_album_entry.insert(0, audio.get(TALB, "").text[0])

        except ID3NoHeaderError:
            # Handle file without ID3 tags
            pass
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while loading metadata: {e}")


if __name__ == "__main__":
    app = App()
    app.mainloop()
