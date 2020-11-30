import hebrew_numbers
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
	['Zechariah', 14,  'זכאיה'],
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
	['זהר על התורה - בראשית', [
		[1, a, 1, 14, b, 7, 'הקדמה'],
		[15, a, 1, 59, a, 7, 'בראשית'],
		[59, b, 1, 76, b, 4, 'נח'],
		]],
	['זהר על התורה - שמות', [
		]],
	['זהר על התורה - ויקרא, במדבר, דברים', [
		#[287, b, 15, 299, b, 13, 'אדרא זוטא']
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
		book.chapters.append(chapter)
	Zohar.append(book)