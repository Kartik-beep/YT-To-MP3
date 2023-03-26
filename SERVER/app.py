import os
os.system('pip install flask pytube moviepy Werkzeug')
from flask import Flask, request, redirect, url_for, render_template, send_from_directory
from werkzeug.utils import secure_filename
import glob
from pytube import YouTube
import urllib.request
import re
import shutil
from moviepy.editor import *

html = '''<!doctype html>
    <title>YT To MP3</title>
    <h1>Upload new File</h1>
    <form action="" method=POST enctype=multipart/form-data>
      <p>
        <input type="text" name="name">
        <input type=submit value=Upload>
        <input type=file name=file>
        </p>
    </form>
</html>'''

ab_path = os.path.dirname(os.path.abspath(__file__)).replace("'", '')

try:
    open(f'{ab_path}\\error.txt', 'w+')
    os.mkdir(f'{ab_path}\\Songs')
    open(f'{ab_path}\\songs.txt', 'w+')
    open(f'{ab_path}\\error_file.txt', 'w+')
    os.mkdir(f'{ab_path}\\Uploads')
    os.mkdir(f'{ab_path}\\Template')
    open('./Template/index.html', 'w+')
    open('./Template/index.html', 'w').write(html)
except:
    pass

if os.path.exists('songs.zip'):
    os.remove('./songs.zip')
else:
    pass
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

def Download_Song(Name):
    destination = 'Songs'
    if os.path.exists('Songs'):
        shutil.rmtree('./Songs/')
    else:
        pass
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

def Download_File(filename):
    destination = 'downloads'
    song_file = open(filename, 'r')
    read_lines = song_file.readlines()
    count = 0
    for line in read_lines:
        count += 1
        try:
            song_formatted = ("{}".format(line.strip()))
            for k in song_formatted.split("\n"):
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
            print(e)
            error_file = open('error.txt', 'a')
            error = '{}: {} '.format(count, k)
            error_file.write(f'{error} \n')
    song_file.close()
    shutil.make_archive('songs', 'zip', './downloads/')
    shutil.rmtree('./downloads/')
    os.remove(filename)

DOWNLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__)) + '/Songs/'
UPLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__)) + '/Uploads/'
ZIP_FOLDER = os.path.dirname(os.path.abspath(__file__))
ALLOWED_EXTENSIONS = {'txt'}

app = Flask(__name__,template_folder='./Template' , static_url_path="/static")
DIR_PATH = os.path.dirname(os.path.realpath(__file__))
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER
app.config['ZIP_FOLDER'] = ZIP_FOLDER
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        song = request.form['name']
        file = request.files['file']
        if request.form['name'].isspace() == False and song != '':
            Download_Song(song)
            list_of_files = glob.glob('./Songs/*.mp3')
            latest_file = max(list_of_files, key=os.path.getctime)
            list_of_files = glob.glob('./Songs/*.mp3')
            latest_file = max(list_of_files, key=os.path.getctime)
            file = latest_file.replace(r"./Songs", '')
            filename = file.replace('\\', '')
            return redirect(url_for('req_file', filename=filename))
        if 'file' and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            Download_File('./Uploads/'+filename)
            return redirect(url_for('req_zip', filename='songs.zip'))
            # return render_template('index.html')
        if song.isspace() == True or song == '':
            pass
    return render_template('index.html')

@app.route('/downloads/<filename>')
def req_file(filename):
    return send_from_directory(app.config['DOWNLOAD_FOLDER'], filename, as_attachment=True)

@app.route('/zips/<filename>')
def req_zip(filename):
    return send_from_directory(app.config['ZIP_FOLDER'], filename, as_attachment=True)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
