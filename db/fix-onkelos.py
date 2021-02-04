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

print (len(chapter.verses))

for verse in chapter.verses:
	print (verse.onkelos_text)
	verse.onkelos_text = re.sub('\:$', '', verse.onkelos_text)
	verse.save_onkelos()