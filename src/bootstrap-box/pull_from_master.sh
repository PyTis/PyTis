#!/bin/sh
current_branch=$(git branch | grep '*' | cut -c3-)
echo "CURRENT BRANCH: $current_branch";
echo '';
git fetch; sleep 1;
git pull; sleep 1;
echo '';
git checkout master; sleep 1;
git fetch; sleep 1;
git pull; sleep 1;
git checkout "$current_branch"
echo '';
sleep 1; 
git fetch; sleep 1;
git pull; sleep 1;
git merge master; sleep 1;
git push; sleep 1;
echo Done.; echo ; echo bye!Â 
