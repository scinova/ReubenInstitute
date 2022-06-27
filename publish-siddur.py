#!/usr/bin/env python
# -*- coding: utf-8  -*-

from scribus import *
import re
import Liturgy
from common import Span, SpanKind

data = open('/root/work/reubeninstitute/db/liturgy/Minchah.txt').read()
#data = open('/root/work/reubeninstitute/db/liturgy/Shacharit.txt').read()
sections = Liturgy.something(data, 1)
#prayer = Liturgy.Prayer(Liturgy.Time.SHAHARIT)
#text = prayer.variant(prayer.text, 0)

#openDoc('/root/SIDDUR.sla')
newDocument((135, 205), (10, 10, 10, 10), PORTRAIT, 1, UNIT_MILLIMETERS, PAGE_1, 0, 1)
setRedraw(False)
setUnit(UNIT_PT)
defineColorRGB("Orange", 255, 165, 0)
defineColorRGB("DarkRed", 0xc0, 0, 0)
defineColorRGB("Silver", 0xcc, 0xcc, 0xcc)
defineColorRGB("DarkGreen", 0x33, 0xcc, 0x33)

serif = "ReuvenSerif Regular"
sans = "Nachlieli CLM Light"
charstyles = [
	["Default Character Style", serif, 15, 'Black'],
	["h1", sans, 22, 'Orange'],
	["h2", sans, 18, 'Orange'],
	["h4", sans, 15, 'Orange'],
	["initial", serif, 15, 'Blue'],
	["explanation", sans, 12, 'Silver'],
	["info", sans, 12, 'DarkGreen'],
	["citation", serif, 16, 'DarkRed'],
	["link", sans, 10, 'Red'],
	["regular", serif, 15, 'Black'],
	["holly", serif, 15, 'Black'],
	["cantillation", serif, 15, 'Red']]
for name, font, size, fillcolor in charstyles:
	createCharStyle(name, font, size, fillcolor=fillcolor)

createParagraphStyle("Default Paragraph Style", linespacingmode=1, linespacing=17, alignment=ALIGN_CENTERED, gapafter=0)
#createParagraphStyle("poem", linespacingmode=0, linespacing=17, alignment=1,
#		leftmargin=0, rightmargin=0, gapbefore=0, gapafter=6,
#		firstindent=0, hasdropcap=0, dropcaplines=0, dropcapoffset=0)
#createParagraphStyle("link", alignment=ALIGN_CENTERED)
#createParagraphStyle("centered", alignment=ALIGN_CENTERED)
#createParagraphStyle("justified", alignment=ALIGN_BLOCK)
#"""

createParagraphStyle("optional", linespacingmode=0, linespacing=17, alignment=ALIGN_BLOCK, gapafter=6)

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

for section in sections:
	for block in section:
		for span in block.spans:
			value = span.value
			if span.kind == SpanKind.ADDITION:
				value = '[%s]'%value
			if span.kind == SpanKind.EXPLANATION:
				value = '[%s]'%value
			#value = re.sub('\u05bd', '', value)
			length = len(value)
			pos = getTextLength(frame)
			insertText(value, pos, frame)
			selectText(pos, length, frame)
			print (span.kind, span.value)
			if span.kind == SpanKind.H1:
				setCharacterStyle("h1", frame)
				insertText('\n', getTextLength(frame), frame)
			elif span.kind == SpanKind.H2:
				setCharacterStyle("h2", frame)
				insertText('\n', getTextLength(frame), frame)
			elif span.kind == SpanKind.H4:
				setCharacterStyle("h4", frame)
				insertText('\n', getTextLength(frame), frame)
			elif span.kind == SpanKind.BOLD:
				setCharacterStyle("initial", frame)
			elif span.kind == SpanKind.ADDITION:
				setCharacterStyle("explanation", frame)
			elif span.kind == SpanKind.EXPLANATION:
				setCharacterStyle("explanation", frame)
			elif span.kind == SpanKind.INFO:
				setCharacterStyle("info", frame)
			elif span.kind == SpanKind.CITATION:
				setCharacterStyle("citation", frame)
			else:
				setCharacterStyle("regular", frame)

		insertText('\n', getTextLength(frame), frame)

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
