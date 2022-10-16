import sys
sys.path.append('..')
import Mishnah
import os

for order in Mishnah.orders:
	for t in order.tractates:
		name = t.latin_name
		if name == 'Avot':
			prefix = 'Pirkei'
		else:
			prefix = 'Mishnah'
		if name == 'Maaserot':
			aname = 'Maasrot'
		elif name == 'Tohorot':
			aname = 'Tahorot'
		elif name == 'Uktzim':
			aname = 'Oktzin'
		else:
			aname = name
		filename = 'bartenura/%s.txt'%t.latin_name
		cmd = 'wget "https://www.sefaria.org.il/download/version/Bartenura on %s %s - he - On Your Way.plain.txt" -O "%s"'%(prefix, aname, filename)

		if not os.path.exists(filename):
			os.system(cmd)
