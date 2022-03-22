#!/usr/bin/python3

import getpass
import os, sys

username = 'pytis'
original_username = username

print('INIT...')

if len(sys.argv) > 1:
	u = sys.argv[1]
	if str(u).lower() in \
		('-h','/h','h','/?','-?','?','-help','/help','help'):
		print('USAGE: ./setup-user.py [optional: <username>]')
		print('this script will by default, install for the "pytis" user, unless ' \
			'you provide a different username (you must be logged in as that ' \
			'user, to override the username).')

	else:
		pu = str(u)
		if pu.lower() == str(getpass.getuser()).lower():
			username = pu
		else:
			print('ERROR: username "%s" does not match logged in user "%s"' % (
				pu, getpass.getuser()))
			print('You must be logged in as "%s" to install for "%s."' % (pu, pu))
			sys.exit(0)


print('installing for %s' % username)

if not os.path.exists('/home/%s/bashrc.orig' % username):
	print('making backup of .bashrc file')
	os.system('cp /home/%s/.bashrc /home/%s/bashrc.orig' % (username, username))

target = os.path.abspath('/home/%s' % username)

if not os.path.exists(target):
	print("ERROR!")
	print("This script is for installing your user settings to a LINUX " \
		"operating system.  It appers that the home directory for \"%s\" does " \
		"not exist as the path \"%s\" cannot be found." % (username, target)
	sys.exit(1)


print('copying all files from bootstrap/home-pytis to /home/%s' % username)
os.system('/bin/cp -rf home-pytis/* %s/' % target)
os.system('/bin/cp -rf home-pytis/.sessions/ %s/' % target)
os.system('/bin/cp -rf home-pytis/.ssh %s/' % target)
os.system('/bin/cp -rf home-pytis/.vim %s/' % target)
os.system('/bin/cp -rf home-pytis/.vim.php %s/' % target)

os.system('/bin/cp -rf home-pytis/.bash_profile %s/' % target)
os.system('/bin/cp -rf home-pytis/.bashrc %s/' % target)
os.system('/bin/cp -rf home-pytis/.dir_colors %s/' % target)
os.system('/bin/cp -rf home-pytis/.gitconfig %s/' % target)
os.system('/bin/cp -rf home-pytis/.git-credentials %s/' % target)
os.system('/bin/cp -rf home-pytis/.kshrc %s/' % target)
os.system('/bin/cp -rf home-pytis/.lesshst %s/' % target)
os.system('/bin/cp -rf home-pytis/.minttyrc %s/' % target)
os.system('/bin/cp -rf home-pytis/.multitail %s/' % target)
os.system('/bin/cp -rf home-pytis/.my-credentials %s/' % target)
os.system('/bin/cp -rf home-pytis/.profile %s/' % target)
os.system('/bin/cp -rf home-pytis/.pypirc %s/' % target)
os.system('/bin/cp -rf home-pytis/.screenrc %s/' % target)
os.system('/bin/cp -rf home-pytis/.vimrc %s/' % target)


if username != original_username:

	os.chdir(target)

	command1 = "find .  -type f | egrep -v 'home-pytis'  |xargs sed -i " \
		"'s/%s/%s/g'" % (original_username, username)

	if not os.path.abspath(os.curdir) == os.path.abspath(target):
		print('ERROR: we are in the wrong directory to run the following command:')
		print(command1)
		sys.exit(1)
	else:
		os.system(command1)

	command2 = "find . -type f -name '.netrwhist' | egrep -v 'home-pytis' | " \
		"xargs sed -i 's/%s/%s/g'" % (original_username, username)
	os.system(command2)

	command3 = "find . -type f -name 'php.vim' | egrep -v 'home-pytis' | " \
		"xargs sed  -i 's/%s/%s/g'" % (original_username, username)

	os.system(command3)

print("\ndone.")
