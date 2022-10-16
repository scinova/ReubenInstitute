from flask import Blueprint
from flask import render_template, request, redirect
import sys
sys.path.append('../../')
import Aramaic

aramaic_bp = Blueprint('aramaic_bp', __name__, template_folder='templates', static_folder='static')

@aramaic_bp.route('/aramaic')
def aramaic_main():
	return render_template('aramaic.html')

@aramaic_bp.route('/aramaic/<string:name>', methods=['GET'])
def aramaic_dictionary(name):
	dictionary = Aramaic._dictionaries[name]
	groups = []
	if dictionary.type in [Aramaic.Verb, Aramaic.Noun]:
		roots = sorted(set([word.root for word in dictionary.words]))
		groups = [[word for word in dictionary.words if word.root == root] for root in roots]
	else:
		groups = [dictionary.words]
	return render_template('aramaic-dictionary.html', dictionary=dictionary, groups=groups)

@aramaic_bp.route('/aramaic/<string:name>', methods=['POST'])
def save_dictionary(name):
	text = request.form['text'].replace('\r\n', '\n')
	text = common.unicode_reorder(text)
	open(aramaic[name]._filename, 'w').write(text)
	aramaic.load()
	return redirect('/aramaic/%s'%name)

@aramaic_bp.route('/aramaic/<string:dictionary>/<string:word>', methods=['POST', 'GET'])
def aramaic_word(dictionary, word):
	if request.method == 'GET':
		d = Aramaic._dictionaries[dictionary]
		if word in [w.value for w in d.words]:
			w = d[word]
		else:
			if d.type == Aramaic.Verb:
				w = Aramaic.Verb('%s:,,,,,='%word)
			elif d.type == Aramaic.Noun:
				w = Aramaic.Noun('%s:,,='%word)
			elif d.type == Aramaic.Pronoun:
				w = Aramaic.Pronoun('%s:,,='%word)
			elif d.type == Aramaic.Number:
				w = Aramaic.Number('%s:,,='%word)
			else:
				w = Aramaic.Word('%s:='%word)
		return render_template('aramaic-word.html', word=w)
	if request.method == 'POST':
		d = Aramaic._dictionaries[dictionary]
		value = request.form['value']
		print ("VALUE", value)
		if word in [w.value for w in d.words]:
			p = d[word]
			print ("WORD", p)
			print ("ARGS", list(request.args))
			print ("PARAMS", request.form)
		else:
			if d.type == Aramaic.Verb:
				p = Aramaic.Verb('%s:,,,,,='%word)
			elif d.type == Aramaic.Noun:
				p = Aramaic.Noun('%s:,,='%word)
			elif d.type == Aramaic.Pronoun:
				p = Aramaic.Pronoun('%s:,,='%word)
			elif d.type == Aramaic.Number:
				p = Aramaic.Number('%s:,,='%word)
			else:
				p = Aramaic.Word('%s:='%word)

		if 'root' in dir(p):
			p.root = request.form['root']
		if 'stem' in dir(p):
			p.stem = request.form['stem']
		if 'tense' in dir(p):
			p.tense = request.form['tense']
		if 'person' in dir(p):
			p.person = request.form['person']
		if 'gender' in dir(p):
			p.gender = request.form['gender']
		if 'kount' in dir(p):
			p.kount = request.form['count']
		if 'translation' in dir(p):
			p.translation = request.form['translation']
		p.value = common.unicode_reorder(value)
		#print (p.root)
		d[word] = p
		#for w in d.words:
		#	if 'root' in dir(w):
		#		print ("W", w.value, w.root)
		d.save()
		#for w in d.words:
		#	if 'root' in dir(w):
		#		print ("W2", w.value, w.root)
		#aramaic.load()
		return redirect('/aramaic/%s'%(dictionary))
