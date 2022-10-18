from flask import Blueprint, g, render_template, request, redirect
import common
import Mishnah

mishnah_bp = Blueprint('mishnah_bp', __name__)#, template_folder='templates')

@mishnah_bp.route('/mishnah/')
def main():
	return render_template('mishnah/main.html')

@mishnah_bp.route('/mishnah/<int:order_no>/<int:tractate_no>')
def view_tractate(order_no, tractate_no):
	tractate = Mishnah.orders[order_no - 1].tractates[tractate_no - 1]
	return render_template('mishnah/tractate.html', tractate=tractate)

@mishnah_bp.route('/mishnah/full')
def view_full():
	return render_template('mishnah/full.html')

@mishnah_bp.route('/mishnah/<int:order_no>')
def view_order(order_no):
	order = Mishnah.orders[order_no - 1]
	return render_template('mishnah/order.html', order=order)

@mishnah_bp.route('/mishnah/<int:order_no>/<int:tractate_no>/<int:chapter_no>/edit/<int:verse_no>', methods=['GET'])
def edit_verse(order_no, tractate_no, chapter_no, verse_no):
	verse = Mishnah.orders[order_no - 1].tractates[tractate_no - 1].chapters[chapter_no - 1].verses[verse_no - 1]
	return render_template('mishnah/verse-edit.html', verse=verse)

@mishnah_bp.route('/mishnah/<int:order_no>/<int:tractate_no>/<int:chapter_no>/edit/<int:verse_no>', methods=['POST'])
def save_verse(order_no, tractate_no, chapter_no, verse_no):

	tractate = Mishnah.orders[order_no - 1].tractates[tractate_no - 1]
	chapter = tractate.chapters[chapter_no - 1]
	verse = chapter.verses[verse_no - 1]

	value = common.unicode_reorder(request.form['mishnah_text'].replace('\r\n', '\u2028'))
	verse.mishnah_text = value
	ct = '\n'.join([verse.mishnah_text for verse in chapter.verses])
	cs = tractate.mishnah_text.split('\n\n')
	cs[chapter_no - 1] = ct
	tractate.mishnah_text = '\n\n'.join(cs)

	value = common.unicode_reorder(request.form['bartenura_text'].replace('\r\n', '\u2028'))
	verse.bartenura_text = value
	ct = '\n'.join([verse.bartenura_text for verse in chapter.verses])
	cs = tractate.bartenura_text.split('\n\n')
	cs[chapter_no - 1] = ct
	tractate.bartenura_text = '\n\n'.join(cs)

	return redirect('/mishnah/%d/%d#%d.%d'%(tractate.order.number, tractate.number, chapter.number, verse.number))
