import os
import tkinter as tk
import customtkinter as ctk
from yt_downloader_jh.download import download_video
from yt_downloader_jh.metadata import save_metadata, load_metadata
from yt_downloader_jh.utils import choose_cover_image, update_file_list
from pathlib import Path

DOWNLOADS_DIR = Path.home() / "Downloads"
cover_image_path = None
current_file_path = None

def create_main_window():
    global home_frame, third_frame

    root = ctk.CTk()
    root.title("MP3 Metadata Editor")
    root.geometry("700x450")

    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)

    navigation_frame = create_navigation_frame(root)
    navigation_frame.grid(row=0, column=0, sticky="nsew")

    home_frame, third_frame = create_frames(root)
    create_home_frame(home_frame)
    create_third_frame(third_frame)

    select_frame_by_name("home")

    return root

def create_navigation_frame(root):
    navigation_frame = ctk.CTkFrame(root, corner_radius=0)
    navigation_frame.grid_rowconfigure(4, weight=1)

    home_button = ctk.CTkButton(navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Home",
                                command=lambda: select_frame_by_name("home"))
    home_button.grid(row=1, column=0, sticky="ew")

    frame_3_button = ctk.CTkButton(navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Frame 3",
                                   command=lambda: select_frame_by_name("frame_3"))
    frame_3_button.grid(row=2, column=0, sticky="ew")
    #frame_3_button.grid_forget()  # Initial verstecken

    appearance_mode_menu = ctk.CTkOptionMenu(navigation_frame, values=["Light", "Dark", "System"],
                                             command=change_appearance_mode_event)
    appearance_mode_menu.grid(row=6, column=0, padx=20, pady=20, sticky="s")
    appearance_mode_menu.set("System")

    return navigation_frame

def create_frames(root):
    home_frame = ctk.CTkFrame(root, corner_radius=0, fg_color="transparent")
    home_frame.grid_columnconfigure(0, weight=1)

    third_frame = ctk.CTkFrame(root, corner_radius=0, fg_color="transparent")

    return home_frame, third_frame

def create_home_frame(home_frame):
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

    download_button = ctk.CTkButton(home_frame, text="Download", command=lambda: download_video(url_var, status_label, title_label, progress_label, progress_bar, lambda: update_file_list(file_listbox, DOWNLOADS_DIR)))
    download_button.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

def create_third_frame(third_frame):
    global file_listbox, metadata_title_entry, metadata_artist_entry, metadata_album_entry

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

    cover_image_button = ctk.CTkButton(third_frame, text="Choose Cover Image", command=choose_cover_image)
    cover_image_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    save_metadata_button = ctk.CTkButton(third_frame, text="Save Metadata", command=lambda: save_metadata(current_file_path, metadata_title_entry, metadata_artist_entry, metadata_album_entry, cover_image_path))
    save_metadata_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

    file_listbox = tk.Listbox(third_frame, selectmode=tk.SINGLE)
    file_listbox.grid(row=6, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
    file_listbox.bind("<<ListboxSelect>>", lambda event: on_listbox_select(event, file_listbox))

def change_appearance_mode_event(new_appearance_mode):
    ctk.set_appearance_mode(new_appearance_mode)
    update_listbox_colors()

def update_listbox_colors():
    current_mode = ctk.get_appearance_mode()
    if current_mode == "Light":
        listbox_bg = "white"
        listbox_fg = "black"
    else:
        listbox_bg = "gray20"
        listbox_fg = "white"
    if 'file_listbox' in globals():
        file_listbox.configure(bg=listbox_bg, fg=listbox_fg)

def select_frame_by_name(name):
    if name == "home":
        home_frame.grid(row=0, column=1, sticky="nsew")
        third_frame.grid_forget()
    elif name == "frame_3":
        third_frame.grid(row=0, column=1, sticky="nsew")
        home_frame.grid_forget()

def on_listbox_select(event, file_listbox):
    global current_file_path
    selection = file_listbox.curselection()
    if selection:
        selected_file = file_listbox.get(selection[0])
        current_file_path = os.path.join(DOWNLOADS_DIR, selected_file)
        load_metadata(current_file_path, metadata_title_entry, metadata_artist_entry, metadata_album_entry)
        select_frame_by_name("frame_3")
