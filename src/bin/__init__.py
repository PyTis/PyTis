import sys

python_version = float("%s.%s"%(sys.version_info.major,sys.version_info.minor))


if python_version >= 3.0:
  import pytis3 as PyTis
else:
  import pytis as PyTis

__all__ = ['python_version', 'PyTis']


