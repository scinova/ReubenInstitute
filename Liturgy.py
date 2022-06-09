#!/usr/bin/env python
# -*- coding: utf-8  -*-

import hebrew_numbers
import os
import re
from enum import Enum

from common import Span, SpanKind

import Tanakh
tanakh = Tanakh.Tanakh()

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(ROOT_PATH, 'db', 'liturgy')

def remove_cantillations(text):
	return re.sub('[\u0591-\u05ae\u05bd\u05c0\u05c3]', '', text)

class Variant(Enum):
	ASHKENAZ = 'ashkenaz'
	SEFARD = 'sefard'
	MIZRAH = 'mizrah'
	TEIMAN = 'teiman'

class Time(Enum):
	SHAHARIT = 'shaharit'
	MINKHA = 'minkha'
	ARVIT = 'arvit'

class Element:
	def __init__(self, value):
		self.value = value

class Block:
	def __init__(self, value, option=None):
		self.value = value
		self.option = option
		self.spans = []

	def __repr__(self):
		return "Block: %s"%self.value

def includes(text, variant=0):
		files = os.listdir(DB_PATH)
		#print(files)
		for f in files:
			if not f.endswith('.txt'):
				continue
			data = open(os.path.join(DB_PATH, f)).read()
			data = variantf(data, variant)
			#self.macros[f] = data
			text = re.sub('\<%s\>'%f[:-4], data, text)
		return text
		#print (self.macros.keys())

def variantf(text='', variant=0):
	l = '\u05d0\u05e1\u05de\u05ea'[variant]
	tags = list(reversed(list(re.finditer('\<[^>]+\>', text))))
	for tag in tags:
		t = tag.group()
		sub = ''
#		for i in list(re.compile('(?<=[\<\|])(\u05d0*\u05e1*\u05de*\u05ea*)\:([^|\>]+)(?=[\|\>])').finditer(t)):
		vs = list(re.compile('(?<=[\<\|])([\u05d0\u05e1\u05de\u05ea]{1,3})\:([^|\>]+)(?=[\|\>])').finditer(t))
		if not vs:
			continue
		for i in vs:
			letters = i.groups()[0]
			if l in letters:
				sub = i.groups()[1]
		start, end = tag.span()
		if sub:
				text = text[:start] + sub + text[end:]
		else:
			text = text[:start] + text[end:]
	#text = re.sub('\n{2,}', '\n\n', text)
	return text

def something(text='', variant=0):
		text = includes(text, variant)
		#text = self.variant(self._text, variant)
		text = variantf(text, variant)

		#print (len(text.split('\n\n\n')))

		sections = []
		for text in text.split('\n\n\n'):
			conditional_blocks = list(re.finditer('\{\{([\u05d0-\u05ea ]+)\:([^}]+)\}\}\n', text))
			for block in conditional_blocks:
				start, end = block.span()
				text = text[0:start] + (end - start) * 'X' + text[end:]
			plain_blocks = list(re.finditer('([^X]+)', text))
			for block in plain_blocks:
				start, end = block.span()
				text = text[0:start] + (end - start) * '.' + text[end:]
			blocks = []
			for idx in range(len(text)):
				for block in conditional_blocks + plain_blocks:
					if idx == block.start():
						groups = block.groups()
						value = groups[0]
						if len(groups) > 1:
							alt = groups[1]
						#value = self.variant(value, variant)
						if value.endswith('\n'):
							value = value[:-1]
						if value.startswith('\n'):
							value = value[1:]
						if block in conditional_blocks:
							b = Block(alt, option=value)
							b.spans = parse(alt)
							blocks.append(b)
						elif block in plain_blocks:
							for v in value.split('\n\n'):
								b = Block(v)
								b.spans = parse(v)
								blocks.append(b)
			sections.append(blocks)
		#print (len(sections))
		return sections

def parse(text, classic=False):
		if not text:
			return []
		text = re.sub('"([^"]+)"', r'“\1”', text)
		text = re.sub("'([^']+)'", r"‘\1’", text)
		#text = re.sub('^- ', '\u2015 ', text)#―
		#text = re.sub(' -', ' \u2013', text)#–
		#text = re.sub('-', '\u2011', text)
		subtitle_items = list(re.finditer('^==([^\n]+?\n)', text, re.M))
#		subtitle_items = list(re.finditer('^==(.+)\n$', text, re.M))
		for item in subtitle_items:
			start, end = item.span()
			text = text[0:start] + (end - start) * 'X' + text[end:]
		title_items = list(re.finditer('^=(.+)$', text, re.M))
		#title_items = []
		for item in title_items:
			start, end = item.span()
			text = text[0:start] + (end - start) * 'X' + text[end:]

		majuscule_items = list(re.finditer('<<([^>]+)>>', text))
		for item in majuscule_items:
			start, end = item.span()
			text = text[0:start] + (end - start) * 'X' + text[end:]
		minuscule_items = list(re.finditer('>>([^<]+)<<', text))
		for item in minuscule_items:
			start, end = item.span()
			text = text[0:start] + (end - start) * 'X' + text[end:]
		bold_items = list(re.finditer('<([^>]+)>', text))
		for item in bold_items:
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
		citation_items = list(re.finditer('“([^”]+)”', text))
		for item in citation_items:
			start, end = item.span()
			text = text[0:start] + (end - start) * 'X' + text[end:]
		link_items = list(re.finditer(' \(([\u05d0-\u05ea־]+ [\u05d0-\u05ea]{1,3} [\u05d0-\u05ea]{1,3})\)', text))
		for item in link_items:
			start, end = item.span()
			text = text[0:start] + (end - start) * 'X' + text[end:]
		plain_items = list(re.finditer('([^X]+)', text))
		for item in plain_items:
			start, end = item.span()
			text = text[0:start] + (end - start) * '.' + text[end:]
		spans = []
		for idx in range(len(text)):
			for item in title_items + subtitle_items + \
					majuscule_items + minuscule_items + bold_items + correction_items + \
					citation_items + link_items + plain_items:
					#nonliteral_items + addition_items + alternative_items + \
					#synonym_items + explanation_items + \
				if idx == item.start():
					groups = item.groups()
					value = groups[0]
					if classic:
						value = re.sub('\n', '=', value)
					if len(groups) > 1:
						alt = groups[1]
					span = None
					if item in title_items:
						span = Span(SpanKind.TITLE, value)
					elif item in subtitle_items:
						span = Span(SpanKind.SUBTITLE, value)
					elif item in majuscule_items:
						span = Span(SpanKind.MAJUSCULE, value)
					elif item in minuscule_items:
						span = Span(SpanKind.MINUSCULE, value)
					elif item in bold_items:
						span = Span(SpanKind.BOLD, value)
					elif item in correction_items:
						span = Span(SpanKind.CORRECTION, value)
					elif item in citation_items:
						span = Span(SpanKind.CITATION, remove_cantillations(value))
					elif item in link_items:
						span = Span(SpanKind.LINK, value)
					else:
						span = Span(SpanKind.PLAIN, value)
					spans.append(span)
		print (spans)
		return spans

class Prayer:
	def __init__(self, time):
		self._time = time
		self.macros = {}
		f = os.path.join(DB_PATH, 'liturgy.txt')
		f = os.path.join(DB_PATH, '../zohar/3.28/01.txt')
		self._text = open(f).read()
		files = os.listdir(DB_PATH)
		print(files)
		for f in files:
			if not f.endswith('.txt'):
				continue
			data = open(os.path.join(DB_PATH, f)).read()
			#self.macros[f] = data
			self._text = re.sub('\<%s\>'%f[:-4], data, self._text)
		print (self.macros.keys())

	@property
	def text(self):
		return self._text

	@text.setter
	def text(self, value):
		pass


if __name__ == '__main__':
	p = Prayer(Time.SHAHARIT)
	#print (p.something()[3][0].spans)
