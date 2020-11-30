import os
import sys

sys.path.append('..')
import common

for book in common.Bible[:5]:
	cmd = 'wget "https://www.sefaria.org.il/download/version/Onkelos %s - he - Onkelos %s.txt" -O onkelos/%s.txt'%(book.name, book.name, book.name)
	os.system(cmd)