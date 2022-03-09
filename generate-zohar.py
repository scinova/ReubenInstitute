#!/usr/bin/env python
# -*- coding: utf-8  -*-

from scribus import *
import re
import Zohar
import Aramaic

aramaic = Aramaic.Aramaic()


newDocument((135, 205), (15, 15, 15, 15), PORTRAIT, 1, UNIT_MILLIMETERS, PAGE_1, 0, 1)
#setUnit(UNIT_PT)
defaultFont = "ReuvenSerif Regular"
normalFont = "Shlomo Regular"
normalFont = "ReuvenSerif Regular"
scriptFont = "SBL Hebrew Regular"
scriptFont = "Hadasim CLM Bold"

defineColorRGB("Silver", 0xcc, 0xcc, 0xcc)
defineColorRGB("DarkRed", 0x99, 0x00, 0x00)

createCharStyle("Default Character Style", scriptFont, 12, fillcolor='Black')
createParagraphStyle("Default Paragraph Style", linespacingmode=0, linespacing=14, alignment=ALIGN_BLOCK)#, direction=DIRECTION_RTL)
createCharStyle("plain", normalFont, 12, fillcolor='Black')
createCharStyle("link", normalFont, 12, fillcolor='Blue')
createCharStyle("citation", scriptFont, 12, fillcolor='DarkRed')
createCharStyle("synonym", normalFont, 12, fillcolor='Silver')
createCharStyle("explanation", normalFont, 12, fillcolor='Silver')
createCharStyle("correction", normalFont, 12, fillcolor='Silver')

pageWidth, pageHeight = getPageSize()
marginTop, marginLeft, marginRight, marginBottom = getPageMargins()
frame = createText(marginLeft, marginTop, pageWidth - marginLeft - marginRight, pageHeight - marginTop - marginBottom, '1')

#for p in range(2, 120):
#<->print("page %s"%p)
#	newPage(-1)
#	frame = createText(marginLeft, marginTop, pageWidth - marginLeft - marginRight, pageHeight - marginTop - marginBottom, '%d'%p)
#	linkTextFrames('%s'%(p - 1), '%s'%p)

def addText(frame, text, charStyle=None):#, paragraphStyle=None):
	#length = len(unicode(text))
	length = len(text)
	pos = getTextLength(frame)
	insertText(text, pos, frame)
	selectText(pos, length, frame)
	if charStyle:
		setCharacterStyle(charStyle, frame)
#	if paragraphStyle:
#		setStyle(paragraphStyle, frame)
#	setTextDirection(DIRECTION_RTL, frame)

setRedraw(False)

zohar = Zohar.Zohar()
articles = zohar.books[2].chapters[27].articles
scribus.progressTotal(len(articles))
scribus.progressReset()
progress = 0
for article in articles:
	p = article.text.split('\n\n\n')
	t = article.translation.split('\n\n\n')
	paragraphs = []
	for i in range(len(t)):
		paragraphs.append(p[i])
		paragraphs.append(t[i])
	for paragraph in paragraphs:
		lines = paragraph.split('\n\n')
		for line in lines:
			spans = article.parse(line)
			for span in spans:
				value = span.value
				if span.kind == Zohar.SpanKind.SYNONYM:
					value = '(=%s)'%value
					style = "synonym"
				elif span.kind == Zohar.SpanKind.EXPLANATION:
					value = '(~%s)'%value
					style = "explanation"
				elif span.kind == Zohar.SpanKind.CORRECTION:
					value = '[%s]'%value
					style = "correction"
				elif span.kind == Zohar.SpanKind.CITATION:
					value = '“%s”'%value
					style = 'citation'
				elif span.kind == Zohar.SpanKind.LINK:
					continue
					value = '(%s)'%value
					style = 'link'
				else:
					value = aramaic.spell(value)
					style = 'plain'
				addText(frame, value, style)
			addText(frame, '\n')
		addText(frame, '\n')
	progress += 1
	scribus.progressSet(progress)


p = 1
while textOverflows(str(p)):
	newPage(-1)
	p += 1
	f = createText(marginLeft, marginTop, pageWidth - marginLeft - marginRight, pageHeight - marginTop - marginBottom, '%d'%p)
	linkTextFrames('%s'%(p - 1), '%s'%p)
setTextDirection(DIRECTION_RTL, '1')



setRedraw(True)
#saveDocAs('zohar.sla')
#pdf = PDFfile()
#pdf.file = 'zohar.pdf'
#pdf.save()

"""
exit()

for p in range(2, 31)
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
#for x in range(0, 18, 2):
#	messageBox('', paragraphs[x] + str(len(paragraphs[x])))
#	selectText(indexes[x], len(paragraphs[x]) + 1, frame)
#	setCharacterStyle("S regular", frame)


#for i in range(1, len(paragraphs)):
#	paragraph = paragraphs
#	offset += len(paragraphs[
	

#setRedraw(True)
"""