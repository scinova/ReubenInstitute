import sys
sys.path.append('..')
import common
import re

if len(sys.argv) != 3:
	print ('usage: %s <book_no> <chapter_no>'%sys.argv[0])
	exit(-1)

def remove_cantillation(text):
	return re.sub('[\u0591-\u05af\u05bd]', '', text)

book_idx = int(sys.argv[1]) - 1
chapter_idx = int(sys.argv[2]) - 1
chapter = common.tanakh.books[book_idx].chapters[chapter_idx]

for verse in chapter.verses:
	data = re.sub('\:\u2028', '.\u2028', verse.rashi_text)
	data = re.sub('\:$', '.', data)
	if data != verse.rashi_text:
		verse.rashi_text = data
		verse.save_rashi()

	text = verse.rashi_text.replace('\u2028', '\n')
	legends = reversed(list(re.finditer('^[^\.]+\.', text, re.M)))
	for idx, legend in enumerate(legends):
		words = legend.group()[:-1].split(' ')
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
		print (verse.number, idx, legend.group()[:-1])

		replacement = remove_cantillation(m.group())
		replacement = re.sub('[,\.]', '', replacement)
		if words[-1] == 'וגו׳':
			replacement += ' …'
		print (verse.number, idx, replacement)
		print (verse.rashi_text[legend.start():legend.end()])

		verse.rashi_text = verse.rashi_text[:legend.start()] + replacement + '.' + verse.rashi_text[legend.end():]
	#verse.save_rashi()
