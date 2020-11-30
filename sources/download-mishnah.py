import sys
sys.path.append('..')
import common
import os

for i in range(len(common.Mishnah)):
	for t in common.Mishnah[i].books:
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
