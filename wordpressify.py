#!/usr/bin/env python3

from __future__ import print_function

import sys

for fname in sys.argv[1:]:
	with open(fname) as f:
		for ln in f.readlines():
			ln = ln.rstrip()

			ln = ln.replace('</p>', '')
			ln = ln.replace('<p>', '\n')
			ln = ln.replace('<h2>', '<strong><em>')
			ln = ln.replace('</h2>', '</em></strong>')
			ln = ln.replace('<h3>', '<strong>')
			ln = ln.replace('</h3>', '</strong>')

			print(ln)
