#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import re
import scribus
import unicodedata

if not scribus.haveDoc():
	scribus.messageBox('Error', 'No document opened')
	sys.exit(1)
if scribus.selectionCount() == 1:
	frame = scribus.getSelectedObject()
	if scribus.getObjectType(frame) != 'TextFrame':
		scribus.messageBox('Error', 'No text frame selected')
		sys.exit(1)
else:
	scribus.messageBox('Error', 'Select one text frame')
	sys.exit(1)

content = unicode(scribus.getAllText(frame))

scribus.setRedraw(False)
i = 0
replacements = 0
for letter in content:
	d = unicodedata.normalize('NFD', letter)
	if d == letter:
		i += 1
		continue
	replacements += 1
	scribus.selectText(i, 1)
	scribus.deleteText()
	scribus.insertText(d, i)
	i += len(d)

scribus.messageBox("", str(replacements) + ' replacements')
scribus.setRedraw(True)
scribus.docChanged(True)
