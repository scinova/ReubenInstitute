#!/usr/bin/env python
# -*- coding: utf-8  -*-

import scribus

if not scribus.haveDoc():
	scribus.messageBox('Error',"No opened document.", scribus.ICON_WARNING, scribus.BUTTON_OK)
	sys.exit(2)

numpages = scribus.pageCount()
for page in range(1, numpages + 1):
	scribus.gotoPage(page)
	xdimension, ydimension = scribus.getPageSize()
	top, left, right, bottom = scribus.getPageMargins()
	items = scribus.getPageItems()
	for frame, kind, ssind in items:
		if kind != 4:
			continue
		scribus.sizeObject((xdimension - left - right), (ydimension - top - bottom), frame)
		scribus.moveObjectAbs(left, top, frame)
#scribus.setRedraw(True)
scribus.docChanged(True)

scribus.redrawAll()

