#!/usr/bin/env python3

from __future__ import print_function

import re
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
	pre = False
	for ln in f.readlines():
		lineno += 1
		msgctx = (f.name, lineno, ln.strip())

		# Skip comments (comments should generally be avoided
		# but if it avoids revert wars on the github wiki
		# then these are OK)
		if ln.strip().startswith('faq-comment: '):
			continue

		# Track whether we are in a preformatted block
		if '<pre>' in ln:
			pre = True
		if '</pre>' in ln:
			pre = False

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

		# Check for signs of github flavoured markdown. This is not
		# supported by cmark (and mostly also not by wordpress)

		# Table syntax (this is targetting the --- | ---- | ---- line)
		if re.match('^[ ]*-[ -]*[|+][ -|+]*$', ln.rstrip()) and not pre:
			err('github table syntax extensions are not supported (use <pre>?)')

for fname in sys.argv[1:]:
	with open(fname) as f:
		check(f)

if numerr > 0:
	sys.exit(1)
