#!/usr/bin/env python
# -*- coding: utf-8  -*-

from scribus import *
import re
from hebrew_numbers import *
import sys
import common

newDocument((135, 205), (10, 10, 10, 10), PORTRAIT, 1, UNIT_MILLIMETERS, PAGE_1, 0, 1)
setUnit(UNIT_PT)
font = "SBL Hebrew Regular"
createCharStyle("title", "Hadasim CLM Regular", 22, fillcolor='Red')
createCharStyle("subtitle", "Hadasim CLM Regular", 15, fillcolor='Red')
createCharStyle("link", font, 10, fillcolor='Blue')
createCharStyle("verse_no", font, 11, fillcolor='Blue')
createCharStyle("regular", font, 15)
createCharStyle("holly", font, 15)
createCharStyle("cantillation", font, 15)

createParagraphStyle("poem", linespacingmode=0,linespacing=17, alignment=1,
		leftmargin=0, rightmargin=0, gapbefore=0, gapafter=6,
		firstindent=0, hasdropcap=0, dropcaplines=0, dropcapoffset=0)
createParagraphStyle("link", alignment=ALIGN_CENTERED)
createParagraphStyle("centered", alignment=ALIGN_CENTERED)
createParagraphStyle("justified", alignment=ALIGN_BLOCK)

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
#setRedraw(False)
frame = createText(marginLeft, marginTop, pageWidth - marginLeft - marginRight, pageHeight - marginTop - marginBottom, '1')
createMasterPage('left')
createMasterPage('right')
for p in range(2, 15):
	newPage(-1)
	frame = createText(marginLeft, marginTop, pageWidth - marginLeft - marginRight, pageHeight - marginTop - marginBottom, '%s'%p)
	linkTextFrames('%s'%(p - 1), '%s'%p)
setTextDirection(DIRECTION_RTL, '1')


data = unicode(open('siddur.txt').read())
lines = data.split('\n')
citations = len(lines) * [0]
frame = '1'
for line_number in range(len(lines)):
	line = lines[line_number]
	is_subtitle = line.startswith('==')
	if is_subtitle:
		line = line[2:]
	is_title = line.startswith('=')
	if is_title:
		line = line[1:]
	tags = list(re.finditer('\{[^}]+\}', line))
	whole_chapter = 2 in [len(p) for p in [tag.group()[1:-1].split(' ') for tag in tags]]
	for tag in tags:
		parts = tag.group()[1:-1].split(' ')
		#whole_chapter = len(parts) == 2
		has_words = len(parts) == 4
		if not whole_chapter:
			if has_words:
				book_hebrew_name, chapter_string, verses_string, words_string = parts
			else:
				book_hebrew_name, chapter_string, verses_string = parts
			if '-' in verses_string:
				start_verse, end_verse = [int(gematria_to_int(s)) for s in verses_string.split('-')]
			else:
				start_verse = end_verse = int(gematria_to_int(verses_string))
			if has_words and '-' in words_string:
				start_word, end_word = [int(s) for s in words_string.split('-')]
		else:
			book_hebrew_name, chapter_string = parts
		book_hebrew_name = book_hebrew_name.replace('־', ' ')
		chapter_number = gematria_to_int(chapter_string)
		book = [b for b in common.Bible if b.hname == book_hebrew_name][0]
		filename = '%02d.%03d.txt'%(book.ind, chapter_number)
		print (book_hebrew_name)
		print (book.ind, chapter_number, filename)
		tanakh_text = open('db/tanakh/' + filename).read()

		link_string = book_hebrew_name + ', פרק ' + int_to_gematria(chapter_number)
		#if not whole_chapter:
		#	link_string += ', '

		tanakh_lines = tanakh_text.split('\n')[:-1]
		if whole_chapter:
			verses = tanakh_lines
		else:
			print('s', start_verse, end_verse)
			verses = tanakh_lines[start_verse - 1 : end_verse]

		add_text(frame, link_string + '\n', 'link', 'link')
#		pos = getTextLength(frame)
#		insertText(link_string + '\n', pos, frame)

		print ('x', start_verse, end_verse, len(verses))
		for verse_ind in range(len(verses)):
			if whole_chapter:
				verse_number = verse_ind + 1
			else:
				verse_number = start_verse + verse_ind
			
			print ('y', verse_ind, verse_number, len(verses))
			verse_text = verses[verse_ind]
			# REMOVE KTIV
			verse_text = re.sub('\[[^]]+\]', '', verse_text)
			# REMOVE PARASHA TYPE
			verse_text = re.sub('\{[^}]+\}', '', verse_text)

			add_text(frame, '%s '%int_to_gematria(verse_number), 'verse_no', 'poem')
			add_text(frame, unicode(verse_text) + '\n', 'regular', 'poem')
			#t = '%s %s\n'%(int_to_gematria(verse_number), verse_text)
			#add_text(frame, t, 'regular', 'poem')
			#pos = getTextLength(frame)
			#insertText(int_to_gematria(verse_number) + ' ' + verse_text + '\n', pos, frame)


		#line = line[:item.start()] + '[' + line[item.start() + 1 : item.end() - 1] + ']' + line[item.end():]
		#citations[line_number] = tag

	if not len(tags):
		length = len(line)
		pos = getTextLength(frame)
		insertText(line + '\n', pos, frame)
		selectText(pos, length, frame)
		if is_title:
			setCharacterStyle("title", frame)
			setStyle("centered", frame)
		elif is_subtitle:
			setCharacterStyle("subtitle", frame)
			setStyle("centered", frame)
		else:
			setCharacterStyle("regular", frame)
			setStyle("justified", frame)
setTextDirection(DIRECTION_RTL, frame)


pdf = PDFfile()
pdf.file = 'siddur.pdf'
pdf.save()
#setRedraw(True)
