import os
import sys

sys.path.append('..')
import common

for book in common.tanakh.books[5:26]:
	name = book.latin_name.replace('Samuel 1', 'I Samuel').replace('Samuel 2', 'II Samuel').replace('Kings 1', 'I Kings').replace('Kings 2', 'II Kings')
	print (book.latin_name)
#https://www.sefaria.org.il/download/version/Targum%20Jonathan%20on%20Numbers%20-%20he%20-%20Targum%20Jonathan%20on%20Numbers.plain.txt
	cmd = 'wget "https://www.sefaria.org.il/download/version/Targum Jonathan on %s - he - Mikraot Gedolot.plain.txt" -O "jonathan/%s.txt"'%(name, book.latin_name)
	os.system(cmd)
                                