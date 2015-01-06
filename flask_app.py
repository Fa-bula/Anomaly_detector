from flask import Flask, render_template, request, redirect, url_for
from werkzeug import secure_filename
import os
from os import listdir
from os.path import isfile, join

id = 0
UPLOAD_FOLDER = '/home/anomaly/Anomaly_detection/data/'
ALLOWED_EXTENSIONS = set(['txt', 'csv'])
DESC_FOLDER = '/home/anomaly/Anomaly_detection/static/txt/'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route("/")
def home():
    onlyfiles = [ f for f in listdir(DESC_FOLDER) if isfile(join(DESC_FOLDER, f)) ]
    descriptions = []
    names = []
    for file in onlyfiles:
        with open(join(DESC_FOLDER, file), 'r') as f:
            descriptions.append(f.read())
        names.append(file)
    return render_template('home.html', descriptions=descriptions, names=names)


@app.route("/upload/", methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('home'))
        else:
            return "expected .csv or .txt"

@app.route("/about/")
def about():
    return render_template('about.html')
if __name__ == "__main__":
    app.run(debug=True)