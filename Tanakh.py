#!/usr/bin/env python
# -*- coding: utf-8  -*-

import hebrew_numbers
import os
import re
from enum import Enum
from common import Span, SpanKind

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(ROOT_PATH, 'db')

class VerseKind(Enum):
	OPENED = 1
	CLOSED = 2
	BREAK = 3

bible_arr = [
	['Genesis', 50, 'בראשית'],
	['Exodus', 40, 'שמות'],
	['Leviticus', 27, 'ויקרא'],
	['Numbers', 36, 'במדבר'],
	['Deuteronomy', 34, 'דברים'],

	['Joshua', 24, 'יהושע'],
	['Judges', 21, 'שופטים'],
	['Samuel 1', 31,  'שמואל א׳'],
	['Samuel 2', 24, 'שמואל ב׳'],
	['Kings 1', 22, 'מלכים א׳'],
	['Kings 2', 25, 'מלכים ב׳'],

	['Isaiah', 66, 'יְשַׁעְיָה'],
	['Jeremiah', 52, 'ירמיה'],
	['Ezekiel', 48, 'יחזקאל'],

	['Hosea', 14, 'הושע'],
	['Joel', 4, 'יואל'],
	['Amos', 9, 'עמוס'],
	['Obadiah', 1, 'עובדיה'],
	['Jonah', 4, 'יונה'],
	['Micah', 7, 'מיכה'],
	['Nahum', 3, 'נחום'],
	['Habakkuk', 3, 'חבקוק'],
	['Zephaniah', 3,  'צפניה'],
	['Haggai', 2, 'חגי'],
	['Zechariah', 14,  'זכריה'],
	['Malachi', 3, 'מלאכי'],

	['Psalms', 150, 'תהלים'],
	['Proverbs', 31, 'משלי'],
	['Job', 42, 'איוב'],

	['Song of Songs', 8, 'שיר השירים'],
	['Ruth', 4, 'רות'],
	['Lamentations', 5, 'איכה'],
	['Ecclesiastes', 12, 'קהלת'],
	['Esther', 10, 'אסתר'],

	['Daniel', 12, 'דניאל'],
	['Ezra', 10, 'עזרא'],
	['Nehemiah', 13, 'נחמיה'],
	['Chronicles 1', 29, 'דברי הימים א׳'],
	['Chronicles 2', 36, 'דברי הימים ב׳']
	]

parashot_arr = [
	[
		# book_number, a-sc, a-sv, s-sc, s-sv, m-sc, m-sv, y-sc, y-sv,
		# a-ec, a-ev, s-ec, s-ev, m-ec, m-ev, y-ec, y-ev
		[1, 1, 6, 8, 'BeReshit', 'בְּרֵאשִׁית', 12, 42, 5, 42, 5, 42, 5, 42, 1, 43, 10, 42, 21, 42, 21, 42, 16],
		[6, 9, 11, 32, 'Noach', 'נֹחַ', 12, 54, 1, 54, 1, 54, 1, 54, 1, 54, 10, 54, 10, 54, 1, 55, 5],
		[12, 1, 17, 27, 'Lech Lecha', 'לֶךְ-לְךָ', 1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
		[18, 1, 22, 24, 'VaYera', 'וַיֵּרָא', 1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
		[23, 1, 25, 18, 'Chayei Sarah', 'חַיֵּי שָׂרָה', 1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
		[25, 19, 28, 9, 'Toledot', 'תּוֹלְדֹת', 1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
		[28, 10, 32, 3, 'VaYetze', 'וַיֵּצֵא', 1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
		[32, 4, 36, 43, 'VaYishlach', 'וַיִּשְׁלַח', 1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
		[37, 1, 40, 23, 'VaYeshev', 'וַיֵּשֶׁב', 1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
		[41, 1, 44, 17, 'MiKetz', 'מִקֵּץ', 1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
		[44, 18, 47, 27, 'VaYigash', 'וַיִּגַּשׁ', 1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
		[47, 28, 50, 26, 'VaYechi', 'וַיְחִי', 1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
	], [
		[1, 1, 6, 1, 'Shemot', 'שְׁמוֹת', 1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
		[6, 2, 9, 35, 'VaEira', 'וָאֵרָא', 1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
		[10, 1, 13, 16, 'Bo', 'בֹּא', 1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
		[13, 17, 17, 16, 'BeShalach', 'בְּשַׁלַּח', 1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
		[18, 1, 20, 23, 'Yitro', 'יִתְרוֹ', 1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
		[21, 1, 24, 18, 'Mishpatim', 'מִּשְׁפָּטִים', 1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
		[25, 1, 27, 19, 'Terumah', 'תְּרוּמָה', 1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
		[27, 20, 30, 10, 'Tetzaveh', 'תְּצַוֶּה', 1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
		[30, 11, 34, 35, 'Ki Tisa', 'כִּי תִשָּׂא', 1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
		[35, 1, 38, 20, 'VaYakhel', 'וַיַּקְהֵל', 1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
		[38, 21, 40, 38, 'Pekudei', 'פְקוּדֵי', 1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
	], [
		[1, 1, 5, 26, 'VaYikra', 'וַיִּקְרָא', 1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
		[6, 1, 8, 36, 'Tzav', 'צַו', 1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
		[9, 1, 11, 47, 'Shemini', 'שְּׁמִינִי', 1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
		[12, 1, 13, 59, 'Tazria', 'תַזְרִיעַ', 1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
		[14, 1, 15, 33, 'Metzora', 'מְּצֹרָע', 1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
		[16, 1, 18, 30, 'Acharei Mot', 'אַחֲרֵי מוֹת', 1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
		[19, 1, 20, 27, 'Kedoshim', 'קְדֹשִׁים', 1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
		[21, 1, 24, 23, 'Emor', 'אֱמֹר', 1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
		[25, 1, 26, 1, 'BeHar', 'בְּהַר', 1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
		[26, 3, 27, 34, 'BeChukotai', 'בְּחֻקֹּתַי', 1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
	], [
		[1, 1, 4, 20, 'BaMidbar', 'בְּמִדְבַּר', 1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
		[4, 21, 7, 89, 'Naso', 'נָשֹׂא', 1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
		[8, 1, 12, 16, 'BeHaalotecha', 'בְּהַעֲלֹתְךָ', 1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
		[13, 1, 15, 41, 'Shlach ', 'שְׁלַח-לְךָ', 1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
		[16, 1, 18, 32, 'Korach', 'קֹרַח', 1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
		[19, 1, 22, 1, 'Chukat', 'חֻקַּת', 1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
		[22, 2, 25, 9, 'Balak', 'בָּלָק', 1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
		[25, 10, 30, 1, 'Pinchas', 'פִּינְחָס', 1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
		[30, 2, 32, 42, 'Matot', 'מַּטּוֹת', 1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
		[33, 1, 36, 13, 'Masei', 'מַסְעֵי', 1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
	], [
		[1, 1, 3, 22, 'Devarim', 'דְּבָרִים', 1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
		[3, 23, 7, 11, 'VaEtchanan', 'וָאֶתְחַנַּן', 1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
		[7, 12, 11, 25, 'Eikev', 'עֵקֶב', 1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
		[11, 26, 16, 17, "Re'eh", 'רְאֵה', 1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
		[16, 18, 21, 9, 'Shoftim', 'שֹׁפְטִים', 1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
		[21, 10, 25, 19, 'Ki Teitzei', 'כִּי-תֵצֵא', 1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
		[26, 1, 29, 8, 'Ki Tavo', 'כִּי-תָבוֹא', 1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
		[29, 9, 30, 20, 'Nitzavim', 'נִצָּבִים', 1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
		[31, 1, 31, 30, 'VaYelech', 'וַיֵּלֶךְ', 1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
		[32, 1, 32, 52, 'Haazinu', 'הַאֲזִינוּ', 1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
		[33, 1, 34, 12, 'VeZot Haberakha', 'וְזֹאת הַבְּרָכָה', 1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]]
	]

def parse(text):
	if not text:
		return []
	text = re.sub('"([^"]+)"', r'“\1”', text)
	text = re.sub("'([^']+)'", r"‘\1’", text)
	text = re.sub('^- ', '\u2015 ', text)
	text = re.sub(' -', ' \u2013', text)
	text = re.sub('-', '\u2011', text)
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
	plain_items = list(re.finditer('([^X]+)', text))
	for item in plain_items:
		start, end = item.span()
		text = text[0:start] + (end - start) * '.' + text[end:]
	spans = []
	for idx in range(len(text)):
		for item in nonliteral_items + addition_items + alternative_items + \
				synonym_items + explanation_items + correction_items + plain_items:
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
				elif item in plain_items:
					span = Span(SpanKind.PLAIN, value)
				spans.append(span)
	return spans




#class Verse:
#	def __init__(self, no, text):
#		self.no = no
#		self.hno = hebrew_numbers.int_to_gematria(no, gershayim=False)
#		self.hnog = hebrew_numbers.int_to_gematria(no)
#		self.text = text

#class VerseKind(Enum):
#	OPENED = 1
#	CLOSED = 2
#	BREAK = 3

#class Chapter:
#	def __init__(self, no):
#		self.no = no
#		self.hno = hebrew_numbers.int_to_gematria(no, gershayim=False)
#		self.hnog = hebrew_numbers.int_to_gematria(no)
#		self.verses = []
#		self.articles = []

#class Book:
#	def __init__(self, name, hname, ind):
#		self.name = name
#		self.hname = hname
#		self.ind = ind
#		self.chapters = []
		
		
		
		
		
		
		
		
		
		

#class Collection:
#	def __init__(self):
#		self.books = []

#class Order:
#	def __init__(self, name, hname):
#		self.name = name
#		self.hname = hname
#		self.books = []

#class Span:
#	def __init__(self, kind, value, alt=None):
#		self.kind = kind
#		self.value = value
#		self.alt = alt
#
#	def __repr__(self):
#		return 'span=%s'%self.kind + '\n' + self.value + '\n'

class NVerse:
	def __init__(self, chapter, number, text):
		self.chapter = chapter
		self.parasha = None
		self.number = number
		self.hebrew_number = hebrew_numbers.int_to_gematria(number)

		self._mikra_text = text
		self._title_text = ''
		self._onkelos_text = ''
		self._onkelos_trans_text = ''
		self._jerusalmi_text = ''
		self._jerusalmi_trans_text = ''
		self._jonathan_text = ''
		self._jonathan_trans_text = ''
		self._targum_text = ''
		self._targum_trans_text = ''
		self._rashi_text = ''

	def __repr__(self):
		return "Verse %d.%d.%d"%(self.chapter.book.number, self.chapter.number, self.number)

	@property
	def book(self):
		return self.chapter.book

	def get_text(self, name):
		if self.__dict__['_' + name + '_text']:
			return self.__dict__['_' + name + '_text']
		filename = '%02d.%03d.txt'%(self.book.number, self.chapter.number)
		data = open(os.path.join(DB_PATH, name, filename)).read()
		value = data.split('\n')[self.number - 1]
		self.__dict__['_' + name + '_text'] = value
		return value

	def set_text(self, name, value):
		print (name)
		self.__dict__['_' + name + '_text'] = value
		filename = '%02d.%03d.txt'%(self.book.number, self.chapter.number)
		path = os.path.join(DB_PATH, name, filename)
		lines = open(path).read().split('\n')
		lines[self.number - 1] = value
		data = '\n'.join(lines)
		open(path, 'w').write(data)

	@property
	def mikra_text(self):
		return self.get_text('mikra')

	@mikra_text.setter
	def mikra_text(self, value):
		self.set_text('mikra', value)

	@property
	def title_text(self):
		return self.get_text('title')

	@title_text.setter
	def title_text(self, value):
		self.set_text('title', value)

	@property
	def onkelos_text(self):
		if not self.has_onkelos:
			return
		return self.get_text('onkelos')

	@onkelos_text.setter
	def onkelos_text(self, value):
		if not self.has_onkelos:
			return
		self.set_text('onkelos', value)

	@property
	def onkelos_trans_text(self):
		if not self.has_onkelos:
			return
		return self.get_text('onkelos_trans')

	@onkelos_trans_text.setter
	def onkelos_trans_text(self, value):
		if not self.has_onkelos:
			return
		self.set_text('onkelos_trans', value)

	@property
	def jerusalmi_text(self):
		if not self.has_jerusalmi:
			return
		return self.get_text('jerusalmi')

	@jerusalmi_text.setter
	def jerusalmi_text(self, value):
		if not self.has_jerusalmi:
			return
		self.set_text('jerusalmi', value)

	@property
	def jerusalmi_trans_text(self):
		if not self.has_jerusalmi:
			return
		return self.get_text('jerusalmi_trans')

	@jerusalmi_trans_text.setter
	def jerusalmi_trans_text(self, value):
		if not self.has_jerusalmi:
			return
		self.set_text('jerusalmi_trans', value)

	@property
	def jonathan_text(self):
		if not self.has_jonathan:
			return
		return self.get_text('jonathan')

	@jonathan_text.setter
	def jonathan_text(self, value):
		if not self.has_jonathan:
			return
		self.set_text('jonathan', value)

	@property
	def jonathan_trans_text(self):
		if not self.has_jonathan:
			return
		return self.get_text('jonathan_trans')

	@jonathan_trans_text.setter
	def jonathan_trans_text(self, value):
		if not self.has_jonathan:
			return
		self.set_text('jonathan_trans', value)

	@property
	def targum_text(self):
		if not self.has_targum:
			return
		return self.get_text('targum')

	@targum_text.setter
	def targum_text(self, value):
		if not self.has_targum:
			return
		self.set_text('targum', value)

	@property
	def targum_trans_text(self):
		if not self.has_targum:
			return
		return self.get_text('targum_trans')

	@targum_trans_text.setter
	def targum_trans_text(self, value):
		if not self.has_targum:
			return
		self.set_text('targum_trans', value)

	@property
	def rashi_text(self):
		return self.get_text('rashi')

	@rashi_text.setter
	def rashi_text(self, value):
		self.set_text('rashi', value)

	@property
	def kind(self):
		if self.number > 1:
			prev_verse = self.chapter.verses[self.number - 2]
		else:
			if self.chapter.number > 1:
				prev_chapter = self.book.chapters[self.chapter.number - 2]
				prev_verse = prev_chapter.verses[-1]
			else:
				prev_verse = None
		if prev_verse:
			if prev_verse.mikra_text.endswith('{פ}') or prev_verse.mikra_text.endswith('{פ} '):
				return VerseKind.OPENED
			elif prev_verse.mikra_text.endswith('{ס}') or prev_verse.mikra_text.endswith('{ס} '):
				return VerseKind.CLOSED
		if self.mikra_text.startswith(chr(12)):
			return VerseKind.BREAK
		return None


	@property
	def has_onkelos(self):
		return self.chapter.has_onkelos

	@property
	def onkelos(self):
		return parse(self.onkelos_text)

	@property
	def onkelos_trans(self):
		return parse(self.onkelos_trans_text)

	@property
	def has_jerusalmi(self):
		return self.chapter.has_jerusalmi

	@property
	def jerusalmi(self):
		return parse(self.jerusalmi_text)

	@property
	def jerusalmi_trans(self):
		return parse(self.jerusalmi_trans_text)

	@property
	def has_jonathan(self):
		return self.chapter.has_jonathan

	@property
	def jonathan(self):
		return parse(self.jonathan_text)

	@property
	def has_targum(self):
		return self.chapter.has_targum

	@property
	def targum(self):
		return parse(self.targum_text)

	@property
	def targum_trans(self):
		return parse(self.targum_trans_text)

	@property
	def mikra(self):
		text = self.mikra_text
		text = re.sub('"([^"]+)"', r'“\1”', text)
		text = re.sub("'([^']+)'", r"‘\1’", text)
		text = re.sub(' -', ' \u2013', text)
		text = re.sub('-', '\u2011', text)
		aliyot_items = list(re.finditer('\{(ראשון|שני|שלישי|רביעי|חמישי|ששי|שביעי|מפטיר)\} ', text))
		for item in aliyot_items:
			start, end = item.span()
			text = text[0:start] + (end - start) * 'X' + text[end:]
		kriktiv_items = list(re.finditer('\[([^|]+)\|([^]]+)\]', text))
		for item in kriktiv_items:
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
		plain_items = list(re.finditer('([^X]+)', text))
		for item in plain_items:
			start, end = item.span()
			text = text[0:start] + (end - start) * '.' + text[end:]
		spans = []
		for idx in range(len(text)):
			for item in aliyot_items + kriktiv_items + majuscule_items + minuscule_items + plain_items:
				if idx == item.start():
					groups = item.groups()
					value = groups[0]
					if len(groups) > 1:
						alt = groups[1]
					span = None
					if item in aliyot_items:
						span = Span(SpanKind.ALIYA, value)
					elif item in kriktiv_items:
						span = Span(SpanKind.KRIKTIV, value, alt)
					elif item in majuscule_items:
						span = Span(SpanKind.MAJUSCULE, value)
					elif item in minuscule_items:
						span = Span(SpanKind.MINUSCULE, value)
					elif item in plain_items:
						value = re.sub('\{\{[^\}]+\}\}\s* ', '', value)
						value = re.sub('\{[^\}]+\}\s*', '', value) # open/closed portion
						span = Span(SpanKind.PLAIN, value)
					spans.append(span)
		return spans

	@property
	def rashi(self):
		text = self.rashi_text.replace('\u2028', '\n')
		legend_items = list(re.finditer('^([^\.]+)\.', text, re.M))
		for item in legend_items:
			start, end = item.span()
			text = text[0:start] + (end - start) * 'X' + text[end:]
		citation_items = list(re.finditer('"([^"]+)"', text))
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
#		text = text.replace('\n', '\u2028')
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
					span = None
					if item in legend_items:
						#value = value[:-1]
						span = Span(SpanKind.LEGEND, value)
					elif item in citation_items:
						#value = re.sub('"([^"]+)"', r'“\1”', value)
						span = Span(SpanKind.CITATION, value)
					elif item in link_items:
						value = re.sub(' ', '\u00a0', value)
						span = Span(SpanKind.LINK, value)
					elif item in reference_items:
						value = re.sub(' ', '\u00a0', value)
						span = Span(SpanKind.REFERENCE, value)
					elif item in plain_items:
						value = re.sub("'([^']+)'", r"‘\1’", value)
						span = Span(SpanKind.PLAIN, value)
					spans.append(span)
		return spans

def verses_to_paragraphs(verses):
	paragraphs = []
	vbuffer = []
	sbuffer = []
	for verse in verses:
		if verse == verses[0]:
			vbuffer = [verse]
		elif verse.kind == VerseKind.OPENED:
			sbuffer.append(vbuffer)
			paragraphs.append(sbuffer)
			sbuffer = []
			vbuffer = [verse]
		elif verse.kind in [VerseKind.CLOSED, VerseKind.BREAK]:
			sbuffer.append(vbuffer)
			vbuffer = [verse]
#		elif verse.kind == VerseKind.BREAK:
#			vbuffer.append(verse)
		else:
			vbuffer.append(verse)
	sbuffer.append(vbuffer)
	paragraphs.append(sbuffer)
	#print (paragraphs[0])
	return paragraphs

	"""def verses_to_paragraphsx(verses):
	paragraphs = []
	part = []
	parts = []
	for verse in verses:
		if verse == verses[0]:
			part = [verse]
		elif verse.kind == VerseKind.OPENED:
			parts.append(part)
			paragraphs.append(parts)
			parts = []
			part = [verse]
		elif verse.kind == VerseKind.CLOSED:
			parts.append(part)
			part = [verse]
		else:
			part.append(verse)
	parts.append(part)
	paragraphs.append(parts)
	return paragraphs
	"""

class NChapter:
	def __init__(self, book, number):
		self.book = book
		self.number = number
		self.hebrew_number = hebrew_numbers.int_to_gematria(number)
		self._verses = []

	@property
	def verses(self):
		if self._verses:
			return self._verses
		filename = '%02d.%03d.txt'%(self.book.number, self.number)
		f = open(os.path.join(DB_PATH, 'mikra', filename))
		for number, text in enumerate(f, start=1):
			if text.endswith('\n'):
				text = text[:-1]
			verse = NVerse(self, number, text)
			self._verses.append(verse)
		return self._verses

	@property
	def paragraphs(self):
		return verses_to_paragraphs(self.verses)

	@property
	def has_onkelos(self):
		return self.book.has_onkelos

	@property
	def has_jerusalmi(self):
		return self.book.has_jerusalmi

	@property
	def has_jonathan(self):
		return self.book.has_jonathan

	@property
	def has_targum(self):
		return self.book.has_targum

class Parasha:
	def __init__(self, book, number, name, latin_name):
		self.book = book
		self.number = number
		self.name = name
		self.latin_name = latin_name
		self.verses = []
		self.haftara = None

	@property
	def paragraphs(self):
		return verses_to_paragraphs(self.verses)

class Haftara:
	def __init__(self):
		flavors = ['ashkenaz', 'sefard', 'mizrah', 'yemen']
		self.book = 4 * [None]
		self.start_chapter = 4 * [None]
		self.start_verse = 4 * [None]
		self.end_chapter = 4 * [None]
		self.end_verse = 4 * [None]
		self.verses = []

	@property
	def paragraphs(self):
		return verses_to_paragraphs(self.verses)

class NBook:
	def __init__(self, number, name, latin_name):
		self.number = number
		self.name = name
		self.latin_name = latin_name
		self.chapters = []
		self.has_onkelos = number in [1, 2, 3, 4, 5]
		self.has_onkelos = number in [1]
		self.has_jerusalmi = self.has_onkelos
		self.has_jonathan = number in list(range(6, 27))
		self.has_targum = number in [27]
		self.is_poem = number in [27, 28, 29, 30]
		filenames = [f for f in os.listdir(os.path.join(DB_PATH, 'mikra')) if f.startswith('%02d.'%number)]
		for idx, filename in enumerate(filenames):
			chapter = NChapter(self, idx + 1)
			self.chapters.append(chapter)
		if self.number > 5:
			return
		self.parashot = []
		for number, value in enumerate(parashot_arr[self.number - 1], start=1):
			start_chapter, start_verse, end_chapter, end_verse, latin_name, name = value[:6]
#			print (number, value[:6])
#		for number, value in enumerate(parashot_arr[self.number - 1], start=1):
#			start_chapter, start_verse, end_chapter, end_verse, latin_name, name = value[:6]
#					book_number, a_start_chapter, a_start_verse, s_start_chapter, s_start_verse, \
#					m_start_chapter, m_start_verse, y_start_chapter, y_start_verse, \
#					a_end_chapter, a_end_verse, s_end_chapter, s_end_verse, \
#					m_end_chapter, m_end_verse, y_end_chapter, y_end_verse = value
			parasha = Parasha(self, number, name, latin_name)
			chapter_idx = start_chapter - 1
			verse_idx = start_verse - 1
			while True:
				chapter = self.chapters[chapter_idx]
				verse = chapter.verses[verse_idx]
				verse.parasha = parasha
				parasha.verses.append(verse)
				if chapter_idx == end_chapter - 1 and verse_idx == end_verse - 1:
					break
				if verse_idx < len(chapter.verses) - 1:
					verse_idx += 1
				else:
					verse_idx = 0
					chapter_idx += 1
			self.parashot.append(parasha)

class Tanakh:
	def __init__(self):
		self.books = []
		for x in range(len(bible_arr)):
			latin_name, num_chapters, name = bible_arr[x]
			book = NBook(x + 1, name, latin_name)
			self.books.append(book)
	def __postinit__(self):
		for b in range(5):
			book = self.books[b]
			for p in range(len(book.parashot)):
				parasha = book.parashot[p]
				haftara = Haftara()
#		for number, value in enumerate(parashot_arr[self.number - 1], start=1):
				book_number = parashot_arr[b][p][6]
				haftara.book[0] = self.books[book_number - 1]
				haftara.start_chapter[0], haftara.start_verse[0], haftara.start_chapter[1], haftara.start_verse[1], \
					haftara.start_chapter[2], haftara.start_verse[2], haftara.start_chapter[3], haftara.start_verse[3], \
					haftara.end_chapter[0], haftara.end_verse[0], haftara.end_chapter[1], haftara.end_verse[1], \
					haftara.end_chapter[2], haftara.end_verse[2], haftara.end_chapter[3], haftara.end_verse[3] = parashot_arr[b][p][7:]
				start_chapter = min(haftara.start_chapter)
				start_verse = min([haftara.start_verse[x] for x in [i for i in range(4) if start_chapter == haftara.start_chapter[i]]])
				end_chapter = max(haftara.end_chapter)
				end_verse = max([haftara.end_verse[x] for x in [i for i in range(4) if end_chapter == haftara.end_chapter[i]]])
				chapter_idx = start_chapter - 1
				verse_idx = start_verse - 1
				while True:
					chapter = haftara.book[0].chapters[chapter_idx]
					verse = chapter.verses[verse_idx]
					verse.parasha = parasha
					haftara.verses.append(verse)
					if chapter_idx == end_chapter - 1 and verse_idx == end_verse - 1:
						break
					if verse_idx < len(chapter.verses) - 1:
						verse_idx += 1
					else:
						verse_idx = 0
						chapter_idx += 1

				self.books[b].parashot[p].haftara = haftara



#tanakh = Tanakh()
#tanakh.__postinit__()

#Bible = []
#for x in range(len(bible_arr)):
#	name, num_chapters, hname = bible_arr[x]
#	book = Book(name, hname, x + 1)
#	for c in range(1, num_chapters + 1):
#		chapter = Chapter(c)
#		book.chapters.append(chapter)
#	Bible.append(book)

