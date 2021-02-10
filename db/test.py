import os
import sys
sys.path.append('..')
import common
import unicodedata
import re

def remove_accents(text):
	return re.sub('[\u0591-\u05af\u05bd]', '', text)

words = []
chars = []
for book in common.tanakh.books[:5]:
	for chapter in book.chapters:
		for verse in chapter.verses:
			text = verse.text

			# replace kriktiv with kri
			for i in re.finditer('\[([^|]+)\|([^]]+)\]', text):
				string = text[i.start():i.end()]
				kri = i.groups()[1]
				kripos = string.find(kri)
				string = kripos * 'X' + kri + 'X'
				text = text[:i.start()] + string + text[i.end():]
				#print (text2)
				#print (len(text), len(text2))
			if 'X' in text:
				print (chapter.number, verse.number, text.replace('X', ''))

			text = re.sub('\{\{[^\}]+\}\}\s', 'X', text) # parasha name
			text = re.sub('\{[^\}]+\}\s*', 'X', text) # open/closed portion
			text = re.sub('[“”‘’"\'!\-\.,:;?<>\[\]\|]', 'X', text)

			text = re.sub('[׃׀]', 'X', text)
			text = re.sub('־', ' ', text)
			
			text = text.replace('X', '').replace('Y', '')
			#text = re.sub('\s+', ' ', text)
			for word in re.split('\s+', text):
				if '\u05bc' in word or '\u05b0' in word:
					words.append(remove_accents(word))
			#print (words)

			for c in text:
				chars.append(c)

chars = list(set(chars))
print (len(chars))
chars.sort()
for c in chars:
	print (hex(ord(c)), unicodedata.name(c))

print ('-000000-')
words = list(set(words))
words.sort()
print (len(words))
for word in words:
	print (word)
