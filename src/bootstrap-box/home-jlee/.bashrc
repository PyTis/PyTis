# To the extent possible under law, the author(s) have dedicated all 
# copyright and related and neighboring rights to this software to the 
# public domain worldwide. This software is distributed without any warranty. 
# You should have received a copy of the CC0 Public Domain Dedication along 
# with this software. 
# If not, see <http://creativecommons.org/publicdomain/zero/1.0/>. 

# base-files version 4.2-4

# ~/.bashrc: executed by bash(1) for interactive shells.

# The latest version as installed by the Cygwin Setup program can
# always be found at /etc/defaults/etc/skel/.bashrc

# Modifying /etc/skel/.bashrc directly will prevent
# setup from updating it.

# The copy in your home directory (~/.bashrc) is yours, please
# feel free to customise it to create a shell
# environment to your liking.  If you feel a change
# would be benifitial to all, please feel free to send
# a patch to the cygwin mailing list.

# User dependent .bashrc file

# If not running interactively, don't do anything
[ -z "$PS1" ] && return

export PSQL_PATH='/usr/bin/psql'

# don't put duplicate lines in the history. See bash(1) for more options
# ... or force ignoredups and ignorespace
HISTCONTROL=ignoredups:ignorespace

# append to the history file, don't overwrite it
shopt -s histappend

# for setting history length see HISTSIZE and HISTFILESIZE in bash(1)
HISTSIZE=1000
HISTFILESIZE=2000

# check the window size after each command and, if necessary,
# update the values of LINES and COLUMNS.
shopt -s checkwinsize

# make less more friendly for non-text input files, see lesspipe(1)
[ -x /usr/bin/lesspipe ] && eval "$(SHELL=/bin/sh lesspipe)"

# set variable identifying the chroot you work in (used in the prompt below)
if [ -z "$debian_chroot" ] && [ -r /etc/debian_chroot ]; then
    debian_chroot=$(cat /etc/debian_chroot)
fi

# set a fancy prompt (non-color, unless we know we "want" color)
case "$TERM" in
    xterm-color) color_prompt=yes;;
esac

# uncomment for a colored prompt, if the terminal has the capability; turned
# off by default to not distract the user: the focus in a terminal window
# should be on the output of commands, not on the prompt
#force_color_prompt=yes

if [ -n "$force_color_prompt" ]; then
    if [ -x /usr/bin/tput ] && tput setaf 1 >&/dev/null; then
        # We have color support; assume it's compliant with Ecma-48
        # (ISO/IEC-6429). (Lack of such support is extremely rare, and such
        # a case would tend to support setf rather than setaf.)
        color_prompt=yes
    else
        color_prompt=
    fi
fi

#IP=`LANG=c ifconfig wlp2s0b1 | grep 'inet addr' | awk -F: '{print $2}' | awk '{print $1}'`
IP=`LANG=c getip | awk -F: '{print $1}'`

if [ "$color_prompt" = yes ]; then
    PS1='${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u@$IP\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\$ '
    # customized to show actual public IP
    PS1="\n\[\e[30;1m\](\[\e[0;33m\]\u\[\e[1;30m\]@\[\e[0;33m\]IP:$IP\[\e[30;1m\])-(\[\e[1;34m\]\w\[\e[30;1m\])-(\[\e[0;32m\]\@ \d\[\e[30;1m\])->\[\e[30;1m\]\n(\[\e[37;1m\]\$(/bin/ls -1 | /usr/bin/wc -l | /bin/sed 's: ::g') files, \$(/bin/ls -lah | /bin/grep -m 1 total | /bin/sed 's/total //')b\[\e[30;1m\])--> \[\e[0m\]"
else
    # customized to show actual public IP
    PS1="\n\[\e[30;1m\](\[\e[0;33m\]\u\[\e[1;30m\]@\[\e[0;33m\]\h  ( IP:$IP )  \[\e[30;1m\])-(\[\e[1;34m\]\w\[\e[30;1m\])-(\[\e[0;32m\]\@ \d\[\e[30;1m\])->\[\e[30;1m\]\n(\[\e[37;1m\]\$(/bin/ls -1 | /usr/bin/wc -l | /bin/sed 's: ::g') files, \$(/bin/ls -lah | /bin/grep -m 1 total | /bin/sed 's/total //')b\[\e[30;1m\])--> \[\e[0m\]"


fi

unset color_prompt force_color_prompt

# If this is an xterm set the title to user@host:dir
case "$TERM" in
xterm*|rxvt*)
    PS1="\[\e]0;${debian_chroot:+($debian_chroot)}\u@\h: \w\a\]$PS1"
    ;;
*)
    ;;
esac

# SHOULD ALWAYS LOAD
# Alias definitions.
# You may want to put all your additions into a separate file like
# ~/.bash_aliases, instead of adding them here directly.
# See /usr/share/doc/bash-doc/examples in the bash-doc package.
if [ -f ~/bashrc/common.rc ]; then
    . ~/bashrc/common.rc
fi
if [ -f ~/.bash_profile ]; then
  . ~/.bash_profile
fi
if [ -f ~/bashrc/git-shortcuts.rc ]; then
    . ~/bashrc/git-shortcuts.rc
fi
if [ -f ~/.bash_aliases ]; then
    . ~/.bash_aliases
fi

# SERVER DEPENDENT LOADERS
if [ -f ~/bashrc/.franklin-templeton.serv ]; then
    if [ -f ~/bashrc/franklin-templeton.rc ]; then
	    . ~/bashrc/franklin-templeton.rc
    fi
fi

if [ -f ~/bashrc/.chimp.serv ]; then
    if [ -f ~/bashrc/chimp.rc ]; then
	    . ~/bashrc/chimp.rc
    fi
fi

if [ -f ~/bashrc/sun.serv ]; then
    if [ -f ~/bashrc/sun.rc ]; then
	    . ~/bashrc/sun.rc
    fi
fi

if [ -f ~/bashrc/mercury.serv ]; then
    if [ -f ~/bashrc/mercury.rc ]; then
	    . ~/bashrc/mercury.rc
    fi
fi

if [ -f ~/bashrc/venus.serv ]; then
    if [ -f ~/bashrc/venus.rc ]; then
	    . ~/bashrc/venus.rc
    fi
fi

if [ -f ~/bashrc/earth.serv ]; then
    if [ -f ~/bashrc/earth.rc ]; then
	    . ~/bashrc/earth.rc
    fi
fi

if [ -f ~/bashrc/mars.serv ]; then
    if [ -f ~/bashrc/mars.rc ]; then
	    . ~/bashrc/mars.rc
    fi
fi

if [ -f ~/bashrc/jupitor.serv ]; then
    if [ -f ~/bashrc/jupitor.rc ]; then
	    . ~/bashrc/jupitor.rc
    fi
fi

if [ -f ~/bashrc/saturn.serv ]; then
    if [ -f ~/bashrc/saturn.rc ]; then
	    . ~/bashrc/saturn.rc
    fi
fi

if [ -f ~/bashrc/neptune.serv ]; then
    if [ -f ~/bashrc/neptune.rc ]; then
	    . ~/bashrc/neptune.rc
    fi
fi

if [ -f ~/bashrc/uranus.serv ]; then
    if [ -f ~/bashrc/uranus.rc ]; then
	    . ~/bashrc/uranus.rc
    fi
fi

if [ -f ~/bashrc/pluto.serv ]; then
    if [ -f ~/bashrc/pluto.rc ]; then
	    . ~/bashrc/pluto.rc
    fi
fi

if [ -f ~/bashrc/sandbox.serv ]; then
    if [ -f ~/bashrc/sandbox.rc ]; then
        . ~/bashrc/sandbox.rc
    fi
elif [ -f ~/bashrc/vamp.serv ]; then
    if [ -f ~/bashrc/vamp.rc ]; then
        . ~/bashrc/vamp.rc
    fi
elif [ -f ~/bashrc/.kit-kat.serv ]; then
    if [ -f ~/bashrc/kit-kat.rc ]; then
        . ~/bashrc/kit-kat.rc
    fi
elif [ -f ~/bashrc/root-dev-direct-connect.serv ]; then
    if [ -f ~/bashrc/root-dev-direct-connect.rc ]; then
        . ~/bashrc/root-dev-direct-connect.rc
    fi
fi


# enable programmable completion features (you don't need to enable
# this, if it's already enabled in /etc/bash.bashrc and /etc/profile
# sources /etc/bash.bashrc).
if ! shopt -oq posix; then
  if [ -f /usr/share/bash-completion/bash_completion ]; then
    . /usr/share/bash-completion/bash_completion
  elif [ -f /etc/bash_completion ]; then
    . /etc/bash_completion
  fi
fi

# _loadProject;

# the following sets the window title
set "localhost"
echo -ne "\e]0;$1\a"

