import re
import unicodedata

for i in range(1, 32):
	data = open('%02d.txt'%i).read()

	parts = data.split('\n\n')

	ara = [parts[x * 2] for x in range(int(len(parts) / 2))]
	heb = [parts[x * 2 + 1] for x in range(int(len(parts) / 2))]

	print ('%02d.txt'%i, len(parts), len(ara), len(heb))

	ara = '\n\n'.join(ara)
	heb = '\n\n'.join(heb)[:-1]

	ara = re.sub('\n\n', 'www', ara)
	ara = re.sub('\n', '\n\n', ara)
	ara = re.sub('www', '\n\n\n', ara)
	heb = re.sub('\n\n', 'www', heb)
	heb = re.sub('\n', '\n\n', heb)
	heb = re.sub('www', '\n\n\n', heb)

	ara = unicodedata.normalize('NFD', ara)
	heb = unicodedata.normalize('NFD', heb)
	ara = re.sub('[‘’]', "'", ara)
	ara = re.sub('[“”]', '"', ara)
	heb = re.sub('[‘’]', "'", heb)
	heb = re.sub('[“”]', '"', heb)
	print ('---------')
	print (ara)
	print ('---------')
	print (heb)
	print ('---------')

	open('../%02d.txt'%i, 'w').write(ara)
	open('../%02dt.txt'%i, 'w').write(heb)
