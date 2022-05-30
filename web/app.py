import sys
sys.path.append('..')

from flask import Flask

app = Flask(__name__)
app.jinja_options['trim_blocks'] = True
app.jinja_options['lstrip_blocks'] = True
print (app.jinja_options)
print (dir(app.jinja_env))
app.jinja_env.lstrip_blocks = True
app.jinja_env.trim_blocks = True

print (app.jinja_env.lstrip_blocks)
print (app.jinja_env.trim_blocks)
	
#app.jinja_env.trim_blocks = True
#app.jinja_env.lstrip_blocks = True
from flask import render_template, send_from_directory, request, redirect

import common
import hebrew_numbers
import re
import unicodedata
import os

import Tanakh
tanakh = Tanakh.Tanakh()
tanakh.__postinit__()

import Mishnah
mishnah = Mishnah.Mishnah

import Liturgy

import Zohar
ZOHAR = Zohar.Zohar()

import Aramaic
aramaic = Aramaic.Aramaic()
numbers = [hebrew_numbers.int_to_gematria(x) for x in range(0, 151)]

@app.context_processor
def inject_variables():
	return dict(tanakh=tanakh, 
	re=re, Span=common.Span, SpanKind=common.SpanKind,
	VerseKind=Tanakh.VerseKind)
    
@app.route('/@@/<path:filename>')
def files(filename):
    return send_from_directory('static', filename)

@app.route('/@@/fonts/<path:filename>')
def fonts(filename):
    return send_from_directory('../fonts', filename)

@app.route('/')
def main():
	return render_template('index.html')

@app.route('/liturgy/')
def liturgy():
	prayer = Liturgy.Prayer('SHAHARIT')
	return render_template('liturgy.html', prayer=prayer, re=re, Span=common.Span, SpanKind=common.SpanKind)

@app.route('/liturgy/<string:variant>/<string:time>')
def prayer(variant, time):
	if variant == 'ashkenaz':
		variant = 0
	elif variant == 'sefard':
		variant = 1
	elif variant == 'mizrah':
		variant = 2
	elif variant == 'teiman':
		variant = 3
	prayer = Liturgy.Prayer(time)
	return render_template('prayer.html', prayer=prayer, variant=variant, re=re, Span=common.Span, SpanKind=common.SpanKind)

@app.route('/oldliturgy/<string:variation>/<string:kind>')
def oldprayer(variation, kind):
	p = common.Prayer(variation, kind)
	return render_template('oldprayer.html', spans=p.spans, divs=p.divs, re=re, Span=common.Span, SpanKind=common.SpanKind)

@app.route('/psalms/')
def psalms():
	s = ''
	book = common.tanakh.books[26]
	for chapter in book.chapters:
		for verse in chapter.verses:
			x = ''.join([s.value for s in verse.mikra])
			x = x.replace('R', ' ')
			x = common.remove_cantillations(x)
			x = re.sub('[׀׃\?\!\,\.\:\;]+', '', x)
			x = x.replace('־', ' ')
			x = re.sub('[\s]+', ' ', x)
			s += ' ' + x
	words = list(set(s.split(' ')))
	words.sort()
	return render_template('psalms.html', words=words, s=s, tanakh=common.tanakh, enumerate=enumerate)

@app.route('/tanakh/')
def tanakh_main():
	return render_template('tanakh.html', enumerate=enumerate)

@app.route('/tanakh/<int:book_no>/<int:chapter_no>')
def view_chapter(book_no, chapter_no):
	book = tanakh.books[book_no - 1]
	chapter = book.chapters[chapter_no - 1]
	if book.is_poem:
		return render_template('tanakh-chapter-poem.html', chapter=chapter)
	else:
		return render_template('tanakh-chapter.html', chapter=chapter)

@app.route('/tanakh/<int:book_no>/p<int:parasha_no>')
def view_parasha(book_no, parasha_no):
	book = tanakh.books[book_no - 1]
	print (book)
	parasha = book.parashot[parasha_no - 1]
	print (parasha)
	return render_template('tanakh-parasha.html', parasha=parasha, ord=ord, chr=chr, list=list)

#@app.route('/tanakh/<int:book_no>/psmet/<int:parasha_no>')
#def view_parasha_smet(book_no, parasha_no):
#	book = common.tanakh.books[book_no - 1]
#	parasha = book.parashot[parasha_no - 1]
#	return render_template('tanakh-parasha-smet.html', parasha=parasha, re=re, Span=common.Span, SpanKind=common.SpanKind, VerseKind=common.VerseKind)

@app.route('/tanakh/<int:book_no>/<int:chapter_no>/<int:verse_no>/p<int:parasha_book_no>.<int:parasha_no>/edit', methods=['GET','POST'])
@app.route('/tanakh/<int:book_no>/p<int:parasha_no>/<int:chapter_no>/<int:verse_no>/edit', methods=['GET','POST'])
def verse_edit(book_no, chapter_no, verse_no, parasha_book_no=None, parasha_no=None):
	book = tanakh.books[book_no - 1]
	chapter = book.chapters[chapter_no - 1]
	verse = chapter.verses[verse_no - 1]
	if request.method == 'POST':
		if verse.mikra_text != request.form['mikra_text']:
			verse.mikra_text = request.form['mikra_text']
			verse.mikra_text = unicodedata.normalize('NFD', verse.mikra_text)
		if verse.rashi_text != request.form['rashi_text'].replace('\r\n', '\u2028'):
			verse.rashi_text = request.form['rashi_text'].replace('\r\n', '\u2028')
		if 'title_text' in request.form and verse.title_text != request.form['title_text']:
			verse.title_text = request.form['title_text']
		if verse.has_onkelos:
			if verse.onkelos_text != request.form['onkelos_text']:
				verse.onkelos_text = request.form['onkelos_text']
			if verse.onkelos_trans_text != request.form['onkelos_trans_text']:
				verse.onkelos_trans_text = request.form['onkelos_trans_text']
		if verse.has_jerusalmi:
			if verse.jerusalmi_text != request.form['jerusalmi_text']:
				verse.jerusalmi_text = request.form['jerusalmi_text']
			if verse.jerusalmi_trans_text != request.form['jerusalmi_trans_text']:
				verse.jerusalmi_trans_text = request.form['jerusalmi_trans_text']
		if verse.has_jonathan:
			if verse.jonathan_text != request.form['jonathan_text']:
				verse.jonathan_text = request.form['jonathan_text']
		if verse.has_targum:
			if verse.targum_text != request.form['targum_text'].replace('\r\n', '\u2028'):
				verse.targum_text = request.form['targum_text'].replace('\r\n', '\u2028')
			if verse.targum_trans_text != request.form['targum_trans_text'].replace('\r\n', '\u2028'):
				verse.targum_trans_text = request.form['targum_trans_text'].replace('\r\n', '\u2028')
		if parasha_book_no:
			return redirect('/tanakh/%d/p%d#h%d.%d.%d'%(parasha_book_no, parasha_no, book.number, chapter.number, verse.number))
		elif parasha_no:
			return redirect('/tanakh/%d/p%d#%d.%d'%(book.number, parasha_no, chapter.number, verse.number))
		else:
			return redirect('/tanakh/%d/%d#%d'%(book.number, verse.chapter.number, verse.number))
	return render_template('tanakh-verse-edit2.html', verse=verse, parasha_no=parasha_no)

@app.route('/mishnah/')
def mishnah_main():
	return render_template('mishnah.html', mishnah=mishnah)

@app.route('/mishnah/<int:order_no>/<int:tractate_no>')
def view_tractate(order_no, tractate_no):
	data = open('../db/mishnah/%1d.%02d.txt'%(order_no, tractate_no)).read()
	order = mishnah[order_no - 1]
	tractate = order.books[tractate_no - 1]
	chapters = []
	parags = data.split('\n\n')
	for c in range(len(parags)):
		chapter = Mishnah.Chapter(c + 1)
		verses = parags[c].split('\n')
		for v in range(len(verses)):
			verse = Mishnah.Verse(v + 1, verses[v])
			chapter.verses.append(verse)
		chapters.append(chapter)
	return render_template('mishnah-tractate.html', chapters=chapters, order=order, tractate=tractate)

@app.route('/aramaic', methods=['POST', 'GET'])
def edit_aramaic():
	if request.method == 'GET':
		text = open('../aramaic.txt').read()
		return render_template('aramaic.html', text=text, aramaic=aramaic)
	if request.method == 'POST':
		text = request.form['text'].replace('\r\n', '\n')
		open('../aramaic.txt', 'w').write(text)
		return redirect('/aramaic')

@app.route('/aramaic/<string:word>/edit', methods=['POST', 'GET'])
def edit_aramaic_word(word):
	if request.method == 'GET':
		data = aramaic._dictionary[word]
		if ' ' in data:
			data = data.split(' ')[0]
		spelling, rest = data.split(':')
		translation = ''
		if '=' in rest:
			rest, translation = rest.split('=')
		options = rest.split(',')
		ddata = spelling, options, translation
		return render_template('aramaic-word-edit.html', word=word,
				data=data, ddata=ddata, aramaic=aramaic)
	if request.method == 'POST':
		kind = request.form['kind']
		spelling = request.form['spelling']
		clean_spelling = remove_diacritics(spelling).replace('[', '').replace(']', '')
		if kind == 'כינוי':
			s = '%s:%s,%s,%s,%s=%s'%(
					spelling,
					kind,
					request.form['person'],
					request.form['gender'],
					request.form['count'],
					request.form['translation'])
			print (aramaic._dictionary[clean_spelling])
			print (s)
			aramaic._dictionary[clean_spelling] = s
			aramaic.save()
			return redirect('/aramaic#%s'%clean_spelling)
		if kind == 'שם-עצם':
			s = '%s:%s'%(spelling, kind)
			if request.form['root']:
				s += '(%s)'%request.form['root']
			s += ',%s,%s'%(request.form['gender'], request.form['count'])
			if request.form['translation']:
				s += '=%s'%request.form['translation']
			print (aramaic._dictionary[clean_spelling])
			print (s)
			aramaic._dictionary[clean_spelling] = s
			aramaic.save()
			return redirect('/aramaic#%s'%clean_spelling)

@app.route('/zohar/')
def zohar():
	return render_template('zohar.html', zohar=ZOHAR)

@app.route('/zohar/<int:book_number>/<int:chapter_number>')
def view_zohar_chapter(book_number, chapter_number):
#	filename = os.path.join(DB_PATH, '%1d%02d'%(book_number, chapter_name), '00.txt')
#	data = open(filename).read.split('\n')

#	articles = {}
##	for i in ['1.01', '3.28']:
#		data = open('../db/zohar/%s/00.txt'%i).read().split('\n')
#		articles[i] = data
	chapter = ZOHAR.books[book_number - 1].chapters[chapter_number - 1]
	return render_template('zohar-chapter.html', chapter=chapter)

@app.route('/zohar/<int:book_number>/<int:chapter_number>/<int:article_number>')
def view_zohar_article(book_number, chapter_number, article_number):
	book = ZOHAR.books[book_number - 1]
	chapter = book.chapters[chapter_number - 1]
	article = chapter.articles[article_number - 1]
	return render_template('zohar-article.html', aramaic=aramaic, article=article, SpanKind=common.SpanKind, re=re)

@app.route('/zohar/<int:book_number>/<int:chapter_number>/<int:article_number>/edit/<int:paragraph_number>', methods=['GET','POST'])
def edit_zohar_paragraph(book_number, chapter_number, article_number, paragraph_number):
	book = ZOHAR.books[book_number - 1]
	chapter = book.chapters[chapter_number - 1]
	article = chapter.articles[article_number - 1]
	if request.method == 'POST':
		paragraphs = article.text.split('\n\n\n')
		paragraphs[paragraph_number - 1] = request.form['text'].replace('\r\n', '\n').replace('\r', '')
		article.text = '\n\n\n'.join(paragraphs).replace('\r\n', '\n')
		paragraphs = article.translation.split('\n\n\n')
		paragraphs[paragraph_number - 1] = request.form['translation'].replace('\r\n', '\n')
		article.translation = '\n\n\n'.join(paragraphs)
		return redirect('/zohar/%d/%d/%d#v%d'%(book_number, chapter_number, article_number, paragraph_number))
	if request.method == 'GET':
		text = article.text.split("\n\n\n")[paragraph_number - 1]
		translation = article.translation.split("\n\n\n")[paragraph_number - 1]

		return render_template('zohar-edit-paragraph.html', re=re, aramaic=aramaic, text=text, translation=translation,
				book=book, chapter=chapter, article=article, Zohar=Zohar, article_number=article_number, paragraph_number=paragraph_number)


def older():
	text = article.sections
#	book = common.Zohar[book_ind - 1]
#	chapter = book.chapters[chapter_no - 1]
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
		data = open('../dictionary.txt').read().split('\n')[:-1]
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

@app.route('/x/zohar/<int:book_ind>/<int:chapter_no>')
def OLDview_zohar_chapter(book_ind, chapter_no):
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

