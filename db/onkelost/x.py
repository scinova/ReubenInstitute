import sys
sys.path.append('../..')
import common


for b in range(5):
	book = common.tanakh.books[b]
	print (book.number)
