#!/usr/bin/env python
# -*- coding: utf-8  -*-

import hebrew_numbers
import os
import re

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(ROOT_PATH, 'db')

def remove_cantillations(text):
	return re.sub('[\u0591-\u05ae\u05bd\u05c0\u05c3]', '', text)

def remove_diacritics(text):
	return re.sub('[\u05b0-\u05bc\u05c7\u05c1\u05c2]', '', text)

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

#shaharit_ashkenaz = Prayer("ashkenaz", "shaharit")
#shaharit_sefard = Prayer("sefard", "shaharit")
#shaharit_mizrah = Prayer("mizrah", "shaharit")






class VerseKind(Enum):
	OPENED = 1
	CLOSED = 2
	BREAK = 3

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

	def __repr__(self):
		return 'span=%s'%self.kind + '\n' + self.value + '\n'

class NVerse:
	def __init__(self, chapter, number, text):
		self.chapter = chapter
		self.parasha = None
		self.number = number
		self.hebrew_number = hebrew_numbers.int_to_gematria(number)
		self.title = ''
		self.text = text
		self.onkelos_text = ''
		self.onkelos_trans_text = ''
		self.jerusalmi_text = ''
		self.jerusalmi_trans_text = ''
		self.jonathan_text = ''
		self.jonathan_trans_text = ''
		self.targum_text = ''
		self.targum_trans_text = ''
		self.rashi_text = ''

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
		if self.text.startswith(chr(12)):
			return VerseKind.BREAK
		return None

	def parse(self, text=''):
		if not text:
			return []
		text = re.sub('"([^"]+)"', r'“\1”', text)
		text = re.sub("'([^']+)'", r"‘\1’", text)
		text = re.sub('-', '–', text)
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

	@property
	def has_onkelos(self):
		return self.chapter.has_onkelos

	@property
	def onkelos(self):
		return self.parse(self.onkelos_text)

	@property
	def onkelos_trans(self):
		return self.parse(self.onkelos_trans_text)

	@property
	def has_jerusalmi(self):
		return self.chapter.has_jerusalmi

	@property
	def jerusalmi(self):
		return self.parse(self.jerusalmi_text)

	@property
	def jerusalmi_trans(self):
		return self.parse(self.jerusalmi_trans_text)

	@property
	def has_jonathan(self):
		return self.chapter.has_jonathan

	@property
	def jonathan(self):
		return self.parse(self.jonathan_text)

	@property
	def has_targum(self):
		return self.chapter.has_targum

	@property
	def targum(self):
		return self.parse(self.targum_text)

	@property
	def targum_trans(self):
		return self.parse(self.targum_trans_text)

	@property
	def mikra(self):
		text = self.text
		text = re.sub('-', '–', text)
		text = re.sub('"([^"]+)"', r'“\1”', text)
		text = re.sub("'([^']+)'", r"‘\1’", text)
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

	def save_title(self):
		filename = '%02d.%03d.txt'%(self.chapter.book.number, self.chapter.number)
		path = os.path.join(DB_PATH, 'headings', filename)
		f = open(path)
		lines = f.read().split('\n')
		lines[self.number - 1] = self.title
		data = '\n'.join(lines)
		open(path, 'w').write(data)

	def save_mikra(self):
		filename = '%02d.%03d.txt'%(self.chapter.book.number, self.chapter.number)
		path = os.path.join(DB_PATH, 'tanakh', filename)
		f = open(path)
		lines = f.read().split('\n')
		lines[self.number - 1] = self.text
		data = '\n'.join(lines)
		open(path, 'w').write(data)

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

	def save_onkelos_translation(self):
		if not self.chapter.book.has_onkelos:
			return
		filename = '%01d.%02d.txt'%(self.chapter.book.number, self.chapter.number)
		path = os.path.join(DB_PATH, 'onkelost', filename)
		f = open(path)
		lines = f.read().split('\n')
		lines[self.number - 1] = self.onkelos_trans_text
		data = '\n'.join(lines)
		open(path, 'w').write(data)

	def save_jerusalmi(self):
		if not self.chapter.book.has_jerusalmi:
			return
		filename = '%01d.%02d.txt'%(self.chapter.book.number, self.chapter.number)
		path = os.path.join(DB_PATH, 'jerusalmi', filename)
		f = open(path)
		lines = f.read().split('\n')
		lines[self.number - 1] = self.jerusalmi_text
		data = '\n'.join(lines)
		open(path, 'w').write(data)

	def save_jerusalmi_translation(self):
		if not self.chapter.book.has_jerusalmi:
			return
		filename = '%01d.%02d.txt'%(self.chapter.book.number, self.chapter.number)
		path = os.path.join(DB_PATH, 'jerusalmit', filename)
		f = open(path)
		lines = f.read().split('\n')
		lines[self.number - 1] = self.jerusalmi_trans_text
		data = '\n'.join(lines)
		open(path, 'w').write(data)

	def save_jonathan(self):
		if not self.chapter.book.has_jonathan:
			return
		filename = '%01d.%02d.txt'%(self.chapter.book.number, self.chapter.number)
		path = os.path.join(DB_PATH, 'jonathan', filename)
		f = open(path)
		lines = f.read().split('\n')
		lines[self.number - 1] = self.jonathan_text
		data = '\n'.join(lines)
		open(path, 'w').write(data)


	def save_targum(self):
		filename = '%02d.%03d.txt'%(self.chapter.book.number, self.chapter.number)
		path = os.path.join(DB_PATH, 'targum', filename)
		f = open(path)
		lines = f.read().split('\n')
		lines[self.number - 1] = self.targum_text
		data = '\n'.join(lines)
		open(path, 'w').write(data)

	def save_targum_translation(self):
		filename = '%02d.%03d.txt'%(self.chapter.book.number, self.chapter.number)
		path = os.path.join(DB_PATH, 'targumt', filename)
		f = open(path)
		lines = f.read().split('\n')
		lines[self.number - 1] = self.targum_trans_text
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
		self.verses = []
		filename = '%02d.%03d.txt'%(self.book.number, self.number)
		f = open(os.path.join(DB_PATH, 'tanakh', filename))
		for number, text in enumerate(f, start=1):
			if text.endswith('\n'):
				text = text[:-1]
			verse = NVerse(self, number, text)
			self.verses.append(verse)
		filename = '%02d.%03d.txt'%(self.book.number, self.number)
		f = open(os.path.join(DB_PATH, 'rashi', filename))
		for idx, text in enumerate(f):
			if text.endswith('\n'):
				text = text[:-1]
			self.verses[idx].rashi_text = text
		if book.has_onkelos:
			filename = '%1d.%02d.txt'%(self.book.number, self.number)
			f = open(os.path.join(DB_PATH, 'onkelos', filename))
			for idx, text in enumerate(f):
				if text.endswith('\n'):
					text = text[:-1]
				self.verses[idx].onkelos_text = text
			filename = '%1d.%02d.txt'%(self.book.number, self.number)
			f = open(os.path.join(DB_PATH, 'onkelost', filename))
			for idx, text in enumerate(f):
				if text.endswith('\n'):
					text = text[:-1]
				self.verses[idx].onkelos_trans_text = text
		if book.has_jerusalmi:
			filename = '%1d.%02d.txt'%(self.book.number, self.number)
			f = open(os.path.join(DB_PATH, 'jerusalmi', filename))
			for idx, text in enumerate(f):
				if text.endswith('\n'):
					text = text[:-1]
				self.verses[idx].jerusalmi_text = text
			filename = '%1d.%02d.txt'%(self.book.number, self.number)
			f = open(os.path.join(DB_PATH, 'jerusalmit', filename))
			for idx, text in enumerate(f):
				#print (self.book.number, self.number, idx)
				if text.endswith('\n'):
					text = text[:-1]
				self.verses[idx].jerusalmi_trans_text = text
		if book.has_jonathan:
			filename = '%1d.%02d.txt'%(book.number, self.number)
			f = open(os.path.join(DB_PATH, 'jonathan', filename))
			for idx, text in enumerate(f):
				if text.endswith('\n'):
					text = text[:-1]
				if idx < len(self.verses):
					self.verses[idx].jonathan_text = text
		if book.has_targum:
			filename = '%02d.%03d.txt'%(self.book.number, self.number)
			f = open(os.path.join(DB_PATH, 'targum', filename))
			for idx, text in enumerate(f):
				if text.endswith('\n'):
					text = text[:-1]
				self.verses[idx].targum_text = text
			filename = '%02d.%03d.txt'%(self.book.number, self.number)
			f = open(os.path.join(DB_PATH, 'targumt', filename))
			for idx, text in enumerate(f):
				if text.endswith('\n'):
					text = text[:-1]
				self.verses[idx].targum_trans_text = text
#		if (book.number == 27 and self.number in [1]) or \
#				(book.number == 1 and self.number in [1, 2, 3, 4, 5, 6]):

		if (book.number == 27 and self.number in [1]) or book.number == 1:
			filename = '%02d.%03d.txt'%(self.book.number, self.number)
			f = open(os.path.join(DB_PATH, 'headings', filename))
			for idx, text in enumerate(f):
				if text.endswith('\n'):
					text = text[:-1]
				self.verses[idx].title = text

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
		filenames = [f for f in os.listdir(os.path.join(DB_PATH, 'tanakh')) if f.startswith('%02d.'%number)]
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


tanakh = Tanakh()
tanakh.__postinit__()

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


class Prayer:
	def __init__(self, variation, kind):
		self.variation = variation
		self.kind = kind
		filename = '%s-%s.txt'%(kind, variation)
		path = os.path.join(DB_PATH, 'liturgy', filename)
		text = open(path).read()
		items = reversed(list(re.finditer('\{\{([a=/-z\-]+)\}\}', text, re.M)))
		for item in items:
			filename = '%s.txt'%item.groups()[0]
			path = os.path.join(DB_PATH, 'liturgy', filename)
			if os.path.isfile(path):
				data = open(path).read()
				text = text[0:item.start()] + data + text[item.end():]
		self.text = text
		lines = self.text.split('\n')

	def parse_tags(self, text):
		if not text:
			return [[], '']

		def search(pattern, text):
			items = list(re.finditer(pattern, text, re.M))
			for item in items:
				text = text[0:item.start()] + (item.end() - item.start()) * 'X' + text[item.end():]
			return items, text

		"""
		# SUBSTIUTES
		+subs = list(re.finditer('(?<!=\{)\{([^}]+)\}(?!=\})', text))
		subs, text = search('(?<!=\{)\{([^}]+)\}(?!=\})', text)
		for item in subs:
			parts = item.groups()[0].split(' ')
			if len(parts) not in [2, 3, 4]:
				continue
			book = None
			book_name = parts[0]
			for b in tanakh.books:
				if b.name == book_name:
					book = b
					break
			if not book:
				continue
			chapter_number = parts[1]
			chapter_idx = hebrew_numbers.gematria_to_int(chapter_number) - 1
			#print (chapter_idx, chapter_number)
			chapter = book.chapters[chapter_idx]
			if len(parts) == 3 and '-' not in parts[2]:
				verse_number = parts[2]
				verse_idx = hebrew_numbers.gematria_to_int(verse_number) - 1
				verse = chapter.verses[verse_idx]
				#spans.append(Span(SpanKind.LINK, 'xxx'))
				print ("SUB", book.number, chapter.number, verse.number)
		"""
		title_items, text = search('^==(.+)$', text)
		subtitle_items, text = search('^=(.+)$', text)
		info_items, text = search('\{\{([^}]+)\}\}', text)
		bold_items, text = search('\<([^>]+)\>', text)
		link_items, text = search('\[([^]]+)\]', text)
		plain_items, text = search('([^X]+)', text)
		items = list(title_items + subtitle_items + info_items + bold_items + link_items + plain_items)
		items.sort(key=lambda x:x.start())
		spans = []
		for item in items:
			groups = item.groups()
			value = groups[0]
			if len(groups) > 1:
				alt = groups[1]
			if value.endswith('\n'):
				value = value[:-1]
			if not value:
				break
			if item in title_items:
				spans.append(Span(SpanKind.TITLE, value))
			elif item in subtitle_items:
				spans.append(Span(SpanKind.SUBTITLE, value))
			elif item in info_items:
				spans.append(Span(SpanKind.INFO, value))
			elif item in bold_items:
				spans.append(Span(SpanKind.BOLD, value))
			elif item in link_items:
				spans.append(Span(SpanKind.LINK, value))
			elif item in plain_items:
				spans.append(Span(SpanKind.PLAIN, value))#.replace('\n', ''))\
		return spans

	@property
	def divs(self):
		divs = []
		divs_text = self.text.split('\n\n')
		for div_text in divs_text:
			paragraphs = []
			paragraphs_text = div_text.split('\n')
			for paragraph_text in paragraphs_text:
				spans = self.parse_tags(paragraph_text)
				paragraphs.append(spans)
			divs.append(paragraphs)
		return divs
	
	@property
	def spans(self):
		text = self.text
		spans = self.parse_tags(text)
		return spans

class Siddur:
	def __init__(self, variation):
		self.variation = variation
		self.prayers = []

