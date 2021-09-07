for c in range(12, 51):

	src = '../tanakh/%02d.%03d.txt'%(1, c)
	data = open(src).read()
	num_lines = len(data.split('\n')) - 1
	print (src, num_lines)
	s = ''.join(num_lines * ['\n'])
#	print (len(s))
#	continue
	f = '1.%02d.txt'%c
	open('../onkelost/' + f, 'w').write(s)
	f = '1.%02d.txt'%c
	open('../jerusalmit/' + f, 'w').write(s)
	f = '01.%03d.txt'%c
	open('../headings/' + f, 'w').write(s)