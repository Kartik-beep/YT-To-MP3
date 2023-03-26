import os
os.system('pip install tkinter moviepy pytube')
from pytube import YouTube
import urllib.request
import re
from moviepy.editor import *
import tkinter as tk
from tkinter import *
from tkinter.filedialog import askopenfilename
def MP4ToMP3(mp4, mp3):
    FILETOCONVERT = AudioFileClip(mp4)
    FILETOCONVERT.write_audiofile(mp3)
    FILETOCONVERT.close()
def remove_line():
    with open('songs.txt', 'r') as fr:
        lines = fr.readlines()
        ptr = 0
        with open('songs.txt', 'w') as fw:
            for line in lines:
                if ptr != 0:
                    fw.write(line)
                ptr += 1
def check_link(link):
    a = list(link)
    if a[0] == 'h' and a[1] == 't' and a[2] == 't' and a[3] == 'p' and a[4] == 's':
        return True
    else:
        return False
def Download_Song():
    Name = song_name_entry.get()
    destination = path
    song_name = Name
    for k in song_name.split("\n"):
        song_artist = k
        if check_link(song_artist) == True:
            yt_link = song_artist
        else:
            song_line = re.sub(r"[^a-zA-Z0-9]+", ' ', k)
            if ' ' in song_line:
                song_artist = song_line.replace(' ', '+')
            else:
                song_artist = song_line
            search_keyword = (song_artist + '+lyrics+audio')
            html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + search_keyword)
            video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
            yt_link = ("https://www.youtube.com/watch?v=" + video_ids[0])
        yt = YouTube(str(yt_link))
        video = yt.streams.filter(only_audio=True).first()
        out_file = video.download(output_path=destination)
        base, ext = os.path.splitext(out_file)
        new_file = base + '.mp4'
        os.rename(out_file, new_file)
        MP4ToMP3(new_file, base + '.mp3')
        os.remove(new_file)
def Download_File(filename, folder_path):
    destination = folder_path
    song_file = open(filename, 'r')
    read_lines = song_file.readlines()
    count = 0
    for line in read_lines:
        count += 1
        try:
            song_formatted = ("{}".format(line.strip())).split("\n")
            for k in song_formatted:
                song = k
                if check_link(song) == True:
                    yt_link = song
                else:
                    song_line = re.sub(r"[^a-zA-Z0-9]+", ' ', k)
                    song = song_line.replace(' ', '+')
                    search_keyword = (song + '+lyrics+audio')
                    html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + search_keyword)
                    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
                    yt_link = ("https://www.youtube.com/watch?v=" + video_ids[0])
                yt = YouTube(str(yt_link))
                video = yt.streams.filter(only_audio=True).first()
                out_file = video.download(output_path=destination)
                base, ext = os.path.splitext(out_file)
                new_file = base + '.mp4'
                os.rename(out_file, new_file)
                MP4ToMP3(new_file, base + '.mp3')
                os.remove(new_file)
                try:
                    remove_line()
                except:
                    print(f"Couldn't remove {k}")		
        except Exception as e:
            pass
    song_file.close()
def upload_file():
    global file
    file = tk.filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    text_file.delete(1.0, tk.END)
    text_file.insert(tk.END, file)
    with open(file, 'r') as filer:
        contents = filer.read()
        text_content.delete(1.0, tk.END)
        text_content.insert(tk.END, contents)
def dd():
    Download_File(file, path)
def ask_directory():
    global path
    path = tk.filedialog.askdirectory(title = "Select Folder")
    text.delete(1.0, tk.END)
    text.insert(tk.END, path)
window = tk.Tk()
window.title("YT TO MP3")
frame = tk.Frame(window)
frame.pack()
download_location_frame = tk.LabelFrame(frame, text='Download Location')
download_location_frame.grid(row=0, column=0)
file_name = tk.Label(download_location_frame, text='Folder Location:')
file_name.grid(row=0, column=0)
text = tk.Text(download_location_frame, height=1, width=50)
text.grid(row=0, column=2)
enter_ss = tk.Button(download_location_frame, text='Select', command=ask_directory)
enter_ss.grid(row=1, column=2)
song_name_frame = tk.LabelFrame(frame, text="Download Individual Song")
song_name_frame.grid(row= 1,column= 0, padx=20, pady=20)
song_name = tk.Label(song_name_frame, text='Song Name:')
song_name.grid(row=0, column=0)
song_name_entry = tk.Entry(song_name_frame)
song_name_entry.grid(row=0, column=1)
enter_ss = tk.Button(song_name_frame, text='Submit', command=Download_Song)
enter_ss.grid(row=0, column=3)
file_name_frame = tk.LabelFrame(frame, text="Download File")
file_name_frame.grid(row= 2,column= 0, padx=20, pady=20)
file_name = tk.Label(file_name_frame, text='File Name:')
file_name.grid(row=0, column=0, padx=20, pady=20)
text_file = tk.Text(file_name_frame, height=1, width=50)
text_file.grid(row=0, column=1)
enter_ss = tk.Button(file_name_frame, text='Upload', command=upload_file)
enter_ss.grid(row=0, column=4)
text_content = tk.Text(file_name_frame, height=10, width=50)
text_content.grid(row=2, column=1)
submit_ss = tk.Button(file_name_frame, text='Submit', command=dd)
submit_ss.grid(row=3, column=1)
window.mainloop()