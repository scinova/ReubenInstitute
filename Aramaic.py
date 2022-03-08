#!/usr/bin/env python
# -*- coding: utf-8  -*-

import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))
DBFILE = os.path.join(ROOT, 'aramaic.txt')

def remove_diacritics(text):
	return re.sub('[\u05b0-\u05bc\u05c7\u05c1\u05c2]', '', text)

class Aramaic:
	def load(self):
		lines = open(DBFILE).read().split('\n')
		for line in lines:
			parts = line.split(' ')
			variants_txt = parts[1:]
			word = parts[0]
			if not len(variants_txt):
				continue
			self._dictionary[word] = ' '.join(variants_txt)
			self._words[word] = []
			variants = []
			for variant_txt in variants_txt:
				variant, r = variant_txt.split(':')
				self._spellings.append(variant)
				meanings_txt = r.split('|')
				for meaning_txt in meanings_txt:
					if '=' in meaning_txt:
						prop_txt, translation = re.split('[\=]', meaning_txt)
					else:
						prop_txt = meaning_txt
					props = prop_txt.split(',')
				self._words[word].append(variant)

	def save(self):
		s = '\n'.join([' '.join([k, v]) for k, v in self._dictionary.items()])
		open(DBFILE + 'x', 'w').write(s)
		print (s)

	def __init__(self):
		self._dictionary = {}
		self._words = {}
		self._spellings = []
		self.load()

	def spell(self, text):
		#print ('spell', text)
		word_items = list(re.finditer('([\u05d0-\u05ea\u05b0-\u05bc\u05c1\u05c2\u05bd]+)', text))
		for item in word_items:
			text = text[:item.start()] + ((item.end() - item.start()) * 'X') + text[item.end():]
		other_items = list(re.finditer('([^X]+)', text))
		s = ''
		for idx in range(len(text)):
			for item in word_items + other_items:
				if idx != item.start():
					continue
				if item in word_items:
					value = item.groups()[0]
					for spelling in self._spellings:
						#print ('spelling', spelling)
						clean_spelling = spelling.replace('[', '').replace(']', '').replace('\u05b0\u05b0', '\u05b0').replace('\u05bc\u05bc', '\u05bc')
						if value == clean_spelling:
							print ('YES', spelling, clean_spelling, len(spelling), len(clean_spelling))
							value = spelling
					s += value
				elif item in other_items:
					s += item.groups()[0]
		return s

	def sx():
		#print (words)
		for word in words:
			#if not word.groups():
			#	continue
			value = word.groups()[0]
			for spelling in self._spellings:
				#print ('spelling', spelling)
				clean_spelling = spelling.replace('[', '').replace(']', '').replace('\u05b0\u05b0', '\u05b0').replace('\u05bc\u05bc', '\u05bc')
				if value == clean_spelling:
					print ('YES', spelling, clean_spelling, len(spelling), len(clean_spelling))
					value = spelling
			text = text[0:word.start()] + value + text[word.end():]
		return text

	def remove_diacritics(self, text):
		return re.sub('[\u05b0-\u05bc\u05c7\u05c1\u05c2]', '', text)

	def search(self, text):
		#print ('search %s'%text)
		results = []
		text = remove_diacritics(text)
		for word, spellings in self._words.items():
			#print (word, len(spellings))
			match = False
			idx = 0
			chars = re.compile('(([\[\{]*)[\u05b0-\u05ea][\]\}]*)').findall(word)
			chars = [c[0] for c in chars]
			for char in chars:
				if idx >= len(text):
					match = False
					break
				isoptional = False
				islectionis = False
				if char.startswith('{') and char.endswith('}'):
					isoptional = True
					char = char[1]
				elif char.startswith('[') and char.endswith(']'):
					islectionis = True
					char = char[1]
				#print ("char: %d %d %s"%(len(char), ord(char), char))

				dstchar = text[idx]
				if char != text[idx]:
					if isoptional or islectionis:
						continue
					match = False
					break
				match = True
				idx += 1
			if match:
				print ("found", word, spellings)
				results += spellings
		return results

#aramaic = Aramaic()
#for w in ['אנפוי', 'אוכמתא', 'אכמתא', 'אדנוי', 'אודנוי', 'אודנוהי', 'אדנוהי', 'אבהתא', 'אדכר']:
#for w in ['אדכר', 'אפקת', 'אפיקת']:
#	aramaic.search(w)
#	print()
#
#print (aramaic._words)
