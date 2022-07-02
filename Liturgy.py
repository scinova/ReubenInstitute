#!/usr/bin/env python
# -*- coding: utf-8  -*-

import hebrew_numbers
import os
import re
from enum import Enum

import common
from common import Span, SpanKind

import Tanakh
tanakh = Tanakh.Tanakh()

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(ROOT_PATH, 'db', 'liturgy')

def remove_cantillations(text):
	return re.sub('[\u0591-\u05ae\u05bd]', '', text) #\u05c0\u05c3

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
	def __init__(self, value, option=None, style=None):
		self.value = value
		self.option = option
		self.style = style
		self.lines = []
		self.blocks = []

	def __repr__(self):
		return "Block: %s"%self.value

def includes(text, variant):
		files = os.listdir(DB_PATH)
		for f in files:
			if not f.endswith('.txt'):
				continue
			data = open(os.path.join(DB_PATH, f)).read()
			data = variantf(data, variant)
			text = re.sub('≪%s≫'%f[:-4], data, text)
			text = re.sub('\<%s\>'%f[:-4], data, text)
		#text = variantf(text, variant)
		return text

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
	return text

def something(text='', variant=0, oxn=['עשרת ימי תשובה'], on=[], off=[]):
		text = variantf(text, variant)
		text = includes(text, variant)
		text = includes(text, variant)

		sections = []
		for text in text.split('\n\n\n'):

			conditional_blocks = list(re.finditer('\n*\{\{([\)\(]*)([a-z\-]+\: )([^}]+)\}\}\n*', text, re.M))
			for block in conditional_blocks:
				start, end = block.span()
				text = text[0:start] + (end - start) * 'X' + text[end:]

			replacement_blocks = list(re.finditer('\n*\(\(([^)]+)\)\)\n*', text, re.M))
			replacement_blocks = []
			for block in replacement_blocks:
				start, end = block.span()
				text = text[0:start] + (end - start) * 'X' + text[end:]

			styled_blocks = list(re.finditer('\n*{([\(\)=\-\+12345T]*)([^}]+)\}\n*', text, re.M))
			for block in styled_blocks:
				start, end = block.span()
				text = text[0:start] + (end - start) * 'X' + text[end:]

			plain_blocks = list(re.finditer('\n*([^X]+)\n*', text))
			for block in plain_blocks:
				start, end = block.span()
				text = text[0:start] + (end - start) * '.' + text[end:]

			blocks = []
			for idx in range(len(text)):
				for block in styled_blocks + conditional_blocks + replacement_blocks + plain_blocks:
					if idx == block.start():
						if block in conditional_blocks:
							style, option, value = block.groups()
							option = option[:-2]
							b = Block(value, option=option, style=style)
							for v in value.split('\n\n'):
								bb = Block(v)
								bb.lines = parse(v)
								b.blocks.append(bb)
							blocks.append(b)
						elif block in styled_blocks:
							style, value = block.groups()
							b = Block(value, style=style)
							for v in value.split('\n\n'):
								bb = Block(v)
								bb.lines = parse(v)
								b.blocks.append(bb)
							blocks.append(b)
						elif block in plain_blocks:
							value, = block.groups()
							b = Block(value)
							for v in value.split('\n\n'):
								bb = Block(v)
								bb.lines = parse(v)
								b.blocks.append(bb)
							blocks.append(b)

						"""elif block in replacement_blocks:
							value, = block.groups()
							ispoem, repeat, title, verses = tanakh.replace(value)
							#print (ispoem, repeat, title, len(verses))
							b = Block(value, style="1")
							bb = Block(value)
							if verses:
								bb.spans.append(Span(SpanKind.LINK, title))
								bb.spans.append(Span(SpanKind.BREAK))
							for verse in verses:
								if len(verses) > 1 and repeat < 2:
									bb.spans.append(Span(SpanKind.VERSENO, verse.hebrew_number))
								#for s in Tanakh.newparse(verse.mikra_text):
								for s in verse.mikra:
									print (s)
									s.value = common.fix_paseq(s.value)
									bb.spans.append(s)
								if ispoem or repeat > 1:
									if len(verses) > 1 and verses != verses[-1]:
										bb.spans.append(Span(SpanKind.BREAK))
							b.blocks.append(bb)
							blocks.append(b)"""
			sections.append(blocks)
		return sections

def parse(text, classic=False):
	if not text:
		return []
	text = common.fix_yhwh(text)
	text = re.sub('"([^"]+)"', r'“\1”', text)
	text = re.sub("'([^']+)'", r"‘\1’", text)
	text = re.sub('^- ', '\u2015 ', text)#―
	text = re.sub(' -', ' \u2013', text)#–
	#text = re.sub('-', '\u2011', text)

	replacement_items = list(re.finditer('(\(\([^)]+\)\))', text))
	for item in replacement_items:
		start, end = item.span()
		text = text[0:start] + (end - start) * 'X' + text[end:]

	h4_items = list(re.finditer('^====([^\n]+)\n*', text, re.M))
	for item in h4_items:
		start, end = item.span()
		text = text[0:start] + (end - start) * 'X' + text[end:]
	h3_items = list(re.finditer('^===([^\n]+)\n*', text, re.M))
	for item in h3_items:
		start, end = item.span()
		text = text[0:start] + (end - start) * 'X' + text[end:]
	h2_items = list(re.finditer('^==([^\n]+)\n*', text, re.M))
	for item in h2_items:
		start, end = item.span()
		text = text[0:start] + (end - start) * 'X' + text[end:]
	h1_items = list(re.finditer('^=([^\n]+)\n*', text, re.M))
	for item in h1_items:
		start, end = item.span()
		text = text[0:start] + (end - start) * 'X' + text[end:]

	majuscule_items = list(re.finditer('\(\+([^)]+)\)', text))
	for item in majuscule_items:
		start, end = item.span()
		text = text[0:start] + (end - start) * 'X' + text[end:]
	minuscule_items = list(re.finditer('\(\-([^)]+)\)', text))
	for item in minuscule_items:
		start, end = item.span()
		text = text[0:start] + (end - start) * 'X' + text[end:]

	bold_items = list(re.finditer('<([^>]+)>', text))
	for item in bold_items:
		start, end = item.span()
		text = text[0:start] + (end - start) * 'X' + text[end:]
	verseno_items = list(re.finditer('#([^#]+)#', text))
	for item in verseno_items:
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
	link_items = list(re.finditer('\^([^\^]+)\^', text))
	for item in link_items:
		start, end = item.span()
		text = text[0:start] + (end - start) * 'X' + text[end:]
	info_items = list(re.finditer('@([^@]+)@', text))
	for item in info_items:
		start, end = item.span()
		text = text[0:start] + (end - start) * 'X' + text[end:]

	break_items = list(re.finditer('\n', text))
	for item in break_items:
		start, end = item.span()
		text = text[0:start] + (end - start) * 'X' + text[end:]

	plain_items = list(re.finditer('([^X\n]+)', text))
	for item in plain_items:
		start, end = item.span()
		text = text[0:start] + (end - start) * '.' + text[end:]

	all_items = majuscule_items + minuscule_items + \
			h1_items + h2_items + h3_items + h4_items + \
			bold_items + verseno_items + \
			addition_items + synonym_items + explanation_items + correction_items + \
			citation_items + link_items + info_items + \
			replacement_items + plain_items + break_items

	lines = []
	line = []
	for idx in range(len(text)):
		for item in all_items:
			if idx == item.start():
				groups = item.groups()
				value = None
				alt = None
				if len(groups):
					value = groups[0]
				if len(groups) > 1:
					alt = groups[1]
				span = None
				if item in h1_items:
					span = Span(SpanKind.H1, value)
				elif item in h2_items:
					span = Span(SpanKind.H2, value)
				elif item in h3_items:
					span = Span(SpanKind.H3, value)
				elif item in h4_items:
					span = Span(SpanKind.H4, value)
				elif item in majuscule_items:
					span = Span(SpanKind.MAJUSCULE, value)
				elif item in minuscule_items:
					span = Span(SpanKind.MINUSCULE, value)
				elif item in bold_items:
					span = Span(SpanKind.BOLD, value)
				elif item in verseno_items:
					span = Span(SpanKind.VERSENO, value)
				elif item in addition_items:
					span = Span(SpanKind.ADDITION, value)
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
				elif item in info_items:
					span = Span(SpanKind.INFO, value)
				elif item in plain_items:
					span = Span(SpanKind.PLAIN, value)
				if span:
					line.append(span)
				if item in break_items:
					lines.append(line)
					line = []

				if item in replacement_items:
					v = value[2:-2]
					ispoem, repeat, title, verses = tanakh.replace(v)
					#if not verses:
					#	lines.append([Span(SpanKind.PLAIN, value)])
					#	break
					if line:
						lines.append(line)
						line = []
					lines.append([Span(SpanKind.LINK, title)])
					for verse in verses:
						if len(verses) > 1 and repeat < 2:
							line.append(Span(SpanKind.VERSENO, verse.hebrew_number))
						for span in verse.mikra:
							if span.kind in [SpanKind.ALIYA]:
								continue
							if span.kind in [SpanKind.PLAIN]:
								span.kind = SpanKind.SCRIPTURE
							span.value = common.fix_paseq(span.value)
							line.append(span)
						if ispoem:
							lines.append(line)
							line = []
	if line:
		lines.append(line)
	return lines

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
	#p = Prayer(Time.SHAHARIT)
	pass
