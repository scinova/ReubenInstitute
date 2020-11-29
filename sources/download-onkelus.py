import os
import sys

sys.path.append('..')
import common

for b in common.books[:5]:
	cmd = 'wget "https://www.sefaria.org.il/download/version/Onkelos %s - he - Onkelos %s.txt" -O onkelos/%s.txt'%(b[0], b[0], b[0])
	os.system(cmd)