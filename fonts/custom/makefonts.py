import os
import fontforge

point_glyphs = [n for n in """dagesh
hatafpatah
hatafqamats
hatafsegol
hiriq
holam
holamvav
patah
qamats
qamatsqatan
qubuts
segol
sheva
shindot
sindot
tsere""".split('\n')]
#dageshhazak
#shevana

accent_glyphs = [n for n in """etnahta
etnahtahafukh
darga
dehi
gereshac
gereshmuqdam
gershayimac
iluy
mahapakh
merkha
merkhakefula
meteg
munah
ole
paseq
pashta
pazer
qadma
qarneyparah
rafe
revia
segolta
shalshelet
sofpasuq
telishagedola
telishaqetana
tevir
tipeha
yerahbenyomo
yetiv
zaqefgadol
zaqefkatan
zarqa
zinor
masoracircle
upperdot
lowerdot""".split('\n')]

letter_glyphs = [n for n in """alef
alef.wide
ayin
ayin.wide
ayinaltonehebrew
bet
dalet
dalet.wide
finalkaf
finalmem
finalmem.wide
finalnun
finalpe
finaltsadi
gimel
he
he.wide
het
het.wide
kaf
kaf.wide
lamed
lamed.wide
mem
nun
nunhafukha
pe
qof
resh
resh.wide
samekh
shin
tav
tav.wide
tet
tsadi
vav
yod
zayin""".split('\n')]

number_glyphs = [n for n in """zero
one
two
three
four
five
six
seven
eight
nine
ten""".split('\n')]

other_names = [n for n in """ampersand
asciitilde
asterisk
bar
braceleft
braceright
bracketleft
bracketright
bullet
colon
comma
dollar
ellipsis
emdash
endash
equal
exclam
geresh
gershayim
greater
hyphen
hyphennobreak
less
maqaf
nonmarkingreturn
numbersign
overline
parenleft
parenright
percent
period
plus
question
quotedbl
quotedblleft
quotedblright
quoteleft
quoteright
quotesingle
semicolon
slash
space
underscore
uniFB23
uniFB29
""".split('\n')]


points = [
		0x05b0,
		0x05b1,
		0x05b2,
		0x05b3,
		0x05b4,
		0x05b5,
		0x05b6,
		0x05b7,
		0x05b8,
		0x05b9,
		0x05ba,
		0x05bb,
		0x05bc,
		0x05c1,
		0x05c2,
		0x05c7]
accents = [
		0x0591,
		0x0592,
		0x0593,
		0x0594,
		0x0595,
		0x0596,
		0x0597,
		0x0598,
		0x0599,
		0x059a,
		0x059b,
		0x059c,
		0x059d,
		0x059e,
		0x059f,
		0x05a0,
		0x05a1,
		0x05a2,
		0x05a3,
		0x05a4,
		0x05a5,
		0x05a6,
		0x05a7,
		0x05a8,
		0x05a9,
		0x05aa,
		0x05ab,
		0x05ac,
		0x05ad,
		0x05ae,
		0x05af,
		0x05bd,
		0x05c4,
		0x05c5]

#name = 'KeterYG-Medium'
name = 'SBLHebrew'
#name = 'Cardo'
font = fontforge.open('%s.sfdir'%name)
font.generate('%s-LPA.ttf'%name)

font = fontforge.open('%s.sfdir'%name)
for glyph in font.glyphs():
	if glyph.unicode in accents:
		font[glyph.glyphname].setLayer(fontforge.layer(), 'Fore')
font.generate('%s-LP.ttf'%name)

font = fontforge.open('%s.sfdir'%name)
for glyph in font.glyphs():
	if glyph.unicode in accents + points:
		font[glyph.glyphname].setLayer(fontforge.layer(), 'Fore')
font.generate('%s-L.ttf'%name)
