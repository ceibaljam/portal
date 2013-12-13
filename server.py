#!/usr/bin/env python

from flask import Flask
from flask import render_template
import os

NEWS = "noticias"
app = Flask(__name__)


@app.route('/')
def index():
    return "<a href='noticias'>Ver noticias</a>"


@app.route('/noticias')
def noticias():
    _noticias = []
    
    for x in os.listdir(NEWS):
        try:
            n_json = json.load(open(path))
            _noticias.append(n_json)
        except ValueError:
            pass
     
    return render_template("noticias.html", n_json)


@app.route('/noticias/<x>')
def noticias(noticia):
    path = os.path.join(NEWS, x)
    if os.path.exists(path):
        try:
            dic = json.load(open(path))
            return render_template('noticia.html', dic)
        except ValueError:
            return render_template('noticia404.html', x)
    else:
        return render_template('noticia404.html', x)
        

if __name__ == "__main__":
    app.debug = True
    app.run()
