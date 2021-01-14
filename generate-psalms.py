#!/usr/bin/env python
# -*- coding: utf-8  -*-

from scribus import *
import re
from hebrew_numbers import *

newDocument((135, 205), (15, 15, 10, 15), PORTRAIT, 1, UNIT_MILLIMETERS, PAGE_1, 0, 1)

setUnit(UNIT_PT)

font = "SBL Hebrew Regular"

createCharStyle("title", "Hadasim CLM Regular", 22)
createCharStyle("regular", font, 15)
createCharStyle("holly", font, 15)
createCharStyle("cantillation", font, 15)
createParagraphStyle("poem", 0, 17, 1, 0, 0, 0, 6, 0, 0, 0, 0)

pageWidth, pageHeight = getPageSize()
marginTop, marginLeft, marginRight, marginBottom = getPageMargins()

#setRedraw(False)
frame = createText(marginLeft, marginTop, pageWidth - marginLeft - marginRight, pageHeight - marginTop - marginBottom, '1')

createMasterPage('left')
createMasterPage('right')

for p in range(2, 15):
	newPage(-1)
	frame = createText(marginLeft, marginTop, pageWidth - marginLeft - marginRight, pageHeight - marginTop - marginBottom, '%s'%p)
	linkTextFrames('%s'%(p - 1), '%s'%p)

content = ""
for c in range(1, 15):
	title = int_to_gematria(c)
	content += title + '\n'
	data = unicode(open('/home/robert/MachonReuven/db/tanakh/27.%03d.txt'%c).read())
	data = re.sub('{[^}]+} ', '', data)
	data = re.sub('{{[^}]+}} ', '', data)
	content += data + '\n'

setText(content, frame)
selectText(0, len(content), frame)
setCharacterStyle("regular", frame)
setStyle("poem", frame)
setTextDirection(DIRECTION_RTL, frame)


#p = 2
#while textOverflows(frame):
#	newPage(-1)
#	frame = createText(marginLeft, marginTop, pageWidth - marginLeft - marginRight, pageHeight - marginTop - marginBottom, '%s'%p)
#	linkTextFrames('%s'%(p - 1), '%s'%p)
#	p += 1

pdf = PDFfile()
pdf.file = 'psalms.pdf'
pdf.save()





#while True:
#	if not textOverflows(frame):
#		break
#	newPage(-1)
#	frame = createText(marginLeft, marginTop, pageWidth - marginLeft - marginRight, pageHeight - marginTop - marginBottom, '%s'%pageCount())
#	linkTextFrames('%s'%(pageCount() - 1), '%s'%pageCount())

#saveDocAs('2.sla')

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
