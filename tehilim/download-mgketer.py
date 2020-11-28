import common
import os

for i in range(len(common.books)):
	ename, chapters, hname = common.books[i]
	for c in range(1, chapters + 1):
		cmd = 'wget "https://www.mgketer.org/study/mikraseferperek?SeferNum=%d&PerekNum=%d&mnt=3" -O mgketer/%02d.%03d.html'%(i, c, i+1, c)
		os.system(cmd)
