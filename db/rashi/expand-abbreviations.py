import re
import sys
sys.path.append('../../')
import common

if len(sys.argv) != 2:
	print ('missing filename')
	exit()

filename = sys.argv[1]

abbreviations = {}
f = open('00abbreviations.txt')
for line in f:
	p = line[:-1].split(' ')
	abbreviations[p[0]] = ' '.join(p[1:])

data = open(filename).read()
for abbreviation, replacement in abbreviations.items():
	data = re.sub(abbreviation, replacement, data)
open(filename, 'w').write(data)
