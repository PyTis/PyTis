#!/bin/sh

curent_branch=$(git branch | grep '*' | cut -c3-); sleep 1; git fetch; sleep 1;
git pull; sleep 1; git checkout master; sleep 1; git fetch; sleep 1; git pull;
sleep 1; git checkout $current_branch; sleep 1; git fetch; sleep 1; git pull;
sleep 1; git merge master; echo Done.; echo ; echo bye!

