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

print('copying all files from bootstrap/home-jlee to /home/%s' % username)
os.system('/bin/cp -rf home-jlee/* ../')
os.system('/bin/cp -rf home-jlee/.sessions/ ../')
os.system('/bin/cp -rf home-jlee/.ssh ../')
os.system('/bin/cp -rf home-jlee/.vim ../')
os.system('/bin/cp -rf home-jlee/.vim.php ../')

os.system('/bin/cp -rf home-jlee/.bash_profile ../')
os.system('/bin/cp -rf home-jlee/.bashrc ../')
os.system('/bin/cp -rf home-jlee/.dir_colors ../')
os.system('/bin/cp -rf home-jlee/.gitconfig ../')
os.system('/bin/cp -rf home-jlee/.git-credentials ../')
os.system('/bin/cp -rf home-jlee/.kshrc ../')
os.system('/bin/cp -rf home-jlee/.lesshst ../')
os.system('/bin/cp -rf home-jlee/.minttyrc ../')
os.system('/bin/cp -rf home-jlee/.multitail ../')
os.system('/bin/cp -rf home-jlee/.my-credentials ../')
os.system('/bin/cp -rf home-jlee/.profile ../')
os.system('/bin/cp -rf home-jlee/.pypirc ../')
os.system('/bin/cp -rf home-jlee/.screenrc ../')
os.system('/bin/cp -rf home-jlee/.vimrc ../')


if username != original_username:
	os.system("find .  -type f -name '*' | egrep -v 'home-jlee' |xargs sed  -i 's/%s/%s/g'" % (
		original_username, username))

	os.system("find .  -type f  | egrep -v 'home-jlee' | xargs sed  -i 's/%s/%s/g'" % (
		original_username, username))

	os.system("find .  -type f -name '.netrwhist'  | egrep -v 'home-jlee' |xargs sed  -i 's/%s/%s/g'" % (
		original_username, username))

	os.system("find .  -type f -name 'php.vim'  | egrep -v 'home-jlee' |xargs sed  -i 's/%s/%s/g'" % (
		original_username, username))




print("\ndone.")
