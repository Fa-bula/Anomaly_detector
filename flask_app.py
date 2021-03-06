#!/usr/bin/python
from flask import Flask, render_template, request, redirect, url_for
from werkzeug import secure_filename
import os
from os import listdir
from os.path import isfile, join
import sys
import pandas
id = 0
UPLOAD_FOLDER = os.path.dirname(os.path.realpath(__file__)) + '/data/'
ALLOWED_EXTENSIONS = set(['txt', 'csv'])
DESC_FOLDER = os.path.dirname(os.path.realpath(__file__)) + '/static/txt/'

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
   # names = [u'1', u'2']
    #descriptions = [u'one', u'two']
    return render_template('home.html', descriptions=descriptions, names=names)


@app.route("/upload/", methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = os.path.join(app.config['UPLOAD_FOLDER'],  secure_filename(file.filename))
            method = request.form["method"]
            file.save(filename)
            df = pandas.io.parsers.read_csv(filename)
            arr = df.values
            if method == 'svm':
                return svm.svm(arr)
            if method == 'ellipticenvelope':
                return ellipticenvelope.ellipticenvelope(arr)
            if method == 'gaussianmixture':
                return gaussianmixture.gaussianmixture(arr)
            if method == 'kerneldensity':
                return kerneldensity.kerneldensity(arr)
            return 'unknown error'
        else:
            return "expected .csv or .txt"

@app.route("/about/")
def about():
    return render_template('about.html')

if __name__ == "__main__":
    sys.path.append('../AD/')
    import svm
    import ellipticenvelope
    import gaussianmixture
    import kerneldensity
    app.run(debug=True)
    
