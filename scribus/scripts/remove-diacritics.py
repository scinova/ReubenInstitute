#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import sys
import re
import scribus

if not scribus.haveDoc():
	scribus.messageBox('Error', 'No document opened')
	sys.exit(1)
if scribus.selectionCount() != 1:
	scribus.messageBox('Error', 'Select one text frame')
	sys.exit(1)
frame = scribus.getSelectedObject()
if scribus.getObjectType(frame) != 'TextFrame':
	scribus.messageBox('Error', 'Select a text frame')
	sys.exit(1)
content = unicode(scribus.getAllText())
scribus.selectText(0, 0)
all_content = unicode(scribus.getAllText())
if len(all_content) == len(content):
	scribus.messageBox('Error', 'Select some text')
	sys.exit(1)
if all_content.count(content) != 1:
	scribus.messageBox('Error', 'Select more unique text')
	sys.exit(1)

#scribus.setRedraw(False)
pos = all_content.find(content)

#prefix = 'SC '
scribus.selectText(pos, len(content))
#scribus.setCharacterStyle(prefix + 'regular', frame)

#P = u'[\u05b0-\u05bc\u05c1\u05c2\u05c7]'
#C = u'[\u0591-\u05af\u05bd\u05bf]'
#L = u'[\u05d0-\u05ea]'

scribus.deleteText()
out = re.sub(u'[\u05b0-\u05bc]+', '', content)
scribus.insertText(out, pos)

"""styles = [
	(ur'(?<=\u05c3\s)(((?:[\u05d0-\u05e0])|(?:[\u05d8-\u05e0][\u05d0-\u05d8]))\u00a0)', prefix + 'verse no'),
	(ur'(?<=^)(((?:[\u05d0-\u05e0])|(?:[\u05d8-\u05e0][\u05d0-\u05d8]))\u00a0)', prefix + 'verse no'),
	(u'[\u0591-\u05af\u05bd]+', prefix + 'cantillation'),
	(u'[\u05c0\u05c3]+', prefix + 'cantillation small'),
	(u'[\u2018\u2019\u201c\u201d\:\;\,\.\-]+', prefix + 'punctuation')
	]

c = 0
for pattern, style in styles:
	p = re.compile(pattern)
	r = re.finditer(p, content)
	for i in reversed(tuple(r)):
		scribus.selectText(pos + i.start(), i.end() - i.start(), frame)
		scribus.setCharacterStyle(style, frame)
		c += 1"""
scribus.selectText(0, 0)
scribus.setRedraw(True)
scribus.docChanged(True)
sys.exit()
