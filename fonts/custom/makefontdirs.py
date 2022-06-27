import os

point_names = [n for n in """dagesh
dageshhazak
hatafpatah
hatafqamats
hatafsegol
hiriq
holam
holamhaser
patah
qamats
qamatskatan
qubuts
segol
sheva
shevana
shindot
sindot
tsere""".split('\n')]

accent_names = [n for n in """atnahhafukh
etnahta
darga
dehi
ereshaccenth
gereshmuqdam
gershayimaccent
iluy
mahapakh
masoracircle
merkha
merkhakefula
meteg
munah
ole
paseq
pashta
pazer
qadma
qarneypara
rafe
revia
segolta
shalshelet
sofpasuq
telishagedola
telishaqetana
tevir
tipeha
upperdothebrew
yerahbenyomo
yetiv
zaqefgadol
zaqefqatan
zarqa
zinor""".split('\n')]

name = 'ReuvenSerif.sfdir'
for fyle in os.listdir(name):
	if fyle.split('.')[0] not in point_names + accent_names:
		print (fyle)
