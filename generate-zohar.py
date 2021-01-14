#!/usr/bin/env python
# -*- coding: utf-8  -*-

from scribus import *
import re

#newDocument((135, 205), (15, 15, 15, 15), PORTRAIT, 1, UNIT_MILLIMETERS, PAGE_1, 0, 1)
#setUnit(UNIT_PT)
#normalFont = "Shlomo Regular"
#scriptFont = "SBL Hebrew Regular"
#createCharStyle("regular", normalFont, 12)
#createCharStyle("citation", scriptFont, 12)
pageWidth, pageHeight = getPageSize()
marginTop, marginLeft, marginRight, marginBottom = getPageMargins()
frame = createText(marginLeft, marginTop, pageWidth - marginLeft - marginRight, pageHeight - marginTop - marginBottom, '1')
setText("כקכםכק כקם'עק'", frame)
setCharacterStyle("regular", frame)
setTextDirection(DIRECTION_RTL, frame)
#setRedraw(False)

exit()

for p in range(2, 31):
#	print("page %s"%p)
	newPage(-1)
	frame = createText(marginLeft, marginTop, pageWidth - marginLeft - marginRight, pageHeight - marginTop - marginBottom, '%s'%p)
	linkTextFrames('%s'%(p - 1), '%s'%p)

content = ""
for c in range(1, 5):
#	print("chapter %s"%c)
#for c in range(1, 151):
	#messagebarText(str(c))
	data = unicode(open('/home/robert/MachonReuven/bible/src/01.%03d.txt'%c).read())
	data = re.sub('{[^}]+} ', '', data)
	data = re.sub('{{[^}]+}} ', '', data)
#	data = re.sub('\[[^]+\]', '', data)
#	paragraphs = data.split('\n')
	content += data + '\n'

setText(content, frame)
selectText(0, len(content), frame)
setCharacterStyle("SC regular", frame)
#setStyle("poem", frame)

#while True:
#	if not textOverflows(frame):
#		break
#	newPage(-1)
#	frame = createText(marginLeft, marginTop, pageWidth - marginLeft - marginRight, pageHeight - marginTop - marginBottom, '%s'%pageCount())
#	linkTextFrames('%s'%(pageCount() - 1), '%s'%pageCount())

saveDocAs('2.sla')

#for x in range(0, 18, 2):
#	messageBox('', paragraphs[x] + str(len(paragraphs[x])))
#	selectText(indexes[x], len(paragraphs[x]) + 1, frame)
#	setCharacterStyle("S regular", frame)


#for i in range(1, len(paragraphs)):
#	paragraph = paragraphs
#	offset += len(paragraphs[
	

#setRedraw(True)
