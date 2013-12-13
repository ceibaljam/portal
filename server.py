#!/usr/bin/env python

from flask import Flask
from flask import render_template
import os

NEWS = "noticias"
app = Flask(__name__)


@app.route('/')
def index():
    return "<a href='noticias'>Ver noticias</a>"


def _getnoticia(n):
    path = os.path.join(NEWS, n + ".json")
    if os.path.exists(path):
        try:
            return json.load(open(path))
        except ValueError:
            return None
            

@app.route('/noticias/<x>')
def noticias(noticia=None):
    
    if noticia:
        noticia_d = _getnoticia()
        if noticia_d:
            return render_template('noticia.html', dic)
        else:
            return render_template('noticia404.html', x)
    else:
        for x in os.listdir(NEWS):
            noticia_d = _getnoticia()
            if noticia_d:
                _noticias.append(noticia_d)
     
        return render_template("noticias.html", n_json)
        

if __name__ == "__main__":
    app.debug = True
    app.run()
