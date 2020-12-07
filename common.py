import hebrew_numbers
import os
import re

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
