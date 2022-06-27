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
	def __init__(self, value, option=None, style=None, margin=False):
		self.value = value
		self.option = option
		self.style = style
		self.margin = margin
		self.spans = []

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
	#text = re.sub('\n{2,}', '\n\n', text)
	return text

def something(text='', variant=0, oxn=['עשרת ימי תשובה'], on=[], off=[]):
		#text = includes(text, variant)
		#text = self.variant(self._text, variant)
		text = variantf(text, variant)
		text = includes(text, variant)
		text = includes(text, variant)

		#print (len(text.split('\n\n\n')))

		sections = []
		for text in text.split('\n\n\n'):
#			conditional_blocks = list(re.finditer('\{\{([\u05d0-\u05ea ,]+)\: (.+?)\}\}\n{0,2}', text, re.M))
			conditional_blocks = list(re.finditer('\n*\{\{([^:]+)\: ([^}]+)\}\}\n', text, re.M))
			for block in conditional_blocks:
				option_name, option_value = block.groups()
				start, end = block.span()
				#if option_name in on:
				#	text = text[0:start] + (len('{{' + option_name + ': ')) * 'X' + option_value + 'XX' + text[end:]
				#if option_name in off:
				#	text = text[0:start] + (end - start) * 'X' + text[end:]
				#else:
				text = text[0:start] + (end - start) * 'X' + text[end:]
			for idx in range(len(conditional_blocks) - 1, 0, -1):
				block = conditional_blocks[idx]
				option_name, option_value = block.groups()
				# remove block
				if option_name in on or option_name in off:
					conditional_blocks.pop(idx)
			styled_blocks = list(re.finditer('\n*{([=\-\+]*)([^}]+)\}\n{0,2}', text, re.M))
			for block in styled_blocks:
				start, end = block.span()
				text = text[0:start] + (end - start) * 'X' + text[end:]
			plain_blocks = list(re.finditer('([^X]+)', text))
			for block in plain_blocks:
				start, end = block.span()
				text = text[0:start] + (end - start) * '.' + text[end:]

			blocks = []
			for idx in range(len(text)):
				for block in styled_blocks + conditional_blocks + plain_blocks:
					if idx == block.start():
						if block in conditional_blocks:
							option, value = block.groups()
							b = Block(value, option=option)
							b.spans = parse(value)
							blocks.append(b)
						elif block in styled_blocks:
							style, value = block.groups()
							b = Block(value, style=style)
							b.spans = parse(value)
							blocks.append(b)
						elif block in plain_blocks:
							value, = block.groups()
							#if not value.replace('\n', '').replace(' ', ''):
							#	break
							for v in value.split('\n\n'):
								b = Block(v)
								b.spans = parse(v)
								blocks.append(b)
			# h blocks (no margin)
			for idx in range(len(blocks)):
				if [span for span in blocks[idx].spans if span.kind not in [SpanKind.H1, SpanKind.H2, SpanKind.H3, SpanKind.H4]]:
					blocks[idx].margin = True
				#if [span for span in blocks[idx].spans if span.value.replace('\n', '').replace(' ', '')]:
				#	blocks[idx].margin = True
			sections.append(blocks)
		#print (len(sections))
		return sections

def parse(text, classic=False):
		if not text:
			return []
		text = re.sub('"([^"]+)"', r'“\1”', text)
		text = re.sub("'([^']+)'", r"‘\1’", text)
		text = re.sub('^- ', '\u2015 ', text)#―
		text = re.sub(' -', ' \u2013', text)#–
		#text = re.sub('-', '\u2011', text)

		replacement_items = list(re.finditer('(\(\([^)]+\)\))', text))
		for item in replacement_items:
			start, end = item.span()
			text = text[0:start] + (end - start) * 'X' + text[end:]

		h4_items = list(re.finditer('^====([^\n]+)\n{0,2}', text, re.M))
		for item in h4_items:
			start, end = item.span()
			text = text[0:start] + (end - start) * 'X' + text[end:]
		h3_items = list(re.finditer('^===([^\n]+)\n{0,2}', text, re.M))
		for item in h3_items:
			start, end = item.span()
			text = text[0:start] + (end - start) * 'X' + text[end:]
		h2_items = list(re.finditer('^==([^\n]+)\n{0,2}', text, re.M))
		for item in h2_items:
			start, end = item.span()
			text = text[0:start] + (end - start) * 'X' + text[end:]
		h1_items = list(re.finditer('^=([^\n]+)\n{0,2}', text, re.M))
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
		plain_items = list(re.finditer('([^X]+)', text))
		for item in plain_items:
			start, end = item.span()
			text = text[0:start] + (end - start) * '.' + text[end:]
		spans = []
		for idx in range(len(text)):
			for item in h1_items + h2_items + h3_items + h4_items + \
					majuscule_items + minuscule_items + bold_items + verseno_items + \
					addition_items + synonym_items + explanation_items + correction_items + \
					citation_items + link_items + info_items + replacement_items + plain_items:
					#nonliteral_items + 
				if idx == item.start():
					print (idx)
					print (item)
					print (item.groups())
					groups = item.groups()
					value = groups[0]
					if classic:
						if value.startswith('\n'):
							value = 'X' + value[1:]
						value = re.sub('\n', '=', value)
						value = re.sub('X', '\n', value)
					#else:
					#	if value.startswith('\n'):
					#		value = value[1:]
					if len(groups) > 1:
						alt = groups[1]
					span = None
					if item in h1_items:
						span = Span(SpanKind.H1, value)
						spans.append(span)
					elif item in h2_items:
						span = Span(SpanKind.H2, value)
						spans.append(span)
					elif item in h3_items:
						span = Span(SpanKind.H3, value)
						spans.append(span)
					elif item in h4_items:
						span = Span(SpanKind.H4, value)
						spans.append(span)
					elif item in majuscule_items:
						span = Span(SpanKind.MAJUSCULE, value)
						spans.append(span)
					elif item in minuscule_items:
						span = Span(SpanKind.MINUSCULE, value)
						spans.append(span)
					elif item in bold_items:
						span = Span(SpanKind.BOLD, value)
						spans.append(span)
					elif item in verseno_items:
						span = Span(SpanKind.VERSENO, value)
						spans.append(span)
					elif item in addition_items:
						span = Span(SpanKind.ADDITION, value)
						spans.append(span)
					elif item in synonym_items:
						span = Span(SpanKind.SYNONYM, value)
						spans.append(span)
					elif item in explanation_items:
						span = Span(SpanKind.EXPLANATION, value)
						spans.append(span)
					elif item in correction_items:
						span = Span(SpanKind.CORRECTION, value)
						spans.append(span)
					elif item in citation_items:
						span = Span(SpanKind.CITATION, value)#, remove_cantillations(value))
						#span = Span(SpanKind.CITATION, value)
						spans.append(span)
					elif item in link_items:
						span = Span(SpanKind.LINK, value)
						spans.append(span)
					elif item in info_items:
						span = Span(SpanKind.INFO, value)
						spans.append(span)
					elif item in replacement_items:
						v = value[2:-2]
						ispoem, repeat, title, verses = tanakh.replace(v)
						if verses:
							spans.append(Span(SpanKind.LINK, title))
							spans.append(Span(SpanKind.PLAIN, '\n'))
							for verse in verses:
								if len(verses) > 1 and repeat < 2:
									spans.append(Span(SpanKind.VERSENO, verse.hebrew_number))
								for s in verse.mikra:
									spans.append(s)
									if ispoem or repeat > 1:
										if len(verses) > 1 and verses != verses[-1]:
											spans.append(Span(SpanKind.PLAIN, '\n'))
						else:
							spans.append(Span(SpanKind.PLAIN, value))
					elif item in plain_items:
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
