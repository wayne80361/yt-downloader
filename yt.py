import tkinter
import customtkinter
from pytube import YouTube
from moviepy.editor import *

def startDownload(): 
    try: 
        ytLink = link.get()
        ytObject = YouTube(ytLink, on_progress_callback=on_progress)
        video_stream = ytObject.streams.filter(file_extension='mp4', only_video=True, resolution='2160p').first()
        if not video_stream:
            video_stream = ytObject.streams.filter(file_extension='mp4', only_video=True, resolution='1440p').first()
        if not video_stream:
            video_stream = ytObject.streams.filter(file_extension='mp4', only_video=True, resolution='1080p').first()
        if not video_stream:
            video_stream = ytObject.streams.filter(file_extension='mp4', only_video=True, resolution='720p').first()
        audio = ytObject.streams.get_by_itag(140)
        title.configure(text=ytObject.title, text_color="black")
        finishLabel.configure(text="")
        video_stream.download(filename="video.mp4")
        audio.download(filename="audio.mp4")
        finishLabel.configure(text="Download Completed")
    except:
        finishLabel.configure(text="Invalid Link", text_color="red")

def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    byte_downloaded = total_size - bytes_remaining
    percentage_of_compeletion = byte_downloaded / total_size * 100
    per = str(int(percentage_of_compeletion))
    progress.configure(text=per + '%')
    progress.update()

    # update progress bar
    progressBar.set(float(percentage_of_compeletion) / 100)

def combineVideoAudio():
    try:
        # combine the video clip with the audio clip
        video_clip = VideoFileClip("video.mp4")
        audio_clip = AudioFileClip("audio.mp4")
        final_clip = video_clip.set_audio(audio_clip)
        final_clip.write_videofile("combined" + ".mp4")
        finishCombineLabel.configure(text="Combining Completed", text_color="red")
    except:
        finishCombineLabel.configure(text="Error Combining Clips", text_color="red")

# Basic GUI
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

# App frame
app = customtkinter.CTk()
app.geometry("720x480")
app.title("Youtube Downloader")

# Adding UI elements
title = customtkinter.CTkLabel(app, text="Insert a youtube link")
title.pack(padx=10, pady=10)

# Link input
url_var = tkinter.StringVar()
link = customtkinter.CTkEntry(app, width=350, height=40, textvariable=url_var)
link.pack()

# Finished Downloading
finishLabel = customtkinter.CTkLabel(app, text="")
finishLabel.pack()

# Progress percentage
progress = customtkinter.CTkLabel(app, text="0%")
progress.pack()

progressBar = customtkinter.CTkProgressBar(app, width=400)
progressBar.set(0)
progressBar.pack(padx=10, pady=10)

# Download Button
download = customtkinter.CTkButton(app, text="Download", command=startDownload)
download.pack(padx=10, pady=10)

# Combine Button
combine = customtkinter.CTkButton(app, text="Combine", command=combineVideoAudio)
combine.pack(padx=10, pady=10)

# Finished Combining
finishCombineLabel = customtkinter.CTkLabel(app, text="")
finishCombineLabel.pack()

# Run App
app.mainloop()