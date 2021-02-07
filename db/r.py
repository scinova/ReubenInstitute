import os
import sys
sys.path.append('..')
import common

for book in common.tanakh.books[:5]:
	for chapter in book.chapters:
		f = 'onkelos/%01d.%02d.txt'%(book.number, chapter.number)
		lines = open(f).readlines()
		#lines = data.split('\n')
		if len(chapter.verses) != len(lines):
		#if True:
			print (f, 'verses:%d'%len(chapter.verses), 'lines:%d'%len(lines))

			"""
			for idx, verse in enumerate(chapter.verses, start=1):
				print (idx)
				print (verse.rashi_text)
				print ('-----')
				#print (lines[idx - 1])
				#print ('=====')
			"""
		#exit()
			#open(f, 'a').write('\n')


"""files = os.listdir('rashi')

files.sort()

for f in files:
	data = open("rashi/" + f).read()
	print (f, len(data), data.endswith('\n'))
"""	