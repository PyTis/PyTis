#!/usr/bin/python3
# encoding=utf-8
# ##############################################################################
# The contents of this file are subject to the PyTis Public License Version    #
# 2.0 (the "License"); you may not use this file except in compliance with     #
# the License. You may obtain a copy of the License at                         #
#                                                                              #
#     http://www.PyTis.com/License/                                            #
#                                                                              #
#     Copyright (c) 2018 Josh Lee                                              #
#                                                                              #
# Software distributed under the License is distributed on an "AS IS" basis,   #
# WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License     #
# for the specific language governing rights and limitations under the         #
# License.                                                                     #
#                                                                              #
# @auto-generated by the PyTis Copyright Tool on 02:59 10 Oct, 2018            #
############################################################################## #
"""getip
=====

This new program obtains the WAN ip of a server.  There is no pretty way
of doing this, so I created one.  This program is bountiful in features.
One of my favorites is that any user can open it, and as long as they
follow the general methodology of previous functions, they can create
their own IP Address obtaining function.  All they have to do is add a
decorator above it, called "collector."  Adding this decorator
automatcally will turn this function into one of the options.  You can
run getip --list to see a list of all possible functions, and when
returned, they are printed out in a numbered column.  You can then run
getip [<optional number, or name>] and it will run only for that
function.  Examples:

root@neptune (/root/)--(02:48 AM Mon Oct 15)--> getip --list
 1. hostip
 2. ipecho
 3. ipinfo
 4. opendns


root@neptune (/root/)--(02:48 AM Mon Oct 15)--> getip 1

root@neptune (/root/)--(02:48 AM Mon Oct 15)--> getip ipecho
109.48.118.58

OR, you can ask all of them to run, to test each and every function,
using "getip --all" Using the --debug and/or --verbose will help you
determin which functions are working, and which aren't.

You can also override the default timeout (one second, please use getip
--help to see the full manual).

Second to last, you can simply run "getip" all by itself.  Doing so, it
will run through each and every function it has collected, and attempt
to return the WAN IP as quickly as possible (with no other errors, or
output to the screen, simply because it was designed like this ((for the
abiltiy to later be used to pipe to other programs)), if you wish to see
additonal output, you will need to use the --verbose command.

Lastly, I wrote this program, so that it itself (getip.py) can be
imported by other programs.  This way you can call "run_funcs," or, if
you wish, run a specific one.
This tool will automatically edit files and add your copyright loaded from a 
template.  The use of this "template" can be over-ridden using the -t flag.

"""
import curses
import json
import optparse
import pydoc
import shlex
import socket
from subprocess import Popen, PIPE
import sys
from threading import Timer
python_version = float("%s.%s"%(sys.version_info.major,sys.version_info.minor))
if python_version >= 3.0:
  from urllib.request import urlopen
  from urllib.error import URLError
  from io import StringIO
else:
  from urllib2 import urlopen, URLError
  from cStringIO import StringIO


import logging; log=logging.getLogger('getip')

default_timeout = 1.5
__author__ = 'Josh Lee'
__created__ = '06:14pm 01 October 2018'
__copyright__ = 'PyTis.com'
__version__ = 2.1


class MParser(optparse.OptionParser):

  extra_txt = None

  def print_out(self, txt):
    try:
      #txt = txt.replace("`$","\n")
      txt = txt.replace("`$","\n                     ")
      #txt = txt.replace(":\n",":\n\n")
      win=curses.initscr()
      max_x, max_y = win.getmaxyx()
      curses.endwin()
      if len(txt.split("\n")) > max_x:
        pager = pydoc.getpager()
        try:
          pager(txt)
        except (EOFError, KeyboardInterrupt) as e:
          pass
      else:
        sys.stdout.write("%s\n" % txt)
    except:
      pager = pydoc.getpager()
      try:
        pager(txt)
      except (EOFError, KeyboardInterrupt) as e:
        pass
      sys.stdout.write("%s\n" % txt)


  def print_help(self, errors=None):
    """
    NAME
    SYNOPSIS
    DESCRIPTION
    OPTIONS
    COMMANDS
    ENVIRONMENT
    SEE ALSO
    AUTHOR
    HISTORY
    VERSION
    """
    buf = StringIO()
    sys.stdout = buf

    # The user did not enter --help, they only entered -h, show short help and
    # instructions on howto view full help.
    if '--help' not in sys.argv and self.extra_txt is not None:
      # print the short usage.
      self.set_usage("%s\n%s" % (self.get_usage(), "*** USE '--help' for the full help page. ***"))

    # If NOT (--help was typed in, and there is extra_text to show, and
    # full_help_available)
    if not ('--help' in sys.argv and self.extra_txt is not None and 
      self.full_help_available):
      # print help as the OptionParser normally would, without extra goodies
      optparse.OptionParser.print_help(self)


    extras = ''
    if '--help' in sys.argv and self.extra_txt is not None and errors is None:
      """
      try: extras = "Created: %s\n" % __created__
      except NameError: pass
      try: extras = "%sAuthor: %s\n" % (extras,__author__)
      except NameError: pass
      try: extras = "%sCopyright: %s\n" % (extras,__copyright__)
      except NameError: pass
      try: extras = "%sVersion: %s\n" % (extras,__version__)
      except NameError: pass
      if extras:
        self.extra_txt = "\n%s\n\n%s" % (self.extra_txt, extras)
      """
      #print self.extra_txt
      self.print_out(self.extra_txt)

    if not errors:
      errrors = []
    elif not isinstance(errors, list):
      errors = [errors]

    sys.stdout = sys.__stdout__
    # XXX:TODO - 2 Weeks ago I was writing a ManPage builder.  Afer looking
    # back at this method I wrote years ago.  I realized it would be easy to
    # alter this code just slightly to have it generate manpages.  It may be
    # better to just add a similar method for generating manpages, easier than
    # what I was doing.
    self.print_out(buf.getvalue().replace("Options:\n","OPTIONS:\n").replace(":\n",":\n\n"))
    #txt = txt.replace(":\n",":\n\n")

    if errors:
      sys.stderr.write("\n")
      for error in errors:
        sys.stderr.write(wrap("ERROR: %s\n" % error))
    sys.stderr.flush()
# =============================================================================
# Begin Helpers
# -----------------------------------------------------------------------------
funcs = []
# I like this way more, but the other is easier to understand
def collector(func):
  global funcs
  funcs.append(func) #[func.__name__][method] = func
  return func # this is important, if you don't do this... you cannot call the function EXCEPT through the collector

def run_cmd(cmd, timeout_sec):
  proc = Popen(shlex.split(cmd), stdout=PIPE, stderr=PIPE)

  #iN, out, err = os.popen3('curl ipinfo.io/ip')
  #iN.close() ; err.close()
  #ip = out.read().strip()

  timer = Timer(timeout_sec, proc.kill)
  try:
    timer.start()
    stdout, stderr = proc.communicate()
  finally:
    timer.cancel()
  return stdout

def validate_ip(s):
  a = s.split('.')
  if len(a) != 4:
    return '' 
  for x in a:
    if not x.isdigit():
      return ''
    i = int(x)
    if i < 0 or i > 255:
      return ''
  return s

def valid_ip(ip):
  if ip:
    if type(ip) != type(str('string')):
      ip = ip.decode('utf-8')
    ip=str(ip).strip().replace("\\n","")
  else:
    ip=''
  try:
    socket.inet_aton(ip)
  except socket.error as e:
    return ''
  else:
    return validate_ip(ip)

class Timeout(Exception): pass

# -----------------------------------------------------------------------------
# End Helpers
# =============================================================================


@collector
def hostip(log, timeout=default_timeout):
  #ol_level = logging.getLogger().getLevel()
  #logging.getLogger.setLevel(level=logging.CRITICAL)
  try:
    url = 'http://api.hostip.info/get_json.php'
    info = json.loads(urlopen(url,
      timeout=timeout).read().decode('utf-8'))
    ip = info['ip']
    '''
    if ip: 
      ip = str(ip).strip()
      print('about to test: %s' % ip)
      #socket.inet_aton(ip)
    '''
  except URLError as e:
    #log.error(e.reason) # e.g. 'timed out'
    #log.error('(are you connected to the internet?)')
    raise Timeout(str(e))
  except socket.timeout as e:
    raise Timeout("timeout: %s" % str(e))
  except KeyboardInterrupt:
    return None
  else:
    log.debug('hostip: "%s"' % str(ip).strip())
    return valid_ip(ip)
    return ip


@collector
def ipecho(log, timeout=default_timeout):

  try:
    response = urlopen('http://ipecho.net/plain', timeout=timeout)
    ip = response.read()
    
  except URLError as e:
    raise Timeout("timeout: %s" % str(e))
  except socket.timeout as e:
    raise Timeout("timeout: %s" % str(e))
  else:
    log.debug('ipecho: "%s"' % str(ip).strip())
    return valid_ip(ip)
  
@collector
def ipinfo(log, timeout=default_timeout):
  ''' on tested system, generally needs on or over -t0.085 timeout
  '''
  '''
  iN, out, err = os.popen3('curl ipinfo.io/ip')
  iN.close() ; err.close()
  ip = out.read().strip()
  '''

  ip = run_cmd('curl ipinfo.io/ip', timeout) #.readlines(-1)[0].strip()  # timeout happens at 1 second
  log.debug('ipinfo: "%s"' % str(ip).strip())
  return valid_ip(ip)

@collector
def opendns(log, timeout=default_timeout):
  ''' on tested system, generally needs on or over 0.0128 timeout
  '''
#  ip = os.popen('dig +short myip.opendns.com @resolver1.opendns.com').readlines(-1)[0].strip()
  ip = run_cmd('dig +short myip.opendns.com @resolver1.opendns.com', timeout) #.readlines(-1)[0].strip()  # timeout happens at 1 second
  log.debug('opendns: "%s"' % str(ip).strip())
  return valid_ip(ip)

def run_funcs(log, echo=True, verbose=False, run_all=False, 
    timeout=default_timeout, funcs=funcs):

  return_ip = None
  for func in funcs:
    try:
      log.debug("calling: %s" % func.__name__)
      ip = func(log, timeout)
    except KeyboardInterrupt as e:
      log.debug("KeyboardInterrupt:",e)
      log.info("Script terminated by Control-C")
      log.info("bye!")
      # Return Code 130 - Script terminated by Control-C
      sys.exit(130)
    except Timeout as e:
      if verbose > 1:
        log.error('timeout: %s' % str(e))
    except Exception as e:
      log.error('unknown exception')
      log.error(str(e))
      log.exception(e)
    else:
      if ip:
        if echo:
          print(ip)
        return_ip = ip
        if not run_all:
          return ip

  return return_ip 

def main(funcs=funcs):
  """usage: %prog <options> (*use '--help' to see the full help text) """
  global default_timeout, log
  # ----------------------------
  parser = MParser()
  parser.set_usage(main.__doc__)
  parser.formatter.format_description = lambda s:s

  # ----------------------------
#  parser.add_option("-D", "--debug", action="store_true", default=False, help="Enable debugging")

  vrs = optparse.OptionGroup(parser, "Main",' ')

  vrs.add_option("-a", "--all", action="store_true", default=False, dest='all',
    help='Run all available methods.')

  vrs.add_option('-L', '--list', action='store_true', default=False, 
    dest='list', help="List methods we have available to get the IP. " \
    "[-L/-l or --list]")

  vrs.add_option('-l', '', action='store_true', default=False, 
    dest='list', help=optparse.SUPPRESS_HELP)

  vrs.add_option('-t', '--timeout', action='store', type='float', 
    default=default_timeout, metavar='[TIMEOUT]', dest='timeout', 
    help="Amount of time to allow an attempted thread query for your IP. " \
    "(example: -t3)")

  vrs.add_option("-d", "--debug", action="store_true", default=False,
    dest='debug', help="Enable debugging`$")

  vrs.add_option("-q", "--quiet", action="store_true", default=False, 
    dest='quiet', help="be vewwy quiet (I'm hunting wabbits)`$")

  vrs.add_option('-v', '--verbose', dest='verbose', action='count', default=0,
    help="Verbosity, numeric, -vvv is less verbose than -vv which is less " \
    "than -v.")

  vrs.add_option("-V", "--version", action="store_true", default=False,
    dest='version', help="show program's version number and exit")

  parser.add_option_group(vrs)

  help_dict = dict(version=__version__,
             author=__author__,
             created=__created__,
             copyright=__copyright__)

  if '--help' in sys.argv:
    parser.set_description(__doc__)
    extra = """
CODE:
  Flag vs. Argument:
    Flag - an option that accepts no input.
    Argument - an option that requires input.

SEE ALSO:

  dyndns
  powerdns-update

COPYRIGHT:

  %(copyright)s

AUTHOR:

  %(author)s

HISTORY:


  Original Author

CHANGE LOG:

  v2.1 MINOR CHANGE                                              August 16, 2022
    Added exception to catch socket timeout in hostip, and added comments to
    better explain main func.
    

  v2.0 MAJOR CHANGE                                             January 20, 2022
    I noticed this does NOT import my pytis library like MOST of my programs
    do, so I wanted to keep it this way (so it can be exported as a stand alone
    program easily) however, I also wanted to have the "-h" and "--help"
    function as it does with my PyTis.MyParser (custom optparse.OptionParser)
    where --help will work similarly to a manpage, allowing the user to search,
    almost as if it were piped to MORE.  Also, the user doesn't have to scroll.
    This would be about the same as NOT having a custom parser, but running
    "getip.py --help | more"  I have just the simple help displayed when the
    user uses "-h" and the full help with examples, docstrings, etc. being
    displayed when the user inputs "--help."  Since the output IS longer than
    my window (it doesn't all fit), and I wish not only to be able to easily
    PAGEUP/PAGEDOWN but also search the help (JUST like a manpage) I simply
    created a custom parser class here, copying the 2 methods from the pytis
    parser, that perform this task for me, keeping the pytis library separate.
  
  v1.2 MINOR CHANGE                                                 May 29, 2020
    Updated urllib2 import to support both Python2 and Python3

  v1.1 MINOR CHANGE                                             October 15, 2018
    Better error handling.

  v1.0 ORIGINAL RELEASE                                          October 1, 2018
    Original Publish.


EXAMPLES:  

  getip ipecho

  getip 3

  getip

  getip --list

  getip -dv

  getip -v

  getip -vv

  getip -vvv


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
    parser.print_help()
    return 0

  (opts, args) = parser.parse_args()
  
  if opts.version:
    print("getip v%s" % __version__)
    return 0
  # ----------------------------
  if opts.verbose >= 3:
    opts.debug=True

  log.setLevel(0)
  formatter = ' %(name)s | %(asctime)s | %(levelname)-8s | %(message)s'
  logging.basicConfig(level=logging.ERROR, format=formatter, datefmt="%Y%m%d %H:%M:%S")

  if opts.verbose:       logging.getLogger().setLevel(level=logging.WARNING)
  if opts.verbose > 1:   logging.getLogger().setLevel(level=logging.INFO)
  if opts.verbose > 2:   logging.getLogger().setLevel(level=logging.DEBUG)
  if opts.verbose >= 3:   logging.getLogger().setLevel(level=logging.NOTSET)
  if opts.debug:         logging.getLogger().setLevel(level=logging.DEBUG)
  if opts.quiet:         logging.getLogger().setLevel(level=logging.CRITICAL)

  '''
  log.debug('debug')
  log.info('info')
  log.warn('warn')
  log.error('error')
  log.fatal('fatal')
  log.critical('critical')
  log.warning('warning')
  '''
  funcs.sort(key=lambda x: x.__name__)


  try:
    if len(args) > 1:
      log.error('Please only choose one method.')
      return 1
    elif len(args) == 1:
      # user specifically selected just one type to run
      possible = args[0]

      try:
        possible = int(possible)
      except (IndexError,ValueError):
        pass
      else:
        possible-=1

      # try to get the method to run
      try:
        if type(possible) is type(1):
          if possible < 0 or possible > len(funcs):
            raise IndexError
          func = funcs[possible]
        else:
          func = [f for f in funcs if f.__name__ == possible][0]
      except IndexError:
        log.error('Function not found.')
        return 1
      else:
        if opts.verbose > 0:
          print('%s:' % func.__name__)
        try:
          # try to run the one method the user selected
          print(func(log, opts.timeout))
        except Timeout as e:
          if opts.verbose > 1:
            log.error(e)
          else:
            return 1
        return 0


    # user wants to list all methods available.
    if opts.list:
      st = '%' + str(len(str(len(funcs)))+1) + 'd. %s'
      for i, func in enumerate(funcs):
        print(st % (i+1, func.__name__))
    else:
      # user hasn't given any input, just print the first IP we find.
      # the second argument (True) is passed in to make the run_funcs print
      # the IP found, this way this can also be imported as a module and just
      # return the IP if a coder wants, without printing to screen.
      ip = run_funcs(log, True, opts.verbose, opts.all, opts.timeout, funcs)
      if ip:
        return 0
      else:
        return 1
  except KeyboardInterrupt as e:
    log.debug("KeyboardInterrupt:",e)
    log.info("Script terminated by Control-C")
    log.info("bye!")
    # Return Code 130 - Script terminated by Control-C
    # sys.exit(130)
    return 130

if __name__ == '__main__':
  try:
    sys.exit(main())
  except Exception as e:
    print("An error has occured.\n")
    print(str(e))
    sys.exit(1)

