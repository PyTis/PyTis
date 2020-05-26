#!/usr/bin/env python
import codecs
import os.path
import re
import sys

__curdir__ = os.path.abspath(os.path.dirname(__file__))
__created__ = '01:21am 01 Jan, 2014'
__version__ = '1.0'
__author__ = 'Josh Lee'
__copyright__ = 'PyTis, LLC.'


python_version = float("%s.%s"%(sys.version_info.major,sys.version_info.minor))

def import_by_path(fpath, module_name):
	#die(os.path.abspath(os.path.dirname((fpath))))
	global __curdir__
	fpath = os.path.abspath(os.path.join(__curdir__,fpath))
	fdir = os.path.dirname(fpath)
	os.chdir(os.path.abspath((fdir)))

	if python_version >= 3.5:
		import importlib.util
		spec = importlib.util.spec_from_file_location(module_name, fpath)
		mod = importlib.util.module_from_spec(spec)
		spec.loader.exec_module(mod)
		os.chdir(__curdir__)
		return mod
	elif python_version >= 3.3:
		from importlib.machinery import SourceFileLoader
		mod = SourceFileLoader(module_name, fpath).load_module()
		os.chdir(__curdir__)
		return mod
	else:
		import imp
		mod = imp.load_source(module_name, fpath)
		os.chdir(__curdir__)
		return mod


from setuptools import setup, find_packages

def die(string=None):
	global log
	try:
		if log and string:
			log.fatal(string)

	except NameError:
		if string:
			print("output: '%s'" % string)
	else:
		if not log and string:
			print("output: '%s'" % string)

	sys.exit()
DIE=Die=die





def read(*parts):
	fpath = os.path.abspath(os.path.join(__curdir__, *parts))
	handle = codecs.open(fpath, 'r')
	ret_val = handle.read()
	handle.close()
	del handle
	return ret_val
	


def load_pytis():
	pytis_path = 'src/pytis/pytis.py'
	sys.path.append(os.path.abspath(os.path.join(__curdir__,'src/')))
	sys.path.append(os.path.abspath(os.path.join(__curdir__,'src/pytis/')))
	sys.path.append(os.path.abspath(os.path.join(__curdir__,'src/pytis/pylib')))
	sys.path.append(os.path.abspath(os.path.join(__curdir__,'src/pytis/pylib3')))
	PyTis=import_by_path(pytis_path, 'pytis')
	return PyTis


	#raise RuntimeError("Unable to find version string.")


install_requires = [
#    'botocore==1.16.12',
    'docutils>=0.10,<0.16',
#    'rsa>=3.1.2,<=3.5.0',
#    's3transfer>=0.3.0,<0.4.0',
]

file_handle = open('README.md','r')
readme_contents = file_handle.read(-1)
file_handle.close()

#file_handle = open('LICENSE.txt','r')
#license_contents = file_handle.read(-1)
#file_handle.close()

'''
if sys.version_info[:2] == (3, 4):
    install_requires.append('PyYAML>=3.10,<5.3')
    install_requires.append('colorama>=0.2.5,<0.4.2')
else:
    install_requires.append('PyYAML>=3.10,<5.4')
    install_requires.append('colorama>=0.2.5,<0.4.4')
'''

PyTis = load_pytis()

os.chdir(os.path.abspath(os.path.join(__curdir__,'src')))
setup_options = dict(
    name='pytis',
    version=PyTis.__version__,

    author=__author__,
		author_email='pytis@PyTis.com',

		description='pytis-toolkit',
		url='https://github.com/PyTis/PyTis',

		long_description=readme_contents,
		long_description_content_type="text/markdown",

    packages=find_packages( include=[
										'pytis*',
			],
		exclude=['src/.zombie_hunter_files',
																		'src/etc*',
																		'src/log*']),
    package_data={
			'pytis' : [ 'pytis*' ],
		},
		data_files = [
			('', [os.path.abspath(os.path.join(__curdir__,'LICENSE.txt')),
						os.path.abspath(os.path.join(__curdir__,'README.md')),
						os.path.abspath(os.path.join(__curdir__,'PyTis_Logo.jpg'))
					 ]
			),
		],

		#license_file=os.path.abspath(os.path.join(__curdir__,'LICENSE')),

    scripts=[
			os.path.abspath(os.path.join(__curdir__, 'src/bin/copyright')),
			os.path.abspath(os.path.join(__curdir__, 'src/pytis/copyright.py')),
			os.path.abspath(os.path.join(__curdir__, 'src/bin/bulkcopy')),
			os.path.abspath(os.path.join(__curdir__, 'src/bin/bulkmove'))
		],
    install_requires=install_requires,
    extras_require={},
    license="PyTis LICENSE 3.0",
		#license=license_contents,
    classifiers=[
					'Development Status :: 5 - Production/Stable',
					'Intended Audience :: Developers',
					'Intended Audience :: System Administrators',
					'Natural Language :: English',
					'Programming Language :: Python :: 3',
#					'License :: OSI Approved :: PyTis License',
					'License :: Other/Proprietary License',
					'Operating System :: OS Independent',
					'Programming Language :: Python',
					'Programming Language :: Python :: 2',
					'Programming Language :: Python :: 2.7',
					'Programming Language :: Python :: 3',
					'Programming Language :: Python :: 3.4',
					'Programming Language :: Python :: 3.5',
					'Programming Language :: Python :: 3.6',
					'Programming Language :: Python :: 3.7',
					'Programming Language :: Python :: 3.8',
    ],
)


if 'py2exe' in sys.argv:
    # This will actually give us a py2exe command.
    import py2exe
    # And we have some py2exe specific options.
    setup_options['options'] = {
        'py2exe': {
            'optimize': 0,
            'skip_archive': True,
            'dll_excludes': ['crypt32.dll'],
            'packages': ['docutils', 'urllib', 'httplib', 'HTMLParser',
                         'awscli', 'ConfigParser', 'xml.etree', 'pipes'],
        }
    }
    setup_options['console'] = ['bin/aws']


setup(**setup_options)

