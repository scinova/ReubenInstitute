import sys
sys.path.append('..')
import common
import os

for i in range(len(common.mishnah)):
	for t in common.mishnah[i][2]:
		name = t[0]
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
