from flask import Flask, g
from flask import render_template, send_from_directory, request, redirect

#import hebrew_numbers
import re
#import unicodedata
#import os



import sys
sys.path.append('..')
import common
import Zohar
import Aramaic
import Tanakh
import Mishnah

#numbers = [hebrew_numbers.int_to_gematria(x) for x in range(0, 151)]


class User:
	def __init__(self):
		self.isloggedin = True
		#self.isloggedin = False

def create_app():
	app = Flask(__name__)
	app.jinja_options['trim_blocks'] = True
	app.jinja_options['lstrip_blocks'] = True
	app.jinja_env.lstrip_blocks = True
	app.jinja_env.trim_blocks = True
	with app.app_context():
		from .zohar import zohar
		app.register_blueprint(zohar.zohar_bp)
		from .aramaic import aramaic
		app.register_blueprint(aramaic.aramaic_bp)
		from .tanakh import tanakh
		app.register_blueprint(tanakh.tanakh_bp)
		from .mishnah import mishnah
		app.register_blueprint(mishnah.mishnah_bp)


	@app.before_request
	def before_request():
		g.user = User()
		#g.request_start_time = time.time()
		#g.request_time = lambda: '%.5fs'%(time.time() - g.request_start_time)
		pass

	@app.context_processor
	def inject_variables():
		return dict(
		Aramaic=Aramaic, Tanakh=Tanakh, Mishnah=Mishnah,
		Person=Aramaic.Person, Gender=Aramaic.Gender, Count=Aramaic.Count,
		Tense=Aramaic.Tense, Stem=Aramaic.Stem,
		Noun=Aramaic.Noun, Number=Aramaic.Number, Pronoun=Aramaic.Pronoun, Verb=Aramaic.Verb, Name=Aramaic.Name,
		#random=random, 
		type=type, re=re, dir=dir, len=len, int=int, ord=ord, chr=chr, list=list,
		enumerate=enumerate,
		Span=common.Span, SpanKind=common.SpanKind,
		VerseKind=Tanakh.VerseKind,
		request=request, common=common,
		#aramaic=aramaic,
		#user=user
		Zohar=Zohar
		)

	@app.route('/@@/<path:filename>')
	def files(filename):
		return send_from_directory('static', filename)

	@app.route('/@@/fonts/<path:filename>')
	def fonts(filename):
		return send_from_directory('../fonts', filename)

	@app.route('/')
	def main():
		return render_template('index.html')

#@app.route('/login', methods=['GET'])
#def login():
#	user.isloggedin = True
#	return redirect(request.args['url'])

#@app.route('/logout', methods=['GET'])
#def logout():
#	user.isloggedin = False
#	return redirect(request.args['url'])

	return app
