PyTis toolbox Readme
==

This library was originally maintained on SourceForge (sf.net).  I will
probably try to maintain this project at both locations simultaneously, within
.git on

Eventually to be staged via GIT on GitHub, and SVN (Subversion) on SourceForge,
the overall structure is about to get a major overhaul, as I begin to allow
this to have examples, man pages, an installer, builds, distributions, misc.,
src, testsuite, etc.

Until I finish getting much of this code migrated into GitHub, though some of
them may be outdated, you may be able to find what you are looking for in the
original repository at sf.net.

	SourceForge Project: https://sourceforge.net/projects/pytis/

	SourceForge Repository: https://sourceforge.net/p/pytis/code/HEAD/tree/trunk/


PLEASE READ FIRST.
--

This library should be updated again soon.  For now it is a work in progress.
I will try to keep a running list of working, up-to-date programs below,
although I am not even going to get to do that until next week.

I wrote many, many of these scripts, very, very long ago, as I learned Python
and Linux.  I've make scripts all the time to help achieve mundane tasks.
Since I've started, I have learned a few one or two of these scripts were
unneeded as there are already built in Linux commands.  Many others are still
useful to this day.

When programmers find themselves doing the same thing over and over again, they
write a function, well, in some cases, I've written programs to streamline
programming from a higher level.  Carpenters and mechanics have toolboxes, this
library is mine.  I've written useful tools like: copyright - which inspects
(recursively if requested) files, and depending on the file extension, which it
is already written to handle many of, applies the copyright you've selected
appropriately, to pg_diff which works much like diff, or vimdiff, to bulk find
and replace programs that will actually find and replace parts of file names,
to programs that manage the synchronization of files across many servers.

Now I wish to share them, and to allow them to be expanded upon.  Since I've
started, I've almost always used 1 and only 1 file as a central class and
function library; pytis.py (for Python version < 3) and pytis3.py (for Python
version >= 3).  I usually use some OO inheritance as well.  About a year ago, I
also created a single pylib module (and pylib3 for python >= v3) however I try
to limit the files within to only absolutely necessary items.  Currently there
are only 3 files in pylib, and the 2nd imports the 3rd.

Many of my tools need updated; as my central library grew and changed over the
years, I haven't kept many of the older scripts up-to-date, so a few of them,
though they may have worked fine in the past, will not run until I bring them
up-to-date with the new version of the central library.

Again, some of these programs work now, perfectly, and are up-to-date with the
current pytis/pytis3 modules, however a few need brought up to date with
changes made in that module.  In the next week or two, I hope to begin listing
which are which, and over the next few months bring all of them up-to-date, or
remove incomplete, dead programs.


USAGE/HOWTO
--

Howto use import from this module.

To allow me to easily move from Python2.x to Python3, I treat PyTis (pytis.py)
as a module, however in order to import a local module, path manipulation is
required.  Below is an example of howto do it command line, then below that is
an actual example from a program that actually does it.

  (~/gitlab/aws-tools/aws-tools/bin)-> python3
  Python 3.4.3 (default, Oct 14 2015, 20:28:29)
  [GCC 4.8.4] on linux
  Type "help", "copyright", "credits" or "license" for more information.
  >>> import os, sys
  >>> sys.path.append(os.path.abspath(os.path.join(os.path.dirname(os.curdir),'..')))
  >>> from bin import PyTis
  >>> from pylib3 import awslib
  >>>

  # This program needs to import PyTis v3, which imports stuff from the
  # sub-package pylib3, this program also needs to import from the sub-package
  # awslib, pylib3.awslib itself, has to import from the parent, pytis3, which it
  # can only do if the parent directory is a package, turning the parent (bin)
  # into a package breaks importing pytis3 for this program in the first place
  # and caused severe circular import errors.  To fix this, we have to adjust the
  # path.
  import os, sys
  sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))

  # Internal
  #
  try:
    #import pytis as PyTis # Shared GPL/PPL License
    from bin import PyTis # Shared GPL/PPL License
    from pylib3 import awslib
    from pylib3 import configobj as COBJ
  except ImportError as e:
    # We cannot go any further than this, we can't use the Parser or Logging tool
    # to display these errors because those very tools are loaded from PyTis.
    # Therefore, display errors now and exit with an errored exit code.
    print("This program requires the PyTis python library to run.")
    print("You may download the PyTis library, or do an SVN checkout from:")
    print("<https://sourceforge.net/projects/pytis/>")
    print("This program should be installed in the bin directory of the PyTis library.")
    print(str(e))
    sys.exit(1)

LICENSE:
--

This library of tools is released under a license similar to the GPL or MPL, it
has been slightly modified. In summary, you must give the original author
credit, and leave a copy of the logo in the directory.  To view the license in
its entirety, go here: http://pytis.com/License/

* Feel free to download and share this library of tools,
* Feel free to make fixes or even add-ons;
  however I retain the right to control what gets added in, or not.

VERSION(s):
--

May vary, I will get this all under control soon though.

NICENESS:
--

It appears that the only file that used "ioclass" instead of "ioniceness_class"
is pysync, after fixing the merger between pytis on pluto from sourceforge, and
GitHub from work, I also need to remember to push these changes to pytis3.py.

