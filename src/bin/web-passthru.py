#!/usr/bin/env python
"""web-passthru
============
"""

import os
import sys

__curdir__ = os.path.abspath(os.path.dirname(__file__))
__author__ = 'Josh Lee'
__created__ = '06:50pm 12 Dec, 2015'
__copyright__ = 'PyTis'
__version__ = '1.0'



def main():
	"""usage: web-passthru"""

	del sys.argv[0]
	if not len(sys.argv):
		print("USAGE: web-passthru.py your command -arguments --and-flags")
		return 0
	else:
		return os.system(' '.join(sys.argv))

if __name__ == '__main__':
		sys.exit(main())

