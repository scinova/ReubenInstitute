import sys
sys.path.append('..')
import common
import os

for i in range(len(common.Bible)):
	book = common.Bible[i]
	for c in range(1, len(book.chapters) + 1):
		cmd = 'wget "https://www.mgketer.org/study/mikraseferperek?SeferNum=%d&PerekNum=%d&mnt=3" -O tanakh/%02d.%03d.html'%(i, c, i+1, c)
		os.system(cmd)
