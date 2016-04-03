
PyTis toolbox Readme
==

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

LICENSE:
--

This library of tools is released under a license similar to the GPL or MPL, it
has been slightly modified. In summary, you must give the original author
credit, and leave a copy of the logo in the directory.  To view the license in
its entirety, go here: http://pytis.com/License/

* Feel free to download and share this library of tools,
* Feel free to make fixes or even add-ons;
  however I retain the right to control what gets added in, or not.


