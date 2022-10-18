#!/usr/bin/env python
# -*- coding: utf-8  -*-

import hebrew_numbers
import os
import re
from common import Span, SpanKind

MISHNAH_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'db', 'mishnah')
BARTENURA_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'db', 'bartenura')

TOC = [
	['Zeraim', 'זְרָעִים', [
		['Berakhot', 'בְּרָכוֹת'],
		['Peah', 'פֵּאָה'],
		['Demai', 'דְּמַאי'],
		['Kilayim', 'כִּלְאַיִם'],
		['Sheviit', 'שְֹבִיעִית'],
		['Terumot', 'תְּרוּמוֹת'],
		['Maaserot', 'מַעֲשְׂרוֹת'], #Maasrot
		['Maaser Sheni', 'מַעֲשֵׂר שֵׁנִי'],
		['Challah', 'חַלָּה'],
		['Orlah', 'עָרְלָה'],
		['Bikkurim', 'בִּכּוּרִים']
		]],
	['Moed', 'מוֹעֵד', [
		['Shabbat', 'שַׁבָּת'],
		['Eruvin', 'עֵרוּבִין'],
		['Pesachim', 'פְּסָחִים'],
		['Shekalim', 'שְׁקָלִים'],
		['Yoma', 'יוֹמָא'],
		['Sukkah', 'סֻכָּה'],
		['Beitzah', 'בֵּיצָה'], ###
		['Rosh Hashanah', 'רֹאשׁ הַשָּׁנָה'],
		['Taanit', 'תַּעֲנִית'],
		['Megillah', 'מְגִלָּה'],
		['Moed Katan', 'מוֹעֵד קָטָן'],
		['Chagigah', 'חֲגִיגָה']
		]],
	['Nashim', 'נָשִׁים', [
		['Yevamot', 'יְבָמוֹת'],
		['Ketubot', 'כְּתוּבּוֹת'],
		['Nedarim', 'נְדָרִים'],
		['Nazir', 'נָזִיר'],
		['Sotah', 'סוֹטָה'],
		['Gittin', 'גִּטִּין'],
		['Kiddushin', 'קִדּוּשִׁין']
		]],
	['Nezikin', 'נְזִיקִין', [
		['Bava Kamma', 'בָּבָא קַמָּא'],
		['Bava Metzia', 'בָּבָא מְצִיעָא'],
		['Bava Batra', 'בָּבָא בָּתְרָא'],
		['Sanhedrin', 'סַנְהֶדְרִין'],
		['Makkot', 'מַכּוֹת'],
		['Shevuot', 'שְׁבוּעוֹת'],
		['Eduyot', 'עֵדֻיּוֹת'],
		['Avodah Zarah', 'עֲבוֹדָה זָרָה'],
		['Avot', 'אָבוֹת'],
		['Horayot', 'הוֹרָיוֹת'],
		]],
	['Kodashim', 'קָדָשִׁים', [
		['Zevachim', 'זבחים'],
		['Menachot', 'מנחות'],
		['Chullin', 'חולין'],
		['Bekhorot', 'בְּכוֹרוֹת'],
		['Arakhin', 'ערכין'],
		['Temurah', 'תְּמוּרָה'],
		['Keritot', 'כָּרֵתוֹת'],
		['Meilah', 'מעילה'],
		['Tamid', 'תָּמִיד'],
		['Middot', 'מִדּוֹת'],
		['Kinnim', 'קִנִּים'],
		]],
	['Tohorot', 'טְהָרוֹת', [
		['Kelim', 'כלים'], ###
		['Oholot', 'אהלות'],
		['Negaim', 'נגעים'],
		['Parah', 'פרה'],
		['Tohorot', 'טְהָרות'], #Tahorot
		['Mikvaot', 'מִקֶוָאוֹת'],
		['Niddah', 'נידה'],
		['Makhshirin', 'מכשירים'],
		['Zavim', 'זבים'],
		['Tevul Yom', 'טבול יום'],
		['Yadayim', 'יָדַיִם'],
		['Uktzim', 'עוקצים']#Oktzin
		]]
	]

class Verse:
	def __init__(self, number, chapter, mishnah_text, bartenura_text):
		self.number = number
		self.chapter = chapter
		self._mishnah_text = mishnah_text
		self._bartenura_text = bartenura_text
		self.hebrew_clean_number = hebrew_numbers.int_to_gematria(number, gershayim=False)
		self.hebrew_number = hebrew_numbers.int_to_gematria(number)

	@property
	def mishnah_text(self):
		return self._mishnah_text

	@mishnah_text.setter
	def mishnah_text(self, value):
		self._mishnah_text = value

	@property
	def mishnah(self):
		return parse(self._mishnah_text)

	@property
	def bartenura_text(self):
		return self._bartenura_text

	@bartenura_text.setter
	def bartenura_text(self, value):
		self._bartenura_text = value

	@property
	def bartenura(self):
		return parse_bartenura(self._bartenura_text)

class Chapter:
	def __init__(self, number, tractate, text):
		self.number = number
		self.tractate = tractate
		self.hebrew_number = hebrew_numbers.int_to_gematria(number)
		self.hebrew_clean_clean = hebrew_numbers.int_to_gematria(number, gershayim=False)
		self.verses = []
		self.text = text

class Tractate:
	def __init__(self, name, latin_name, number, order):
		self.name = name
		self.latin_name = latin_name
		self.number = number
		self.order = order
		self._chapters = None

	@property
	def mishnah_text(self):
		filename = '%d.%02d.txt'%(self.order.number, self.number)
		filename = os.path.join(MISHNAH_FOLDER, filename)
		return open(filename).read()

	@mishnah_text.setter
	def mishnah_text(self, value):
		filename = '%d.%02d.txt'%(self.order.number, self.number)
		filename = os.path.join(MISHNAH_FOLDER, filename)
		open(filename, 'w').write(value)

	@property
	def bartenura_text(self):
		filename = '%d.%02d.txt'%(self.order.number, self.number)
		filename = os.path.join(BARTENURA_FOLDER, filename)
		return open(filename).read().replace(':\u2028', '.\u2028')
		

	@bartenura_text.setter
	def bartenura_text(self, value):
		filename = '%d.%02d.txt'%(self.order.number, self.number)
		filename = os.path.join(BARTENURA_FOLDER, filename)
		open(filename, 'w').write(value)

	#def save(self):
	#	#self.mishnah_text = '\n\n'.join(['\n'.join([verse.mishnah_text for verse in chapter.verses]) for chapter in tractate.chapters])
	#	data = [[verse.mishnah_text for verse in chapter.verses] for chapter in tractate.chapters]
	#	print (data)

	@property
	def chapters(self):
		if self._chapters is None:
			self._chapters = []
			mishnah = [c.split('\n') for c in self.mishnah_text.split('\n\n')]
			bartenura = [c.split('\n') for c in self.bartenura_text.split('\n\n')]
			#print ("LEN", len(mishnah), len(bartenura))
			for chapter_nr in range(1, len(mishnah) + 1):
				#print ("ch nr", chapter_nr)
				#print ("LENCH", len(mishnah[chapter_nr - 1]), len(bartenura[chapter_nr - 1]))
				chapter = Chapter(chapter_nr, self, mishnah[chapter_nr - 1])
				for verse_nr in range(1, len(mishnah[chapter_nr - 1]) + 1):
					#print ("v nr", verse_number)
					#mishnah_text = verses_mishnah_parts[verse_number - 1]
					verse = Verse(verse_nr, chapter, mishnah[chapter_nr - 1][verse_nr - 1], 
							#mishnah[chapter_nr - 1][verse_nr - 1])
							bartenura[chapter_nr - 1][verse_nr - 1])
					chapter.verses.append(verse)
				self._chapters.append(chapter)
		return self._chapters

class Order:
	def __init__(self, name, latin_name, number):
		self.name = name
		self.latin_name = latin_name
		self.number = number
		self.tractates = []

orders = []
for x in range(len(TOC)):
	latin_name, name, toc = TOC[x]
	order = Order(name, latin_name, x + 1)
	for t in range(len(toc)):
		tractate_latin_name, tractate_name = toc[t]
		tractate = Tractate(tractate_name, tractate_latin_name, t + 1, order)
		order.tractates.append(tractate)
	orders.append(order)

def parse(text=''):
	if not text:
		return []
	text = re.sub('"([^"]+)"', r'”\1”', text)
	text = re.sub("'([^']+)'", r"’\1’", text)
	text = re.sub('^- ', '\u2015 ', text)#―
	text = re.sub(' -', ' \u2013', text)#–
	text = re.sub('-', '\u2011', text)
	#text = re.sub('{[^}]*}', '', text) #remove zohar page no
	#text = re.sub(' +', ' ', text)
#	h1_items = list(re.finditer('^=([^\n]+)', text, re.M))
#	for item in h1_items:
#		start, end = item.span()
#		text = text[0:start] + (end - start) * 'X' + text[end:]
#	alternative_items = list(re.finditer('\[([^|\]]*)\|([^]]+)\]', text))
#	for item in alternative_items:
#		start, end = item.span()
#		text = text[0:start] + (end - start) * 'X' + text[end:]
#	nonliteral_items = list(re.finditer('_([^_]+)_', text))
#	for item in nonliteral_items:
#		start, end = item.span()
#		text = text[0:start] + (end - start) * 'X' + text[end:]
#	addition_items = list(re.finditer('\+([^+]+)\+', text))
#	for item in addition_items:
#		start, end = item.span()
#		text = text[0:start] + (end - start) * 'X' + text[end:]
#	synonym_items = list(re.finditer('\(\=([^)]+)\)', text))
#	for item in synonym_items:
#		start, end = item.span()
#		text = text[0:start] + (end - start) * 'X' + text[end:]
#	explanation_items = list(re.finditer('\(\~([^)]+)\)', text))
#	for item in explanation_items:
#		start, end = item.span()
#		text = text[0:start] + (end - start) * 'X' + text[end:]
#	correction_items = list(re.finditer('\[([^]]+)\]', text))
#	for item in correction_items:
#		start, end = item.span()
#		text = text[0:start] + (end - start) * 'X' + text[end:]
	citation_items = list(re.finditer('\{([^}]+)\}', text))
	for item in citation_items:
		start, end = item.span()
		text = text[0:start] + (end - start) * 'X' + text[end:]
	link_items = list(re.finditer('\(([\u05d0-\u05ea־]+ [\u05d0-\u05ea]{1,3} [\u05d0-\u05ea]{1,3})\)', text)) + \
			list(re.finditer('\^([^^]+)\^', text))
	for item in link_items:
		start, end = item.span()
		text = text[0:start] + (end - start) * 'X' + text[end:]
	plain_items = list(re.finditer('([^X]+)', text))
	for item in plain_items:
		start, end = item.span()
		text = text[0:start] + (end - start) * '.' + text[end:]
	spans = []
	for idx in range(len(text)):
		for item in citation_items + link_items + plain_items:
			#nonliteral_items + addition_items + alternative_items + \
			#	synonym_items + explanation_items + correction_items + \
			# + h1_items:
			if idx == item.start():
				groups = item.groups()
				value = groups[0]
				#if len(groups) > 1:
				#	alt = groups[1]
				span = None
				#if item in h1_items:
				#	span = Span(SpanKind.H1, value)
				#elif item in nonliteral_items:
				#	span = Span(SpanKind.NONLITERAL, value)
				#elif item in addition_items:
				#	span = Span(SpanKind.ADDITION, value)
				#elif item in alternative_items:
				#	span = Span(SpanKind.ALTERNATIVE, value, alt)
				#elif item in synonym_items:
				#	span = Span(SpanKind.SYNONYM, value)
				#elif item in explanation_items:
				#	span = Span(SpanKind.EXPLANATION, value)
				#elif item in correction_items:
				#	span = Span(SpanKind.CORRECTION, value)
				if item in citation_items:
					span = Span(SpanKind.SCRIPTURE, value)
				elif item in link_items:
					span = Span(SpanKind.LINK, value)
				elif item in plain_items:
					span = Span(SpanKind.PLAIN, value)
				spans.append(span)
	return spans

#@property
def parse_bartenura(text):
	if 1:
		#if not text:
		#	return []
		text = text.replace('\u2028', '\n')
		text = re.sub('"([^"]+)"', r'”\1”', text)
		text = re.sub("'([^']+)'", r"’\1’", text)
		text = re.sub('^- ', '\u2015 ', text)#―
		text = re.sub(' -', ' \u2013', text)#–
		text = re.sub('-', '\u2011', text)
		legend_items = list(re.finditer('^([^\.]+)\.', text, re.M))
		for item in legend_items:
			start, end = item.span()
			text = text[0:start] + (end - start) * 'X' + text[end:]
		citation_items = list(re.finditer('\{([^}]+)\}', text))
		for item in citation_items:
			start, end = item.span()
			text = text[0:start] + (end - start) * 'X' + text[end:]
		link_items = list(re.finditer('\(([^\)]+)\)', text))
		for item in link_items:
			start, end = item.span()
			text = text[0:start] + (end - start) * 'X' + text[end:]
		reference_items = list(re.finditer('\{([^\}]+)\}', text))
		for item in reference_items:
			start, end = item.span()
			text = text[0:start] + (end - start) * 'X' + text[end:]
		plain_items = list(re.finditer('([^X]+)', text))
		for item in plain_items:
			start, end = item.span()
			text = text[0:start] + (end - start) * '.' + text[end:]
		spans = []
		for idx in range(len(text)):
			for item in legend_items + citation_items + link_items + reference_items + plain_items:
				if idx == item.start():
					groups = item.groups()
					value = groups[0]
					value = value.replace('\n', '')
					span = None
					if item in legend_items:
						#value = value[:-1]
						span = Span(SpanKind.LEGEND, value)
					elif item in citation_items:
						value = re.sub('"([^"]+)"', r'“\1”', value)
						span = Span(SpanKind.SCRIPTURE, value)
					elif item in link_items:
						#value = re.sub(' ', '\u00a0', value)
						span = Span(SpanKind.LINK, value)
					elif item in reference_items:
						#value = re.sub(' ', '\u00a0', value)
						span = Span(SpanKind.REFERENCE, value)
					#elif item in plain_items:
					else:
						#value = re.sub("'([^']+)'", r"‘\1’", value)
						span = Span(SpanKind.PLAIN, value)
					spans.append(span)
		return spans
#	print (spans)
