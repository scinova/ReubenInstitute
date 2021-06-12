import os
import sys
sys.path.append('..')
import common
import unicodedata
import re

def remove_accents(text):
	return re.sub('[\u0591-\u05af\u05bd]', '', text)

words = []
onkelos_words = []
jerusalmi_words = []
chars = []
for book in common.tanakh.books[0:1]:
	for chapter in book.chapters[0:6]:
		for verse in chapter.verses:

			text = verse.text
			# replace kriktiv with kri
			for i in re.finditer('\[([^|]+)\|([^]]+)\]', text):
				string = text[i.start():i.end()]
				kri = i.groups()[1]
				kripos = string.find(kri)
				string = kripos * 'X' + kri + 'X'
				text = text[:i.start()] + string + text[i.end():]
			# remove parasha name
			text = re.sub('\{\{[^\}]+\}\}\s', 'X', text)
			# remove open/closed portion
			text = re.sub('\{[^\}]+\}\s*', 'X', text)
			# remove punctuation
			text = re.sub('[“”‘’"\'!\-\.,:;?<>\[\]\|]', 'X', text)
			# remove letter sized accents
			text = re.sub('[׃׀]', 'X', text)
			# split words with makaf
			text = re.sub('־', ' ', text)
			text = text.replace('X', '').replace('Y', '')
			for word in re.split('\s+', text):
				if '\u05bc' in word or '\u05b0' in word:
					words.append(remove_accents(word))

			text = verse.onkelos_text
			# remove addition and non-literal tags
			text = re.sub('[_\+]', '', text)
			# remove alternative text
			for i in re.finditer('\[([^|]+)\|([^]]+)\]', text):
				string = text[i.start():i.end()]
				kri = i.groups()[0]
				kripos = string.find(kri)
				string = kripos * 'X' + kri + 'X'
				text = text[:i.start()] + string + text[i.end():]
			# remove punctuation
			text = re.sub('[“”‘’"\'!\-\.,:;?<>\[\]\|]', 'X', text)

			text = text.replace('X', '').replace('Y', '')
			for word in re.split('\s+', text):
				#if '\u05bc' in word or '\u05b0' in word:
				onkelos_words.append(word)

			text = verse.jerusalmi_text or ''
			# remove addition and non-literal tags
			text = re.sub('[_\+]', '', text)
			# remove alternative text
			for i in re.finditer('\[([^|]+)\|([^]]+)\]', text):
				string = text[i.start():i.end()]
				kri = i.groups()[0]
				kripos = string.find(kri)
				string = kripos * 'X' + kri + 'X'
				text = text[:i.start()] + string + text[i.end():]
			# remove punctuation
			text = re.sub('[“”‘’"\'!\-\.,:;?<>\[\]\|]', 'X', text)

			text = text.replace('X', '').replace('Y', '')
			for word in re.split('\s+', text):
				#if '\u05bc' in word or '\u05b0' in word:
				jerusalmi_words.append(word)




			for c in text:
				chars.append(c)

chars = list(set(chars))
print (len(chars))
chars.sort()
for c in chars:
	print (hex(ord(c)), unicodedata.name(c))

words = list(set(words))
words.sort()
print ('Mikra words: ', len(words))
open('WORDS-MIKRA.txt', 'w').write('\n'.join(words))

words = list(set(onkelos_words))
words.sort(key=lambda x:common.remove_diacritics(x))
print ('Onkelos words: ', len(words))
open('WORDS-ONKELOS.txt', 'w').write('\n'.join(words))

words = list(set(jerusalmi_words))
words.sort()
print ('Jerusalmi words: ', len(words))
open('WORDS-JERUSALMI.txt', 'w').write('\n'.join(words))
