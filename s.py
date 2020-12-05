import unicodedata
import re
import common


def remove_cantillation(text):
	return re.sub('[\u0591-\u05af\u05bd]', '', text)

def remove_diacritics(text):
	return re.sub('[\u05b0-\u05bc\u05c1\u05c2\u05c7]', '', text)

data = ''
articles = open('db/zohar/1.01/00.txt').read().split('\n')[:-1]
for i in range(len(articles)):
	data += open('db/zohar/1.01/%02d.txt'%i).read()
articles = open('db/zohar/3.28/00.txt').read().split('\n')[:-1]
for i in range(len(articles)):
	data += open('db/zohar/3.28/%02d.txt'%i).read()

data = unicodedata.normalize('NFD', data)

data = re.sub('{[^}]+}', '', data)
data = re.sub('[\=~\.\,\!\?…\(\)\:\;\u2022\u2013\-]', '', data)
data = re.sub('[“”]', '"', data)
data = re.sub('[‘’]', "'", data)
data = re.sub('\u00a0', ' ', data)

chars = []
for c in data:
	if c != '\n':
		if c not in chars:
			chars.append(c)
chars.sort()
for c in chars:
	print (unicodedata.name(c))
#print (len(chars))


data = re.sub('"[^"]+"', ' ', data)
data = re.sub("'", ' ', data)
data = re.sub('[\s]+', ' ', data)

inwords = data.split(' ')
words = list(set(inwords))
words.sort()
print (len(words))

prevs = {}
for i in range(len(inwords)):
	word = inwords[i]
	if i:
		prev = inwords[i - 1]
	else:
		prev = ''
	if word not in prevs:
		prevs[word] = []
	prevs[word].append(prev)

for word in sorted(words, key=lambda word: remove_diacritics(remove_cantillation(word))):
	if word in prevs:
		prevs[word] = sorted(list(set(prevs[word])))
	if '\u05b0' in word or '\u05bc' in word:
		print (word, prevs[word])
