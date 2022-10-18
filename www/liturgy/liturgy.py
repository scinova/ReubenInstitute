from flask import Blueprint, render_template, request, redirect
import re
import Liturgy

liturgy_bp = Blueprint('liturgy_bp', '__name__')

@liturgy_bp.route('/liturgy/')
def liturgy():
	return render_template('liturgy/index.html')

@liturgy_bp.route('/liturgy/<string:name>/edit', methods=['GET','POST'])
def edit_prayer(name):
	prayer = Liturgy.prayers[name]
	if request.method == 'POST':
		prayer.text = request.form['text'].replace('\r\n', '\n')
		return redirect('/liturgy/%s/%s'%(request.args['version_name'], name))
	return render_template('liturgy/prayer-edit.html', prayer=prayer)

@liturgy_bp.route('/liturgy/<string:version_name>/<string:name>')
def prayer(version_name, name):
	if version_name == 'ashkenaz':
		version = 0
	elif version_name == 'sefard':
		version = 1
	elif version_name == 'mizrah':
		version = 2
	elif version_name == 'teiman':
		version = 3
	prayer = Liturgy.prayers[name]
	return render_template('liturgy/prayer.html', prayer=prayer, version=version, version_name=version_name)
