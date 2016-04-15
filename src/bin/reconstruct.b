#!/usr/bin/env python
"""reconstruct
===========
Doc Here"""

import optparse
import os
import sys

backuppath = ''
tmp_dir = ''

__curdir__ = os.path.abspath(os.path.dirname(__file__))
__created__ = '04:25pm 11 Nov, 2009'
__version__ = '1.0'

def version():
    print  __version__

def main():
    """usage: reconstruct """
    parser = optparse.OptionParser(description=__doc__)
    parser.set_usage(main.__doc__)
    parser.formatter.format_description = lambda s:s

    parser.add_option("-D", "--debug", action="store_true",
                      default=False, 
                      help="Enable debugging")

    parser.add_option("-v", "--version", action="store_true",
                      default=False, 
                      help="Display Version")

    parser.add_option("-i", "--ini", action="store",
                      default=False, 
                      help="INI file to save on typing")

    parser.add_option("-d", "--database", action="store",
                      default=False, 
                      help="Database")

    parser.add_option("-p", "--pass", action="store",
                      default=False, 
                      help="Password")

    parser.add_option("-u", "--user", action="store",
                      default=False, 
                      help="User Name")

    (opts, args) = parser.parse_args()

    

    if opts.version:
        return version()

    parser.print_help()

if __name__ == '__main__':
    main()
