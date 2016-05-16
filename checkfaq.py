#!/usr/bin/env python3

from __future__ import print_function

import sys

msgctx = None
numerr = 0
numwarn = 0

def _msg(klass, msg):
	print('{}:{}:1: {}: {}: {}'.format(msgctx[0], msgctx[1], klass, msg, msgctx[2]), file=sys.stderr)

def err(msg):
	global numerr
	_msg('error', msg)
	numerr += 1

def warn(msg):
	global numwarn
	_msg('warning', msg)
	numwarn += 1

def check(f):
	global msgctx

	lineno = 0
	draft = False
	for ln in f.readlines():
		lineno += 1
		msgctx = (f.name, lineno, ln.strip())

		# Warn for every draft question (but disable all other checks)
		if '**' in ln and 'Q:' in ln and '?' in ln:
			draft = 'DRAFT' in ln
			if draft:
				warn('Draft question')
		if draft:
			continue
	
		# Check for proper formatting of questions
		if 'Q:' in ln and '?' in ln and \
				(not ln.strip().startswith('**') or \
				 not ln.strip().endswith('**')):
			err('Missing **')

		# Check there are no notes for pending changes
		if 'TODO' in ln:
			err('Still TODO (missing DRAFT?)')
		if 'TBD' in ln:
			err('Still TDB (missing DRAFT?)')

		# Check for real name tags
		names = ('akira', 'daniel', 'danielt', 'vchong', 'jorge')
		for name in names:
			if name + ':' in ln:
				err('Private note')
				break

for fname in sys.argv[1:]:
	with open(fname) as f:
		check(f)

if numerr > 0:
	sys.exit(1)
