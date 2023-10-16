from flask import Flask, render_template, request, Response, redirect
from pymongo import MongoClient
from gridfs import GridFS
from werkzeug.utils import secure_filename
from bson import ObjectId

app = Flask(__name__)
client = MongoClient('mongodb://localhost:27017/')
db = client['AudioHub']
fs = GridFS(db, collection='Music.files')
app.static_folder = 'static'

# @app.route('/')
# def main():
#     return render_template('main.html')


@app.route('/app')
def app_page():
    return render_template('index.html')

@app.route('/main')
def main_page():
    return render_template('main.html')

@app.route('/')
def index():
    audio_files = list(fs.find())
    return render_template('index.html', audio_files=audio_files)

@app.route('/upload', methods=['POST'])
def upload_audio():
    audio_file = request.files['audio']
    if audio_file:
        filename = secure_filename(audio_file.filename)
        audio_id = fs.put(audio_file, filename=filename)
        return redirect('/')
    else:
        return "Nie wybrano pliku muzycznego."

@app.route('/play/<file_id>')
def play_audio(file_id):
    audio_file = fs.get(ObjectId(file_id))
    response = Response(audio_file.read(), content_type='audio/mpeg')
    return response

if __name__ == '__main__':
    app.run(debug=True)
