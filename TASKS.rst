
TODO/TASKS
==========

Need to create a passthru program so that apache can easily access the scripts
without a .py extension.

Need to clean up each programs helptext and remove old un-needed options.

I realized that one some of my programs use the generic, catch-all
pytis_tools.ini, and others use only their own .ini, I'd like there be an easy
option for it to be both, with inheritance, where a program could look for its
own ini file, as the primary, but if not found, load default values from the
pytis_tools.ini.


I've recently come to the realization, after spending ours merging pytis.py and pytis3.py for the 3rd tiem, that it would make more sence to merge them back into a single file, do away with pylib and pylib3, and handle language version difference within the file.  99.9% of pytis is the same as pytis3, the subtle differences could be coded around right there in the file itself.

TODO - INI Files
----------------
I realized that some of my programs use the generic, catch-all pytis_tools.ini,
and others use only their own .ini, I would like there be an easy option for it
to be both, with inheritance, where a program could look for its own ini file,
as the primary, but if not found, load default values from the pytis_tools.ini.

TODO - Log Files
----------------

When I build a stand alone project for someone, it may be confusing how logging
works.  For me, I like all output going to the single pytis_tools.log, UNLESS,
the -D/--debug option is given.  In this case a tool uses its own, custom log
file, named after itself.  However, when I deploy a standalone script for
someone, for them to end up with two different log files, is not only
confusing, it is pointless.  I need to through an option in configure.py, that
allows me to turn off writing to pytis_toos.log, and force the current
application to always use its own log file.  This way upon install/setup, I can
just flip that switch and problem solved.

TODO - Meging
-------------

I have recently come to the realization, after spending ours merging pytis.py 
and pytis3.py for the 3rd tiem, that it would make more sence to merge them
back into a single file, do away with pylib and pylib3, and handle language
version difference within the file.  99.9% of pytis is the same as pytis3, the
subtle differences could be coded around right there in the file itself.  **
Thusfar, the pytis libraries have been merged, however "pylib" and "pylib3"
still need to be merged.  After running a diff on configobject however, I
realize that this will be a more lengthy process, then first realized.

TODO - Option Parser
--------------------

Whether I stay with OptParser, or migrate to ArgParser, I still do not like how
the help is handled.  I want to create a custom option class, a subclass of the
built-in that allows me to provide a long and short version of the help, then
depending on if the user asks for the full help or short help (-h vs --help) it
can auto build.  This would prevent the giant IF ELSE I currently use.

TODO - ITEM 5
-------------

DESC GOES HERE


TODO - src/bin/pg_diff
----------------------

Currently, this program will output a very nice diff between two PostgreSQL file dumps, along with whatever commands would be needed to bring one database schema to the other.  I.E.  you have a dev and a live, your dev had undergone weeks of changes, but you lost track of them, and need to push your code live, but need to run the alter, drop, rename, add table (etc.) commands to bring live up-to-date with the schema, so that commands can be ran on live, bringing up to match dev.
Next version needed.  
I would like to have some sort of config file, where I can specify the dev db and live db as parent ini sections by name, the recall them via the command line.  Thus the user would type something like: "pg_diff mydev mylive" and then, this program could utilize pgdump and cache the sql temporarily for the diff itself.

MILESTONES
==========

Need to get the list of working programs completed for GitHub.

Create setup.py installer for our tools.

Create a tool that uses our deep help (--help) and generates man pages, and
installs them ( w.i.p., 60% done)) 

Create Man Pages for each of our tools, alter setup.py to actually install
these as well.

# DONE, but added to.
	Need to learn git branching, so I can have one branch for W.I.P. and one for
	completed, functional scripts.  

Now that I have learned branching, I have one last objective.  I wrote a bash
script that will take any program and its flags, options, etc. and run it, then
return the exit code a a single int on stdout.  I want to create a wrapper for
git-push with a hook to check if the push is to the LIVE branch. If it is, then
providing the exit code is 0 (no errors) then I want to auto-increment the
"VERSION" file.  There is more to it than this.  I have in mind, a tool that
runs interactively, and promps the user asking, is this a MAJOR CHANGE, or
MINOR CHANGE, and asks for details on what changes occured.  This program would
not only manage the MAJOR and MINOR VERSION numbers, but also maintain the
CHANGE LOG for me.

# DONE.
	I need to break out the Database interaction into a module with a parent
	layer.  This way a user can pick and choose which Database that he/she wishes
	to use.  I would like to have first release support PostgreSQL, MySQL and
	Sqlite3.


DYNDNS
======

(root@neptune ( IP:192.168.1.17 )  )-(~/bin)-(01:55 PM Wed Sep 12)->
(115 files, 1.4Mb)--> dyndns
INFO     config file not found, creating: /home/jlee/.dyndns
Traceback (most recent call last):
  File "/root/bin/dyndns", line 165, in <module>
    main()
  File "/root/bin/dyndns", line 162, in main
    if run: do(conf)
  File "/root/bin/dyndns", line 106, in do
    conf_set(conf, 'ip address', nip)
  File "/root/bin/dyndns", line 46, in conf_set
    conf.set('info', option, value)
  File "/usr/lib/python2.7/ConfigParser.py", line 396, in set
    raise NoSectionError(section)
ConfigParser.NoSectionError: No section: 'info'

