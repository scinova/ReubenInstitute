from flask import Blueprint, g, render_template, request, redirect, send_from_directory
import sys
sys.path.append('..')
import Zohar
import common

zohar_bp = Blueprint('zohar_bp', __name__)#, template_folder='templates')

#@zohar_bp.route('/@@/<path:filename>')
#def files(filename):
#	return send_from_directory('static', filename)
#
@zohar_bp.route('/zohar/')
def main():
	return render_template('zohar/main.html')

@zohar_bp.route('/zohar/<int:book_number>/<int:chapter_number>')
def view_chapter(book_number, chapter_number):
	chapter = Zohar.books[book_number - 1].chapters[chapter_number - 1]
	return render_template('zohar/chapter.html', chapter=chapter)#, data=data)

@zohar_bp.route('/zohar/<int:book_number>/<int:chapter_number>/<int:article_number>')
def view_article(book_number, chapter_number, article_number):
	book = Zohar.books[book_number - 1]
	chapter = book.chapters[chapter_number - 1]
	article = chapter.articles[article_number - 1]
	return render_template('zohar/article.html', article=article)#, data=data)

@zohar_bp.route('/zohar/issues/<int:issue_number>')
def view_issue(issue_number):
	issue = Zohar.issues[issue_number - 1]
	return render_template('zohar/issue.html', issue=issue)

@zohar_bp.route('/zohar/<int:book_number>/<int:chapter_number>/<int:article_number>/edit/<int:paragraph_number>', methods=['GET','POST'])
def edit_paragraph(book_number, chapter_number, article_number, paragraph_number):
	book = Zohar.books[book_number - 1]
	chapter = book.chapters[chapter_number - 1]
	article = chapter.articles[article_number - 1]
	if request.method == 'POST':
		paragraphs = article.text.split('\n\n')
		text = request.form['text'].replace('\r\n', '\n').replace('\r', '')
		text = common.unicode_reorder(text)
		paragraphs[paragraph_number - 1] = text
		text = '\n\n'.join(paragraphs).replace('\r\n', '\n')
		text = text.replace('\u05c7', '\u05b8')
		article.text = text
		#ZOHAR.books[book_number - 1].chapters[chapter_number - 1].articles[article_number - 1].text = text
		paragraphs = article.translation.split('\n\n')
		paragraphs[paragraph_number - 1] = request.form['translation'].replace('\r\n', '\n')
		text = '\n\n'.join(paragraphs)
		article.translation = text
		#ZOHAR.books[book_number - 1].chapters[chapter_number - 1].articles[article_number - 1].translation = text
		return redirect('/zohar/%d/%d/%d#v%d'%(book_number, chapter_number, article_number, paragraph_number))
	if request.method == 'GET':
		text = article.text.split("\n\n")[paragraph_number - 1]
		for s, d in [
				#['', ''],
				['סָתִים', 'סְתִים'],
				['אִתְמַר', 'אִתְּמַר'],
				['רִבִּי', 'רַבִּי'],
				['בַּר נָשׁ', 'בַּר־נָשׁ'],
				['בַר נָשׁ', 'בַר־נָשׁ'],
				['אָמַר', 'אֲמַר'],
				['עַתִּּיק יוֹמִין', 'עַתִּּיק־יוֹמִין'],
				['בְּרִיךְ הוּא', 'בְּרִיךְ־הוּא'],
				['הָֽכִי', 'הָכִי'],
				['שַׁעְתָּא', 'שַׁעֲתָא'],
				['אֶֽלָּא', 'אֶלָּא'],
				['אִֽיהוּ', 'אִיהוּ'],
				['אִתְּמָר', 'אִתְּמַר'],
				['כֹֽלָא', 'כֹלָּא'],
				['כֹֽלָּא', 'כֹלָּא'],
				['אִֽיהִי', 'אִיהִי'],
				['לָהּ', 'לַהּ'],
				['מִינָהּ', 'מִינַּהּ'],
				['לְגַבָּהּ', 'לְגַבַּהּ'],
				['א ָמ ַר', 'אֲמַר'],
				['מ ָאן', 'מַאן'],
				['לְתַֽתָּא', 'לְתַתָּא'],
				['עֵֽילָא', 'עֵלָּא'],
				['עֵֽלָא', 'עֵלָּא']]:
			text = text.replace(s, d)
			text = common.fix_yhwh(text)
			text = common.unicode_reorder(text)
		translation = article.translation.split("\n\n")[paragraph_number - 1]
		return render_template('zohar/paragraph-edit.html', text=text, translation=translation,
				book=book, chapter=chapter, article=article, article_number=article_number, paragraph_number=paragraph_number)
