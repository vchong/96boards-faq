#!/usr/bin/env python3

import sys

for fname in sys.argv[1:]:
	with open(fname) as f:
		draft = False
		g = None

		for ln in f.readlines():
			# Skip comments (comments should generally be avoided
			# but if it avoids revert wars on the github wiki
			# then these are OK)
			if ln.strip().startswith('faq-comment: '):
				continue

			# Open a new topic file for first level headings
			if ln.strip().startswith('# '):
				if g:
					g.close()
				gname = ln[1:].strip().replace(' ', '-')+'.md'
				g = open(gname, 'w')
				continue

			# Identify and (arrange to) skip DRAFT questions
			if '**' in ln and 'Q:' in ln and '?' in ln:
				draft = 'DRAFT' in ln

                        if g and not draft:
				g.write(ln)

		if g:
			g.close()
