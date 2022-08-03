#!/bin/python3
"""passthru
============
"""

import os
import optparse
import sys
import subprocess

#
# Internal
#
try:
  #import pytis as PyTis # Shared GPL/PPL License
  from pytis import pytis as PyTis # Shared GPL/PPL License
except ImportError as e:
  # We cannot go any further than this, we can't use the Parser or Logging tool
  # to display these errors because those very tools are loaded from PyTis.
  # Therefore, display errors now and exit with an errored exit code.
  print("This program requires the PyTis Python library to run.")
  print("You may download the PyTis library, or do an SVN checkout from:")
  print("<https://sourceforge.net/projects/pytis/>")
  print("This program should be installed in the bin directory of the PyTis library.")
  print(str(e))
  sys.exit(1)

__curdir__ = os.path.abspath(os.path.dirname(__file__))
__author__ = 'Josh Lee'
__created__ = '06:50pm 12 Dec, 2015'
__copyright__ = 'PyTis'
__version__ = '1.1'


class SingleThread(PyTis.MyThread):

	def buildNice(self):
		return ['nice', '-n%s' % self.default_niceness]

	def buildIoNice(self):
		return ['ionice', '-c%s' % self.default_ioniceness_class, '-n%s' % self.default_ioniceness]
		
	def relogOpts(self):
		""" After all config file loading, option parsing and data crunching	has 
				been completed, ths function will re-log to debug all options gathered,
				so we	can see what their values are.
		"""

		self.opts.ip_addresses=PyTis.unique(self.opts.ip_addresses)

		# I want the output alphabatized, so I am going to create a list of tuples,
		# sort them, no wait, you know what would be faster? to just grab the keys,
		# sort those, request each value by key.
		self.log.debug('-'*80) 
		opt_keys = list(self.opts.__dict__.keys())
		opt_keys.sort()
		for opt in opt_keys:
			value = self.opts.__dict__[opt]
		#for opt, value in self.opts.__dict__.items():
			if type(value) == type(str('')):
				if value.strip() == '_empty_val_trick_':
					value = ''

			if str(opt) == 'db_password':
				if self.opts.db_password:
					value = '*'*96 
				else:
					value = 'N/A'
				
			self.log.debug("OPTION %s: %s" % (opt,value))

		self.log.debug("%s IP Addresses Collected." % len(self.opts.ip_addresses))
		self.log.debug('-'*80) 


	def run(self):
		"""
			Extra help goes here...
		"""
		# Call function to generate the NMAP targets list
		argv=[]
		[argv.extend(arg.split()) for arg in sys.argv]
		
		#cmd_list = self.buildIoNice()
		#cmd_list.extend(self.buildNice())
		cmd_list=[]
		cmd_list.extend(argv)

		#print(repr(cmd_list))
		#print(repr(cmd_list))
		self.log.info(repr(cmd_list))
		subprocess.call(cmd_list)


# =============================================================================
# End MAIN PROGRAM FUNCTION
# -----------------------------------------------------------------------------

# =============================================================================
# Begin MAIN 
# -----------------------------------------------------------------------------


def main():
	"""usage: passthru"""

	global log
	parser = PyTis.MyParser()
	parser.formatter.format_description = lambda s:s
	# ----------------------------
	dbgroup = optparse.OptionGroup(parser, "-- DEBUG", ' ')

	dbgroup.add_option("-D", "--debug", action="store_true", default=False, 
		dest='debug', 
		help=optparse.SUPPRESS_HELP)

	dbgroup.add_option("-V", "--verbose", action="store_true", default=False,
		dest='verbose', 
		help=optparse.SUPPRESS_HELP)

	dbgroup.add_option("", "--totaly-verbose", action="store_true",
		default=False, dest='totally_verbose', 
		help=optparse.SUPPRESS_HELP)

	dbgroup.add_option("-v", "--version", action="store_true", default=False,
		dest='version', 
		help="Display Version`$")

	parser.add_option_group(dbgroup)
	# ----------------------------
	# OptParser OPTIONS ABOVE
	parser._error = parser.error
	parser.error = lambda x:x

	help_dict = dict(version=__version__,
						 author=__author__,
						 created=__created__,
						 copyright=__copyright__)

	if '--help' in sys.argv:
		extra = """
CODE:
	Flag vs. Argument:
		Flag - an option that accepts no input.
		Argument - an option that requires input.

SEE ALSO:

	web-passthru
	test-exit-code
	return-exit-code
	test_onetime_daemon

COPYRIGHT:

	%(copyright)s

AUTHOR:

	%(author)s

HISTORY:

	Original Author

CHANGE LOG:
	
	v1.1 MINOR CHANGE																							 March 22, 2019
		Added updated changelog and removed the prefix "web-" from "web-passthru" 
		now it is just "passthru."
		 
	v1.0 ORIGINAL RELEASE																				December 12, 2015
    Original Publish.

EXAMPLES:	

	passthru [--arguments] {your command [--arguments] --and-flags}


BUGS - KNOWN ISSUES:

	NONE (at tis time).

CREATED:

	%(created)s

VERSION:

	%(version)s

"""  % help_dict

		parser.set_description(__doc__ + extra)
		parser.print_help()
		print("\n\n")
		parser.print_usage()
		return 0
	elif '-h' in sys.argv:
		parser.print_usage()
		return 0

	(opts, args) = parser.parse_args()
	parser.error = parser._error

	old_version = opts.version
	opts.version = True
	log = PyTis.set_logging(opts, os.path.basename(sys.argv[0]))
	opts.version = old_version

	if opts.version:
		return PyTis.version(__version__)


	del sys.argv[0]
	if not len(args):
		print("USAGE: passthru.py your command -arguments --and-flags")
		return 0
	else:
		log.info("passthru started at %s" % PyTis.prettyNow())

		argv=[]
		[argv.extend(arg.split()) for arg in sys.argv]
		
		cmd_list=[]
		cmd_list.extend(argv)

		log.info(repr(cmd_list))
		subprocess.call(cmd_list)

		'''
		y	= SingleThread()
		y.run()
		'''
		return 0 #os.system(' '.join(sys.argv))

if __name__ == '__main__':
	sys.exit(main())

