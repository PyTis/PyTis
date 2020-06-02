#!/bin/bash

echo 'python2 setup.py clean..'
python2 setup.py clean

echo "/bin/rm -f `find . -iname '*.pyc'` ..."
/bin/rm -f `find . -iname '*.pyc'`


echo "/bin/rm -rf src/build/* ..."
/bin/rm -rf src/build/*

#echo "/bin/rm -rf src/dist/* ..."
/bin/rm -rf src/dist/*

echo "python2 setup.py build ..."
python2 setup.py build

echo "python2 setup.py sdist bdist_wheel ..."
python2 setup.py sdist bdist_wheel

#echo "python2 -m twine upload --repository pypi src/dist/* ..."
#python2 -m twine upload --repository pypi src/dist/*



