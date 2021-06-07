import os
import sys

sys.path.append('..')
import common

for book in common.tanakh.books[:5]:
	print (book.latin_name)
#https://www.sefaria.org.il/download/version/Targum%20Jonathan%20on%20Numbers%20-%20he%20-%20Targum%20Jonathan%20on%20Numbers.plain.txt
	cmd = 'wget "https://www.sefaria.org.il/download/version/Targum Jonathan on %s - he - Targum Jonathan on %s.plain.txt" -O jerusalmi/%s.txt'%(book.latin_name, book.latin_name, book.latin_name)
	os.system(cmd)                                