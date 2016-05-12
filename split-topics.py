#!/usr/bin/env python3

import sys

for fname in sys.argv[1:]:
	with open(fname) as f:
		g = open('front-matter.md', 'w')

		for ln in f.readlines():
			if ln.strip().startswith('# '):
				g.close()
				gname = ln[1:].strip().replace(' ', '-')+'.md'
				g = open(gname, 'w')
				continue

			g.write(ln)

		g.close()
