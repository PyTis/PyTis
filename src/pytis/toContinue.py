#!/usr/bin/env python3
"""toContinue
==========
Simply pauses the screen and awaits any keypress to exit.
"""

import os
import sys
import pytis.pytis as PyTis

__curdir__ = os.path.abspath(os.path.dirname(__file__))
__created__ = '12:38pm 05 May, 2020'
__version__ = '1.0'
__author__ = 'Josh Lee'
__copyright__ = 'PyTis, LLC.'

def run(opts,args):
	"""toContinue run doc help"""
	return PyTis.toContinue(' '.join(args))

def main():
	"""usage: toContinue"""

	parser = PyTis.MyParser()
	parser.formatter.format_description = lambda s:s
	parser.set_description(__doc__)
	parser.set_usage(main.__doc__)

	(opts, args) = parser.parse_args()

	try:
		run(opts, args)
	except KeyboardInterrupt:
		sys.exit(0)


if __name__ == '__main__':
		main()

