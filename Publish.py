import scribus
import re
from common import Span, SpanKind

import Liturgy
import Zohar
zohar = Zohar.Zohar()
import Tanakh
tanakh = Tanakh.Tanakh()
tanakh.__postinit__()

_colors = (
		('Orange', 255, 165, 0),
		('DarkRed', 0xc0, 0, 0),
		('Silver', 0xcc, 0xcc, 0xcc),
		('DarkGreen', 0x33, 0xcc, 0x33))
serif = "SBL Hebrew Regular"
serif = "Frank Ruehl CLM Medium"
sans = "Nachlieli CLM Light"
_charstyles = [
	["Default Character Style", serif, 1, 'Black'],
	["h1", serif, 2, 'Black'],
	["h2", serif, 18./15, 'Orange'],
	["h4", serif, 22./15, 'Orange'],
	["bold", serif, 1, 'Blue'],
	["majuscule", serif, 18./15, 'Black'],
	["minuscule", serif, 12./15, 'Black'],
	["addition", serif, 12./15, 'Silver'],
	["synonym", serif, 1, 'Silver'],
	["explanation", serif, 12./15, 'Silver'],
	["correction", serif, 12./15, 'Black'],
	["info", sans, 12./15, 'DarkGreen'],
	["scripture", serif, 16./15, 'DarkRed'],
	["accent", serif, 16./15, 'DarkRed'],
	["point", serif, 16./15, 'DarkRed'],
	["link", serif, 12./15, 'Silver'],
	["verseno", serif, 10./15, 'Silver'],
#	["points", serif, 1, 'Green'],
#	["accents", serif, 1, 'Red'],
	["punctuation", serif, 1, 'Blue'],
	["nonliteral", serif, 1, 'Blue'],
	["alternative", serif, 1, 'Green'],
	["legend", serif, 1, 'Green'],
	["space", serif, 1, 'Black'],
	["plain", serif, 1, 'Black']]

class Div:
	"""div of lines of spans"""
	def __init__(self, width, name):
		self.width = width
		self.height = 1
		self.name = name
		scribus.createText(0, 0, self.width, 1, name)
		#scribus.setFillColor('Red', name)
		scribus.setTextDistances(0, 0, 1, 1, name)
		scribus.setTextDirection(scribus.DIRECTION_RTL, name)
		#scribus.setTextAlignment(scribus.ALIGN_BLOCK, name)
		scribus.setTextAlignment(scribus.ALIGN_RIGHT, name)

	def enlarge(self):
		while scribus.textOverflows(self.name):
			scribus.sizeObject(self.width, self.height + 1, self.name)
			self.height = scribus.getSize(self.name)[1]

	def render(self, spans):
		scribus.setRedraw(False)
		for span in spans:
			text = span.value
			style = span.kind.name.lower()
			print (style)
			scribus.setRedraw(False)
			length = len(text)
			pos = scribus.getTextLength(self.name)
			scribus.insertText(text, pos, self.name)
			scribus.selectText(pos, length, self.name)
			scribus.setCharacterStyle(style, self.name)
			scribus.setRedraw(True)
		self.enlarge()
		scribus.setRedraw(True)

class Print:
	def __init__(self, size=(116, 165), margins=(10, 10, 13, 8)):
		self.frame = None
		self.pageWidth, self.pageHeight = size
		self.marginLeft, self.marginRight, self.marginTop, self.marginBottom = margins
		self.contentWidth = self.pageWidth - self.marginLeft - self.marginRight
		self.contentHeight = self.pageHeight - self.marginTop - self.marginBottom
		self.pos = 0
		scribus.newDocument(size, margins, scribus.PORTRAIT, 1, scribus.UNIT_MILLIMETERS, scribus.PAGE_1, 0, 1)
		scribus.setUnit(scribus.UNIT_PT)
		for color, r, g, b in _colors:
			scribus.defineColorRGB(color, r, g, b)
		for name, font, size, fillcolor in _charstyles:
			scribus.createCharStyle(name, font, size * 10. * (0.8/0.784), fillcolor=fillcolor)
		scribus.createParagraphStyle("Default Paragraph Style", linespacingmode=1, linespacing=16, alignment=scribus.ALIGN_RIGHT)#, gapafter=7)
		scribus.setUnit(scribus.UNIT_MM)

	def adddiv(self, div):
		scribus.moveObject(self.marginLeft, self.marginTop + self.pos, div.name)
		if self.pos + div.height > self.contentHeight:
			scribus.sizeObject(self.contentWidth, self.contentHeight - self.pos, div.name)
			scribus.newPage(-1)
			d = Div(self.contentWidth, div.name + 'X')
			scribus.linkTextFrames(div.name, d.name)
			d.enlarge()
			scribus.moveObject(self.marginLeft, self.marginTop, d.name)
			self.pos = d.height
		else:
			self.pos += div.height

	def adddivs(self, rdiv, ldiv):
		scribus.moveObject(self.marginLeft, self.marginTop + self.pos, ldiv.name)
		scribus.moveObject(self.marginLeft + self.contentWidth / 2, self.marginTop + self.pos, rdiv.name)
		if self.pos + max(rdiv.height, ldiv.height) > self.contentHeight:
			scribus.sizeObject(rdiv.width, self.contentHeight - self.pos, rdiv.name)
			scribus.sizeObject(ldiv.width, self.contentHeight - self.pos, ldiv.name)
			scribus.newPage(-1)
			rd = Div(rdiv.width, rdiv.name + 'X')
			ld = Div(ldiv.width, ldiv.name + 'X')
			scribus.linkTextFrames(rdiv.name, rd.name)
			scribus.linkTextFrames(ldiv.name, ld.name)
			rd.enlarge()
			ld.enlarge()
			scribus.moveObject(self.marginLeft, self.marginTop, rd.name)
			scribus.moveObject(self.marginLeft + self.contentWidth / 2, self.marginTop, ld.name)
			self.pos = max(rd.height, ld.height)
		else:
			self.pos += max(rdiv.height, ldiv.height)

	def publish(self, name):
		#scribus.saveDocAs('-.sla')
		pdf = scribus.PDFfile()
		pdf.file = name
		pdf.save()

class LiturgyPrint(Print):
	def __init__(self):
		super().__init__()

	def render(self):
		sections = Liturgy.something(open('/root/work/reubeninstitute/db/liturgy/Slichot.txt').read(), 2)
		for section_id in range(len(sections[:4])):
			section = sections[section_id]
			for outerblock_id, outerblock in enumerate(section, start=0):
				for block_id, block in enumerate(outerblock.blocks, start=0):
					name = '%s-%s-%s'%(section_id, outerblock_id, block_id)
					div = Div(self.contentWidth, name)
					spans = []
					for line in block.lines:
						spans += line
						if line != block.lines[-1]:
							spans += [Span(SpanKind.PLAIN, '\u2028')]
					div.render(spans)
					self.adddiv(div)

class ZoharPrint(Print):
	def __init__(self):
		super().__init__()

	def render(self):
		paragraphs = zohar.books[0].chapters[0].articles[17].sections
		txparagraphs = zohar.books[0].chapters[0].articles[17].translation_sections
		for paragraph_id in range(len(paragraphs)):
			name = '%s'%paragraph_id
			#zohar
			paragraph = paragraphs[paragraph_id]
			rdiv = Div(self.contentWidth / 2, 'zohar' + name)
			spans = []
			for line in paragraph:
				spans += line
				if line != paragraph[-1]:
					spans.append(Span(SpanKind.PLAIN, '\n'))
			rdiv.render(spans)
			#translation
			ldiv = Div(self.contentWidth / 2, 'zohartx' + name)
			paragraph = txparagraphs[paragraph_id]
			spans = []
			for line in paragraph:
				spans += line
				if line != paragraph[-1]:
					spans.append(Span(SpanKind.PLAIN, '\n'))
			ldiv.render(spans)
			self.adddivs(rdiv, ldiv)

class MikraotPrint(Print):
	def __init__(self):
		super().__init__()

	def render(self):
		data = tanakh.books[0].parashot[0].paragraphs
		for section_id, section in enumerate(data[:2], start=0):
			for paragraph_id, paragraph in enumerate(section, start=0):
				name = '%s%s'%(section_id, paragraph_id)
				#mikra
				spans = []
				for verse in paragraph:
					spans += [Span(SpanKind.VERSENO, verse.hebrew_number)]
					spans += verse.mikra
				div = Div(self.contentWidth, 'mikra' + name)
				div.render(spans)
				self.adddiv(div)
				#onkelos
				spans = []
				for verse in paragraph:
					spans += [Span(SpanKind.VERSENO, verse.hebrew_number)]
					spans += verse.onkelos
				rdiv = Div(self.contentWidth / 2, 'onkelos' + name)
				rdiv.render(spans)
				spans = []
				for verse in paragraph:
					spans += [Span(SpanKind.VERSENO, verse.hebrew_number)]
					spans += verse.onkelos_trans
				ldiv = Div(self.contentWidth / 2, 'onkelostx' + name)
				ldiv.render(spans)
				self.adddivs(rdiv, ldiv)
				#jerusalmi
				spans = []
				for verse in paragraph:
					spans += [Span(SpanKind.VERSENO, verse.hebrew_number)]
					spans += verse.jerusalmi
				rdiv = Div(self.contentWidth / 2, 'jerusalmi' + name)
				rdiv.render(spans)
				spans = []
				for verse in paragraph:
					spans += [Span(SpanKind.VERSENO, verse.hebrew_number)]
					spans += verse.jerusalmi_trans
				ldiv = Div(self.contentWidth / 2, 'jerusalmitx' + name)
				ldiv.render(spans)
				self.adddivs(rdiv, ldiv)
				#rashi
				spans = []
				for verse in paragraph:
					spans += [Span(SpanKind.VERSENO, verse.hebrew_number)]
					spans += verse.rashi
				div = Div(self.contentWidth, 'rashi' + name)
				#scribus.setColumns(3, div.name)
				div.render(spans)
				self.adddiv(div)

if __name__ == '__main__':
	p = LiturgyPrint()
	#p = MikraotPrint()
	#p = ZoharPrint()
	p.render()
	#p.publish('/sdcard/Download/siddur.pdf')
