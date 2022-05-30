#!/usr/bin/env python
# -*- coding: utf-8  -*-

import hebrew_numbers
import os
import re
from enum import Enum

from common import Span, SpanKind

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(ROOT_PATH, 'db', 'liturgy')

class Variant(Enum):
	ASHKENAZ = 'ashkenaz'
	SEFARD = 'sefard'
	MIZRAH = 'mizrah'
	TEIMAN = 'teiman'

class Time(Enum):
	SHAHARIT = 'shaharit'
	MINKHA = 'minkha'
	ARVIT = 'arvit'

class Prayer:
	def __init__(self, time):
		self._time = time
		f = os.path.join(DB_PATH, 'liturgy.txt')
		f = os.path.join(DB_PATH, '../zohar/3.28/01.txt')
		self._text = open(f).read()

	@property
	def text(self):
		return self._text

	@text.setter
	def text(self, value):
		pass

	@staticmethod
	def variant(text='', variant=0):
		l = '\u05d0\u05e1\u05de\u05ea'[variant]
		tags = list(reversed(list(re.finditer('\<[^>]+\>', text))))
		for tag in tags:
			t = tag.group()
			sub = ''
			for i in list(re.compile('(?<=[\<\|])(\u05d0*\u05e1*\u05de*\u05ea*)\:([^|\>]+)(?=[\|\>])').finditer(t)):
				letters = i.groups()[0]
				if l in letters:
					sub = i.groups()[1]
			start, end = tag.span()
			if sub:
				#text = text[:start] + '[' + sub + ']' + text[end:]
				text = text[:start] + sub + text[end:]
			else:
				text = text[:start] + text[end:]
		text = re.sub('\n{2,}', '\n\n', text)
		return text#.replace('\u05bd', '~')

		#p = '\<(?:[^|\\>]+\|)*\u05d0\u05e1*\u05de*\u05ea*\:([^|\>]+)[^>]+\>'
		#cond_items = reversed(list(re.finditer(p, text)))
		#for item in cond_items:
		#	print (item.groups())
		#	replacement = item.groups()[0]
		#	start, end = item.span()
		#	text = text[0:start] + '+' + replacement + '+' + text[end:]
		#	#print()


	@staticmethod
	def parse(text='', variant=0):
		if not text:
			return []
		text = re.sub('"([^"]+)"', r'“\1”', text)
		text = re.sub("'([^']+)'", r"‘\1’", text)
		#text = re.sub('^- ', '\u2015 ', text)#―
		#text = re.sub(' -', ' \u2013', text)#–
		#text = re.sub('-', '\u2011', text)
		subtitle_items = list(re.finditer('^==([^\n]+\n)', text, re.M))
		for item in subtitle_items:
			start, end = item.span()
			text = text[0:start] + (end - start) * 'X' + text[end:]
		title_items = list(re.finditer('^=(.+)$', text, re.M))
		for item in title_items:
			start, end = item.span()
			text = text[0:start] + (end - start) * 'X' + text[end:]
#		alternative_items = list(re.finditer('\[([^|]*)\|([^]]+)\]', text))
#		for item in alternative_items:
#			start, end = item.span()
#			text = text[0:start] + (end - start) * 'X' + text[end:]
#		nonliteral_items = list(re.finditer('_([^_]+)_', text))
#		for item in nonliteral_items:
#			start, end = item.span()
#			text = text[0:start] + (end - start) * 'X' + text[end:]
#		addition_items = list(re.finditer('\+([^+]+)\+', text))
#		for item in addition_items:
#			start, end = item.span()
#			text = text[0:start] + (end - start) * 'X' + text[end:]
#		synonym_items = list(re.finditer('\(\=([^)]+)\)', text))
#		for item in synonym_items:
#			start, end = item.span()
#			text = text[0:start] + (end - start) * 'X' + text[end:]
#		explanation_items = list(re.finditer('\(\~([^)]+)\)', text))
#		for item in explanation_items:
#			start, end = item.span()
#			text = text[0:start] + (end - start) * 'X' + text[end:]
		correction_items = list(re.finditer('\[([^]]+)\]', text))
		for item in correction_items:
			start, end = item.span()
			text = text[0:start] + (end - start) * 'X' + text[end:]
#		citation_items = list(re.finditer('“([^”]+)”', text))
#		for item in citation_items:
#			start, end = item.span()
#			text = text[0:start] + (end - start) * 'X' + text[end:]
#		link_items = list(re.finditer(' \(([\u05d0-\u05ea־]+ [\u05d0-\u05ea]{1,3} [\u05d0-\u05ea]{1,3})\)', text))
#		for item in link_items:
#			start, end = item.span()
#			text = text[0:start] + (end - start) * 'X' + text[end:]
		plain_items = list(re.finditer('([^X]+)', text))
		for item in plain_items:
			start, end = item.span()
			text = text[0:start] + (end - start) * '.' + text[end:]
		spans = []
		for idx in range(len(text)):
			for item in title_items + subtitle_items + correction_items + plain_items:
					#nonliteral_items + addition_items + alternative_items + \
					#synonym_items + explanation_items + correction_items + \
					#citation_items + link_items + plain_items:
				if idx == item.start():
					groups = item.groups()
					value = groups[0]
					if len(groups) > 1:
						alt = groups[1]
					span = None
					if item in title_items:
						span = Span(SpanKind.TITLE, value)
					if item in subtitle_items:
						span = Span(SpanKind.SUBTITLE, value)
					#if item in nonliteral_items:
					#	span = Span(SpanKind.NONLITERAL, value)
					#elif item in addition_items:
					#	span = Span(SpanKind.ADDITION, value)
					#elif item in alternative_items:
					#	span = Span(SpanKind.ALTERNATIVE, value, alt)
					#elif item in synonym_items:
					#	span = Span(SpanKind.SYNONYM, value)
					#elif item in explanation_items:
					#	span = Span(SpanKind.EXPLANATION, value)
					elif item in correction_items:
						span = Span(SpanKind.CORRECTION, value)
					#elif item in citation_items:
					#	span = Span(SpanKind.CITATION, value)
					#elif item in link_items:
					#	span = Span(SpanKind.LINK, value)
					#el
					elif item in plain_items:
						span = Span(SpanKind.PLAIN, value)
					spans.append(span)
		return spans

if __name__ == '__main__':
	p = Prayer(Time.SHAHARIT)
	print (p.variant(p.text, 3))

