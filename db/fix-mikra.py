import sys
sys.path.append('..')
import common
import re

if len(sys.argv) != 3:
	print ('usage: %s <book_no> <chapter_no>'%sys.argv[0])
	exit(-1)

def remove_diacritics(text):
	return re.sub('[\u05b0-\u05b8]', '', text)

book_idx = int(sys.argv[1]) - 1
chapter_idx = int(sys.argv[2]) - 1
chapter = common.tanakh.books[book_idx].chapters[chapter_idx]

for verse in chapter.verses:
	# remove space before siluk
	text = re.sub(' ׀', '׀', verse.text)
	# remove diacritics from explicit name
	name = 'יהוה'
	pattern = ''
	for l in range(len(name)):
		pattern += name[l] + '[\u0591-\u05bd]*'
	for m in reversed(list(re.finditer(pattern, text))):
		replacement = remove_diacritics(m.group())
		text = text[:m.start()] + replacement + text[m.end():]

	if text != verse.text:
		verse.text = text
		verse.save_mikra()
