import os
import sys
try:
    import tkinter
    import customtkinter
    from pytube import YouTube
    import subprocess
except ImportError:
     print("ImportError")
     sys.exit(0)

version = "b 0.1.1"

def startDownload():
    try:
        def onProgress(stream, chunk, bytes_remaining):
            totalSize = stream.filesize
            bytesDownloaded = totalSize - bytes_remaining
            progressPercentage = bytesDownloaded / totalSize * 100
            per = str(int(progressPercentage))
            pPercentage.configure(text=per + "%")
            pPercentage.update()
            pBar.set(float(progressPercentage) / 100)

        ytLink = link.get()
        ytObject = YouTube(ytLink, on_progress_callback=onProgress)
        video = ytObject.streams.get_highest_resolution()
        audio = ytObject.streams.get_audio_only()

        title.configure(text=ytObject.title, text_color="white")
        finishLabel.configure(text="")
        
        #Download options
        if optionmenu_var.get() == "mp4":
            video.download()
        elif optionmenu_var.get() == "mp3":
            play()
            downloadedAudio = audio.download(filename="s.mp4")
            newfile = audio.title + ".mp3"
            subprocess.call([resource_path("./ffmpeg/ffmpeg.exe"), '-i', downloadedAudio, '-q:a', '0', '-map', 'a', newfile])
            os.remove(downloadedAudio)
            
        elif optionmenu_var.get() == "wav":
            play()
            downloadedAudio = audio.download(filename="s.mp4")
            newfile = audio.title + ".wav"
            subprocess.call([resource_path("./ffmpeg/ffmpeg.exe"), '-i', downloadedAudio, '-vn', '-acodec', 'pcm_s16le', '-ar', '44100', '-ac', '2', newfile])
            os.remove(downloadedAudio)
            
        finishLabel.configure(text="Downloaded", text_color="green")
    except:
        finishLabel.configure(text="Youtube link is invalid", text_color="red")

def optionmenu_callback(choice):
    print("optionmenu dropdown clicked:",choice)

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
    
def play():
   ffmpeg_path = "./ffmpeg/bin/ffmpeg.exe"
   if len(sys.argv) > 1:
      file_path = sys.argv[1]
      p = subprocess.Popen([resource_path(ffmpeg_path), file_path])
   else:
      print("No file passed as argument!")


#APP UI

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("green")

app = customtkinter.CTk()
app.geometry("720x300")
app.minsize(720,300)
app.title("Youtube Downloader")
app.iconbitmap(resource_path("favicon.ico"))

title = customtkinter.CTkLabel(app, text="Insert Youtube link",font=("Arial", 18))
title.pack(padx=10, pady=15)

url_var = tkinter.StringVar()
link = customtkinter.CTkEntry(app, width=350, height=46, textvariable=url_var)
link.pack()

optionmenu_var = customtkinter.StringVar(value="mp4")
optionmenu = customtkinter.CTkOptionMenu(app, values=["mp4", "mp3", "wav"], command=optionmenu_callback,variable=optionmenu_var)
optionmenu.pack(padx=10, pady=10)

finishLabel = customtkinter.CTkLabel(app, text="")
finishLabel.pack()

versionLabel = customtkinter.CTkLabel(app, text=version)
versionLabel.pack(side=tkinter.BOTTOM, anchor="w",padx="8")

pPercentage = customtkinter.CTkLabel(app, text="0%")
pPercentage.pack()

pBar = customtkinter.CTkProgressBar(app, width=400)
pBar.set(0)
pBar.pack(padx=10, pady=10)

download = customtkinter.CTkButton(app, text="Download", command=startDownload)
download.pack(side=tkinter.TOP, anchor="s")

app.mainloop()