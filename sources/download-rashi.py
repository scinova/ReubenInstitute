import os
import sys
sys.path.append('..')
import common

for book in common.Bible:
	name = book.name.replace('Samuel 1', 'I Samuel').replace('Samuel 2', 'II Samuel').replace('Kings 1', 'I Kings').replace('Kings 2', 'II Kings')
	name = name.replace('Chronicles 1', 'I Chronicles').replace('Chronicles 2', 'II Chronicles')
	cmd = 'wget "https://www.sefaria.org.il/download/version/Rashi on %s - he - merged.plain.txt" -O "rashi/%02d.txt"'%(name, book.ind)
	os.system(cmd)
