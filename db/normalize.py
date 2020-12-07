import sys
sys.path.append('..')
import common
import re

L = 'א-ת'
S = '\u05c1\u05c2'
D = '\u05bc'
P = '\u05b0-\u05bb\u05c7'
C = '\u0591-\u05af\u05bd'

lens = []
outs = []
for book in common.Zohar:
	for chapter in book.chapters:
		for article in chapter.articles:
			filename = 'zohar/%1d.%02d/%02d.txt'%(book.ind, chapter.no, article.no)
			data = open(filename).read()
			print (filename)
			subs = []
			for item in re.finditer('[%s][%s%s%s%s]+'%(L, S, D, P, C), data):
				out = ''
				text = item.group(0)
				word = ''
				for pattern in ['[%s]'%L, '[%s]'%S, '[%s]'%D, '[%s]'%P, '[%s]'%C]:
					for c in text:
						m = re.match(pattern, c)
						if m:
							word += m.group(0)
				if word != text:
					if [text, word] not in subs:
						subs.append([text, word])
				for c in text:
					if re.match('[%s]'%L, c):
						out += 'L'
					if re.match('[%s]'%P, c):
						out += 'P'
					if re.match('[%s]'%C, c):
						out += 'C'
					if re.match('[%s]'%S, c):
						out += 'S'
					if re.match('[%s]'%D, c):
						out += 'D'
				if out not in outs:
					outs.append(out)
				if 'PP' in out or 'DD' in out:
					print (text)
				if len(text) not in lens:
					lens.append(len(text))
			outdata = data
			for pattern, sub in subs:
				outdata = re.sub(pattern, sub, outdata)
			open(filename, 'w').write(outdata)
print (lens)
print (outs)
