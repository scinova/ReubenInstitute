import re
import sys
sys.path.append('../../')
import common


abbreviations = {}
f = open('00abbreviations.txt')
for line in f:
	p = line[:-1].split(' ')
	abbreviations[p[0]] = ' '.join(p[1:])

"""
allwords = []
for book in common.tanakh.books:
	for chapter in book.chapters:
		filename = '%02d.%03d.txt'%(book.number, chapter.number)
		data = open(filename).read()
		words = re.split('[\s,\-–—\.:\?\(\)\;\[\]]+', data)
		for word in words:
			if word.startswith('"') or word.startswith("'"):
				word = word[1:]
			if word.endswith('"') or word.endswith("'"):
				word = word[:-1]
			allwords.append(word)
#allwords = list(set(allwords))
#allwords.sort(key=lambda x: len(x))
for word in allwords:
	if '"' in word and word not in abbreviations:
		print (word)
"""

data = open('01.002.txt').read()
for abbreviation, replacement in abbreviations.items():
	#print (abbreviation, replacement)
	data = re.sub(abbreviation, replacement, data)
print (data)




