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

replacements = [
    # open/closed portion
#	(u'(\u05c3)\s\((\u05e1)\)\s', ur'\1\u00a0\2\n'),
#	(u'(\u05c3)\s\((\u05e4)\)\s', ur'\1\u00a0\2\n\n'),
    # verse no
	(u'((?:^)|(?:\u05c3\s)|(?:\r))' +
		u'((?:[\u05d0-\u05e0])|(?:[\u05d8-\u05e0][\u05d0-\u05d8]))' +
		u'(?=[\u05d0-\u05ea][\u0591-\u05bf])', ur'\1\2\u00a0'),
    # chapter no
	(u'(\r)([\u05d8-\u05e0])\u05f4([\u05d0-\u05d8])(\r)', ur'\r\2\3\u00a0'),
	(u'(\r)([\u05d0-\u05e0])\u05f3(\r)', ur'\r\2\u00a0'),
	# new lines
	(u'\r', ur'\u00a0')
	]
	
for pattern, text in replacements:
	content = unicode(scribus.getAllText(frame))
	p = re.compile(pattern)#, flags=re.M)
	r = re.finditer(p, content)
	for i in reversed(tuple(r)):
		length = i.end() - i.start()
		if length != 0:
			scribus.selectText(i.start(), length, frame)
			scribus.deleteText(frame)
		out = i.expand(text)
		scribus.insertText(out, i.start(), frame)
scribus.setRedraw(True)
scribus.docChanged(True)
