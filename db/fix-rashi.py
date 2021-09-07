import sys
sys.path.append('..')
import common
import re

if len(sys.argv) != 3:
	print ('usage: %s <book_no> <chapter_no>'%sys.argv[0])
	exit(-1)

def remove_cantillation(text):
	return re.sub('[\u0591-\u05af\u05bd]', '', text)

def remove_diacritics(text):
	return re.sub('[\u05b0-\u05bc\u05c1\u05c2\u05c7]', '', text)

book_idx = int(sys.argv[1]) - 1
chapter_idx = int(sys.argv[2]) - 1
chapter = common.tanakh.books[book_idx].chapters[chapter_idx]

for verse in chapter.verses:
	# remove final colon
	data = re.sub('\:\u2028', '.\u2028', verse.rashi_text)
	data = re.sub('\:$', '.', data)
	if data != verse.rashi_text:
		verse.rashi_text = data
		verse.save_rashi()
	# copy legends from mikra
	text = verse.rashi_text.replace('\u2028', '\n')
	legends = reversed(list(re.finditer('^[^\.]+\.', text, re.M)))
	for idx, legend in enumerate(legends):
		legend_text = remove_diacritics(legend.group()[:-1]).replace('־', ' ').replace('…', 'וגו׳')
		words = legend_text.split(' ')
		patterns = []
		for w in range(len(words)):
			if words[w] == 'ה׳':
				words[w] = 'יהוה'
			if words[w] == 'וגו׳':
				continue
			s = ''
			for l in range(len(words[w])):
				s += words[w][l] + '[\u0591-\u05bd\u05c1-\u05c2\u05c7]*'
			patterns.append(s)
		pattern = '[\s־׀,\.]+'.join(patterns)

		m = re.search(pattern, verse.text)
		print (verse.number, idx, legend_text)

#		try:

		if not m:
			continue
		replacement = m.group()
#		except:
#			print ("ERROR")
#			continue
		replacement = remove_cantillation(replacement)
		replacement = re.sub('[,\.]', '', replacement)
		if words[-1] == 'וגו׳':
			replacement += ' …'
		print (verse.number, idx, replacement)
		print (verse.rashi_text[legend.start():legend.end()])

		verse.rashi_text = verse.rashi_text[:legend.start()] + replacement + '.' + verse.rashi_text[legend.end():]

	# expand abbreviations
	abbreviations = {}
	f = open('../db/rashi/00abbreviations.txt')
	for line in f:
		p = line[:-1].split(' ')
		abbreviations[p[0]] = ' '.join(p[1:])
	for abbreviation, replacement in abbreviations.items():
		verse.rashi_text = re.sub(abbreviation, replacement, verse.rashi_text)



	verse.save_rashi()
