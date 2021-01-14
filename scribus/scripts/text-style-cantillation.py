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
occurences = all_content.count(content)
if not occurences == 1:
	scribus.messageBox('Error', 'Select more unique text')
	sys.exit(1)

#scribus.setRedraw(True)
#sys.exit()
scribus.setRedraw(False)
pos = all_content.find(content)

prefix = 'SC '
scribus.selectText(pos, len(content))
scribus.setCharacterStyle(prefix + 'regular', frame)
scribus.selectText(0, 0)

P = u'[\u05b0-\u05bc\u05c1\u05c2\u05c7]'
C = u'[\u0591-\u05af\u05bd\u05bf]'
L = u'[\u05d0-\u05ea]'

styles = [
	#(u'(?<=^)' + 
	(ur'(?<=\u05c3\s)(((?:[\u05d0-\u05e0])|(?:[\u05d8-\u05e0][\u05d0-\u05d8]))\u00a0)' +
			u'(?=%s%s*%s*)'%(L, P, C), prefix + 'verse no'),
	(ur'(?<=^)(((?:[\u05d0-\u05e0])|(?:[\u05d8-\u05e0][\u05d0-\u05d8]))\u00a0)' +
			u'(?=%s%s*%s*)'%(L, P, C), prefix + 'verse no'),
#	(ur'(?<=\u05c3\s)(((?:[\u05d0-\u05e0])|(?:[\u05d8-\u05e0][\u05d0-\u05d8]))\u00a0)' +
#			u'(?=%s%s*%s*)'%(L, P, C), prefix + 'verse no'),
#	(ur'(?<=^)(((?:[\u05d0-\u05e0])|(?:[\u05d8-\u05e0][\u05d0-\u05d8]))\u00a0)' +
#			u'(?=%s%s*%s*)'%(L, P, C), prefix + 'verse no'),
	(u'[\u0591-\u05af\u05bd]+', prefix + 'cantillation')


#	(u'(?<=\r)(((?:[\u05d0-\u05e0])|(?:[\u05d8-\u05e0][\u05d0-\u05d8]))\u00a0)' +
#			u'(?=%s%s+%s*)'%(L, P, C), prefix + 'verse no'), # TODO: more symbols
#	(ur'(?<=\r)((?:[\u05d0-\u05e0])\u00a0)'
#			u'(?=[\u05d0-\u05ea][\u0591-\u05bf])', '-SC verse no') # TODO: more symbols
#	(ur'(?<=\r)([\u05d8-\u05e0][\u05d0-\u05d8]\u00a0)'
#			u'(?=[\u05d0-\u05ea][\u0591-\u05bf])', '-SC verse no') # TODO: more symbols
#	(ur'(?<=\u05c3\u00a0)([\u05e4\u05e1])', 'portion'),
#	(ur'(?<=\u05c3\s)' + u'((?:[\u05d0-\u05e0])|(?:[\u05d8-\u05e0][\u05d0-\u05d8]))' +
#			u'(?=\u00a0[\u05d0-\u05ea][\u0591-\u05bf])', 'verse no'), # TODO: more symbols
	]

words = [
		u'כל־אלהים',
		u'כל־אלהי'
		]
for word in words:
	pattern = ''.join(['%s%s*%s*'%(l, P, C) for l in word]) + '(?!%s)'%L
	styles.insert(0, [pattern, prefix + 'regular'])
words = [
		u'יהוה',
		u'אלהים',
		u'אלהי',
		u'אלהינו',
		u'אלהיהם',
		u'אלהיך',
		u'אדני',
		u'אדונינו'
		]
for word in words:
	pattern = ''.join(['%s%s*%s*'%(l, P, C) for l in word]) + '(?!%s)'%L
	styles.insert(0, [pattern, prefix + 'holly'])
words = [
		u'יה'
		]
for word in words:
	pattern = r'(?<=[־\s])' + ''.join(['%s%s*%s*'%(l, P, C) for l in word]) + u'(?=[\s\u05c3,])'
	styles.insert(0, [pattern, prefix + 'holly'])

c = 0
for pattern, style in styles:
	p = re.compile(pattern)
	r = re.finditer(p, content)
	for i in reversed(tuple(r)):
		scribus.selectText(pos + i.start(), i.end() - i.start(), frame)
		scribus.setCharacterStyle(style, frame)
		c += 1
scribus.setRedraw(True)
scribus.docChanged(True)
#scribus.messageBox('', str(c) + ' replacements')

sys.exit()


#def error(message):
#	scribus.messageBox('Error', message, scribus.ICON_WARNING, scribus.BUTTON_OK)
#	sys.exit(1)

#scribus.gotoPage(1)
#frame, kind, order = scribus.getPageItems()[0]
#if kind != 4:
#	error('no text object')

content = unicode(scribus.getAllText(frame))
#scribus.selectText(0, len(content), frame)
#scribus.setCharacterStyle('regular', frame)
styles = [
	(u'[\u0591-\u05af\u05bd]+', '-SC cantillation'),
#	(ur'(?<=\u05c3\u00a0)([\u05e4\u05e1])', 'portion'),
#	(ur'(?<=\u05c3\s)' + u'((?:[\u05d0-\u05e0])|(?:[\u05d8-\u05e0][\u05d0-\u05d8]))' +
#			u'(?=\u00a0[\u05d0-\u05ea][\u0591-\u05bf])', 'verse no'), # TODO: more symbols
	]


for pattern, style in styles:
	p = re.compile(pattern)
	r = re.finditer(p, content)
	for i in reversed(tuple(r)):
		scribus.selectText(i.start(), i.end() - i.start(), frame)
		scribus.setCharacterStyle(style, frame)
scribus.setRedraw(True)
scribus.docChanged(True)
