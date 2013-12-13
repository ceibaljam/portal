#!/usr/bin/env python

from flask import Flask
from flask import render_template
import os
import json

NEWS = "noticias"
app = Flask(__name__)


@app.route('/')
def index():
    return "<a href='noticias'>Ver noticias</a>"


def _getnoticia(n):
    path = os.path.join(NEWS, n)
    if os.path.exists(path):
        try:
            return json.load(open(path))
        except ValueError:
            return None

@app.route('/noticias')
def noticias():            
    _noticias = []
    for x in os.listdir(NEWS):
        noticia_d = _getnoticia(x)
        if noticia_d:
            _noticias.append(noticia_d)
    print _noticias
 
    return render_template("noticias.html", noticias=_noticias)


@app.route('/noticias/<noticia>')
def noticias_(noticia=None):
    if noticia:
        noticia_d = _getnoticia('%s.json' % noticia)
        if noticia_d:
            return render_template('noticia.html', noticia=noticia_d)
        else:
            return render_template('noticia404.html', noticia=noticia)
        

if __name__ == "__main__":
    app.debug = True
    app.run()
