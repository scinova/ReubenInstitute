import sys
sys.path.append('..')

from flask import Flask
from flask import render_template, send_from_directory

import common
import hebrew_numbers
import re

numbers = [hebrew_numbers.int_to_gematria(x) for x in range(0, 151)]

app = Flask(__name__)

@app.route('/@@/<path:filename>')
def files(filename):
    return send_from_directory('static', filename)

@app.route('/@@/fonts/<path:filename>')
def fonts(filename):
    return send_from_directory('../fonts', filename)

@app.route('/')
def main():
	return render_template('index.html')

@app.route('/tanakh/')
def tanakh():
	return render_template('tanakh.html', books=common.books, numbers=numbers)

@app.route('/tanakh/<int:book>/<int:chapter>')
def view_chapter(book, chapter):
	data = open('../db/tanakh/%02d.%03d.txt'%(book, chapter)).read()
	return render_template('tanakh-chapter.html', data=data, re=re)

@app.route('/mishnah/')
def mishnah():
	return render_template('mishnah.html', orders=common.mishnah)
