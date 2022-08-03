#!/usr/bin/env python
from pydoc import locate, HTMLDoc, describe, pathdirs, ErrorDuringImport
from mod_python import apache
import sys

def handler(req):
    req.content_type = "text/html"
    html = HTMLDoc()
    path = req.uri
    if path[-5:] == '.html':
        path = path[:-5]
    path = path.split('/')[-1]
    if path and path != '.':
        # Return documentation for an object
        try:
            obj = locate(path, forceload=1)
        except ErrorDuringImport, value:
            req.write(html.page(path, html.escape(str(value))))
            return apache.OK
        if obj:
            req.write(html.page(describe(obj), html.document(obj, path)))
            return apache.OK
        else:
            req.write(html.page(path,
                'no Python documentation found for %s' % repr(path)))
            return apache.OK
    else:
        heading = html.heading(
            '<big><big><strong>Python: Index of Modules</strong></big></big>',
            '#ffffff', '#7799ee')
        def bltinlink(name):
            return '<a href="%s.html">%s</a>' % (name, name)
        names = filter(lambda x: x != '__main__',
                       sys.builtin_module_names)
        contents = html.multicolumn(names, bltinlink)
        indices = ['<p>' + html.bigsection(
            'Built-in Modules', '#ffffff', '#ee77aa', contents)]
        seen = {}
        for dir in pathdirs():
            indices.append(html.index(dir, seen))
        contents = heading + ' '.join(indices) + '''<p align=right>
<font color="#909090" face="helvetica, arial"><strong>
pydoc</strong> by Ka-Ping Yee &lt;ping@lfw.org&gt;</font>'''
        req.write(html.page('Index of Modules', contents))
        return apache.OK

