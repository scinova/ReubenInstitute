#!/usr/bin/env python
# -*- coding: utf-8  -*-

import hebrew_numbers
import os
import re
from enum import Enum

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(ROOT_PATH, 'db')

def remove_accents(text):
	return re.sub('[\u0591-\u05ae]', '', text)

def remove_points(text):
	return re.sub('[\u05b0-\u05bc\u05c7\u05c1\u05c2]', '', text)

def remove_meteg(text):
	return re.sub('\u05bd', '', text)

class SpanKind(Enum):

	PLAIN = 0
	LEGEND = 1
	#CITATION = 2
	SCRIPTURE = 2
	LINK = 3

	MAJUSCULE = 4
	MINUSCULE = 5

	KRIKTIV = 6
	ALIYA = 7

	CHAPTERNO = 10
	VERSENO = 11

	ALTERNATIVE = 20
	ADDITION = 21
	NONLITERAL = 22
	REFERENCE = 23

	TITLE = 24
	SUBTITLE = 25
	INFO = 26
	
	BOLD = 27

	SYNONYM = 28
	EXPLANATION = 29
	CORRECTION = 30

	H1 = 31
	H2 = 32
	H3 = 33
	H4 = 34

	PUNCTUATION = 36
	POINT = 37
	ACCENT = 38

	BREAK = 40
	TAB = 41
	SPACE = 42

class Span:
	def __init__(self, kind, value=None, alt=None):
		self.kind = kind
		self.value = value
		self.alt = alt

	def __repr__(self):
		return '<Span.%s:%s>'%(self.kind, self.value or '')

	@property
	def style(self):
		return ''

def fix_yy(text):
	return text.replace('יְיָ', 'יי')

def fix_yhwh(text):
	y = '\u05d9'
	h = '\u05d4'
	w = '\u05d5'
	a = '([\u0591-\u05af\u05bd\u05c0\u05c3]*)'
	p = '([\u05b0-\u05bc\u05c1\u05c2\u05c7]*)'
	pattern = y + p + a + h + p + a + w + p + a + h + p + a
	#print (pattern)
	for match in reversed(list(re.finditer(pattern, text, re.M))):
		orig = text[match.start():match.end()]
		p1, a1, p2, a2, p3, a3, p4, a4 = match.groups()
		out = y + a1 + '\ufb23' + a2 + w + a3 + '\ufb23' + a4
		start, end = match.span()
		text = text[0:start] + out + text[end:]
	return text

def fix_paseq(text):
	return re.sub(' ׀', '׀', text)

ACCENTS_REGEX = '[\u0591-\u05af\u05bd\u05c0\u05c3]'
POINTS_REGEX = '[\u05b0-\u05bc\u05c1\u05c2\u05c7]'
PUNCTUATION_REGEX = '[\?\!\;\:\.\,\-’‘”“]'

def unicode_reorder(text):
	order = ['\u05d0-\u05ea', #letters
			'\u05c1\u05c2', #sin/shin dots
			'\u05bc', #dagesh
			'\u05b0', #shva
			'\u05b1-\u05bb\u05c7', #diacritics
			'\u0591-\u05af\u05bd' #cantillations
			]
	regexp = '([%s]{1}[%s%s%s%s%s]+)'%(order[0], order[1], order[2], order[3], order[4], order[5])
	tavs = list(re.finditer(regexp, text, re.M))
	for tav in tavs:
		ttav = tav.groups()[0]
		out = ''
		for o in order:
			for c in ttav:
				if re.match('[%s]'%o, c):
					out = out + c
		text = text[:tav.start()] + out + text[tav.end():]
	return text
