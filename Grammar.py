#!/usr/bin/env python
# -*- coding: utf-8  -*-

import hebrew_numbers
import os
import re
from enum import Enum

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(ROOT_PATH, 'db')


class Person(Enum):
	A = 1
	B = 2
	C = 3

class Gender(Enum):
	M = 'm'
	F = 'f'
	MF = 'm/f'

class Count(Enum):
	S = 's'
	P = 'p'
	SP = 's/p'

class Tense(Enum):
	P = 'past'
	N = 'now'
	F = 'future'
	I = 'imperative'

class Stem(Enum):
	PAAL = 'paal' # simple active
	NIFAL = 'nifal' # simple passive
	PIEL = 'piel' # intensive active
	PUAL = 'pual' # intensive active
	HIFIL = 'hifil' # causative active
	HUFAL = 'hufal' # causative passive
	HITPAEL = 'hitpael' # reflexive

class Noun:
	def __init__(self, gender, kount):
		self.gender = gender
		self.count = kount

noun = Noun(Gender.M, Count.S)

class Verb:
	def __init__(self, stem, root, person, gender, kount, tense):
		self.stem = stem
		self.root = root
		self.person = person
		self.gender = gender
		self.count = kount
		self.tense = tense

verb = Verb(Stem.PAAL, 'אכל', Person.A, Gender.M, Count.S, Tense.I)

class Word:
	def __init__(self, string):
		self._string = string

class Particle:
	def __init__(self):
		pass
"""