import sys
sys.path.append('..')
import common
import re

for b in range(len(common.zohar_arr)):
	if b in [0, 1, 2]:
		data = open('zohar/Zohar - he - New Torat Emet Zohar.plain.txt').read()
		books = re.split('\nVolume [1-3]\n\n', data)[1:]
		pages = re.split('\n\nDaf [0-9]{1,3}[ab]\n\n', books[b])[1:]
	if b == 4:
		data = open('zohar/Tikkunei Zohar - he - Tikkunei Zohar.plain.txt').read()
		pages = re.split('\n\nDaf [0-9]{1,3}[ab]\n\n', data)[1:]
	book_name, chapter_arr = common.zohar_arr[b]
	for c in range(len(chapter_arr)):
		start_daf, start_amud, start_verse, end_daf, end_amud, end_verse, hname = chapter_arr[c]
		start_page = (start_daf - 1) * 2 + (start_amud - 1)
		end_page = (end_daf - 1) * 2 + (end_amud - 1)
		chapter = common.Chapter(c + 1)
		chapter.hname = hname
		o = ''
		out_verses = []
		for p in range(start_page, end_page + 1):
			verses = pages[p].split('\n')
			if p == start_page and p == end_page:
				r = range(start_verse - 1, end_verse)
			elif p == start_page:
				r = range(start_verse - 1, len(verses))
			elif p == end_page:
				r = range(end_verse)
			else:
				r = range(len(verses))
			for v in r:
				if v == 0 and out_verses:
					out_verses[len(out_verses) - 1] += ' ' + verses[v]
				else:
					out_verses.append(verses[v])
		out = '\n'.join(out_verses)
		dst = '../db/zohar/%1d.%02d.txt'%(b + 1, chapter.no)
		print ('----', b + 1, chapter.no, start_page, start_verse, end_page, end_verse,
				len(out_verses), len(out), dst)
		open(dst, 'w').write(out)
