
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

Need to learn git branching, so I can have one branch for W.I.P. and one for
completed, functional scripts.

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

