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

letters = []
for letter in content:
	if not letter in letters:
		letters.append(letter)
letters.sort()

output = ""
for letter in letters:
	output += str('%04X'%ord(letter)) + ' ' + unicodedata.category(letter) + ' ' + (u'\u25cc' if unicodedata.category(letter) in ['Mn'] else u'') + letter + ' ' + unicodedata.name(letter, "NONAME") + "\n"

scribus.messageBox('Output', output)
