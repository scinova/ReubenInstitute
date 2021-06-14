#!/usr/bin/env python
# -*- coding: utf-8  -*-

from scribus import *
import re
from hebrew_numbers import *
import sys
import common
from common import Span, SpanKind

parasha = common.tanakh.books[0].parashot[0]
name = 'bereshit'

sizes = {
	'LARGE': (135, 205),
	'MEDIUM': (120, 170)
	}

newDocument(sizes['MEDIUM'], (10, 10, 10, 10), PORTRAIT, 1, UNIT_MILLIMETERS, PAGE_1, 0, 1)
setRedraw(False)
setUnit(UNIT_PT)

defineColorRGB("Orange", 255, 165, 0)
defineColorRGB("DarkRed", 0xc0, 0, 0)
defineColorRGB("Silver", 0xcc, 0xcc, 0xcc)
defineColorRGB("Gray", 0x66, 0x66, 0x66)
defineColorRGB('Green', 0x94, 0xa3, 0)

font = "SBL Hebrew Regular"
font2 = "Shlomo Regular"
createCharStyle("Default Character Style", font, 15, fillcolor='Black', language='he')
createCharStyle("chapterno", font, 10, fillcolor='Silver', language='he')
createCharStyle("verseno", font, 8, fillcolor='Silver', language='he')
createCharStyle("mikra", font, 15, fillcolor='Black', language='he')
createCharStyle("punctuation", font, 15, fillcolor='Blue', language='he')
createCharStyle("transparent", font, 15, fillcolor='White', language='he')
createCharStyle("aliya", font2, 10, fillcolor='Silver', language='he')
createCharStyle("keri", font, 15, fillcolor='Silver', language='he')
createCharStyle("majuscule", font, 20, fillcolor='Black', language='he')
createCharStyle("minuscule", font, 12, fillcolor='Black', language='he')
createCharStyle("cantillation", font, 15, fillcolor='Blue', language='he')
createCharStyle("dcantillation", font, 15, fillcolor='Red', language='he')
createCharStyle("punctuation", font, 15, fillcolor='Blue', language='he')
createCharStyle("translation", font, 12, fillcolor='Black', language='he')
createCharStyle("ttranslation", font, 9, fillcolor='Black', language='he')
createCharStyle("nonliteral", font, 12, fillcolor='Red', language='he')
createCharStyle("addition", font, 11, fillcolor='Blue', language='he')

createParagraphStyle("Default Paragraph Style", linespacingmode=1, alignment=ALIGN_BLOCK)
createParagraphStyle("mikra", linespacingmode=0, linespacing=18, alignment=ALIGN_BLOCK)
createParagraphStyle("paragraph-opened", linespacingmode=1, alignment=ALIGN_BLOCK)
createParagraphStyle("paragraph-closed", linespacingmode=1, alignment=ALIGN_BLOCK, firstindent=40)

def add_text(frame, text, char_style=None, paragraph_style=None):
	#text = common.remove_cantillations(text)
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

scribus.progressTotal(len(parasha.verses))
scribus.progressReset()
progress = 0
paragraphs = parasha.paragraphs
for paragraph in paragraphs[:6]:
	for subparagraph in paragraph:
		# MIKRA
		is_first_subparagraph = subparagraph == paragraph[0]
		if is_first_subparagraph:
			paragraph_style = 'paragraph-opened'
		else:
			paragraph_style = 'paragraph-closed'
		for verse in subparagraph:
			spans = verse.mikra
			#i = 1 * (spans[0].kind == SpanKind.ALIYA)
			spans.insert(0, Span(SpanKind.VERSENO, verse.hebrew_number))
			if verse.number == 1:
				spans.insert(0, Span(SpanKind.CHAPTERNO, verse.chapter.hebrew_number))
			for span in spans:
				# eplace he + mapik with wide he + mapik
				span.value = re.sub('\u05d4\u05bc', '\ufb23\u05bc', span.value)
				if span.kind == SpanKind.CHAPTERNO:
					add_text(frame, span.value, 'chapterno', paragraph_style)
					add_text(frame, ' ', 'transparent', paragraph_style)
				elif span.kind == SpanKind.VERSENO:
					add_text(frame, span.value, 'verseno', paragraph_style)
					add_text(frame, ' ', 'transparent', paragraph_style)
				#elif span.kind == SpanKind.ALIYA:
				#	add_text(frame, span.value, 'aliya', paragraph_style)
				#	add_text(frame, '_', 'transparent', paragraph_style)
				if span.kind == SpanKind.KRIKTIV:
					add_text(frame, span.value, 'keri', paragraph_style)
					add_text(frame, ' ' + span.alt, 'mikra', paragraph_style)
				elif span.kind == SpanKind.MAJUSCULE:
					add_text(frame, span.value, 'majuscule', paragraph_style)
				elif span.kind == SpanKind.MINUSCULE:
					add_text(frame, span.value, 'minuscule', paragraph_style)
				elif span.kind == SpanKind.PLAIN:
					add_text(frame, span.value, 'mikra', paragraph_style)
			is_last_verse = verse == subparagraph[-1]
			if not is_last_verse:
				add_text(frame, ' ')
		add_text(frame, '\n')

		# ONKELOS
		is_first_subparagraph = subparagraph == paragraph[0]
		if is_first_subparagraph:
			paragraph_style = 'paragraph-opened'
		else:
			paragraph_style = 'paragraph-closed'
		for verse in subparagraph:
			spans = verse.onkelos
			spans.insert(0, Span(SpanKind.VERSENO, verse.hebrew_number))
			if verse.number == 1:
				spans.insert(0, Span(SpanKind.CHAPTERNO, verse.chapter.hebrew_number))
			for span in spans:
				if span.kind == SpanKind.CHAPTERNO:
					add_text(frame, span.value, 'chapterno', paragraph_style)
					add_text(frame, ' ', 'transparent', paragraph_style)
				elif span.kind == SpanKind.VERSENO:
					add_text(frame, span.value, 'verseno', paragraph_style)
					add_text(frame, ' ', 'transparent', paragraph_style)
				elif span.kind == SpanKind.NONLITERAL:
					add_text(frame, span.value, 'nonliteral', paragraph_style)
				elif span.kind == SpanKind.ADDITION:
					add_text(frame, span.value, 'addition', paragraph_style)
				elif span.kind == SpanKind.PLAIN:
					add_text(frame, span.value, 'translation', paragraph_style)
			is_last_verse = verse == subparagraph[-1]
			if not is_last_verse:
				add_text(frame, ' ')
		add_text(frame, '\n')

		# ONKELOS TRANSLATION
		is_first_subparagraph = subparagraph == paragraph[0]
		if is_first_subparagraph:
			paragraph_style = 'paragraph-opened'
		else:
			paragraph_style = 'paragraph-closed'
		for verse in subparagraph:
			spans = verse.onkelos_trans
			spans.insert(0, Span(SpanKind.VERSENO, verse.hebrew_number))
			if verse.number == 1:
				spans.insert(0, Span(SpanKind.CHAPTERNO, verse.chapter.hebrew_number))
			for span in spans:
				if span.kind == SpanKind.CHAPTERNO:
					add_text(frame, span.value, 'chapterno', paragraph_style)
					add_text(frame, ' ', 'transparent', paragraph_style)
				elif span.kind == SpanKind.VERSENO:
					add_text(frame, span.value, 'verseno', paragraph_style)
					add_text(frame, ' ', 'transparent', paragraph_style)
				elif span.kind == SpanKind.NONLITERAL:
					add_text(frame, span.value, 'nonliteral', paragraph_style)
				elif span.kind == SpanKind.ADDITION:
					add_text(frame, span.value, 'addition', paragraph_style)
				elif span.kind == SpanKind.PLAIN:
					add_text(frame, span.value, 'ttranslation', paragraph_style)
			is_last_verse = verse == subparagraph[-1]
			if not is_last_verse:
				add_text(frame, ' ')
		add_text(frame, '\n')

		# JERUSALMI
		is_first_subparagraph = subparagraph == paragraph[0]
		if is_first_subparagraph:
			paragraph_style = 'paragraph-opened'
		else:
			paragraph_style = 'paragraph-closed'
		for verse in subparagraph:
			spans = verse.jerusalmi
			spans.insert(0, Span(SpanKind.VERSENO, verse.hebrew_number))
			if verse.number == 1:
				spans.insert(0, Span(SpanKind.CHAPTERNO, verse.chapter.hebrew_number))
			for span in spans:
				if span.kind == SpanKind.CHAPTERNO:
					add_text(frame, span.value, 'chapterno', paragraph_style)
					add_text(frame, ' ', 'transparent', paragraph_style)
				elif span.kind == SpanKind.VERSENO:
					add_text(frame, span.value, 'verseno', paragraph_style)
					add_text(frame, ' ', 'transparent', paragraph_style)
				elif span.kind == SpanKind.NONLITERAL:
					add_text(frame, span.value, 'nonliteral', paragraph_style)
				elif span.kind == SpanKind.ADDITION:
					add_text(frame, span.value, 'addition', paragraph_style)
				elif span.kind == SpanKind.PLAIN:
					add_text(frame, span.value, 'ttranslation', paragraph_style)
			is_last_verse = verse == subparagraph[-1]
			if not is_last_verse:
				add_text(frame, ' ')
		add_text(frame, '\n')

		# JERUSALMI TRANSLATION
		is_first_subparagraph = subparagraph == paragraph[0]
		if is_first_subparagraph:
			paragraph_style = 'paragraph-opened'
		else:
			paragraph_style = 'paragraph-closed'
		for verse in subparagraph:
			spans = verse.jerusalmi_trans
			spans.insert(0, Span(SpanKind.VERSENO, verse.hebrew_number))
			if verse.number == 1:
				spans.insert(0, Span(SpanKind.CHAPTERNO, verse.chapter.hebrew_number))
			for span in spans:
				if span.kind == SpanKind.CHAPTERNO:
					add_text(frame, span.value, 'chapterno', paragraph_style)
					add_text(frame, ' ', 'transparent', paragraph_style)
				elif span.kind == SpanKind.VERSENO:
					add_text(frame, span.value, 'verseno', paragraph_style)
					add_text(frame, ' ', 'transparent', paragraph_style)
				elif span.kind == SpanKind.NONLITERAL:
					add_text(frame, span.value, 'nonliteral', paragraph_style)
				elif span.kind == SpanKind.ADDITION:
					add_text(frame, span.value, 'addition', paragraph_style)
				elif span.kind == SpanKind.PLAIN:
					add_text(frame, span.value, 'translation', paragraph_style)
			is_last_verse = verse == subparagraph[-1]
			if not is_last_verse:
				add_text(frame, ' ')
		add_text(frame, '\n')

		progress += 1
		#scribus.progressSet(progress)
		#add_text(frame, '\n')
	add_text(frame, '\n')

setTextDirection(DIRECTION_RTL, frame)

selectText(0, getTextLength(frame), frame)
content = getAllText(frame)
cantillations = list(reversed(list(re.finditer(u'[\u0591-\u05af\u05bd\u05c3\u05c0]+', content))))
punctuations = list(reversed(list(re.finditer(u'[\.\'\!\?\;\:]+', content))))
scribus.progressTotal(len(cantillations))
scribus.progressReset()
for progress, i in enumerate(cantillations):
	selectText(i.start(), i.end() - i.start(), frame)
	setCharacterStyle('dcantillation', frame)
	scribus.progressSet(progress)
#scribus.progressTotal(len(punctuations))
#scribus.progressReset()
#for progress, i in enumerate(punctuations):
#	selectText(i.start(), i.end() - i.start(), frame)
#	setCharacterStyle('punctuation', frame)
#	scribus.progressSet(progress)

"""for i in reversed(tuple(re.finditer(u'[\u0591\u05c3\u0592\u0593\u0594\u0595\u05c0]+', content))):
	selectText(i.start(), i.end() - i.start(), frame)
	setCharacterStyle('dcantillation', frame)"""

p = 1
while textOverflows(str(p)):
	newPage(-1)
	p += 1
	f = createText(marginLeft, marginTop, pageWidth - marginLeft - marginRight, pageHeight - marginTop - marginBottom, '%s'%p)
	linkTextFrames('%s'%(p - 1), '%s'%p)
setTextDirection(DIRECTION_RTL, '1')

pdf = PDFfile()
pdf.file = '%s.pdf'%name
pdf.save()
saveDocAs('%s.sla'%name)

setRedraw(True)
