#!/usr/bin/python3

import getpass
import os, sys

username = 'jlee'
original_username = username

print('INIT...')

if len(sys.argv) > 1:
	u = sys.argv[1]
	if str(u).lower() in \
		('-h','/h','h','/?','-?','?','-help','/help','help'):
		print('USAGE: ./setup-user.py [optional: <username>]')
		print('this script will by default, install for the "jlee" user, unless ' \
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
		"not exist as the path \"%s\" cannot be found." % (username, target))
	sys.exit(1)


print('copying all files from bootstrap/home-jlee to /home/%s' % username)
os.system('/bin/cp -rf home-jlee/* %s/' % target)
os.system('/bin/cp -rf home-jlee/.sessions/ %s/' % target)
os.system('/bin/cp -rf home-jlee/.ssh %s/' % target)
os.system('/bin/cp -rf home-jlee/.vim %s/' % target)
os.system('/bin/cp -rf home-jlee/.vim.php %s/' % target)

os.system('/bin/cp -rf home-jlee/.bash_profile %s/' % target)
os.system('/bin/cp -rf home-jlee/.bashrc %s/' % target)
os.system('/bin/cp -rf home-jlee/.dir_colors %s/' % target)
os.system('/bin/cp -rf home-jlee/.gitconfig %s/' % target)
os.system('/bin/cp -rf home-jlee/.git-credentials %s/' % target)
os.system('/bin/cp -rf home-jlee/.kshrc %s/' % target)
os.system('/bin/cp -rf home-jlee/.lesshst %s/' % target)
os.system('/bin/cp -rf home-jlee/.minttyrc %s/' % target)
os.system('/bin/cp -rf home-jlee/.multitail %s/' % target)
os.system('/bin/cp -rf home-jlee/.my-credentials %s/' % target)
os.system('/bin/cp -rf home-jlee/.profile %s/' % target)
os.system('/bin/cp -rf home-jlee/.pypirc %s/' % target)
os.system('/bin/cp -rf home-jlee/.screenrc %s/' % target)
os.system('/bin/cp -rf home-jlee/.vimrc %s/' % target)


if username != original_username:

	os.chdir(target)

	command1 = "find .  -type f | egrep -v 'home-jlee|bootstrap' | " \
		"xargs sed -i 's/%s/%s/g'" % (original_username, username)

	if not os.path.abspath(os.curdir) == os.path.abspath(target):
		print('ERROR: we are in the wrong directory to run the following command:')
		print(command1)
		sys.exit(1)
	else:
		os.system(command1)

	command2 = "find . -type f -name '.netrwhist' | egrep -v " \
		"'home-jlee|bootstrap' | xargs sed -i 's/%s/%s/g'" % (original_username,
		username)
	os.system(command2)

	command3 = "find . -type f -name 'php.vim' | egrep -v " \
		"'home-jlee|bootstrap' | xargs sed  -i 's/%s/%s/g'" % (original_username,
		username)

	os.system(command3)

	command4 = "find . -type f -name '.vimrc' | egrep -v " \
		"'home-jlee|bootstrap' | xargs sed  -i 's/%s/%s/g'" % (original_username,
		username)

	os.system(command4)

print("\ndone.")
