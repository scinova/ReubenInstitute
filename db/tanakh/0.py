import re
import unicodedata
from hebrew_numbers import int_to_gematria

def remove_accents(text):
	return re.sub('[\u0591-\u05af\u05bd]', '', text)

def remove_marks(text):
	return re.sub('[\u05b0-\u05bc\u05c1\u05c2\u05c7]', '', text)

def clean(text):
	return (remove_accents(remove_marks(text)))

words = []
freq = {}
links = {}
letters = []

for c in range(1, 151):
	filename = '27.%03d.txt'%c
	data = open(filename).read()
	data = re.sub('׃', '', data)
	data = re.sub(',', '', data)
	data = re.sub(' ׀', '', data)
	data = re.sub('־', ' ', data)
#	data = re.sub('\[[^\]+]\]', '', data)
	data = re.sub('\[', '{', data)
	data = re.sub('\]', '}', data)
	data = re.sub('{[^}]+}', '', data)
	data = remove_accents(data)
	lines = data.split('\n')
	for l in range(len(lines)):
		line = lines[l]
		parts = line.split(' ')
		for part in parts:
			if not part:
				continue
			if part not in freq:
				freq[part] = 0
			freq[part] += 1
			if part not in links:
				links[part] = []
			links[part].append("%s.%s"%(int_to_gematria(c, gershayim=False), int_to_gematria(l+1, gershayim=False)))
			if part not in words:
				words.append(part)
			for letter in part:
				if letter not in letters:
					letters.append(letter)
#words.sort(key=lambda x:-freq[x])
words.sort()
for word in words:
	if ('\u05b0' in word or '\u05bc' in word):
		print (clean(word), word, freq[word], links[word])

words.sort(key=lambda word:clean(word))
out = ""
for word in words:
	if ('\u05b0' not in word and '\u05bc' not in word):
		continue
	
	if len(clean(word)) != len(list(re.finditer('[\u05d0-\u05ea][^\u05d0-\u05ea]*', word))):
		print (word)
		exit()

	s = ''
	for item in re.finditer('[\u05d0-\u05ea][^\u05d0-\u05ea]*', word):
#		print (len(item.string[item.start():item.end()]), item)
		chars = item.string[item.start():item.end()]
		if ('\u05bc' in chars):
			s += 'd'
		if ('\u05b0' in chars):
			s += 's'
	print (word, s)

	#out += word + ' ' + ' '.join(links[word]) + '\n'
	out += word + ' ' + s + '\n'
open('00.txt', 'w').write(out)

letters.sort()
for letter in letters:
	print (unicodedata.name(letter))

