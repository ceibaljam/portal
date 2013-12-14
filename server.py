#!/usr/bin/env python

# Copyright (C) 2013 CeibalJAM

from flask import Flask
from flask import render_template
import os
import json

NEWS = "noticias"
images = "static/covers"
TAGS_CACHE = {}

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', images=os.listdir(images))


def _getnoticia(n):
    path = os.path.join(NEWS, n)
    if os.path.exists(path):
        try:
            return json.load(open(path))
        except ValueError:
            return None


def _getnoticias():
    _noticias = []
    for x in os.listdir(NEWS):
        if x.endswith(".json"):
            noticia_d = _getnoticia(x)
            noticia_d['name'] = x[:-5]
            if noticia_d:
                _noticias.append(noticia_d)
        
    return _noticias


@app.route('/noticias/')
def noticias():            
    return render_template("noticias.html", noticias=_getnoticias())
        

@app.route('/noticias/<noticia>')
def noticias_(noticia=None):
    if noticia:
        noticia_d = _getnoticia('%s.json' % noticia)
        if noticia_d:
            return render_template('noticia.html', noticia=noticia_d)
        else:
            return render_template('noticia404.html', noticia=noticia)
            

@app.route('/noticias/tags/<_tag>')
def tags(_tag):
    if not _tag in TAGS_CACHE:
        TAGS_CACHE[_tag] = []
        for noticia in _getnoticias():
            if _tag in noticia['tags']:
                del noticia['content']
                del noticia['tags']
                TAGS_CACHE[_tag].append(noticia)

    if _tag in TAGS_CACHE and TAGS_CACHE[_tag] != []:
        return render_template('tag.html', tag=_tag, noticias=TAGS_CACHE[_tag])
    else:
        return render_template('tag404.html', tag=_tag)


if __name__ == "__main__":
    app.debug = True
    app.run()
