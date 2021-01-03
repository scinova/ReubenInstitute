import re

for i in range(1, 151):
	filename = '27.%03d.txt'%i
	data = open(filename).read()
	out = re.sub("\s*׀ ", " ׀ ",  data)
	if len(data) != len(out):
		open(filename, 'w').write(out)
		print (filename)
