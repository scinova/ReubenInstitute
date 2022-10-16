import sys
sys.path.append('..')
import Mishnah
import re
import unicodedata

for order_nr, order in enumerate(Mishnah.orders, start=1):
	for trac_nr, trac in enumerate(order.tractates, start=1):
		src = 'bartenura/%s.txt'%(trac.latin_name)
		dst = '../db/bartenura/%1d.%02d.txt'%(order_nr, trac_nr)
		data = open(src, newline='').read()
		data = re.sub('\nMishnah [0-9]+\n\n', '\n', data)
		chapters = re.split('\n\nChapter [0-9]+\n\n\n\n', data)[1:]
		
		if order_nr == 1 and trac_nr == 11:
			chapters = chapters[:-1]
		
		print (order_nr, trac_nr, src, dst, len(chapters))

#		data = '\n'.join(chapters[:])
#		data = ''.join([unicodedata.normalize('NFD', l) for l in data])

		data = [c.replace('\n\n', 'X').replace('\n', '\u2028').replace('X', '\n').replace('\n\n', '\n-\n') for c in chapters]

		for c, cd in enumerate(data, start=1):
			num_verses = len(Mishnah.orders[order_nr - 1].tractates[trac_nr - 1].chapters[c - 1].verses)
			diff = num_verses - len(cd.split('\n'))
			if diff:
				print ("DIFF", diff)
				data[c - 1] += diff * '\n-'
			#for v, vd in enumerate(cd):
		out = '\n\n'.join(data)

		open(dst, 'w').write(out)
