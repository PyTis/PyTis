#!/bin/bash

echo 'python3 setup.py clean..'
python3 setup.py clean

echo "/bin/rm -f `find . -iname '*.pyc'` ..."
/bin/rm -f `find . -iname '*.pyc'`


#echo "/bin/rm -rf src/build/* ..."
#/bin/rm -rf src/build/*

#echo "/bin/rm -rf src/dist/* ..."
#/bin/rm -rf src/dist/*

echo "python3 setup.py build ..."
python3 setup.py build

echo "python3 setup.py sdist bdist_wheel ..."
python3 setup.py sdist bdist_wheel

echo "python3 -m twine upload --repository pypi src/dist/* ..."
python3 -m twine upload --repository pypi src/dist/*



