#!/usr/bin/env python
# -*- coding: utf-8  -*-

import hebrew_numbers
import os
import re

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(ROOT_PATH, 'db')

mishnah_arr = [
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

	['Isaiah', 66, 'ישעיה'],
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
		[1, 1, 6, 8, 'BeReshit', 'בְּרֵאשִׁית'],
		[6, 9, 11, 32, 'Noach', 'נֹחַ'],
		[12, 1, 17, 27, 'Lech Lecha', 'לֶךְ-לְךָ'],
		[18, 1, 22, 24, 'VaYera', 'וַיֵּרָא'],
		[23, 1, 25, 18, 'Chayei Sarah', 'חַיֵּי שָׂרָה'],
		[25, 19, 28, 9, 'Toledot', 'תּוֹלְדֹת'],
		[28, 10, 32, 3, 'VaYetze', 'וַיֵּצֵא'],
		[32, 4, 36, 43, 'VaYishlach', 'וַיִּשְׁלַח'],
		[37, 1, 40, 23, 'VaYeshev', 'וַיֵּשֶׁב'],
		[41, 1, 44, 17, 'MiKetz', 'מִקֵּץ'],
		[44, 18, 47, 27, 'VaYigash', 'וַיִּגַּשׁ'],
		[47, 28, 50, 26, 'VaYechi', 'וַיְחִי']
	], [
		[1, 1, 6, 1, 'Shemot', 'שְׁמוֹת'],
		[6, 2, 9, 35, 'VaEira', 'וָאֵרָא'],
		[10, 1, 13, 16, 'Bo', 'בֹּא'],
		[13, 17, 17, 16, 'BeShalach', 'בְּשַׁלַּח'],
		[18, 1, 20, 23, 'Yitro', 'יִתְרוֹ'],
		[21, 1, 24, 18, 'Mishpatim', 'מִּשְׁפָּטִים'],
		[25, 1, 27, 19, 'Terumah', 'תְּרוּמָה'],
		[27, 20, 30, 10, 'Tetzaveh', 'תְּצַוֶּה'],
		[30, 11, 34, 35, 'Ki Tisa', 'כִּי תִשָּׂא'],
		[35, 1, 38, 20, 'VaYakhel', 'וַיַּקְהֵל'],
		[38, 21, 40, 38, 'Pekudei', 'פְקוּדֵי']
	], [
		[1, 1, 5, 26, 'VaYikra', 'וַיִּקְרָא'],
		[6, 1, 8, 36, 'Tzav', 'צַו'],
		[9, 1, 11, 47, 'Shemini', 'שְּׁמִינִי'],
		[12, 1, 13, 59, 'Tazria', 'תַזְרִיעַ'],
		[14, 1, 15, 33, 'Metzora', 'מְּצֹרָע'],
		[16, 1, 18, 30, 'Acharei Mot', 'אַחֲרֵי מוֹת'],
		[19, 1, 20, 27, 'Kedoshim', 'קְדֹשִׁים'],
		[21, 1, 24, 23, 'Emor', 'אֱמֹר'],
		[25, 1, 26, 1, 'BeHar', 'בְּהַר'],
		[26, 3, 27, 34, 'BeChukotai', 'בְּחֻקֹּתַי']
	], [
		[1, 1, 4, 20, 'BaMidbar', 'בְּמִדְבַּר'],
		[4, 21, 7, 89, 'Naso', 'נָשֹׂא'],
		[8, 1, 12, 16, 'BeHaalotecha', 'בְּהַעֲלֹתְךָ'],
		[13, 1, 15, 41, 'Shlach ', 'שְׁלַח-לְךָ'],
		[16, 1, 18, 32, 'Korach', 'קֹרַח'],
		[19, 1, 22, 1, 'Chukat', 'חֻקַּת'],
		[22, 2, 25, 9, 'Balak', 'בָּלָק'],
		[25, 10, 30, 1, 'Pinchas', 'פִּינְחָס'],
		[30, 2, 32, 42, 'Matot', 'מַּטּוֹת'],
		[33, 1, 36, 13, 'Masei', 'מַסְעֵי']
	], [
		[1, 1, 3, 22, 'Devarim', 'דְּבָרִים'],
		[3, 23, 7, 11, 'VaEtchanan', 'וָאֶתְחַנַּן'],
		[7, 12, 11, 25, 'Eikev', 'עֵקֶב'],
		[11, 26, 16, 17, "Re'eh", 'רְאֵה'],
		[16, 18, 21, 9, 'Shoftim', 'שֹׁפְטִים'],
		[21, 10, 25, 19, 'Ki Teitzei', 'כִּי-תֵצֵא'],
		[26, 1, 29, 8, 'Ki Tavo', 'כִּי-תָבוֹא'],
		[29, 9, 30, 20, 'Nitzavim', 'נִצָּבִים'],
		[31, 1, 31, 30, 'VaYelech', 'וַיֵּלֶךְ'],
		[32, 1, 32, 52, 'Haazinu', 'הַאֲזִינוּ'],
		[33, 1, 34, 12, 'VeZot Haberakha', 'וְזֹאת הַבְּרָכָה']
	]]

a = 1
b = 2
zohar_arr = [
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

class Article:
	def __init__(self, no, title, he_title):
		self.no = no
		self.hno = hebrew_numbers.int_to_gematria(no, gershayim=False)
		self.hnog = hebrew_numbers.int_to_gematria(no)
		self.title = title
		self.he_title = he_title

class ZoharChapter:
	def __init__(self, no):
		self.no = no
		self.hno = hebrew_numbers.int_to_gematria(no, gershayim=False)
		self.hnog = hebrew_numbers.int_to_gematria(no)
		self.articles = []

class Verse:
	def __init__(self, no, text):
		self.no = no
		self.hno = hebrew_numbers.int_to_gematria(no, gershayim=False)
		self.hnog = hebrew_numbers.int_to_gematria(no)
		self.text = text

from enum import Enum
class SpanKind(Enum):

	PLAIN = 0
	LEGEND = 1
	CITATION = 2
	REFERENCE = 3

	MAJUSCULE = 4
	MINUSCULE = 5

	KRIKTIV = 6
	ALIYA = 7

	CHAPTERNO = 10
	VERSENO = 11

	ALTERNATIVE = 20
	ADDITION = 21
	NONLITERAL = 22

class VerseKind(Enum):
	OPENED = 1
	CLOSED = 2

class Chapter:
	def __init__(self, no):
		self.no = no
		self.hno = hebrew_numbers.int_to_gematria(no, gershayim=False)
		self.hnog = hebrew_numbers.int_to_gematria(no)
		self.verses = []
		self.articles = []

class Book:
	def __init__(self, name, hname, ind):
		self.name = name
		self.hname = hname
		self.ind = ind
		self.chapters = []

#class Collection:
#	def __init__(self):
#		self.books = []

class Order:
	def __init__(self, name, hname):
		self.name = name
		self.hname = hname
		self.books = []

class Span:
	def __init__(self, kind, value, alt=None):
		self.kind = kind
		self.value = value
		self.alt = alt

class NVerse:
	def __init__(self, chapter, number, text):
		self.chapter = chapter
		self.parasha = None
		self.number = number
		self.hebrew_number = hebrew_numbers.int_to_gematria(number)
		self.text = text
		self.onkelos_text = None
		self.rashi_text = None

	def __repr__(self):
		return "Verse %d.%d.%d"%(self.chapter.book.number, self.chapter.number, self.number)

	@property
	def kind(self):
		if self.number > 1:
			prev_verse = self.chapter.verses[self.number - 2]
		else:
			if self.chapter.number > 1:
				prev_chapter = self.chapter.book.chapters[self.chapter.number - 2]
				prev_verse = prev_chapter.verses[-1]
			else:
				prev_verse = None
		if prev_verse:
			if prev_verse.text.endswith('{פ}') or prev_verse.text.endswith('{פ} '):
				return VerseKind.OPENED
			elif prev_verse.text.endswith('{ס}') or prev_verse.text.endswith('{ס} '):
				return VerseKind.CLOSED
		return None

	@property
	def onkelos(self):
		text = self.onkelos_text
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
		plain_items = list(re.finditer('([^X]+)', text))
		for item in plain_items:
			start, end = item.span()
			text = text[0:start] + (end - start) * '.' + text[end:]
		spans = []
		for idx in range(len(text)):
			for item in nonliteral_items + addition_items + alternative_items + plain_items:
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
					elif item in plain_items:
						span = Span(SpanKind.PLAIN, value)
					spans.append(span)
		return spans

	@property
	def mikra(self):
		text = self.text
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
		legend_items = list(re.finditer('^[^\.]+\.', text, re.M))
		for item in legend_items:
			start, end = item.span()
			text = text[0:start] + (end - start) * 'X' + text[end:]
		citation_items = list(re.finditer('"[^"]+"', text))
		for item in citation_items:
			start, end = item.span()
			text = text[0:start] + (end - start) * 'X' + text[end:]
		reference_items = list(re.finditer('\([^\)]+\)', text))
		for item in reference_items:
			start, end = item.span()
			text = text[0:start] + (end - start) * 'X' + text[end:]
#		text = text.replace('\n', '\u2028')
		plain_items = list(re.finditer('[^X]+', text))
		for item in plain_items:
			start, end = item.span()
			text = text[0:start] + (end - start) * '.' + text[end:]
		spans = []
		for idx in range(len(text)):
			for item in legend_items + citation_items + reference_items + plain_items:
				if idx == item.start():
					value = item.group()
					span = None
					if item in legend_items:
						span = Span(SpanKind.LEGEND, value)
					elif item in citation_items:
						value = re.sub('"([^"]+)"', r'“\1”', value)
						span = Span(SpanKind.CITATION, value)
					elif item in reference_items:
						value = re.sub(' ', '\u00a0', value)
						span = Span(SpanKind.REFERENCE, value)
					elif item in plain_items:
						value = re.sub("'([^']+)'", r"‘\1’", value)
						span = Span(SpanKind.PLAIN, value)
					spans.append(span)
		return spans

	def save_onkelos(self):
		if not self.chapter.book.has_onkelos:
			return
		filename = '%01d.%02d.txt'%(self.chapter.book.number, self.chapter.number)
		path = os.path.join(DB_PATH, 'onkelos', filename)
		f = open(path)
		lines = f.read().split('\n')
		lines[self.number - 1] = self.onkelos_text
		data = '\n'.join(lines)
		open(path, 'w').write(data)

	def save_rashi(self):
		filename = '%02d.%03d.txt'%(self.chapter.book.number, self.chapter.number)
		path = os.path.join(DB_PATH, 'rashi', filename)
		f = open(path)
		lines = f.read().split('\n')
		lines[self.number - 1] = self.rashi_text
		data = '\n'.join(lines)
		open(path, 'w').write(data)

def verses_to_paragraphs(verses):
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

class NChapter:
	def __init__(self, book, number):
		self.book = book
		self.number = number
		self.hebrew_number = hebrew_numbers.int_to_gematria(number)
		self.verses = []
		filename = '%02d.%03d.txt'%(self.book.number, self.number)
		f = open(os.path.join(DB_PATH, 'tanakh', filename))
		for number, text in enumerate(f, start=1):
			verse = NVerse(self, number, text[:-1])
			self.verses.append(verse)
		filename = '%02d.%03d.txt'%(self.book.number, self.number)
		f = open(os.path.join(DB_PATH, 'rashi', filename))
		for idx, text in enumerate(f):
			self.verses[idx].rashi_text = text[:-1]
		if book.has_onkelos:
			filename = '%1d.%02d.txt'%(self.book.number, self.number)
			f = open(os.path.join(DB_PATH, 'onkelos', filename))
			for idx, text in enumerate(f):
				self.verses[idx].onkelos_text = text[:-1]

	@property
	def paragraphs(self):
		return verses_to_paragraphs(self.verses)

class Parasha:
	def __init__(self, book, number, name, latin_name):
		self.book = book
		self.number = number
		self.name = name
		self.latin_name = latin_name
		self.verses = []

	@property
	def paragraphs(self):
		return verses_to_paragraphs(self.verses)

class NBook:
	def __init__(self, number, name, latin_name):
		self.number = number
		self.name = name
		self.latin_name = latin_name
		self.is_poem = number in [27, 28, 29, 30]
		self.has_onkelos = number in [1, 2, 3, 4, 5]
		self.chapters = []
		filenames = [f for f in os.listdir(os.path.join(DB_PATH, 'tanakh')) if f.startswith('%02d.'%number)]
		for idx, filename in enumerate(filenames):
			chapter = NChapter(self, idx + 1)
			self.chapters.append(chapter)
		if self.number > 5:
			return
		self.parashot = []
		for number, value in enumerate(parashot_arr[self.number - 1], start=1):
			start_chapter, start_verse, end_chapter, end_verse, latin_name, name = value
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

tanakh = Tanakh()

Bible = []
for x in range(len(bible_arr)):
	name, num_chapters, hname = bible_arr[x]
	book = Book(name, hname, x + 1)
	for c in range(1, num_chapters + 1):
		chapter = Chapter(c)
		book.chapters.append(chapter)
	Bible.append(book)

Mishnah = []
for x in range(len(mishnah_arr)):
	name, hname, tractate_arr = mishnah_arr[x]
	order = Order(name, hname)
	for t in range(len(tractate_arr)):
		tractate_name, tractate_hname = tractate_arr[t]
		tractate = Book(tractate_name, tractate_hname, t + 1)
		order.books.append(tractate)
	Mishnah.append(order)

Zohar = []
for x in range(len(zohar_arr)):
	hname, chapter_arr = zohar_arr[x]
	book = Book('', hname, x + 1)
	for c in range(len(chapter_arr)):
		start_daf, start_amud, start_verse, end_daf, end_amud, end_verse, hname = chapter_arr[c]
		chapter = Chapter(c + 1)
		chapter.hname = hname
		path = '../db/zohar/%1d.%02d/00.txt'%(book.ind, chapter.no)
		if os.path.exists(path):
			names = open(path).read().split('\n')[:-1]
			for a in range(len(names)):
				article = Article(a + 1, names[a], names[a])
				chapter.articles.append(article)
		book.chapters.append(chapter)
	Zohar.append(book)
