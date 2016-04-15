#!/usr/bin/python
import os, sys

def pg(extra_flags=''):
	import os, sys
	import subprocess

	pg_base = "/var/lib/postgresql/bin"
	sys.path.append(pg_base)

	command =  ["python3", os.path.abspath(os.path.join(pg_base,'aws-pis')), "-D"]
	command.extend([flag.strip() for flag in extra_flags.split(';') if flag.strip()])

	return subprocess.call(command)

pg(";".join(sys.argv[1:]))
