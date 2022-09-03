#!/usr/bin/env python
# -*- coding: utf-8  -*-

from scribus import *
import re
import Liturgy
from common import Span, SpanKind

data = open('/root/work/reubeninstitute/db/liturgy/Slichot.txt').read()
#data = open('/root/work/reubeninstitute/db/liturgy/ben-adam-ma-lechah-nirdam.txt').read()
#data = open('/root/work/reubeninstitute/db/liturgy/Boker.txt').read()
#data = open('/root/work/reubeninstitute/db/liturgy/Minchah.txt').read()
#data = open('/root/work/reubeninstitute/db/liturgy/Shacharit.txt').read()
sections = Liturgy.something(data, 1)
#prayer = Liturgy.Prayer(Liturgy.Time.SHAHARIT)
#text = prayer.variant(prayer.text, 0)

#openDoc('/root/SIDDUR.sla')
#newDocument((135, 205), (10, 10, 10, 10), PORTRAIT, 1, UNIT_MILLIMETERS, PAGE_1, 0, 1)
newDocument((116, 165), (10, 10, 13, 8), PORTRAIT, 1, UNIT_MILLIMETERS, PAGE_1, 0, 1)
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
	["h1", serif, 22, 'Orange'],
	["h2", serif, 18, 'Orange'],
	["h4", serif, 22, 'Orange'],
	["bold", serif, 15, 'Blue'],
	["majuscule", serif, 18, 'Black'],
	["minuscule", serif, 12, 'Black'],
	["addition", serif, 12, 'Silver'],
	["explanation", serif, 12, 'Blue'],
	["correction", serif, 12, 'Black'],
	["info", sans, 12, 'DarkGreen'],
	["scripture", serif, 16, 'DarkRed'],
	["accent", serif, 16, 'DarkRed'],
	["point", serif, 16, 'DarkRed'],
	["link", serif, 10, 'Silver'],
	["verseno", serif, 10, 'Silver'],
#	["points", serif, 15, 'Green'],
#	["accents", serif, 15, 'Red'],
	["punctuation", serif, 15, 'Blue'],
	["plain", serif, 15, 'Black']]
for name, font, size, fillcolor in charstyles:
	createCharStyle(name, font, size, fillcolor=fillcolor)

#createParagraphStyle("poem", linespacingmode=0, linespacing=17, alignment=1,
#		leftmargin=0, rightmargin=0, gapbefore=0, gapafter=6,
#		firstindent=0, hasdropcap=0, dropcaplines=0, dropcapoffset=0)
#createParagraphStyle("link", alignment=ALIGN_CENTERED)
#createParagraphStyle("centered", alignment=ALIGN_CENTERED)
#createParagraphStyle("justified", alignment=ALIGN_BLOCK)
#"""

createParagraphStyle("Default Paragraph Style", linespacingmode=0, linespacing=16, alignment=ALIGN_RIGHT, gapafter=7)
createParagraphStyle("block", linespacingmode=1, alignment=ALIGN_BLOCK)
createParagraphStyle("optional", linespacingmode=0, linespacing=16, alignment=ALIGN_RIGHT, gapafter=7)
#createParagraphStyle("centered", linespacingmode=1, alignment=ALIGN_CENTERED)
#createParagraphStyle("justified", linespacingmode=1, alignment=ALIGN_BLOCK)

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
	for outerblock in section:
		for block in outerblock.blocks:
			blockpos = getTextLength(frame)
			for line in block.lines:
				for span in line:
					value = span.value
					if span.kind == SpanKind.ADDITION:
						value = '[%s]'%value
					if span.kind in [SpanKind.EXPLANATION, SpanKind.LINK]:
						value = '[%s]'%value
					if span.kind == SpanKind.VERSENO:
						value = '%s '%value
					pos = getTextLength(frame)
					insertText(value, pos, frame)
					selectText(pos, len(value), frame)
					print (span.kind.name.lower())
					setCharacterStyle(span.kind.name.lower(), frame)
				if line != block.lines[-1]:
					insertText('\u2028', getTextLength(frame), frame)
			insertText('\n', getTextLength(frame), frame)

			#sspans = [span for span in line if span.kind == SpanKind.SCRIPTURE]
			#vspans = [span for span in line if span.kind == SpanKind.VERSENO]
			#print (len(vspans), len(sspans))
			#if len(vspans) > 1 and len(sspans) > len(vspans):
			#	style = "justified"
			#else:
			#	style = "centered"
				
			#pos = getTextLength(frame)
			#selectText(blockpos, pos - blockpos, frame)
			#setParagraphStyle(style, frame)
setTextDirection(DIRECTION_RTL, frame)

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
