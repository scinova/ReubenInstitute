import scribus
import re
import common
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
		('Silver', 0x99, 0x99, 0x99),
		('DarkGreen', 0x33, 0xcc, 0x33))
#serif = "SBL Hebrew Regular"
serif = "Hadasim CLM Regular"
sans = "Nachlieli CLM Light"
sans = "Bellefair Regular"
scripture = "Keter YG Medium"
text = "ReuvenSerif Regular"
text = "Frank Ruehl CLM Medium"
_charstyles = [
	["Default Character Style", serif, 1, 'Black'],
	["h1", sans, 2, 'Silver'],
	["h2", serif, 1.4, 'Orange'],
	["h4", serif, 1.5, 'Orange'],
	["bold", serif, 1, 'Blue'],
	["majuscule", serif, 18./15, 'Black'],
	["minuscule", serif, 0.8, 'Black'],
	["addition", serif, 0.8, 'Silver'],
	["synonym", sans, 0.8, 'Silver'],
	["explanation", sans, 0.8, 'Silver'],
	["correction", serif, 1, 'Silver'],
	["info", sans, 0.8, 'DarkGreen'],
	["scripture", scripture, 1, 'DarkRed'],
	["accent", serif, 0.8, 'DarkRed'],
	["point", serif, 0.8, 'DarkRed'],
	["link", sans, 0.8, 'Silver'],
	["verseno", serif, 0.7, 'Silver'],
#	["points", serif, 1, 'Green'],
#	["accents", serif, 1, 'Red'],
	["punctuation", serif, 1, 'Blue'],
	["nonliteral", serif, 1, 'Blue'],
	["alternative", serif, 1, 'Green'],
	["legend", serif, 1, 'Green'],
	["space", serif, 1, 'Black'],
	["text", text, 1.3, 'Black'],
	["plain", serif, 1, 'Black']]

class Div:
	"""div of lines of spans"""
	def __init__(self, width, name, spans=[]):
		self.width = width
		self.height = 20
		self.name = name
		self.spans = spans

	def enlarge(self):
		scribus.setRedraw(False)
		while scribus.textOverflows(self.name):
			scribus.sizeObject(self.width, self.height + 4, self.name)
			self.height = scribus.getSize(self.name)[1]
		scribus.setRedraw(True)

	def render(self, alt=False):
		scribus.setRedraw(False)
		scribus.createText(0, 0, self.width, self.height, self.name)
		scribus.setTextDistances(0, 0, 0, 0, self.name)
		scribus.setTextDirection(scribus.DIRECTION_RTL, self.name)
		scribus.setTextAlignment(scribus.ALIGN_BLOCK, self.name)
		for span in self.spans:
			text = span.value
			style = span.kind.name.lower()
			if alt and span.kind in [SpanKind.PLAIN, SpanKind.SCRIPTURE]:
				style = "text"
			scribus.setRedraw(False)
			length = len(text)
			pos = scribus.getTextLength(self.name)
			scribus.insertText(text, pos, self.name)
			scribus.selectText(pos, length, self.name)
			scribus.setCharacterStyle(style, self.name)
			scribus.setRedraw(True)
		scribus.setTextDirection(scribus.DIRECTION_RTL, self.name)
		#self.enlarge()
		scribus.setRedraw(True)

def MM2PT(values):
	return tuple([v / 127. * 360 for v in values])

class Print:
	def __init__(self, size=(116, 165), margins=(10, 10, 13, 8)):
	#def __init__(self, size=(210, 297), margins=(9, 9, 13, 8)): #A4
		size = MM2PT(size)
		margins = MM2PT(margins)
		self.frame = None
		self.pageWidth, self.pageHeight = size
		self.marginLeft, self.marginRight, self.marginTop, self.marginBottom = margins
		self.contentWidth = self.pageWidth - self.marginLeft - self.marginRight
		self.contentHeight = self.pageHeight - self.marginTop - self.marginBottom
		self.pos = 0
		#self.create()

	def create(self):
		scribus.newDocument((self.pageWidth, self.pageHeight),
				(self.marginLeft, self.marginRight, self.marginTop, self.marginBottom),
				scribus.PORTRAIT, 1, scribus.UNIT_PT, scribus.FACINGPAGES, scribus.FIRSTPAGELEFT, 2)
		scribus.gotoPage(1)
		for color, r, g, b in _colors:
			scribus.defineColorRGB(color, r, g, b)
		for name, font, size, fillcolor in _charstyles:
			scribus.createCharStyle(name, font, 13 * size, fillcolor=fillcolor)
		scribus.createParagraphStyle("Default Paragraph Style", linespacingmode=1, linespacing=13, alignment=scribus.ALIGN_BLOCK)

	def adddiv(self, div, gap=0):
		scribus.moveObject(self.marginLeft, self.marginTop + self.pos, div.name)
		if self.pos + div.height > self.contentHeight:
			scribus.sizeObject(self.contentWidth, self.contentHeight - self.pos, div.name)
			scribus.newPage(-1)
			d = Div(self.contentWidth, div.name + 'X')
			scribus.linkTextFrames(div.name, d.name)
			d.enlarge(self.baseline)
			scribus.moveObject(self.marginLeft, self.marginTop, d.name)
			self.pos = d.height
		else:
			self.pos += div.height + gap

	def adddiv2(self, div, gap=0):
		scribus.moveObject(self.marginLeft, self.marginTop + self.pos, div.name)
		if self.pos + div.height > self.contentHeight:
			scribus.sizeObject(self.contentWidth, self.contentHeight - self.pos, div.name)
			scribus.newPage(-1)
			scribus.newPage(-1)
			scribus.gotoPage(1)
			d = Div(self.contentWidth, div.name + 'X')
			scribus.linkTextFrames(div.name, d.name)
			d.enlarge(self.baseline)
			scribus.moveObject(self.marginLeft, self.marginTop, d.name)
			self.pos = d.height + gap
		else:
			self.pos += div.height + gap

#	def xadddivs(self, rdiv, ldiv, gap=0):
#		scribus.moveObject(self.marginLeft, self.marginTop + self.pos, ldiv.name)
#		scribus.moveObject(self.marginLeft + self.contentWidth / 2, self.marginTop + self.pos, rdiv.name)
#		if self.pos + max(rdiv.height, ldiv.height) > self.contentHeight:
#			scribus.sizeObject(rdiv.width, self.contentHeight - self.pos, rdiv.name)
#			scribus.sizeObject(ldiv.width, self.contentHeight - self.pos, ldiv.name)
#			scribus.newPage(-1)
#			rd = Div(rdiv.width, rdiv.name + 'X')
#			ld = Div(ldiv.width, ldiv.name + 'X')
#			scribus.linkTextFrames(rdiv.name, rd.name)
#			scribus.linkTextFrames(ldiv.name, ld.name)
#			rd.enlarge(self.baseline)
#			ld.enlarge(self.baseline)
#			scribus.moveObject(self.marginLeft, self.marginTop, ld.name)
#			scribus.moveObject(self.marginLeft + self.contentWidth / 2, self.marginTop, rd.name)
#			self.pos = max(rd.height, ld.height)
#		else:
#			self.pos += max(rdiv.height, ldiv.height) + gap

	def adddivs(self, rdiv, ldiv, gap=0):
		scribus.gotoPage(1)
		#ldiv.render()
		ldiv.enlarge()
		#rdiv.render(alt=True)
		rdiv.enlarge()
		lastpage = scribus.pageCount()
		if self.pos + 30 > self.contentHeight:
			scribus.newPage(-1)
			scribus.newPage(-1)
			self.pos = 0
		lastpage = scribus.pageCount()
		scribus.gotoPage(1)
		scribus.copyObject(ldiv.name)
		scribus.deleteObject(ldiv.name)
		scribus.gotoPage(lastpage)
		scribus.pasteObject()
		scribus.moveObject(self.marginLeft, self.marginTop + self.pos, ldiv.name)
		scribus.gotoPage(1)
		scribus.copyObject(rdiv.name)
		scribus.deleteObject(rdiv.name)
		scribus.gotoPage(lastpage - 1)
		scribus.pasteObject()
		scribus.moveObject(self.marginLeft, self.marginTop + self.pos, rdiv.name)

		if self.pos + max(rdiv.height, ldiv.height) > self.contentHeight:
			scribus.sizeObject(rdiv.width, self.contentHeight - self.pos, rdiv.name)
			scribus.sizeObject(ldiv.width, self.contentHeight - self.pos, ldiv.name)
			scribus.newPage(-1)
			scribus.newPage(-1)

			lastpage = scribus.pageCount()
			scribus.gotoPage(lastpage - 1)
			rd = Div(rdiv.width, rdiv.name + 'X')
			rd.render()
			scribus.moveObject(self.marginLeft, self.marginTop, rd.name)
			scribus.gotoPage(lastpage)
			ld = Div(ldiv.width, ldiv.name + 'X')
			ld.render()
			scribus.moveObject(self.marginLeft, self.marginTop, ld.name)
			scribus.linkTextFrames(rdiv.name, rd.name)
			scribus.linkTextFrames(ldiv.name, ld.name)
			rd.enlarge()
			ld.enlarge()
			#scribus.gotoPage(scribus.pageCount() - 1)
			self.pos = max(rd.height, ld.height) + gap
		else:
			self.pos += max(rdiv.height, ldiv.height) + gap
		#scribus.gotoPage(scribus.pageCount())

	def publish(self, name):
		scribus.saveDocAs('/root/%s.sla'%name)
		pdf = scribus.PDFfile()
		pdf.file = '/root/%s.pdf'%name
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
		self.articles = [
			[0, 0, 10],
			[0, 0, 15],
			[0, 0, 18]#,
			#[0, 0, 20]#,
			#[2, 26, 1],
			#[2, 26, 7]#,
			]
		c = [
			[0, 0, 1],
			[0, 0, 2],
			[0, 0, 3],
			[0, 0, 4],
			[0, 0, 5],
			[0, 0, 6],
			[0, 0, 7],
			[0, 0, 8],
			[0, 0, 9],
			#[0, 0, 10],
			[0, 0, 11],
			[0, 0, 12],
			[0, 0, 13],
			[0, 0, 14],
			#[0, 0, 15],
			[0, 0, 16],
			[0, 0, 17],
			#[0, 0, 18],
			[0, 0, 19],
			[0, 0, 20],
			[0, 0, 21],
			[0, 0, 22],
			[0, 0, 23],
			[0, 0, 24],
			[0, 0, 25],
			[0, 0, 26],
			[0, 0, 27],
			[0, 0, 28],
			[0, 0, 29],
			[0, 0, 30],
			[0, 0, 31],
			[0, 0, 33],
			[0, 0, 34],
			[2, 26, 1],
			[2, 26, 7],
			[2, 27, 1]
			]
		super().__init__()

	def render(self):
		for b, c, a in self.articles:
			article = zohar.books[b].chapters[c].articles[a - 1]
			paragraphs = article.sections
			txparagraphs = article.translation_sections

			for paragraph_id in range(len(paragraphs)):
				paragraph = paragraphs[paragraph_id]
				txparagraph = txparagraphs[paragraph_id]
				for line_id in range(len(paragraph)):
					prefix = '%d-%d-%d-%d-%d'%(article.book.number, article.chapter.number, article.number, paragraph_id, line_id)
					#zohar
					spans = paragraph[line_id]
					spans = self.format_spans(spans)
					rdiv = Div(self.contentWidth / 1, 'zohar' + prefix, spans)
					rdiv.render(alt=True)
					#translation
					spans = txparagraph[line_id]
					spans = self.format_spans(spans, tx=True)
					ldiv = Div(self.contentWidth / 1, 'zohartx' + prefix, spans)
					ldiv.render()
			#self.r2(article)

	def move(self):
		for b, c, a in self.articles:
			article = zohar.books[b].chapters[c].articles[a - 1]
			paragraphs = article.sections
			txparagraphs = article.translation_sections
			for paragraph_id in range(len(paragraphs)):
				paragraph = paragraphs[paragraph_id]
				txparagraph = txparagraphs[paragraph_id]
				for line_id in range(len(paragraph)):
					prefix = '%d-%d-%d-%d-%d'%(article.book.number, article.chapter.number, article.number, paragraph_id, line_id)
					spans = paragraph[line_id]
					spans = self.format_spans(spans)
					rdiv = Div(self.contentWidth / 1, 'zohar' + prefix, spans)
					spans = txparagraph[line_id]
					spans = self.format_spans(spans, tx=True)
					ldiv = Div(self.contentWidth / 1, 'zohartx' + prefix, spans)
					gap = 0
					if line_id == len(paragraph) - 1:
						gap = 16
					self.adddivs(rdiv, ldiv, gap=gap)

	def format_spans(self, spans, tx=False):
		for i in range(len(spans)):
			span = spans[i]
			value = span.value
			value = common.unicode_reorder(value)
			value = common.fix_yhwh(value)
			value = common.remove_accents(value)
			value = common.remove_meteg(value)
			if tx:
				if span.kind != SpanKind.SCRIPTURE:
					value = common.remove_points(value)
			if span.kind == SpanKind.SCRIPTURE:
				value = '“%s”'%value
			if span.kind == SpanKind.SYNONYM:
				value = '(=%s)'%value
			if span.kind == SpanKind.EXPLANATION:
				value = '(%s)'%value
			if span.kind == SpanKind.CORRECTION:
				value = '[%s]'%value
			if span.kind == SpanKind.LINK:
				value = '(%s)'%value
				#a, b, c = value.split(' ')
				#value = '%s,%s,%s'%(a, b, c)
			spans[i].value = value
		return spans

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
				spans = self.format_spans(spans)
				rdiv = Div(self.contentWidth / 2, 'onkelos' + name)
				rdiv.render(spans)
				spans = []
				for verse in paragraph:
					spans += [Span(SpanKind.VERSENO, verse.hebrew_number)]
					spans += verse.onkelos_trans
				spans = self.format_spans(spans)
				ldiv = Div(self.contentWidth / 2, 'onkelostx' + name)
				ldiv.render(spans)
				self.adddivs(rdiv, ldiv)
				#jerusalmi
				spans = []
				for verse in paragraph:
					spans += [Span(SpanKind.VERSENO, verse.hebrew_number)]
					spans += verse.jerusalmi
				spans = self.format_spans(spans)
				rdiv = Div(self.contentWidth / 2, 'jerusalmi' + name)
				rdiv.render(spans)
				spans = []
				for verse in paragraph:
					spans += [Span(SpanKind.VERSENO, verse.hebrew_number)]
					spans += verse.jerusalmi_trans
				spans = self.format_spans(spans)
				ldiv = Div(self.contentWidth / 2, 'jerusalmitx' + name)
				ldiv.render(spans)
				self.adddivs(rdiv, ldiv)
				#rashi
				spans = []
				for verse in paragraph:
					spans += [Span(SpanKind.VERSENO, verse.hebrew_number)]
					spans += verse.rashi
				spans = self.format_spans(spans)
				div = Div(self.contentWidth, 'rashi' + name)
				#scribus.setColumns(3, div.name)
				div.render(spans)
				self.adddiv(div)

	def xformat_spans(self, spans):
		for i in range(len(spans)):
			span = spans[i]
			value = span.value
			if span.kind == SpanKind.SCRIPTURE:
				value = '“%s”'%span.value
			if span.kind == SpanKind.SYNONYM:
				value = '(=%s)'%span.value
			if span.kind == SpanKind.EXPLANATION:
				value = '(~%s)'%span.value
			if span.kind == SpanKind.CORRECTION:
				value = '[%s]'%span.value
			if span.kind == SpanKind.LINK:
				value = '(%s)'%span.value
			spans[i].value = value
		return spans

if __name__ == '__main__':
	#p = LiturgyPrint()
	#p = MikraotPrint()

	p = ZoharPrint()
	p.create()
	p.render()
	p.publish('zohar')
	scribus.closeDoc()

	filename = '/root/zohar.sla'
	data = open(filename).read()
	data = re.sub('FLOP="0"', 'FLOP="1"', data)
	open(filename, 'w').write(data)
	scribus.openDoc(filename)

	p.move()
