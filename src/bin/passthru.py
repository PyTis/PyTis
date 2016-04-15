#!/usr/bin/env python
"""passthru
========
"""

import optparse
import os
import sys
import pytis as PyTis
import subprocess

__curdir__ = os.path.abspath(os.path.dirname(__file__))
__created__ = '07:54pm 03 Mar, 2016'
__version__ = '1.0'

def run(opts,args):
	"""passthru run doc help"""
	pass

def main():
	"""usage: passthru"""
	

	filename = os.path.abspath(os.path.join(PyTis.__configdir__, '%s.ini' % os.path.basename(os.path.abspath(sys.argv[0]))))
	main.__doc__ = "%s\n\n	CONFIG FILE: %s" % (main.__doc__,os.path.abspath(filename))


	errors=[]
	PyTis.__option_always__ = [True]
	help_dict = dict(version=__version__,
						 author=__author__,
						 created=__created__,
						 copyright=__copyright__)
	parser = PyTis.MyParser()

	parser.extra_txt = "\n\n%s\n" % run.__doc__ + """

examples:	
	xxx

SEE ALSO:
	xxx

COPYRIGHT:
	%(copyright)s

AUTHOR:
	%(author)s

HISTORY:
	Original Author

VERSION:
	%(version)s
""" % help_dict

	parser.formatter.format_description = lambda s:s
	parser.set_description(__doc__)
	parser.set_usage(main.__doc__)

	runtime = optparse.OptionGroup(parser, "-- RUNTIME ARGUMENTS")
	parser.add_option_group(runtime)
	# -------------------------------------------------------------------------
	# variable setting
	vars = optparse.OptionGroup(parser, "-- CONFIGURATION SETTINGS")
	parser.add_option_group(vars)
	# ----------------------------
	dbgroup = optparse.OptionGroup(parser, "-- DEBUG")
	dbgroup.add_option("-D", "--debug", action="store_true",
					 default=False, dest='debug',
					 help="Enable debugging")
	helpishere=False
	for a in sys.argv:
		if a == '--help':
			helpishere=True
			dbgroup.add_option("-V", "--verbose", action="store_true",
							 default=True, dest='verbose',
							 help="Be more Verbose (make lots of noise)")
	if not helpishere:
		dbgroup.add_option("-V", "--verbose", action="store_true",
						 default=True, dest='verbose',
						 help=optparse.SUPPRESS_HELP)

	

	dbgroup.add_option("-q", "--quiet", action="store_true",
					 default=False, dest='quiet',
					 help="be vewwy quiet (I'm hunting wabbits)")

	dbgroup.add_option("-v", "--version", action="store_true",
					 default=False, dest='version',
					 help="Display Version")

	parser.add_option_group(dbgroup)
	# ----------------------------

	(opts, args) = parser.parse_args()
	if opts.quiet: opts.verbose = False

	#if opts.action is None and len(args) and args[0] in ('start','stop','restart','status'):
	#	opts.action = args[0]
	#	del args[0]

	old_version = opts.version
	opts.version = True
	log = PyTis.set_logging(opts, os.path.basename(sys.argv[0]))
	
	opts.version = old_version

	if opts.version:
		return PyTis.version(__version__)

	#if opts.action and len(args) == 1 and args[0] in 'start stop restart status'.split() and opts.action != args[0]:
	#	errors.append("Silly human, you provided an action via a flag (%s) and an option on STDIN (%s) and they are different.	Please only provide one action." % (opts.action, args[0]))

	#if len(args) == 1 and args[0] in 'start stop restart status'.split() and opts.action is None:
	#	opts.action = args[0]
	#	del args[0]

	if len(args) == 0 and not errors:
		return parser.print_usage()
	elif not errors:
		try:
			run(opts, args)
		except KeyboardInterrupt,e:
			log.debug("Keyboard-Interrupt, bye!")
			if not opts.quiet:
				log.info("\nbye!")
			return
		else:
			log.info("Done.")
			return
	else:
		parser.print_usage()
		if errors:
			log.error(str("\n".join(errors)))
		return parser.print_help(errors)

	parser.print_help("ERROR: Unknown, but invalid input.")
	sys.exit(0)

if __name__ == '__main__':
		main()

