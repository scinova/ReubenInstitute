import sys
sys.path.append('..')
import common
import os

for order in Mishnah.orders:
	for t in order.tractates:
		name = t.name
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
		cmd = 'wget "https://www.sefaria.org.il/download/version/%s %s - he - Torat Emet 357.plain.txt" -O "mishnah/%s.txt"'%(prefix, aname, name)
		os.system(cmd)
