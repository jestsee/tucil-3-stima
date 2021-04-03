#import read as r
from flask import Flask, render_template, request,redirect, flash, url_for
import os
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
import math
import networkx as nx
import matplotlib.pyplot as plt

app = Flask(__name__)

app.secret_key = 'bantalguling'

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/manual.html")
def manual():
    return render_template('manual.html')

app.config["allowed_file_ext"] = ["txt"]

def onlyfile(filename):
    exten = filename.rsplit(".",1)[1]
    return  '.' in filename and exten.lower() in app.config["allowed_file_ext"]

@app.route("/manual.html", methods=['POST'])
def result():
    if request.files:
        files = request.files["files"]

        if request.files['files'].filename == '':
            flash("File kosong", "error")
            return redirect(request.url)
        else:
            if not(onlyfile(files.filename)):
                flash("File harus dalam bentuk text")
                return redirect(request.url)
            else :
                filename = secure_filename(files.filename)
                # proses file
                

if __name__ == '__main__':
    app.run(debug=True)