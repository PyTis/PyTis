import logging as log
import cStringIO
import re

import util as UTL

COMMENT = re.compile('^\s*#')
BLOCK = re.compile('^\s*BEGIN (.*?)$')
HEAD = re.compile('^(\w+)\s*$')
DIR = re.compile('^%(.+?)\s*$')
IDENT = re.compile('^\s+(.*?)\s*$')

def parse_def(in_file, directives={}, fields=[], blocks=[]):
    """ Parsse a cas relation definition file.
    """
    cur = None

    state = 'OUTER'
    multi_name = None
    multi_val = None
    m_line_no = None

    for line_no, line in enumerate(in_file):
        line_no = line_no + 1
        if state == 'OUTER':
            line = line.rstrip()
            if not line or COMMENT.match(line):
                continue
            
            match = DIR.match(line)
            if match:
                direct = match.groups()[0]
                if ':' not in direct:
                    raise ValueError, 'No : found in directive on line ' \
                        '%s, %s' % (line_no, line)
                name, value = direct.split(':', 1)
                directives[name.strip()] = value.strip()
                continue

            match = BLOCK.match(line)
            if match:
                block_lines = []
                cur = {'block' : match.groups()[0],
                       'lines' : block_lines}
                blocks.append(cur)
                state = 'BLOCK'
                continue

            match = HEAD.match(line)
            if match:
                cur = {'_field' : match.groups()[0]}
                fields.append(cur)
                continue

            match = IDENT.match(line)
            if match:
                if cur is None:
                    raise ValueError, 'Value found with no block on line ' \
                        '%s, %s' % (line_no, line)
                block = match.groups()[0]
                if ':' not in block:
                    raise ValueError, 'No : found in blockive on line %s, %s' \
                        % (line_no, line)
                name, value = block.split(':', 1)

                if name in cur:
                    log.warn('Duplicate name on line %s, %s', line_no, name)
                if value.strip() == '|':
                    state = 'MULTILINE'
                    multi_name = name
                    multi_val = cStringIO.StringIO()
                    m_line_no = line_no + 1
                else:
                    cur[name] = UTL.unrepr(value.strip())
                continue

        elif state == 'MULTILINE':
            if line.rstrip() == '.':
                cur[multi_name] = UTL.unrepr(multi_val.getvalue())
                multi_name = None
                multi_val = None
                state = 'OUTER'
            else:
                multi_val.write(line)
            continue

        elif state == 'BLOCK':
            if line.rstrip() ==  'END':
                state = 'OUTER'
                continue
            else:
                block_lines.append(tuple([y.strip() \
                    for y in [x for x in line.strip().split('|')]]))
                continue

        log.warn('Skipping line %s, %s', line_no, line)

    if state == 'MULTILINE':
        raise ValueError, 'Reached end of file without period ' \
            'in Multi-line block started at %s.' % m_line_no
    return directives, fields, blocks
