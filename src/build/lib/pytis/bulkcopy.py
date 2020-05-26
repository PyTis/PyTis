#!/usr/bin/env python
# ##############################################################################
# The contents of this file are subject to the PyTis Public License Version    #
# 1.0 (the "License"); you may not use this file except in compliance with     #
# the License. You may obtain a copy of the License at                         #
#                                                                              #
#     http://www.PyTis.com/License/                                            #
#                                                                              #
#     Copyright (c) 2010 Josh Lee                                              #
#                                                                              #
# Software distributed under the License is distributed on an "AS IS" basis,   #
# WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License     #
# for the specific language governing rights and limitations under the         #
# License.                                                                     #
#                                                                              #
# @auto-generated by the PyTis Copyright Tool on 12:32 11 Nov, 2011            #
############################################################################## #
"""bulkcopy
========
"""

from pprint import pprint
import optparse
import os
import shutil
import sys
import pytis as PyTis

__curdir__ = os.path.abspath(os.path.dirname(__file__))
__author__ = 'Josh Lee'
__created__ = '12:31am 11 Nov, 2011'
__copyright__ = 'PyTis'
__version__ = '1.1'

def version():
	print	__version__

def find_fix(fpath,rootdir):
	""" finds prefix or postfix for a file.
	"""
	if(os.path.isdir(fpath)):
		child = os.path.abspath(fpath)
	else:
		child = os.path.abspath(os.path.dirname(fpath))
	parent = os.path.abspath(rootdir)
	diff = child.replace(parent,'')
	fix = diff.replace(os.sep,'_')
	try:
		if fix.startswith('_'):
			fix = fix[1:]
	except IndexError, e:
		return ''
	return fix

def safe_fname(fpath,opts,i=None):
	if opts.upper:
		test_fpath = fpath.upper()
	elif opts.lower:
		test_fpath = fpath.lower()
	else:
		test_fpath = fpath

	if not os.path.exists(test_fpath):
		return test_fpath
	else:
		if not i:
			i = 1
		else:
			i=i+1
		fname = os.path.basename(fpath)
		bag = os.path.splitext(fname)
		testname = "%s_%s%s" % (bag[0],i,bag[1])

		if opts.upper:
			newfile = os.path.abspath(os.path.join(os.path.dirname(fpath),testname.upper()))
		elif opts.lower:
			newfile = os.path.abspath(os.path.join(os.path.dirname(fpath),testname.lower()))
		else:
			newfile = os.path.abspath(os.path.join(os.path.dirname(fpath),testname))

		if not os.path.exists(newfile):
			if i is not None:
				log.warn("%s already existed in the outdir, added _%s to the end of the filename." % (fname,i))
			return newfile
		else:
			return safe_fname(fpath,opts,i)

def run(files,rootdir,opts):
	global log
	for old_file in files:
		old_name = os.path.basename(old_file)
		bag = os.path.splitext(old_name)
		new_filename = bag[0]
		try:
			new_fileext = bag[1]
		except IndexError, e:
			continue

		if opts.prefix:
			new_filename = '%s_%s%s' % (find_fix(old_file,rootdir),new_filename,new_fileext)
		if opts.postfix:
			new_filename = '%s_%s%s' % (new_filename,find_fix(old_file,rootdir),new_fileext)
		if not opts.prefix and not opts.postfix:
			new_filename = '%s%s' % (new_filename,new_fileext)
		
		if opts.upper:
			new_file = os.path.abspath(os.path.join(opts.outdir,new_filename.upper()))
		elif opts.lower:
			new_file = os.path.abspath(os.path.join(opts.outdir,new_filename.lower()))
		else:
			new_file = os.path.abspath(os.path.join(opts.outdir,new_filename))

		if os.path.abspath(old_file) == new_file:
			log.error("Source and Destination are the same: cp %s %s" % (old_file,new_file))
		if not opts.dryrun:
			shutil.copy(old_file,safe_fname(new_file,opts))

def main():
	"""usage: bulkcopy [recursive] [optional prefix/postfix[file or pattern]]"""
	global log
	errors = []
	help_dict = dict(version=__version__,
						 author=__author__,
						 created=__created__,
						 copyright=__copyright__)
	parser = PyTis.MyParser()
	parser.extra_txt = """

NAME:
	bulkcopy - Is an advanced copy program with options not normally available in
	you operating system's copy command.

SYNOPSIS:
	bulkcopy [-h][-R] [options...] [-r[Path]] || [*.patern]


DESCRIPTION:
	Allows you to copy files from one location to another, while adding a prefix
	or a postfix to the file name.  Consider this, you have a folder of system
	icons with a file called disk.png (a floppy disk).  In another folder called
	audio, you have a file called disk.png (a DVD image).  If you want to copy
	all of your files into the same directory, effectively flattening the
	structure, you would end up overwriting one file with another.  You could
	increment the name, however this program allows you to have the files from
	the system folder prefixed with the word system, and audio with the word
	audio. Thus, you have system_disk.png and audio_disk.png copied into your
	destination directory.  Additionally, this program will add an increment
	counter to the end of file names when duplicate file names cannot be avoided,
	to prevent overwriting.

COMMANDS:
-v --verbose
	The verbose flag will show additional information, such as which
	files are being checked.  This is useful when you are not sure if this
	tool has read permissions of images in subdirectories.

	XXX-TODO: Finish the advanced help

ENVIRONMENT:
	Written on Linux, tested on Centos and Debian, but should run on
	DOS/Windows as well.


EXAMPLES:
	$ bukcopy -rV pg_*
	$ bukcopy -r *.gif
	$ bulkcopy -rL . -o/home/jlee/image_base/final/
	$ bukcopy -lv -o=/home/myname/newoutdir .

NOTE:
	prefixes and postfixes are based on the directories leading to the file,
	from the current path.  If your structure is:
			/images/apps/
			/images/apps/f1.png
			/images/apps/f2.png
			/images/actions/
			/images/actions/f1.png
			/images/actions/f2.png
			/images/icons/
			/images/icons/f1.png
			/images/icons/f2.png

	bulkcopy -rP will result in prefixes of images_apps_, images_actions_
	Change directory into the images directory before running this program to
	prevent this.
			/24x24/images/apps/
			/24x24/images/apps/f1.png
			/24x24/images/apps/f2.png
			/24x24/images/actions/
			/24x24/images/actions/f1.png
			/24x24/images/actions/f2.png
			/24x24/images/icons/
			/24x24/images/icons/f1.png
			/24x24/images/icons/f2.png
			/32x32/images/apps/
			/32x32/images/apps/f1.png
			/32x32/images/apps/f2.png
			/32x32/images/actions/
			/32x32/images/actions/f1.png
			/32x32/images/actions/f2.png
			/32x32/images/icons/
			/32x32/images/icons/f1.png
			/32x32/images/icons/f2.png

	This is a desired result as the structure may also be:
		bulkcopy -rP will result in prefixes of 24x24_images_apps_,
		24x24_images_actions_

		32x32_images_apps_, 32x32_images_actions_
		Then, running the findrep program the unnecessary _images_ could have been
		replaced.

SEE ALSO:
	bulkcopy, bulkmove, findrep, duplicate-images

COPYRIGHT:
	%(copyright)s

AUTHOR:
	%(author)s

HISTORY:
	Original Author

CHANGE LOG:
		 
	v1.1 MINOR CHANGES																				 September 18, 2019
		Changed typo in log file name from "duplicate-images" to "bulkcopy".

	v1.0 ORIGINAL RELEASE																				September 9, 2009
    Original Publish.

VERSION:
	%(version)s
""" % help_dict

	parser.set_description(__doc__)
	parser.set_usage(main.__doc__)
	parser.formatter.format_description = lambda s:s

	parser.add_option("-?",None,action="store_true",
						default=False,
						help="Alias for -h --help")

	parser.add_option("-D","--debug",action="store_true",
						default=False,
						help="Enable debugging")

	parser.add_option("-L","--lower",action="store_true",
						default=False,
						help="lower-case all output filenames")

	parser.add_option("-U","--upper",action="store_true",
						default=False,
						help="UPPER-CASE all output filenames")

	parser.add_option("-o","--outdir",action="store",
						default=None,
						help="Output Directory")

	parser.add_option("-v","--version",action="store_true",
						default=False,
						help="Display Version")

	parser.add_option("-V","--verbose",action="store_true",
			default=False,
			help="Be more Verbose.")

	parser.add_option("-p","--prefix",action="store_true",
						default=False,
						help="Prefix images with directories")

	parser.add_option("-P","--postfix",action="store_true",
						default=False,
						help="Postfix images with directories")

	parser.add_option("-r","--recursive",action="store_true",
			default=False,
			help="Recursively scan all subdirectories.")

	parser.add_option("-d","--dryrun",action="store_true",
						default=None,
						help="Dry Run only, do not copy files")


	(opts,args) = parser.parse_args()
	log = PyTis.set_logging(opts,'bulkcopy')

	log.debug('-'*80) 
	log.debug("Starting %s at %s" % (os.path.basename(sys.argv[0]),PyTis.prettyNow())) 

	log.debug("OPTS debug: %s" % opts.debug)
	log.debug("OPTS outdir: %s" % opts.outdir)
	log.debug("OPTS version: %s" % opts.version)
	log.debug("OPTS verbose: %s" % opts.verbose)
	log.debug("OPTS prefix: %s" % opts.prefix)
	log.debug("OPTS postfix: %s" % opts.postfix)
	log.debug("OPTS recursive: %s" % opts.recursive)
	log.debug("OPTS dryrun: %s" % opts.dryrun)

	if opts.version:
		return PyTis.version(__version__)

	rootdir = os.path.abspath(os.curdir)
	if not opts.outdir:
		last_arg = sys.argv[-1]
		if os.path.isdir(last_arg):
			opts.outdir = last_arg
			del sys.argv[len(sys.argv)-1]
		else:
			opts.outdir = rootdir
	else:
		i=0
		while i<len(sys.argv):
			if sys.argv[i].startswith('-o') or sys.argv[i].startswith('--outdir'):
				del sys.argv[i]
			i+=1
	if not opts.dryrun:
		if opts.outdir:
			if not os.path.isdir(opts.outdir) or not os.path.exists(opts.outdir):
				try:
					os.mkdir(opts.outdir)
				except OSError, SystemError:
					log.error("Output dir does not exist, and cannot be created, perhaps you do not have permission to do this. Outdir: %s" % opts.outdir)
					sys.exit(1)

	try:
		if sys.stdin.isatty():
			files = PyTis.filesFromArgs(opts,args)
		else:
			files = [x.strip() for x in sys.stdin]

		if not files:
			if len(args) == 0:
				return parser.print_usage()
			else:
				return parser.print_help("No files provided")
		else:
			return run(files,rootdir,opts)
	except PyTis.QuitNow,e:
		print "Exiting now, bye!"
	except KeyboardInterrupt,e:
		if opts.verbose:
			print "\nbye!"
		return


if __name__ == '__main__':
	main()
