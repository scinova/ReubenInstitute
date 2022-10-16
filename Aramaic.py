#!/usr/bin/env python
# -*- coding: utf-8  -*-

import hebrew_numbers
import os
import re
from enum import Enum
import sys
sys.path.append('..')
import common

DATABASE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'db', 'aramaic')

class Entry:
	def __init__(self, string):
		self._string = string
		self.translation = ''
		if '=' in string:
			self.value, params, self.translation = re.split('[\:\=]', string)
		else:
			self.value, params = string.split(':')
		self.params = params.split(',')

	@property
	def name(self):
		self.value.replace('[', '').replace(']', '').replace('\u05b0\u05b0', '\u05b0').replace('\u05bc\u05bc', '\u05bc').replace('\u05bd', '')

	@property
	def dbvalue(self):
		if 'setparams' in dir(self):
			self.setparams()
		params = ','.join(self.params)
		s = '%s:%s'%(self.value, params)
		if self.translation:
			s += '=%s'%self.translation
		return s

	@property
	def uncodedvalue(self):
		return self.value.replace('[', '').replace(']', '').replace('\u05b0\u05b0', '\u05b0').replace('\u05bc\u05bc', '\u05bc').replace('\u05bd', '')

class Variation(Entry):
	def __init__(self, string, word):
		super().__init__(string)
		self.prefix = ''
		self.word = word
		self.mperson = ''
		self.mgender = ''
		self.mkount = ''
		if type(word) == Noun:
			if len(self.params) == 3:
				self.mperson, self.mgender, self.mkount = self.params
		word.variations.append(self)

class Word(Entry):
	def __init__(self, string):
		super().__init__(string)
		self.variations = []

class Name(Word):
	def __init__(self, string):
		super().__init__(string)

class Number(Word):
	def __init__(self, string):
		super().__init__(string)
		self.gender = self.params[0]

	def setparams(self):
		self.params = [self.gender]

class Pronoun(Word):
	def __init__(self, string):
		super().__init__(string)
		self.person, self.gender, self.kount = self.params

	def setparams(self):
		self.params = [self.person, self.gender, self.kount]

class Noun(Word):
	def __init__(self, string):
		super().__init__(string)
		#print (string, self.params)
		self.root, self.gender, self.kount = self.params

	def setparams(self):
		self.params = [self.root, self.gender, self.kount]

class Verb(Word):
	def __init__(self, string):
		super().__init__(string)
		self.stem, self.root, self.tense, self.person, self.gender, self.kount = self.params

	def setparams(self):
		self.params = [self.stem, self.root, self.tense, self.person, self.gender, self.kount]

#def fixstring(string):
#	blocks = []
#	for block in string.split('\n\n'):
#		lines = []
#		for line in block.split('\n'):
#			lines.append(' '.join(line.split(' ')[1:]))
#		blocks.append('\n'.join(lines))
#	string = '\n\n'.join(blocks)
##	print ('STRING: ', string)
#	return string

class Dictionary:
	def __init__(self, name):
		self.name = name
		self.words = []
		filename = os.path.join(DATABASE_PATH, '%s.txt'%self.name)
		self.string = open(filename).read()
		#if name == 'all': s = fixstring(s)
		#self.string = s
		blocks = self.string.split('\n\n')
		for block in blocks:
			lines = block.split('\n')
			firstline = lines.pop(0)
			if self.name == 'names':
				self.type = Name
				word = Name(firstline)
				self.words.append(word)
			elif self.name == 'numbers':
				self.type = Number
				word = Number(firstline)
				self.words.append(word)
			elif self.name == 'pronouns':
				self.type = Pronoun
				word = Pronoun(firstline)
				self.words.append(word)
			elif self.name == 'nouns':
				self.type = Noun
				word = Noun(firstline)
				self.words.append(word)
			elif self.name == 'verbs':
				self.type = Verb
				word = Verb(firstline)
				self.words.append(word)
			else:
				self.type = Word
				word = Word(firstline)
				self.words.append(word)
			if not lines:
				continue
			for line in lines:
				variation = Variation(line, word)
		self.sort()

	@property
	def numwords(self):
		return len(self.words)

	@property
	def numvariations(self):
		return sum([len(w.variations) for w in self.words])

	def sort(self):
		if self.type == Name:
			self.words.sort(key=lambda word:(word.value))
		if self.type == Verb and 0:
			self.words.sort(key=lambda word:(
				word.root,
				[i.value for i in list(dict(Tense.__members__).values())].index(word.tense),
				[i.value for i in list(dict(Person.__members__).values())].index(word.person),
				[i.value for i in list(dict(Gender.__members__).values())].index(word.gender),
				[i.value for i in list(dict(Count.__members__).values())].index(word.kount)
				))
		if self.type == Noun:
			self.words.sort(key=lambda word:(
				word.root,
				[i.value for i in list(dict(Gender.__members__).values())].index(word.gender),
				[i.value for i in list(dict(Count.__members__).values())].index(word.kount)
				))
		if self.type == Pronoun:
			self.words.sort(key=lambda word:(
				[i.value for i in list(dict(Person.__members__).values())].index(word.person),
				[i.value for i in list(dict(Gender.__members__).values())].index(word.gender),
				[i.value for i in list(dict(Count.__members__).values())].index(word.kount)
				))

	def __getitem__(self, value):
		for word in self.words:
			if word.value == value:
				return word
		raise KeyError

	def __setitem__(self, name, word):
		print ("__setitem__", name, word.value)
		#print (word.root)
		for i in range(len(self.words)):
			#word = self.words[i]
			if self.words[i].value == name:
				self.words[i] = word
				#print ('I', self.words[i].root)
				return
		self.words.insert(0, word)

	def save(self):
		#print ("SAVE")
		blocks = []
		for word in self.words:
			#if 'root' in dir(word):
			#	print ("WORD", word.value, word.root)
			lines = [word.dbvalue]
			for variation in word.variations:
				lines.append(variation.dbvalue)
			block = '\n'.join(lines)
			blocks.append(block)
		data = '\n\n'.join(blocks)
		filename = os.path.join(DATABASE_PATH, '%s.txt'%self.name)
		open(filename, 'w').write(data)

class Gender(Enum):
	N = ''
	M = 'זכר'
	F = 'נקבה'

class Count(Enum):
	N = ''
	S = 'יחיד'
	P = 'רבים'

class Person(Enum):
	N = ''
	A = 'ראשון'
	B = 'שני'
	C = 'שלישי'

class Stem(Enum):
	PeAL = 'פְּעַל' # simple active - paal
	ITPeIL = 'אִתְפְּעִל' # simple passive - nifal
	PAEL = 'פַּעֵל' # intensive active - piel
	ITPAAL = 'אִתְפַּעֵל' # intensive passive - nitpaal (pual)
	AFEL = 'אַפְעֵל' # causative active - hifil
	ITTAFAL = 'אתַּפְעַל' # causative passive - hufal

class Tense(Enum):
	aPAST = 'עבר'
	bPRESENT_ACTIVE = 'הווה'
	cPRESENT_PASSIVE = 'פעול'
	dFUTURE = 'עתיד'
	eIMPERATIVE = 'ציווי'
	fSOURCE = 'מקור'


#def __getitem__(name):
#	l = [d for d in dictionaries if d.name == name]
#	if not len(l):
#		raise KeyError
#	return l[0]

@property
def allconjugations():
	o = []
	for entry in _words + _variations:
		o += conjugations(entry.value)
	return o

def spell(text):
	if len(text) < 2:
		return False, text
	if text in entries:
		return True, entries[text][0]
	return False, text

#@property
def numwords():
	return sum([len(d.words) for d in dictionaries])

#@property
def numvariations():
	return sum([sum([len(w.variations) for w in d.words]) for d in dictionaries])

def conjugations(value):
	DAGESH = '\u05bc'
	SHVA = '\u05b0'
	BGDKFT = 'בגדכפת'
	chars = re.split('([\u05d0-\u05ea][\u05c1\u05c2]*[\u05b0-\u05bc\u05c7]*[\u0591-\u05af\u05bd]*)', value)
	chars = [c for c in chars if c]
	res = [value]

	# value without dagesh
	if value[0] in BGDKFT and value[1] == DAGESH:
		res.append(value[0] + value[2:])

	# BE
	c = chars
	c[0] = c[0].replace(DAGESH, '') #remove dagesh
	if SHVA in c[0]:
		c[0] = c[0].replace(SHVA + SHVA, SHVA) #shvana to shva
		if 'I' in c[0]:
			c[0] = c[0].replace(SHVA, '') #no shva
		res.append('בִּ' + ''.join(c))
		res.append('בִ' + ''.join(c))
	else:
		res.append('בְְּ' + ''.join(c))
		res.append('בְְ' + ''.join(c))

	# DE
	c = chars
	c[0] = c[0].replace(DAGESH, '') #remove dagesh
	if SHVA in c[0]:
		c[0] = c[0].replace(SHVA + SHVA, SHVA) #shvana to shva
		if 'י' in c[0]:
			c[0] = c[0].replace(SHVA, '') #no shva
		res.append('דִּ' + ''.join(c))
		res.append('דִ' + ''.join(c))
	else:
		res.append('דְְּ' + ''.join(c))
		res.append('דְְ' + ''.join(c))

	# LE
	c = chars
	c[0] = c[0].replace(DAGESH, '') #remove dagesh
	if SHVA in c[0]:
		c[0] = c[0].replace(SHVA + SHVA, SHVA) #shvana to shva
		if 'י' in c[0]:
			c[0] = c[0].replace(SHVA, '') #no shva
		o = 'לִ' + ''.join(c)
	else:
		o = 'לְְ' + ''.join(c)
	res.append(o)

	# VE
	c = chars
	c[0] = c[0].replace(DAGESH, '') #remove dagesh
	if SHVA in c[0]:
		c[0] = c[0].replace(SHVA + SHVA, SHVA) #shvana to shva
		if 'י' in c[0]:
			c[0] = c[0].replace(SHVA, '') #no shva
			o = 'וִ'
		else:
			o = 'וּ'
	elif 'ב' in c[0] or 'מ' in c[0] or 'ם' in c[0] or 'ו' in c[0]:
		o = 'וּ'
	else:
		o = 'וְְ'
	o += ''.join(c)
	res.append(o)

	# ME
	c = chars
	groni = c[0] not in 'אהחער'
	#hasshva = SHVA in c[0]
	hasdagesh = DAGESH in c[0]
	suffix = ''
	if not groni:
		if hasdagesh:
			suffix = DAGESH
		else:
			suffix = DAGESH + DAGESH
	#if hasshva:
	#	suffix += SHVA #shvana
	prefix = 'מִ' #'מֵ'
	o = common.unicode_reorder(prefix + c[0] + suffix + ''.join(c[1:]))
	#prefix = 'וּמִ'
	#o = common.unicode_reorder(prefix + c[0] + suffix + ''.join(c[1:]))
	res.append(o)

	return res


dictionaries = []
_dictionaries = {}
_words = []
_variations = []

for name in ['names', 'numbers', 'pronouns', 'nouns', 'verbs', 'new', 'adverbs', 'all', 'hebrew']:
	d = Dictionary(name)
	dictionaries.append(d)
	_dictionaries[name] = d

entries = {}
for d in dictionaries:
	for w in d.words:
		_words.append(w)
		for c in conjugations(w.value):
			k = c.replace('[', '').replace(']', '').replace('\u05b0\u05b0', '\u05b0').replace('\u05bc\u05bc', '\u05bc').replace('\u05bd', '')
			entries[k] = (c, w)
		for v in w.variations:
			_variations.append(v)
			for c in conjugations(v.value):
				k = c.replace('[', '').replace(']', '').replace('\u05b0\u05b0', '\u05b0').replace('\u05bc\u05bc', '\u05bc').replace('\u05bd', '')
				entries[k] = (c, v)
