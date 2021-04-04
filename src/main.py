from flask import Flask, render_template, request,redirect, flash, url_for
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
from graphviz import Graph
import math
import platform
import os
import base64
os.environ["PATH"] += os.pathsep + 'C:/Program Files/Graphviz/bin'
import read as r

app = Flask(__name__)

app.secret_key = 'bantalguling'

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/manual.html")
def manual():
    return render_template('manual.html')

platform_name = platform.system()
if(platform_name == "Windows"):
    app.config["Upload_Files"] = '..\\test\\'
else:
    app.config["Upload_Files"] = "../test"

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
                files.save(os.path.join(app.config["Upload_Files"], filename))
                flash("Upload berhasil")
                
                # proses file
                directory = os.path.join(app.config["Upload_Files"], filename)
                g = r.readFile(directory)
                
                chart_data = Graph(strict=True, engine="neato",format='png')
                
                # menambahkan simpul
                for i in range(g.getNSimpul()):
                    x = str(g.getKoor()[i][0]*1000)
                    y = str(g.getKoor()[i][1]*1000)
                    koornya = x+','+y+'!'
                    chart_data.node(g.getDict()[i], pos=koornya, shape='circle')

                # menambahkan sisi
                for i in range(g.getNSimpul()):
                    temp = g.getGraf()[i]
                    for j in range(len(temp)):
                        src = g.getDict()[i]
                        dest = g.getDict()[temp[j][0]]
                        weighted = temp[j][1]
                        chart_data.edge(src, dest, label = str(weighted))
                chart_data.render()

                chart_output = chart_data.pipe(format='png')
                chart_output = base64.b64encode(chart_output).decode('utf-8')

                return render_template('manual.html', chart_output=chart_output)
    

if __name__ == '__main__':
    app.run(debug=True)