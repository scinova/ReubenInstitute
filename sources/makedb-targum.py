import sys
sys.path.append('..')
import common
import re
import unicodedata

if 1:
	book = common.Bible[26]
	src = 'Aramaic Targum to Psalms - he - Mikraot Gedolot.txt'
	data = open(src, newline='').read()
	chapters = re.split('\n\nChapter [0-9]+\n\n', data)[1:]
	for c in range(len(chapters)):
		dst = '../db/targum/27.%03d.txt'%(c + 1)
		out = chapters[c]
		out = ''.join([unicodedata.normalize('NFD', l) for l in out])
		open(dst, 'w').write(out)
		print (dst)
