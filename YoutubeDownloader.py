import os
import sys
from pathlib import Path
try:
    import tkinter
    import customtkinter
    from yt_dlp import YoutubeDL
    import subprocess
    import urllib
except ImportError:
    print("ImportError")
    sys.exit(0)

version = "b 0.1.21"

def progress_hook(d):
    if d['status'] == 'downloading':
        progress = d.get('downloaded_bytes', 0) / d.get('total_bytes', 1)
        pPercentage.configure(text=f"{int(progress * 100)}%")
        pPercentage.update()
        pBar.set(progress)

def startDownload():
    ytLink = link.get()
    finishLabel.configure(text="", text_color="white")
    
    try:
        with YoutubeDL() as ydl:
            info_dict = ydl.extract_info(ytLink, download=False)  # Get video metadata
            video_title = info_dict.get('title', 'Youtube Downloader')
            title.configure(text=video_title, text_color="white")
    except Exception as e:
        finishLabel.configure(text=f"Error: {str(e)}", text_color="red")
        return
    
    download_folder = str(Path.home() / "Downloads")  # Set downloads folder
    ydl_opts = {
        'outtmpl': os.path.join(download_folder, '%(title)s.%(ext)s'),
        'progress_hooks': [progress_hook],
    }
    
    if optionmenu_var.get() == "mp4":
        ydl_opts['format'] = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]'
    elif optionmenu_var.get() == "mp3":
        ydl_opts['format'] = 'bestaudio'
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]
    elif optionmenu_var.get() == "wav":
        ydl_opts['format'] = 'bestaudio'
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
        }]
    
    try:
        with YoutubeDL(ydl_opts) as ydl:
            if ytLink:  # Ensure there's a valid link before downloading
                ydl.download([ytLink])
                finishLabel.configure(text="Downloaded", text_color="green")
    except Exception as e:
        finishLabel.configure(text=f"Error: {str(e)}", text_color="red")

def optionmenu_callback(choice):
    print("optionmenu dropdown clicked:", choice)


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# APP UI
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("green")

app = customtkinter.CTk()
app.geometry("720x300")
app.minsize(720,300)
app.title("Youtube Downloader")
app.iconbitmap(resource_path("favicon.ico"))

title = customtkinter.CTkLabel(app, text="Insert Youtube link", font=("Arial", 18))
title.pack(padx=10, pady=15)

url_var = tkinter.StringVar()
link = customtkinter.CTkEntry(app, width=350, height=46, textvariable=url_var)
link.pack()

optionmenu_var = customtkinter.StringVar(value="mp4")
optionmenu = customtkinter.CTkOptionMenu(app, values=["mp4", "mp3", "wav"], command=optionmenu_callback, variable=optionmenu_var)
optionmenu.pack(padx=10, pady=10)

finishLabel = customtkinter.CTkLabel(app, text="")
finishLabel.pack()

pPercentage = customtkinter.CTkLabel(app, text="0%")
pPercentage.pack()

pBar = customtkinter.CTkProgressBar(app, width=400)
pBar.set(0)
pBar.pack(padx=10, pady=10)

versionLabel = customtkinter.CTkLabel(app, text=version)
versionLabel.pack(side=tkinter.BOTTOM, anchor="w", padx="8")

download = customtkinter.CTkButton(app, text="Download", command=startDownload)
download.pack(side=tkinter.TOP, anchor="s")

app.mainloop()
