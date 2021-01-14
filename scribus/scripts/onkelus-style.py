#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import re
import scribus

def error(message):
	scribus.messageBox('Error', message, scribus.ICON_WARNING, scribus.BUTTON_OK)
	sys.exit(1)

scribus.gotoPage(3)
frame, kind, order = scribus.getPageItems()[0]
if kind != 4:
	error('no text object')

content = unicode(scribus.getAllText(frame))
scribus.selectText(0, len(content), frame)
scribus.setCharacterStyle('regular', frame)
styles = [
#	(ur'[\u0591-\u05af\u05bd]+', 'cantillation'),
#	(ur'(?<=\u003a\u00a0)([\u05e4\u05e1])', 'portion'),
	(ur'(?<=\u003a\u00a0)' + u'((?:[\u05d0-\u05e0])|(?:[\u05d8-\u05e0][\u05d0-\u05d8]))' +
			u'(?=\u00a0[\u05d0-\u05ea][\u0591-\u05bf])', 'verse no'), # TODO: more symbols
	]
for pattern, style in styles:
	p = re.compile(pattern)
	r = re.finditer(p, content)
	for i in reversed(tuple(r)):
		scribus.selectText(i.start(), i.end() - i.start(), frame)
		scribus.setCharacterStyle(style, frame)
scribus.setRedraw(True)
scribus.docChanged(True)
