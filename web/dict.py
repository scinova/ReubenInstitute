import sys
sys.path.append('..')
import common
import hebrew_numbers
import re
import unicodedata

def remove_cantillation(text):
	return re.sub('[\u0591-\u05af\u05bd]', '', text)

def xremove_punctuation(text):
	return re.sub('[\u05b0-\u05bc\u05c1\u05c2\u05c7]', '', text)

def remove_diacritics(text):
	return re.sub('[\u05b0-\u05bc\u05c1\u05c2\u05c7]', '', text)


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




	dictionary = {}
	for book in common.Zohar:
		for chapter in book.chapters:
			for article in chapter.articles:
				for p in range(len(ar_sentences[book.ind][chapter.no][article.no])):
					#print (book.ind, chapter.no, article.no, p, sentences[3].keys())
					for s in range(len(ar_sentences[book.ind][chapter.no][article.no][p])):
						ar_sentence = ar_sentences[book.ind][chapter.no][article.no][p][s]
						try:
							he_sentence = he_sentences[book.ind][chapter.no][article.no][p][s]
						except IndexError:
							he_sentence = ''
						#he_sentence = re.sub('_[^_]+_', '', he_sentence)
						ar_words = ar_sentence.split(' ')
						he_words = he_sentence.split(' ')
#						print ("-------------")
#						print (ar_words)
#						print (he_words)
						if len(ar_words) and len(ar_words) == len(he_words):
							for i in range(len(ar_words)):
								ar_word = ar_words[i]
								he_word = he_words[i]
								if ar_word not in dictionary:
									dictionary[ar_word] = []
								if he_word not in dictionary[ar_word]:
									dictionary[ar_word] = he_word
	l = list(dictionary.keys())
	l.sort()
	#print (l)
	out = ''
	for k in l:
		print (k, dictionary[k])
		if len(k) > 2:
			out += k + ' ' + ''.join(dictionary[k]) + '\n'
	open('dictionary.txt', 'w').write(out)


#				for p in range(len(he_sentences[book.ind][chapter.no][article.no])):
#					#print (book.ind, chapter.no, article.no, p, sentences[3].keys())
#					for s in range(len(he_sentences[book.ind][chapter.no][article.no][p])):
#						sentence = he_sentences[book.ind][chapter.no][article.no][p][s]





"""
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
#	return render_template('dev.html', chars=chars, ar_words=ar_words, ar_links=ar_links,
#			he_words=he_words, he_links=he_links, letter=letter, mispunctuations=mispunctuations, ar_cleans=ar_cleans, he_cleans=he_cleans,
#			replacements=replacements)
"""

dev()
