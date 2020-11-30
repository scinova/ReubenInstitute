import sys
sys.path.append('..')
import common
import re
import unicodedata

for i in range(len(common.Bible[:5])):
	book = common.Bible[i]
	src = 'onkelos/%s.txt'%(book.name)
	data = open(src, newline='').read()
	chapters = re.split('\nChapter [0-9]+\n\n', data)[1:]
	for c in range(len(chapters)):
		dst = '../db/onkelos/%1d.%02d.txt'%(i + 1, c + 1)
		out = chapters[c]
		out = ''.join([unicodedata.normalize('NFD', l) for l in out])
		open(dst, 'w').write(out)
		print (dst)
