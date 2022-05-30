#!/usr/bin/env python
# -*- coding: utf-8  -*-

from scribus import *
import re
import Liturgy
from common import Span, SpanKind

prayer = Liturgy.Prayer(Liturgy.Time.SHAHARIT)
text = prayer.variant(prayer.text, 0)

openDoc('/root/SIDDUR.sla')
"""newDocument((135, 205), (10, 10, 10, 10), PORTRAIT, 1, UNIT_MILLIMETERS, PAGE_1, 0, 1)
setRedraw(False)
setUnit(UNIT_PT)
defineColorRGB("Orange", 255, 165, 0)
defineColorRGB("DarkRed", 0xc0, 0, 0)
defineColorRGB("Silver", 0xcc, 0xcc, 0xcc)
font = "SBL Hebrew Regular"
charstyles = [
	["Default Character Style", 'ReuvenSerif Regular', 15, 'Black'],
	["title", "Hadasim CLM Regular", 22, 'Orange'],
	["subtitle", "Hadasim CLM Regular", 15, 'Orange'],
	["link", font, 10, 'Blue'],
	["regular", font, 15, 'Black'],
	["holly", font, 15, 'Black'],
	["cantillation", font, 15, 'Red']]
for name, font, size, fillcolor in charstyles:
	createCharStyle(name, font, size, fillcolor=fillcolor)
createParagraphStyle("poem", linespacingmode=0, linespacing=17, alignment=1,
		leftmargin=0, rightmargin=0, gapbefore=0, gapafter=6,
		firstindent=0, hasdropcap=0, dropcaplines=0, dropcapoffset=0)
createParagraphStyle("link", alignment=ALIGN_CENTERED)
createParagraphStyle("centered", alignment=ALIGN_CENTERED)
createParagraphStyle("justified", alignment=ALIGN_BLOCK)
"""

def add_text(frame, text, char_style=None, paragraph_style=None):
	length = len(text)
	pos = getTextLength(frame)
	insertText(text, pos, frame)
	selectText(pos, length, frame)
	if char_style:
		setCharacterStyle(char_style, frame)
	if paragraph_style:
		setStyle(paragraph_style, frame)

pageWidth, pageHeight = getPageSize()
marginTop, marginLeft, marginRight, marginBottom = getPageMargins()
frame = createText(marginLeft, marginTop, pageWidth - marginLeft - marginRight, pageHeight - marginTop - marginBottom, '1')
setTextDirection(DIRECTION_RTL, frame)
#createMasterPage('left')
#createMasterPage('right')

for paragraph in text.split('\n\n\n'):
	for span in prayer.parse(paragraph):
		value = span.value
		#value = re.sub('\u05bd', '', value)
		length = len(value)
		pos = getTextLength(frame)
		insertText(value, pos, frame)
		selectText(pos, length, frame)
		print (span.kind, span.value)
		is_title = (span.kind == SpanKind.TITLE)
		is_subtitle = (span.kind == SpanKind.SUBTITLE)
		if is_title:
			setCharacterStyle("title", frame)
		elif is_subtitle:
			setCharacterStyle("subtitle", frame)
#			setStyle("centered", frame)
#		elif is_subtitle:
#			setCharacterStyle("subtitle", frame)
#			setStyle("centered", frame)
#		else:
#			setCharacterStyle("regular", frame)
#			setStyle("justified", frame)
setTextDirection(DIRECTION_RTL, frame)

#selectText(0, getTextLength(frame), frame)
#content = unicode(getAllText(frame))
#for i in reversed(tuple(re.finditer(u'[\u0591-\u05af\u05bd\u05c3]+', content))):
#	print ("XXX", i.start(), i.end() - i.start(), len(content))
#	selectText(i.start(), i.end() - i.start(), frame)
#	setCharacterStyle('cantillation', frame)

p = 1
while textOverflows(str(p)):
	newPage(-1)
	p += 1
	f = createText(marginLeft, marginTop, pageWidth - marginLeft - marginRight, pageHeight - marginTop - marginBottom, '%s'%p)
	linkTextFrames('%s'%(p - 1), '%s'%p)

setRedraw(True)
saveDocAs('/root/siddur-out.sla')
pdf = PDFfile()
pdf.file = '/sdcard/Download/siddur.pdf'
pdf.save()
