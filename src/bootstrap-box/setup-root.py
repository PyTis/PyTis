#!/usr/bin/python3

import os,sys
from time import sleep

def toContinue(prefix=''):
  """ Prompt the user to press a key to continue. Should probably use a pager
  most of the time though.
  """
  if sys.platform in ('win32', 'win64'):
    os.system('PAUSE')
    sys.stdout.write("\n")
  elif sys.stdin.isatty():
    import tty
    if prefix.strip():
      sys.stdout.write("\n%s\n" % prefix)
    sys.stdout.write("Press any key to continue . . .\n")
    tty.setraw(sys.stdin.fileno())
    try:
      sys.stdin.read(1)
    finally:
      os.system("stty sane")
    sys.stdout.write("\n")
  return
def _done():
  return toContinue('done.')
toContinue.done=_done

os.system('yum -y install screen')
os.system('yum -y install dos2unix')

os.system('yum -y groupinstall "Development Tools"')
os.system('yum -y install openssl-devel bzip2-devel libffi-devel')
os.system('gcc --version')
os.system('yum -y install wget')
os.system('yum -y install postgresql')

if not os.path.exists('/root/src/'):
	os.makedirs('/root/src')

os.chdir('/root/src/')

if not os.path.exists(os.path.abspath(os.path.join('/root/src/', \
	'multitail-6.2.1-1.el7.rf.x86_64.rpm'))):
	os.system('yum -y install multitail-6.2.1-1.el7.rf.x86_64.rpm')

os.system('wget http://ftp.tu-chemnitz.de/pub/linux/dag/redhat/el7/en/x86_64/rpmforge/RPMS/multitail-6.2.1-1.el7.rf.x86_64.rpm')

if not os.path.exists(os.path.abspath(os.path.join('/root/src/', \
	'Python-3.8.2.tgz'))):
	os.system('wget https://www.python.org/ftp/python/3.8.2/Python-3.8.2.tgz')

if not os.path.exists(os.path.abspath('/root/src/Python-3.8.2/')) \
	and not os.path.isdir(os.path.abspath('/root/src/Python-3.8.2/')):
	os.system('tar xvf Python-3.8.2.tgz')

os.chdir('/root/src/Python-3.8.2/')

os.system('./configure --enable-optimizations')
os.system('make altinstall')
os.system('python3.8 --version;')
sleep(2)
os.system('pip3.8 --version')
sleep(2)

os.chdir('/root/src/')

## ######################################################
#os.unlink('/bin/python')
#os.system('ln -s /usr/local/bin/python3.8 /bin/python')
# WE CANT DO THIS ^^^^ it breaks yum
## ######################################################
os.system('pip3.8 install --upgrade pip')

os.system('pip install six')
os.system('pip2 install six')
os.system('pip2.7 install six')
os.system('pip3 install six')
os.system('pip3.6 install six')
os.system('pip3.8 install six')

os.system('pip3.8 install pyflakes')
os.system('pip3.8 install vulture')

## below, copy into requirements.txt
os.system('pip3.8 install psycopg2-binary')
os.system('pip3.8 install boto3')
os.system('pip3.8 install requests')

print('about to install pytis-tools python library')
os.system('pip3.6 install --upgrade pytis')
os.system('pip3.8 install --upgrade pytis')

## 
sleep(1)
## 
toContinue.done()



