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
	print (chapter.hname)
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
#	if request.method == 'GET':
	if True:
		translate = request.args.get('t') == '1'
		data = open('dictionary.txt').read().split('\n')[:-1]
		dictionary = {}
		for line in data:
			words = line.split(' ')
			print (line, len(words))
			key = words[0]
			trs = words[1:len(words)]
			dictionary[key] = trs
			print (key, trs, len(words))
	#	print (dictionary)
		ar_text = ar_texts[paragraph_no - 1]
		he_text = he_texts[paragraph_no - 1]
		if not he_text:
			he_text = ar_text
			for key in dictionary:
				#print (key, dictionary[key])
				he_text = re.sub(' ' + key + '(?!=[\u0591-\u05bd\u05bf-\u05c7א-ת])', ' ' + dictionary[key][0], he_text)
		return render_template('zohar-edit-paragraph.html', ar_text=ar_text, he_text=he_text, re=re,
				book=book, chapter=chapter, article_no=article_no, paragraph_no=paragraph_no)

@app.route('/zohar/<int:book_ind>/<int:chapter_no>')
def view_zohar_chapter(book_ind, chapter_no):
	book = common.Zohar[book_ind - 1]
	chapter = book.chapters[chapter_no - 1]
	print (chapter.articles)
	if not len(chapter.articles):
		print ("no artices")
		data = open('../db/zohar/%1d.%02d.txt'%(book_ind, chapter_no)).read()
		verses = data.split('\n')
		for x in range(len(verses)):
			verse = common.Verse(x + 1, verses[x])
			chapter.verses.append(verse)
	return render_template('zohar-chapter.html', chapter=chapter, book=book)

def remove_cantillation(text):
	return re.sub('[\u0591-\u05af\u05bd]', '', text)

def remove_punctuation(text):
	return re.sub('[\u05b0-\u05bc\u05c1\u05c2\u05c7]', '', text)

def remove_diacritics(text):
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

@app.route('/dev/')
@app.route('/dev/<string:letter>/')
def dev(letter=None):
	chars = []
	ar_words = []
	he_words = []
	ar_links = {}
	he_links = {}
	ar_sentences = {}
	he_sentences = {}
	mispunctuations = []
	misparagraphs = []
	for book in common.Zohar:
		ar_sentences[book.ind] = {}
		he_sentences[book.ind] = {}
		for chapter in book.chapters:
			ar_sentences[book.ind][chapter.no] = {}
			he_sentences[book.ind][chapter.no] = {}
			for article in chapter.articles:
				ar_sentences[book.ind][chapter.no][article.no] = {}
				he_sentences[book.ind][chapter.no][article.no] = {}
				ar_data = open('../db/zohar/%1d.%02d/%02d.txt'%(book.ind, chapter.no, article.no)).read()
				he_data = open('../db/zohar/%1d.%02d/%02dt.txt'%(book.ind, chapter.no, article.no)).read()
				ar_paragraphs = ar_data.split('\n\n\n')
				he_paragraphs = he_data.split('\n\n\n')
				if len(ar_paragraphs) != len(he_paragraphs):
					misparagraphs.append({
							'book':book,
							'chapter': chapter,
							'article': article})
				for p in range(len(ar_paragraphs)):
					# AR PARAGRAPHS
					t = ar_paragraphs[p]
					#####
					t = re.sub('[\u2018\u2019]', "'", t)
					t = re.sub('[\u201c\u201d]', '"', t)
					#####
					for b in common.Bible:
						t = re.sub('\(' + b.hname.replace('\u05f3', '') + '[^\)]+\)', '', t)
					t = re.sub('{[^}]+}', '', t)
					t = re.sub('"[^"]+"', '', t)
					t = re.sub('[~\'\=\u2022\u2026\u2013\(\)]', '', t)
					ar_text = t
					# HE PARAGRAPHS
					try:
						t = he_paragraphs[p]
					except IndexError:
						t = 'AAA'
					#####
					t = re.sub('[\u2018\u2019]', "'", t)
					t = re.sub('[\u201c\u201d]', '"', t)
					#####
					for b in common.Bible:
						t = re.sub('\(' + b.hname.replace('\u05f3', '') + '[^\)]+\)', '', t)
					t = re.sub('{[^}]+}', '', t)
					t = re.sub('"[^"]+"', '', t)
					t = re.sub('[~\'\=\u2022\u2026\u2013\(\)]', '', t)
					he_text = t
					# MISPUNCTUATIONS
					x = ''
					y = ''
					for c in range(len(ar_text)):
						if ar_text[c] in ',.:;!?-\n':
							x += ar_text[c].replace('\n', 'ח')
					for c in range(len(he_text)):
						if he_text[c] in ',.:;!?-\n':
							y += he_text[c].replace('\n', 'ח')
					if x != y:
						mispunctuations.append({
								'book_ind':book.ind,
								'chapter_no': chapter.no,
								'article_no': article.no,
								'paragraph_no': p + 1,
								'x': x,
								'y': y,
								'article': article
								})
					# AR SENTENCES
					t = ar_text
					t = re.sub('[\s]+', ' ', t)
					t = re.sub(',', '', t)
					t = re.sub('\?\!', 'X', t)
					t = re.sub('[\?\.\!\;\:]', 'X', t)
					ar_sentences[book.ind][chapter.no][article.no][p] = t.split('X')
					# HE SENTENCES
					t = he_text
					t = re.sub('[\s]+', ' ', t)
					t = re.sub(',', '', t)
					t = re.sub('\?\!', 'X', t)
					t = re.sub('[\?\.\!\;\:]', 'X', t)
					he_sentences[book.ind][chapter.no][article.no][p] = t.split('X')

	for book in common.Zohar:
		for chapter in book.chapters:
			for article in chapter.articles:
				for p in range(len(ar_sentences[book.ind][chapter.no][article.no])):
					#print (book.ind, chapter.no, article.no, p, sentences[3].keys())
					for s in range(len(ar_sentences[book.ind][chapter.no][article.no][p])):
						sentence = ar_sentences[book.ind][chapter.no][article.no][p][s]
						for c in sentence:
							if c not in chars:
								chars.append(c)
						words = sentence.split(' ')
						for word in words:
							if not len(word):
								continue
							if letter and not word.startswith(letter):
								continue
							if word not in ar_words:
								ar_words.append(word)
								ar_links[word] = []
							ar_links[word].append([book.ind, chapter.no, article.no, p + 1])
				for p in range(len(he_sentences[book.ind][chapter.no][article.no])):
					#print (book.ind, chapter.no, article.no, p, sentences[3].keys())
					for s in range(len(he_sentences[book.ind][chapter.no][article.no][p])):
						sentence = he_sentences[book.ind][chapter.no][article.no][p][s]
						for c in sentence:
							if c not in chars:
								chars.append(c)
						words = sentence.split(' ')
						for word in words:
							if not len(word):
								continue
							if letter and not word.startswith(letter):
								continue
							if word not in he_words:
								he_words.append(word)
								he_links[word] = []
							he_links[word].append([book.ind, chapter.no, article.no, p + 1])
	ar_words.sort(key=lambda word: remove_diacritics(remove_cantillation(word)))
	he_words.sort(key=lambda word: remove_diacritics(remove_cantillation(word)))

	ar_cleans = {}
	for word in ar_words:
		c = remove_diacritics(remove_cantillation(word))
		if c not in ar_cleans:
			ar_cleans[c] = []
		if word not in ar_cleans[c]:
			ar_cleans[c].append(word)
	for word in [k for k in ar_cleans.keys()]:
		if word in ar_cleans[word] and len(ar_cleans[word]) == 2:
			pass
		else:
			del ar_cleans[word]
	he_cleans = {}
	for word in he_words:
		c = remove_diacritics(remove_cantillation(word))
		if c not in he_cleans:
			he_cleans[c] = []
		if word not in he_cleans[c]:
			he_cleans[c].append(word)
	replacements = []
	for word in [k for k in he_cleans.keys()]:
		c = remove_diacritics(remove_cantillation(word))
		if word == c and len(he_cleans[c]) == 2 and c in he_cleans[c]:
			replacements.append([c, [x for x in he_cleans[word] if x != c][0]])
#		if word in he_cleans[word] and len(he_cleans[word]) == 2:
#			pass
#		else:
#			del he_cleans[word]

	out = '\n'.join(['%s %s'%(x[0], x[1]) for x in replacements])
	open('replacements.txt', 'w').write(out)




	chars.sort()
	chars = [{'name':unicodedata.name(c), 'code':'%04X'%ord(c)} for c in chars]
	return render_template('dev.html', chars=chars, ar_words=ar_words, ar_links=ar_links,
			he_words=he_words, he_links=he_links, letter=letter, mispunctuations=mispunctuations, ar_cleans=ar_cleans, he_cleans=he_cleans,
			replacements=replacements)

