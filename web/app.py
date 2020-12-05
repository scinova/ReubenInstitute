import sys
sys.path.append('..')

from flask import Flask
from flask import render_template, send_from_directory, request, redirect

import common
import hebrew_numbers
import re
import unicodedata

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
	data = open('../db/onkelos/%1d.%02d.txt'%(book_ind, chapter_no)).read()
	lines = data.split('\n')[:-1]
	onkelos = common.Chapter(chapter_no)
	for l in range(1, len(lines) + 1):
		verse = common.Verse(l, lines[l - 1])
		onkelos.verses.append(verse)
	return render_template('tanakh-chapter.html', chapter=chapter, onkelos=onkelos, book=book, re=re)

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

@app.route('/zohar-articles')
def zohar_articles():
	articles = {}
	for i in ['1.01', '3.28']:
		data = open('../db/zohar/%s/00.txt'%i).read().split('\n')
		articles[i] = data
	return render_template('zohar-articles.html', articles=articles)

@app.route('/zohar/<int:book_ind>/<int:chapter_no>/<int:article_no>')
def view_zohar_article(book_ind, chapter_no, article_no):
	book = common.Zohar[book_ind - 1]
	chapter = book.chapters[chapter_no - 1]
	t = open('../db/zohar/%1d.%02d/%02d.txt'%(book_ind, chapter_no, article_no)).read()
	t = re.sub('"([^"]+)"', '“\\1”', t)
	t = re.sub("'([^']+)'", '‘\\1’', t)
	ar_texts = t.split('\n\n\n')
	t = open('../db/zohar/%1d.%02d/%02dt.txt'%(book_ind, chapter_no, article_no)).read()
	t = re.sub('"([^"]+)"', '“\\1”', t)
	t = re.sub("'([^']+)'", '‘\\1’', t)
	he_texts = t.split('\n\n\n')
	return render_template('zohar-article.html', ar_texts=ar_texts, he_texts=he_texts, re=re,
		book=book, chapter=chapter, article_no=article_no)

@app.route('/zohar/<int:book_ind>/<int:chapter_no>/<int:article_no>/edit/<int:paragraph_no>', methods=['GET','POST'])
def edit_zohar_paragraph(book_ind, chapter_no, article_no, paragraph_no):
	book = common.Zohar[book_ind - 1]
	chapter = book.chapters[chapter_no - 1]
	ar_texts = open('../db/zohar/%1d.%02d/%02d.txt'%(book_ind, chapter_no, article_no)).read().split('\n\n\n')
	he_texts = open('../db/zohar/%1d.%02d/%02dt.txt'%(book_ind, chapter_no, article_no)).read().split('\n\n\n')
	if request.method == 'POST':
		ar_texts[paragraph_no - 1] = request.form['ar_text'].replace('\r\n', '\n')
		he_texts[paragraph_no - 1] = request.form['he_text'].replace('\r\n', '\n')
		ar_text = '\n\n\n'.join(ar_texts)
		t = ''
		for i in range(len(ar_text)):
			t += unicodedata.normalize('NFD', ar_text[i])
		ar_text = t
		he_text = '\n\n\n'.join(he_texts)
		t = ''
		for i in range(len(he_text)):
			t += unicodedata.normalize('NFD', he_text[i])
		he_text = t
		f = '../db/zohar/%1d.%02d/%02d.txt'%(book_ind, chapter_no, article_no)
		open(f, 'w').write(ar_text)
		f = '../db/zohar/%1d.%02d/%02dt.txt'%(book_ind, chapter_no, article_no)
		open(f, 'w').write(he_text)
		return redirect('/zohar/%d/%d/%d#v%d'%(book_ind, chapter_no, article_no, paragraph_no))
	if request.method == 'GET':
		ar_text = ar_texts[paragraph_no - 1]
		he_text = he_texts[paragraph_no - 1]
		return render_template('zohar-edit-paragraph.html', ar_text=ar_text, he_text=he_text, re=re,
				book=book, chapter=chapter, article_no=article_no, paragraph_no=paragraph_no)

@app.route('/zohar/<int:book_ind>/<int:chapter_no>')
def view_zohar_chapter(book_ind, chapter_no):
	book = common.Zohar[book_ind - 1]
	data = open('../db/zohar/%1d.%02d.txt'%(book_ind, chapter_no)).read()
	chapter = book.chapters[chapter_no - 1]
	verses = data.split('\n')
	for x in range(len(verses)):
		verse = common.Verse(x + 1, verses[x])
		chapter.verses.append(verse)
	return render_template('zohar-chapter.html', chapter=chapter, book=book)

def remove_cantillation(text):
	return re.sub('[\u0591-\u05af\u05bd]', '', text)

def remove_punctuation(text):
	return re.sub('[\u05b0-\u05bc\u05c1\u05c2\u05c7]', '', text)

@app.route('/devel/')
def devel():
	data = ''
	for b in range(len(common.Zohar)):
		book = common.Zohar[b]
		for c in range(len(book.chapters)):
			chapter = book.chapters[c]
			src = '../db/zohar/%1d.%02d.txt'%(b + 1, c + 1)
			data += open(src).read()
			print (src)
	data = re.sub('\n', ' ', data)
	data = re.sub('[\(\),\.\:]', ' ', data)
	data = remove_cantillation(data)
	words = data.split(' ')
	words = list(set(words))

	words = [w.replace("''", '״') if w.startswith("''") else w for w in words]
	names = [hebrew_numbers.int_to_gematria(x, gershayim=False) for x in range(1, 800)]
	#print ('------', names)
	names = [''.join(sorted(list(n), reverse=True)) for n in names]
	#print ('------', names)

	numbers = []
	for p in ['', 'ב', 'ו', 'וב', 'ד', 'ל', 'מ']:
		for n in names:
			numbers.append(p + n)
#	print (numbers)
	words = [w.replace("''", '״') if remove_punctuation(w).replace("''", '') in numbers else w for w in words]

	names = ['אלף', 'בית', 'גימל', 'דלת', 'הא', 'ויו', 'ואו', 'זין', 'חית', 'טית', 'יוד', 'כף',
			 'למד', 'מם', 'נון', 'סמך', 'פא', 'עין', 'צדי', 'קוף','ריש', 'שין', 'תיו']
	letters = []
	for p in ['', 'ב', 'ו', 'וב', 'ד', 'ל', 'מ']:
		for n in names:
			letters.append(p + n)
#	print (letters)
	words = [w.replace("''", "״") if remove_punctuation(w).replace("''", "") in letters else w for w in words]

	words = [w.replace("''", '') for w in words]
	words = [w for w in words if "'" in w]
#	print (numbers)
	words.sort(key=remove_punctuation)
	return render_template('devel.html', words = words)
