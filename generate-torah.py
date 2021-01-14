#!/usr/bin/env python
# -*- coding: utf-8  -*-

from scribus import *
import re

newDocument((135, 205), (15, 15, 15, 15), PORTRAIT, 1, UNIT_MILLIMETERS, PAGE_1, 0, 1)

setUnit(UNIT_PT)
#normalFont = "Ezra SIL Regular"
scriptFont = "SBL Hebrew Regular"
#createCharStyle("info", "Miriam CLM Bold", 10)
createCharStyle("title", "Hadasim CLM Regular", 22)
#createCharStyle("subtitle", "Hadasim CLM Regular", 9)
#createCharStyle("subtitle large", "Hadasim CLM Regular", 15)
#createCharStyle("S regular", normalFont, 12, '', 'Red', 100, '', 100, 0, 0, 0, 0, 0, 0 ,0, 0, 1, 1, 0)
#createCharStyle("S holly", normalFont, 12)
#createCharStyle("S cantillation", normalFont, 12)
createCharStyle("SC regular", scriptFont, 15)
createCharStyle("SC holly", scriptFont, 15)
createCharStyle("SC cantillation", scriptFont, 15)
createParagraphStyle("poem", 0, 17, 1, 0, 0, 0, 6, 0, 0, 0, 0)

pageWidth, pageHeight = getPageSize()
marginTop, marginLeft, marginRight, marginBottom = getPageMargins()

#setRedraw(False)
frame = createText(marginLeft, marginTop, pageWidth - marginLeft - marginRight, pageHeight - marginTop - marginBottom, '1')


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
	

#setCharacterStyle("SC regular", frame)
#setTextDirection(DIRECTION_RTL, frame)
#setRedraw(True)
