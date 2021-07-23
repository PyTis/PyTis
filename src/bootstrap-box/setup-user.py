#!/usr/bin/python3

import os
if not os.path.exists('/home/leejo7a/bashrc.orig'):
	print('making backup of .bashrc file')
	os.system('cp /home/leejo7a/.bashrc /home/leejo7a/bashrc.orig')

print('copying all files from bootstrap/home-jlee to /home/leejo7a')
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

#os.system('/bin/cp -rf home-jlee/.bashrc ../')



