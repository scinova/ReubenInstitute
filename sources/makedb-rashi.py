import sys
sys.path.append('..')
import common
import re

for i in range(len(common.Bible)):
	book = common.Bible[i]
	src = 'rashi/%02d.txt'%(book.ind)
	data = open(src, newline='').read()
	chapters = re.split('\nChapter [0-9]+\n\n', data)[1:]
	for c in range(len(chapters)):
		chapter = chapters[c]
		verses = re.split('\n\nVerse [0-9]+\n\n', chapter)[1:]
		out = '\n'.join([verse.replace('\n', ' ') for verse in verses])
		dst = '../db/rashi/%02d.%03d.txt'%(i + 1, c + 1)
		open(dst, 'w').write(out)
		print (c + 1, len(verses), dst)

