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
	return render_template('tanakh.html', bible=common.Bible)

@app.route('/tanakh/<int:book_ind>/<int:chapter_no>')
def view_chapter(book_ind, chapter_no):
	book = common.Bible[book_ind - 1]
	data = open('../db/tanakh/%02d.%03d.txt'%(book_ind, chapter_no)).read()
	data = re.sub('{{[^}]+}} ', '', data)
	lines = data.split('\n')[:-1]
	chapter = common.Chapter(chapter_no)
	for l in range(1, len(lines) + 1):
		verse = common.Verse(l, lines[l - 1])
		chapter.verses.append(verse)
	return render_template('tanakh-chapter.html', chapter=chapter, book=book)

@app.route('/mishnah/')
def mishnah():
	return render_template('mishnah.html', mishnah=common.Mishnah)

@app.route('/mishnah/<int:order_no>/<int:tractate_no>')
def view_tractate(order_no, tractate_no):
	data = open('../db/mishnah/%1d.%02d.txt'%(order_no, tractate_no)).read()
	order = common.Mishnah[order_no - 1]
	tractate = order.books[tractate_no - 1]
	chapters = []
	parags = data.split('\n\n')
	for c in range(len(parags)):
		chapter = common.Chapter(c + 1)
		verses = parags[c].split('\n')
		for v in range(len(verses)):
			verse = common.Verse(v + 1, verses[v])
			chapter.verses.append(verse)
		chapters.append(chapter)
	return render_template('mishnah-tractate.html', chapters=chapters, order=order, tractate=tractate)

@app.route('/zohar/')
def zohar():
	return render_template('zohar.html', zohar=common.Zohar)

@app.route('/zohar/<int:book_ind>/<int:chapter_no>')
def view_zohar_chapter(book_ind, chapter_no):
	book = common.Zohar[book_ind - 1]
	data = open('../db/zohar/%1d.%02d.txt'%(book_ind, chapter_no)).read()
	chapter = book.chapters[chapter_no - 1]#common.Chapter(1)
	verses = data.split('\n')
	for x in range(len(verses)):
		verse = common.Verse(x + 1, verses[x])
		chapter.verses.append(verse)
	return render_template('zohar-chapter.html', chapter=chapter, book=book)
