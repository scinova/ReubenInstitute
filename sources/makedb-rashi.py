import sys
sys.path.append('..')
import common
import re

for book in common.tanakh.books:
	src = 'rashi/%02d.txt'%(book.number)
	data = open(src, newline='').read()
	chapters_string = re.split('\n\nChapter [0-9]+\n\n', data)[1:]
	for idx, chapter in enumerate(book.chapters):
		chapter_string = chapters_string[idx]
		verses = re.split('\n\nVerse [0-9]+\n\n', chapter_string)[1:]
		# MISTAKES
		if book.number == 13 and chapter.number == 31:
			verses = verses[1:]
		if book.number == 2 and chapter.number == 38:
			verses = verses[:31]
		# MISTAKES END
		diff = len(chapter.verses) - len(verses)
		if diff:
			verses.extend(diff * [''])
		out = '\n'.join([v.replace('\n', ' ') for v in verses])
		dst = '../db/rashi/%02d.%03d.txt'%(book.number, chapter.number)
		open(dst, 'w').write(out)
