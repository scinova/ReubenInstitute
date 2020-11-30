import sys
sys.path.append('..')
import common
import re
import unicodedata

for i in range(len(common.Mishnah)):
	order = common.Mishnah[i]
	for t in range(len(order.books)):
		trac = order.books[t]
		src = 'mishnah/%s.txt'%(trac.name)
		dst = '../db/mishnah/%1d.%02d.txt'%(i + 1, t + 1)
		data = open(src, newline='').read()
		chapters = re.split('\nChapter [0-9]+\n\n', data)
		data = '\n'.join(chapters[1:])
		data = ''.join([unicodedata.normalize('NFD', l) for l in data])
		open(dst, 'w').write(data)
		print (src, dst, len(chapters))
