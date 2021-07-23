git clone --branch leejo7a https://gitlab.verizon.com/leejo7a/rehydration-bootsrapers.git


REHYDRATION-BOOTSTRAPPERS
=========================

Synopsis
--------

For each user, you may store your "bootstrapping" code, to easily rebuild a newly
deployed box after rehydration.  A user can simply clone their specific branch of
this project onto their machine, and run their bootstrapping code.  

Suggestion For Maintenance
--------------------------

Any time you find yourself adding a module or 3rd party library for Python
(perhaps with "pip3.8 install --upgrade [PACKAGE_NAME] ), you should add it to
your boot-strapper, allowing it to perform the installer for you.  

After a successful install, simply commit and push your code, and you know it
is up to date.  Now after a rehydration, all you have to do is clone and run
your scripts.  


You are not required to follow the suggested format below, but it is suggested.

Suggestion for Design
---------------------

Four files is all you should need.  
* usersfiles.tar.gz
* setup-user.py
* rootfiles.tar.gz
* setup-root.py

The single script for the user's environment to be deployed may be named:
setup-user.sh or setup-user.py

A single tarball (userfiles.tar.gz) for the user's script to extract into their
environment, and to place the designed .bashrc, .vimrc, .screenrc
(customization files), etc. where desired. It may continue to install specific
items to the user locally, when true root/administrative access is an issue.
Example: "pip3.8 install --user pyflakes"

Similarly, if you will be able to perform administrative commands, a single
tarball (rootfiles.tar.gz) can contain any files you wish to have in the root
environment.  On Linux, one would run "pbrun beroot", authenticate, then you
can run ./setup-root.py and you are done.

*Please feel free to reference the leejo7a branch as an example.

