#!/usr/bin/env python
# -*- coding: utf-8  -*-

import hebrew_numbers
import os
import re
from enum import Enum

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(ROOT_PATH, 'db')

def remove_cantillations(text):
	return re.sub('[\u0591-\u05ae\u05bd\u05c0\u05c3]', '', text)

def remove_diacritics(text):
	return re.sub('[\u05b0-\u05bc\u05c7\u05c1\u05c2]', '', text)

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

class Span:
	def __init__(self, kind, value, alt=None):
		self.kind = kind
		self.value = value
		self.alt = alt

	def __repr__(self):
		return 'span=%s'%self.kind + '\n' + self.value + '\n'
