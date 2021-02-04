import sys
sys.path.append('..')
import common
import re

if len(sys.argv) != 3:
	print ('usage: %s <book_no> <chapter_no>'%sys.argv[0])
	exit(-1)

book_idx = int(sys.argv[1]) - 1
chapter_idx = int(sys.argv[2]) - 1
chapter = common.tanakh.books[book_idx].chapters[chapter_idx]

for verse in chapter.verses:
	verse.rashi_text = re.sub('\:\u2028', '.\u2028', verse.rashi_text)
	verse.rashi_text = re.sub('\:$', '.', verse.rashi_text)
	verse.save_rashi()
