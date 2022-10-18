from flask import Blueprint, g, render_template, send_from_directory, request, redirect
import unicodedata
import sys
sys.path.append('..')
import common
import Tanakh

tanakh_bp = Blueprint('tanakh_bp', __name__)#, template_folder='templates')

@tanakh_bp.route('/psalms/')
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
	return render_template('tanakh/psalms.html', words=words, s=s, tanakh=common.tanakh, enumerate=enumerate)

@tanakh_bp.route('/tanakh/')
def tanakh_main():
	return render_template('tanakh/index.html')

@tanakh_bp.route('/tanakh/<int:book_no>/<int:chapter_no>')
def tanakh_chapter_view(book_no, chapter_no):
	book = Tanakh.books[book_no - 1]
	chapter = book.chapters[chapter_no - 1]
	if book.is_poem:
		return render_template('tanakh/chapter-poem.html', chapter=chapter)
	else:
		return render_template('tanakh/chapter.html', chapter=chapter)

#@tanakh_bp.route('/tanakh/<int:book_no>/<int:chapter_no>/<int:verse_no>/edit')
#def tanakh_verse_edit(book_no, chapter_no, verse_no):
#	book = Tanakh.books[book_no - 1]
#	chapter = book.chapters[chapter_no - 1]
#	verse = chapter.verses[verse_no - 1]
#	if request.method == 'POST':
#		if verse.mikra_text != request.form['mikra_text']:
#			verse.mikra_text = request.form['mikra_text']
#			verse.mikra_text = unicodedata.normalize('NFD', verse.mikra_text)
#		return redirect('/tanakh/%d/%d#%d'%(book.number, verse.chapter.number, verse.number))
#	return render_template('verse-edit2.html', verse=verse, parasha_no=parasha_no)

@tanakh_bp.route('/tanakh/<int:book_no>/p<int:parasha_no>')
def view_parasha(book_no, parasha_no):
	book = Tanakh.books[book_no - 1]
	#print (book)
	parasha = book.parashot[parasha_no - 1]
	#print (parasha)
	return render_template('tanakh/parasha.html', parasha=parasha)

#@tanakh_bp.route('/tanakh/<int:book_no>/psmet/<int:parasha_no>')
#def view_parasha_smet(book_no, parasha_no):
#	book = common.tanakh.books[book_no - 1]
#	parasha = book.parashot[parasha_no - 1]
#	return render_template('tanakh-parasha-smet.html', parasha=parasha, re=re, Span=common.Span, SpanKind=common.SpanKind, VerseKind=common.VerseKind)

@tanakh_bp.route('/tanakh/<int:book_no>/<int:chapter_no>/<int:verse_no>/p<int:parasha_book_no>.<int:parasha_no>/edit', methods=['GET','POST'])
@tanakh_bp.route('/tanakh/<int:book_no>/p<int:parasha_no>/<int:chapter_no>/<int:verse_no>/edit', methods=['GET','POST'])
def verse_edit(book_no, chapter_no, verse_no, parasha_book_no=None, parasha_no=None):
	book = Tanakh.books[book_no - 1]
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
	return render_template('tanakh/tanakh-verse-edit2.html', verse=verse, parasha_no=parasha_no)
