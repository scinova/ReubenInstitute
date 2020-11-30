import sys
sys.path.append('..')
import common
import re
import unicodedata

def clean(data):
	data = re.sub('\<span class="perek-header">[^<]+\</span>', '', data)
	data = re.sub('\<span class="pasuk-header">[^<]+\</span>', '', data)
	data = re.sub('\<br class="sfpsk-br not-displayed" />', '', data)
	data = re.sub('\<br />', '', data)
	data = re.sub('\<span class="stuma"[^>]+>([^<]+)\</span>', '{ס}', data)
	data = re.sub('\<span class="ptucha"[^>]+>([^<]+)\</span>', '{פ}', data)
	data = re.sub('\<p[^>]+>\r\n', '', data)
	data = re.sub('\</p>', '', data)
	data = re.sub('\<span class="mila"[^>]+>([^<]+)\</span>', '\\1', data)
	data = re.sub('\<span class="makaf"[^>]+>([^<]+)\</span>', '\\1', data)
	data = re.sub('\<span class="pasek"[^>]+>([^<]+)\</span>', '\\1', data)
	data = re.sub('\<span[^>]+class="mila kri">([^<]+)\</span>', '\\1', data)
	data = re.sub('\<span[^>]+class="mila ktiv">([^<]+)\</span>', '[\\1]', data)
	data = re.sub('\<span[^>]+class="sfpsk"[^>]+>([^<]+)\</span>\r\n', '\u05c3', data)
	data = re.sub('\<span id="PS[^>]+>\r\n([^<]+)\</span>\r\n', '\\1\n', data)
	data = re.sub('\<span class="parashia-header">\[([^]]+)\]\</span>', '{\\1}', data)
	data = re.sub('\<span class="parasha-header">{פרשת ([^}]+)}\</span>', '{{\\1}}', data)
	data = re.sub('\r\n', ' ', data)
	data = re.sub('( )$', '', data)
	return data

for i in range(len(common.Bible)):
	book = common.Bible[i]
	for c in range(1, len(book.chapters) + 1):
		src = 'tanakh/%02d.%03d.html'%(i + 1, c)
		dst = '../db/tanakh/%02d.%03d.txt'%(i + 1, c)
		data = open(src, newline='').read()
		data = clean(data)
		data = ''.join([unicodedata.normalize('NFD', l) for l in data])
		open(dst, 'w').write(data)
		print (src, dst)
