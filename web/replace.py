import sys
sys.path.append('..')
import common
import re


replacements = [l.split(' ') for l in open('replacements.txt').read().split('\n')]
replacements.sort(key=lambda x: -len(x[0]))
#print (replacements)
#exit()

for book in common.Zohar:
	for chapter in book.chapters:
		for article in chapter.articles:
			f = '../db/zohar/%1d.%02d/%02dt.txt'%(book.ind, chapter.no, article.no)
			print (f)
			data = open(f).read()
			ll = len(data)
			for src, dst in replacements:
				items = list(reversed(tuple(re.finditer('(?<=[^\u0591-\u05ea])(%s)(?=[^\u0591-\u05ea])'%src, data, flags=re.M))))
#				items = list(reversed(tuple(re.finditer(						'^(%s)(?=[\s\,\.\:\!\?\;\'\")~_])'%src, data, flags=re.M)))) +\
#					list(reversed(tuple(re.finditer('(?<=[\s\(\,\.\:\;\?\)\'\"~_])(%s)(?=[\s\,\.\:\!\?\;\'\")~_])'%src, data, flags=re.M)))) +\
#					list(reversed(tuple(re.finditer('(?<=[\s\(\,\.\:\;\?\)\'\"~_])(%s)$'%src, data, flags=re.M))))
				for item in items:
					orig = data[item.start() : item.end()]
					print (src, item.start(), item.end(), 'x%sy'%(orig), dst)
					data = data[:item.start()] + dst + data[item.end():]
			print (ll, len(data))
			open(f, 'w').write(data)
