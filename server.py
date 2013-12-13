#!/usr/bin/env python

# Copyright (C) 2013 CeibalJAM

from flask import Flask
from flask import render_template
import os
import json

NEWS = "noticias"
TAGS_CACHE = {}

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


def _getnoticias():
    _noticias = []
    for x in os.listdir(NEWS):
        if x.endswith(".json"):
            noticia_d = _getnoticia(x)
            noticia_d['name'] = x[:-5]
            if noticia_d:
                _noticias.append(noticia_d)
        
    return _noticias


def _gen_tags_cache_for_tag(tag):
    cache = []
    for noticia in _getnoticias():
        if tag in noticia['tags']:
            del noticia['content']
            del noticia['tags']
            cache.append(noticia)
    return cache


def _gen_tags_cache():
    for noticia in _getnoticias():
        for tag in noticia['tags']:
            if not tag in TAGS_CACHE:
                TAGS_CACHE[tag] = []
            TAGS_CACHE[tag].append({'name': noticia['name'],
                                    'title': noticia['title'],
                                    'desc': noticia['desc']})
            print TAGS_CACHE[tag]
            

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

            
@app.route('/noticias/tags/')
def tags():
    _gen_tags_cache()
    return render_template("tags.html", tags=TAGS_CACHE.keys())
    

@app.route('/noticias/tags/<_tag>')
def tags_(_tag):
    if not _tag in TAGS_CACHE:
        cache = _gen_tags_cache_for_tag(_tag)
        if cache != []:
            TAGS_CACHE[_tag] = cache
            
    if _tag in TAGS_CACHE and TAGS_CACHE[_tag] != []:
        return render_template('tag.html', tag=_tag, noticias=TAGS_CACHE[_tag])
        
    else:
        return render_template('tag404.html', tag=_tag)



if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0")
