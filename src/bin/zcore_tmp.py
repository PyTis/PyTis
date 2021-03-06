#!/usr/bin/env python
""""""

import cStringIO
import pydoc
import optparse
import os
import shutil
import sys
import logging; log=logging.getLogger('zcore')

__curdir__ = os.path.abspath(os.path.dirname(__file__))
__author__ = 'Josh Lee'
__created__ = '11:31pm 10 Oct, 2009'
__copyright__ = 'PyTis.com'
__version__ = '1.0'

__configdir__ = '/home/ut3hax/public_html'

def version():
    print  __version__

class QuitNow(Exception):
    pass

class MyParser(optparse.OptionParser):
    def print_help(self, errors=None):
        buf = cStringIO.StringIO()
        sys.stdout = buf
        print '='*80

        optparse.OptionParser.print_help(self)
        print """
examples:    
 """
        if errors:
            print errors 

        sys.stdout = sys.__stdout__
        pager = pydoc.getpager()
        pager(buf.getvalue())

def license():
    """The contents of this file are subject to the PyTis Public License Version
1.0 (the "License"); you may not use this file except in compliance with
the License. You may obtain a copy of the License at

    http://www.PyTis.com/License/
    
    Copyright \xa9  2009 Josh Lee 

Software distributed under the License is distributed on an "AS IS" basis,
WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License
for the specific language governing rights and limitations under the
License.
"""
    print license.__doc__

def baseDir(opts):
    """ Return the basedir of the zcore_php installation
    """
    if opts.zcore:
        basedir = os.path.abspath(opts.zcore)
    else:
        basedir = os.path.abspath(__configdir__)
    if not testZCoreDir(basedir):
        print "ZCore Installation is missing or invalid"
        sys.exit(1)
    return basedir

def skelDir(opts):
    """ Returns the absolute path of the skeleton directory.
    """
    sd = os.path.abspath(os.path.join(baseDir(opts),'modules','skel'))
    if not dirTest(sd):
        print "ZCore Installation is missing skeleton module"
        print "Missing Folder: ", sd
        sys.exit(1)
    return sd

def modName(opts):
    pass

def fileName(opts):
    """ Returns the proper name of a file to create, case sensative, it will
        properly use the ZCore coding standard.
    """
    if opts.Class:
        return '%s.php' % opts.Class.lower().capitalize()
    if opts.Form:
        return '%s.php' % opts.Form.lower().capitalize()
    else:
        raise AttributeError, "UnKnown filname request\n%s"  % str(dir(opts))

def modDir(opts):
    """ this will return the absolute path of the current ZCore Installation's
        modules directory
    """
    return os.path.abspath(os.path.join(baseDir(opts),'modules'))

def outPath(opts):
    """ This will return the path to output the file or directory being created.
    """
    if opts.mod is not None:
        return os.path.abspath(os.path.join(modDir(opts), str(opts.mod).lower().strip()))
    else:
        return os.path.abspath(os.curdir)

def classPath(opts):
    """ The path for a class abotu to be created.
    """
    if opts.mod is None:
        return os.path.abspath(os.curdir)
    return os.path.abspath(os.path.join(outPath(opts), 'classes'))

def foo():
    if not dirTest(path):
        print "Outpath: '%s' does not exist, would you like to create it now?" % path
    pass

def reset(opts):
    pass

def cp(opts):
    pass

def newForm(opts):
    pass

def newClass(opts):
    """ this will create a new class based on our skeleton, then get the name
        and variables set up.
    """
    from_path = os.path.abspath(os.path.join(skelDir(opts),'classes','Skel.php'))
    to_path = os.path.abspath(os.path.join(classPath(opts), fileName(opts)))
    
    shutil.copy(from_path, to_path)
    rhandle = open(to_path, 'r')
    lines = rhandle.readlines(-1)
    rhandle.close()
    new_lines = []
    for line in lines:
        new_lines.append(line.replace('Skel',opts.Class.strip().lower().capitalize()))
    whandle = open(to_path, 'w')
    whandle.writelines(new_lines)
    whandle.close()


    if opts.extra:
        table_name = None
        table_id = None
        required_fields = []
        searchable_fields = []
        unique_fields = []
        unquote_these = []

        time_stamp_field = None
        entity_name = None
        auto_format = False

        has_folder = False
        doc_base = None
        my_doc_dir = None

        table_name = raw_input("%s DB table name?" % opts.Class)
        if table_name:
            table_id = raw_input("%s primary id field: " % table_name)
        else:
            table_id = raw_input("%s DB table primary id feild: " % opts.Class)
        
        if raw_input("Setup required fields? [y/N]") in ['y','Y']:
            field = raw_input("Field name (leave blank to finish): ")
            while field.strip():
                required_fields.append(field)
                field = raw_input("Field name (leave blank to finish): ")

        if raw_input("Setup searchable fields? [y/N]") in ['y','Y']:
            field = raw_input("Field name (leave blank to finish): ")
            while field.strip():
                searchable_fields.append(field)
                field = raw_input("Field name (leave blank to finish): ")

        time_stamp_field = raw_input("Time Stamp Field: ")
        auto_format = raw_input("Auto Format generic fields? [y/N]")
    
    print 'searchable_fields', searchable_fields
    print 'required_fields', required_fields
    print 'table_name', table_name
    print 'table_id', table_id

def fixWidth(st):
    buf = list(st.split())
    lines = []
    cur = ''
    for word in buf:
        if len('%s %s' % (cur, word)) >= 79:
            lines.append(cur)
            cur = ''
        cur = '%s %s' % (cur,word)
    if cur:
        lines.append(cur)
    return "\n".join(lines)

def getInputYN(question, helptext='No help for this command'):
          
    res = raw_input("%s [y/N]>>> " % question)
    if not res.strip():
        print "Nothing entered, please try again."
        return getInputYN(question, helptext)
    if res.strip().lower() == 'y':
        return True
    if res.strip().lower() == 'n':
        return False
    if res.strip().lower() in ['h','?']:
        print "\nHELP (q to quit):-- \n%s\n" % fixWidth(helptext)
        return getInputYN(question, helptext)
    if res.strip().lower() == 'q':
        raise QuitNow, question
    else:
        return res

def reNameModule(path, old, new):
    lold = old.lower()
    uold = old.lower().capitalize()
    lnew = new.lower()
    unew = new.lower().capitalize()
    lowerCMDa = "findrep %s %s -f" % (lold, lnew)
    lowerCMDb = "findrep %s %s -fn" % (lold, lnew)
    os.system(lowerCMDa)
    os.system(lowerCMDb)

    upperCMDa = "findrep %s %s -f" % (uold, unew)
    upperCMDb = "findrep %s %s -fn" % (uold, unew)
    os.system(upperCMDa)
    os.system(upperCMDb)


def newModule(opts):
    name = opts.module.strip().lower()
    skel = skelDir(opts)
    structure_test = False
    moddir = os.path.abspath(os.path.join(modDir(opts), name))
    classdir = os.path.abspath(os.path.join(moddir,'classes'))

    try: 
        if dirTest(moddir):
            print "Module '%s' already exists. (%s)" % (name,moddir)
            
            if getInputYN('Run structure tests?', 
                        'This tests to see if any files or folders are missing, '
                        'based on the ZCore module structure standard.'):
                structure_test = True
        else:
            print "Creating Module: %s" % name
            shutil.copytree(skel, moddir)
            reNameModule(moddir, 'skel', name)
            
        if structure_test and not dirTest(classdir):
            if getInputYN('Classes folder is missing, create it now?'):
                os.mkdir(classdir)

        opts.Class = name
        opts.mod = name
        class_fpath = os.path.abspath(os.path.join(classPath(opts), fileName(opts)))
        print 'class_fpath', class_fpath
        print 'structure_test', structure_test
        if structure_test and not os.path.exists(class_fpath):

            print "Class folder found, but no class file defined for new module."
            if getInputYN('Would you like to create the %s class now?' % name):
                newClass(opts)

        return True
    except QuitNow, e:
        return False

def getConfig(opts):
    print
    oldpath = os.path.abspath(__configdir__)
    if dirTest(__configdir__):
        print 'ZCORE installation DIR was already set to:', oldpath
        if raw_input('Reset default ZCORE DIR? [y/N]').lower().strip() == 'n':
            return False
    
    newpath = os.path.abspath(os.curdir)
    print "Path to ZCORE base directory (leave blank to use current path) q to quit "
    configdir = raw_input('>>>')
    if not configdir.strip():
        configdir = newpath

    if configdir.lower() == 'q':
        return False

    if not testZCoreDir(configdir):
        print "\nInvalid ZCore Installation."
        print "Please try again."
        return getConfig(opts)
    else:
        return setConfig(configdir)

def setConfig(d):
    d = os.path.abspath(d)
    mpath = os.path.abspath(sys.argv[0])
    handle = open(mpath, 'r')
    lines = handle.readlines(-1)
    handle.close()
    nfile_lines = []
    for line in lines:
        if line.startswith('__configdir__'):
            line = "__configdir__ = '%s'\n" % d
        nfile_lines.append(line)

    handle = open(mpath,'w')
    handle.writelines(nfile_lines)
    handle.close()
    return True

def dirTest(d):
    # ensure it is a valid real existing directory 
    if not d.strip():
        return False

    d = os.path.abspath(d)

    if not os.path.exists(d) or \
        not os.path.isdir(d):
        return False

    return True

def testZCoreDir(d):
    dirs = ['lib', 'modules','admin','res','skins']
    files = ['index.php','pass.php','config.ini','config.inc.php']

    # Basic tests
    if not dirTest(d):
        return False

    d = os.path.abspath(d)

    # direcotry path tests
    for di in dirs:
        test = os.path.join(d,di)
        if not os.path.exists(test) or not os.path.isdir(test):
            return False
    # file path tests
    for fi in files:
        test = os.path.join(d,fi)
        if not os.path.exists(test) or not os.path.isfile(test):
            return False
    # all tests passed
    return True

def config(opts):
    print 'Setting up ZCORE quick script generator.'
    print '='*80
    return getConfig(opts)

def testMod(opts):
    print "No module specified, this means all output will be written to your"
    print "current path."
    print "Continue without a specifing a module?"
    res = raw_input("[y/N/[MODULE NAME]")
    if not res.strip():
        print "Invalid choice."
        return testMod(opts)
    if res.strip().lower() == 'n':
        return False
    if res.strip().lower() == 'y':
        return True
    opts.mod = res.strip()
    return True

def main():
    """usage: zcore 
================================================================================
    """
    parser = MyParser()
    parser.set_description(None)
    parser.set_usage(main.__doc__)
    parser.formatter.format_description = lambda s:s

    # -------------------------------------------------------------------------
    # generics
    gene = optparse.OptionGroup(parser, "Helpers")

    '''
    x = optparse.Option("-D", "--debug", action="store_true", default=False,
                        help="Enable debugging")
    print 'X: ', dir(x)
    print
    print 'x: ', x
    return
    '''
    gene.add_option("-D", "--debug", action="store_true", default=False, 
                    help="Enable debugging")

    gene.add_option("-l", "--license", action="store_true", default=False,
                    help="Display license")

    gene.add_option("-v", "--version", action="store_true", default=False, 
                    help="Display version")
    parser.add_option_group(gene)
    # -------------------------------------------------------------------------
    # file creationg
    news = optparse.OptionGroup(parser, "Creation",
                                 "\t\tOptions used to create new modules or module parts.\n")
    news.add_option("-c", "--Class", action="store", metavar='[NAME]',
                    default=False, help="Create a new Class")

    news.add_option("-f", "--Form", action="store",metavar="[NAME]",
                    default=False, help="Create a new new Form")


    news.add_option("-m", "--module", action="store",metavar="[NAME]",
                    default=None, help="Create a new Module")

    news.add_option("-z", "--zcore", action="store", default=None,
                    metavar="[PATH]",
                    help="Specify a ZCore installation to use, without " \
                         "over-riding the default")
    parser.add_option_group(news)
    # -------------------------------------------------------------------------
    # variable setting
    vars = optparse.OptionGroup(parser, "Settings")

    vars.add_option("-M", "--mod", action="store", default=None,
                    metavar="[MODULE]",
                    help="Specify a module else it will use curent path")

    vars.add_option("-x", "--extra", action="store_true", default=False,
                    help="Process additional setup questions, resulting "
                         "in a more complete output file.")

    # installation / setup
    vars.add_option("-s", "--set", action="store", default=None, metavar="[PATH]",
                    help="Specify a ZCore installation to use, and save " \
                         "for future use")
    parser.add_option_group(vars)
    # -------------------------------------------------------------------------


    (opts, args) = parser.parse_args()

    # Logging Configuration
    log.setLevel(0) 
    formatter = '%(levelname)-8s %(message)s'

    if opts.debug:
        logging.basicConfig(filename='/%s/zcore.log' % __curdir__,
                            level=logging.DEBUG, format=formatter)
    else:
        logging.basicConfig(filename='/%s/zcore.log' % __curdir__,
                            level=logging.INFO, format=formatter)

    if opts.version:
        return version()

    if opts.license:
        return license()

    try:
        if opts.set is not None:
            if not testZCoreDir(opts.set):
                print "\nInvalid ZCore Installation."
                print "Please try again."
                return False
            if setConfig(opts.set):
                print "New default path successfully set."
                print "bye!"
                return True 
            else:
                print "Invalid ZCORE path"
                print "\nbye!"
                return False

        if not testZCoreDir(__configdir__):
            if raw_input("No default ZCore installation specified, would you like to set one now?") in ['y','Y']:
                if config(opts):
                    print "this tool needs restarted (quit now, use again)"
                    print "bye!"
                    return True
            return False
        
        if opts.zcore and not testZCoreDir(opts.zcore):
            print "Invalid ZCore Installation"
            print "bye!"
            return False

        if not opts.mod and (opts.Class or opts.Form):
            if not testMod(opts):
                print "bye!"
                return False
            
        if opts.Class:
            newClass(opts)

        if opts.Form:
            newForm(opts)
        
        if opts.module:
            newModule(opts)

        return

    except KeyboardInterrupt, e:
        print "\nbye!"
        return
    else:
        parser.print_help()
        return

if __name__ == '__main__':
    if not main():
        sys.exit(1)
    else:
        sys.exit(0)
