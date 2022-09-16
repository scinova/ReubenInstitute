#!/usr/bin/env python
# -*- coding: utf-8  -*-

import hebrew_numbers
import os
import re
from enum import Enum
import unicodedata

from common import Span, SpanKind

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(ROOT_PATH, 'db', 'zohar')

a = 1
b = 2
DATA = [
	['על התורה - בראשית', [
		[1, a, 1, 14, b, 7, 'הקדמה'],
		[15, a, 1, 59, a, 7, 'בראשית'],
		[59, b, 1, 76, b, 4, 'נח'],
		[76, b, 5, 96, b, 10, 'לך לך'],
		[97, a, 1, 120, b, 8, 'וירא'],
		[121, a, 1, 134, a, 7, 'חיי שרה'],
		[134, a, 8, 146, b, 5, 'תולדות'],
		[146, b, 6, 165, b, 1, 'ויצא'],
		[165, b, 2, 179, a, 6, 'וישלח'],
		[179, a, 7, 193, a, 3, 'וישב'],
		[193, a, 4, 205, a, 9, 'מקץ'],
		[205, a, 10, 211, b, 5, 'ויגש'],
		[211, b, 5, 251, a, 5, 'ויחי']
		]],
	['על התורה - שמות', [
		[1, b, 1, 22, b, 2, 'שמות'],
		[22, a, 3, 32, a, 10, 'וארא'],
		[32, b, 1, 43, b, 11, 'בא'],
		[44, a, 1, 61, a, 6, 'בשלח'],
		[61, a, 7, 67, a, 3, 'המן'],
		[67, a, 4, 94, a, 6, 'יתרו'],
		[94, a, 7, 126, a, 5, 'משפטים'],
		[126, a, 6, 179, a, 9, 'תרומה'],
		[179, b, 1, 187, b, 3, 'תצוה'],
		[187, b, 4, 194, b, 6, 'כי תשא'],
		[194, b, 7, 220, a, 7, 'ויקהל'],
		[220, a, 8, 268, b, 11, 'פיקודי']
		]],
	['על התורה - ויקרא, במדבר, דברים', [
		[2, a, 1, 26, a, 5, 'ויקרא'],
		[26, a, 6, 35, b, 7, 'צו'],
		[35, b, 8, 42, a, 7, 'שמיני'],
		[42, a, 8, 52, a, 8, 'תזריע'],
		[52, b, 1, 56, a, 5, 'מצורע'],
		[56, a, 6, 80, a, 2, 'אחרי מות'],
		[80, a, 3, 88, a, 3, 'קדושים'],
		[88, a, 4, 107, b, 7, 'אמור'],
		[107, b, 8, 112, a, 7, 'בהר'],
		[112, a, 8, 115, b, 11, 'בחוקתי'],
		[117, a, 1, 121, a, 5, 'במדבר'],
		[121, a, 6, 148, b, 4, 'נשא'],
		[148, b, 5, 156, b, 1, 'בהעלותך'],
		[156, b, 2, 176, a, 3, 'שלח'],
		[176, a, 4, 179, b, 4, 'קרח'],
		[179, b, 5, 184, b, 4, 'חוקת'],
		[184, b, 5, 212, b, 9, 'בלק'],
		[213, a, 1, 259, b, 2, 'פנחס'],
		[259, b, 3, 259, b, 8, 'מטות'],
		[259, b, 9, 259, b, 9, 'דברים'],
		[260, a, 1, 270, b, 7, 'ואתחנן'],
		[270, b, 8, 274, a, 15, 'עקב'],
		[274, a, 16, 275, b, 4, 'שופטים'],
		[275, b, 5, 283, a, 20, 'כי תצא'],
		[283, a, 21, 286, a, 5, 'ןילך'],
		[286, a, 6, 287, b, 14, 'האזינו'],
		[287, b, 15, 299, b, 13, 'אדרא זוטא'],
		[127, b, 5, 145, a, 3, 'אדרא רבא']
		]],
	['זהר חדש', [
		]],
	['תיקוני הזהר', [
		[1, a, 1, 16, b, 4, 'הקדמה'],
		[17, a, 1, 17, b, 6, 'הקדמה אחרת'],
		[17, b, 7, 18, a, 5, 'תיקון א'],
		[18, a, 6, 18, a, 6, 'תיקון ב'],
		#[120, b, 2, 140, b, 1, 'תיקון ע']
		]]
	]


def parse(text=''):
	if not text:
		return []
	text = re.sub('"([^"]+)"', r'“\1”', text)
	text = re.sub("'([^']+)'", r"‘\1’", text)
	text = re.sub('^- ', '\u2015 ', text)#―
	text = re.sub(' -', ' \u2013', text)#–
	text = re.sub('-', '\u2011', text)
	text = re.sub('{[^}]*}', '', text) #remove zohar page no
	text = re.sub(' +', ' ', text)

	alternative_items = list(re.finditer('\[([^|]*)\|([^]]+)\]', text))
	for item in alternative_items:
		start, end = item.span()
		text = text[0:start] + (end - start) * 'X' + text[end:]
	nonliteral_items = list(re.finditer('_([^_]+)_', text))
	for item in nonliteral_items:
		start, end = item.span()
		text = text[0:start] + (end - start) * 'X' + text[end:]
	addition_items = list(re.finditer('\+([^+]+)\+', text))
	for item in addition_items:
		start, end = item.span()
		text = text[0:start] + (end - start) * 'X' + text[end:]
	synonym_items = list(re.finditer('\(\=([^)]+)\)', text))
	for item in synonym_items:
		start, end = item.span()
		text = text[0:start] + (end - start) * 'X' + text[end:]
	explanation_items = list(re.finditer('\(\~([^)]+)\)', text))
	for item in explanation_items:
		start, end = item.span()
		text = text[0:start] + (end - start) * 'X' + text[end:]
	correction_items = list(re.finditer('\[([^]]+)\]', text))
	for item in correction_items:
		start, end = item.span()
		text = text[0:start] + (end - start) * 'X' + text[end:]
	citation_items = list(re.finditer('“([^”]+)”', text))
	for item in citation_items:
		start, end = item.span()
		text = text[0:start] + (end - start) * 'X' + text[end:]
	link_items = list(re.finditer('\(([\u05d0-\u05ea־]+ [\u05d0-\u05ea]{1,3} [\u05d0-\u05ea]{1,3})\)', text))
	for item in link_items:
		start, end = item.span()
		text = text[0:start] + (end - start) * 'X' + text[end:]
	plain_items = list(re.finditer('([^X]+)', text))
	for item in plain_items:
		start, end = item.span()
		text = text[0:start] + (end - start) * '.' + text[end:]
	spans = []
	for idx in range(len(text)):
		for item in nonliteral_items + addition_items + alternative_items + \
				synonym_items + explanation_items + correction_items + \
				citation_items + link_items + plain_items:
			if idx == item.start():
				groups = item.groups()
				value = groups[0]
				if len(groups) > 1:
					alt = groups[1]
				span = None
				if item in nonliteral_items:
					span = Span(SpanKind.NONLITERAL, value)
				elif item in addition_items:
					span = Span(SpanKind.ADDITION, value)
				elif item in alternative_items:
					span = Span(SpanKind.ALTERNATIVE, value, alt)
				elif item in synonym_items:
					span = Span(SpanKind.SYNONYM, value)
				elif item in explanation_items:
					span = Span(SpanKind.EXPLANATION, value)
				elif item in correction_items:
					span = Span(SpanKind.CORRECTION, value)
				elif item in citation_items:
					span = Span(SpanKind.SCRIPTURE, value)
				elif item in link_items:
					span = Span(SpanKind.LINK, value)
				elif item in plain_items:
					span = Span(SpanKind.PLAIN, value)
				spans.append(span)
	return spans

class Article:
	def __init__(self, chapter, number, title):
		self.chapter = chapter
		self.number = number
		self.title = title
		#self.hebrew_number = hebrew_numbers.int_to_gematria(number)
		#self.hebrew_number_nog = hebrew_numbers.int_to_gematria(number, gershayim=False)
		#self.title = title
		self._text = ''
		self._translation = ''

	@property
	def text(self):
		if not self._text:
			filename = os.path.join(DB_PATH, '%1d.%02d'%(self.book.number, self.chapter.number), '%02d.txt'%self.number)
			data = open(filename).read()
			#if '\n\n\n' in data:
				#data = re.sub('\n\n', '\n', data, re.M)
			self._text = data
		return self._text

	@text.setter
	def text(self, value):
		self._text = unicodedata.normalize('NFC', value)
		filename = os.path.join(DB_PATH, '%1d.%02d'%(self.book.number, self.chapter.number), '%02d.txt'%self.number)
		open(filename, 'w').write(value)

	@property
	def translation(self):
		if not self._translation:
			filename = os.path.join(DB_PATH, '%1d.%02d'%(self.book.number, self.chapter.number), '%02dt.txt'%self.number)
			data = open(filename).read()
			#if '\n\n' in data:
				#data = re.sub('\n\n', '\n', data, re.M)
				#open(filename, 'w').write(data)
			self._translation = data
		return self._translation

	@translation.setter
	def translation(self, value):
		self._translation = value
		filename = os.path.join(DB_PATH, '%1d.%02d'%(self.book.number, self.chapter.number), '%02dt.txt'%self.number)
		open(filename, 'w').write(value)

	@property
	def book(self):
		return self.chapter.book

	@property
	def sections(self):
		return [[parse(line) for line in part.split('\n')] for part in self.text.split('\n\n')]

	@property
	def translation_sections(self):
		return [[parse(line) for line in part.split('\n')] for part in self.translation.split('\n\n')]

class Chapter:
	def __init__(self, book, number, title):
		self.book = book
		self.number = number
		self.title = title
		#self.hebrew_number = hebrew_numbers.int_to_gematria(number)
		#self.hebrew_number_nog = hebrew_numbers.int_to_gematria(number, gershayim=False)
#		self.start_daf, self.start_amud, self.start_verse, self.end_daf, self.end_amud, self.end_verse, name = DATA[book.number - 1][number - 1]
		self.articles = []

class Book:
	def __init__(self, number, title):
		self.number = number
		self.title = title
		self.chapters = []

class Zohar:
	def __init__(self):
		self.books = []
		for book_idx in range(len(DATA)):
			name, data = DATA[book_idx]
			book = Book(book_idx + 1, name)
			for chapter_idx in range(len(data)):
				start_daf, start_amud, start_verse, end_daf, end_amud, end_verse, name = data[chapter_idx]
				chapter = Chapter(book, chapter_idx + 1, name)
				filename = os.path.join(DB_PATH, '%1d.%02d'%(book.number, chapter.number), '00.txt')
				if os.path.exists(filename):
					names = open(filename).read().split('\n')[:-1]
					for article_idx in range(len(names)):
						article = Article(chapter, article_idx + 1, names[article_idx])
						chapter.articles.append(article)
				book.chapters.append(chapter)
			self.books.append(book)
