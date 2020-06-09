#!/usr/bin/python3
import sys
#import postgresql.driver as pg_driver

import errno
import os

class oDict:
    """An ordered dictionary. ordereddict = oDict(indict, order)"""
    __doc__ = """ordereddict = oDict({'a' : 1, 'b' : 2}, True)
The dictionary can be initialised with an optional dictionary passed in as the first argument,
You can also pass in an order parameter which chooses the sort method.
order=True (default) means all ordered methods use the normal sort function.
order=False  means all ordered methods use the reverse sort function.
order=None means no sort function.

keys, items, iter and pop methods are ordered - based on the key.
The ordering is implemented in the keys() function.
The iterators are returned using the custom iterator dIter (which will work in three different ways)."""

    def __init__(self, indict={}, order=True):
        self._thedict = {}
        self._thedict.update(indict)
        self._order = order

    def __setitem__(self, item, value):
        """Setting a keyword"""
        self._thedict[item] = value

    def __getitem__(self, item):
        """Fetching a value."""
        return  self._thedict[item]

    def __delitem__(self, item):
        """Deleting a keyword"""
        del self._thedict[item]

    def pop(self, item=[], default=None):
        """Emulates the pop method.
        If item is not supplied it pops the first value in the dictionary.
        This is different from the normal dict pop method."""
        if item != []:
            return self._thedict.pop(item, default)
        else:
            try:
                return self._thedict.pop(self.keys()[0])
            except IndexError:
                raise KeyError(': \'pop(): dictionary is empty\'')

    def popitem(self):
        """Emulates the popitem method - pops the first one in the list based on the chosen sort method."""
        try:
            theitem = self.keys()[0]
        except IndexError:
            raise KeyError(': \'popitem(): dictionary is empty\'')
        return (theitem, self._thedict.pop(theitem))

    def has_key(self, item):
        """Does the dictionary have this key."""
        return self._thedict.has_key(item)           # does the key exist

    def __contains__(self, item):
        """Does the dictionary have this key."""
        return self._thedict.has_key(item)           # does the key exist

    def setdefault(self, item, default=None):
        """Fetch an item if it exists, otherwise set the item to default and return default."""
        return self._thedict.setdefault(item, default)

    def get(self, item, default=None):
        """Fetch the item if it exists, otherwise return default."""
        return self._thedict.get(item, default)

    def update(self, indict):
        """Update the current oDdict with the dictionary supplied."""
        self._thedict.update(indict)

    def copy(self):
        """Create a new oDict object that is a copy of this one."""
        return oDict(self._thedict)

    def dict(self):
        """Create a dictionary version of this oDict."""
        return dict.copy(self._thedict)

    def clear(self):
        """Clear oDict."""
        self._thedict.clear()

    def __repr__(self):
        """An oDict version of __repr__ """
        return 'oDict(' + self._thedict.__repr__() + ')'

    def keys(self):
        """Return an ordered list of the keys of this oDict."""
        thelist = self._thedict.keys()
        if self._order == True:
            thelist.sort()
        elif self._order == False:
            thelist.sort()
            thelist.reverse()
        return thelist

    def items(self):
        """Like keys() but returns a list of (key, value)"""
        return [(key, self._thedict[key]) for key in self.keys()]

    def values(self):
        """Like keys() but returns an ordered list of values (ordered by key)"""
        return [self._thedict[key] for key in self.keys()]

    def fromkeys(cls, *args):
        """Return a new oDict initialised from the values supplied.
        If sys.version_info > 2.2 this becomes a classmethod."""
        return oDict(*args)

    if (sys.version_info[0] + sys.version_info[1]/10.0) >= 2.2:
        fromkeys = classmethod(fromkeys)

    def __len__(self):
        return len(self._thedict)

    def __cmp__(self, other):
        if hasattr(other, '_thedict'):
            other = other._thedict
        return cmp(self._thedict, other)

    def __eq__(self, other):
        if hasattr(other, '_thedict'):
            other = other._thedict
        return self._thedict.__eq__(other)

    def __ne__(self, other):
        if hasattr(other, '_thedict'):
            other = other._thedict
        return self._thedict.__ne__(other)

    def __gt__(self, other):
        if hasattr(other, '_thedict'):
            other = other._thedict
        return self._thedict.__gt__(other)

    def __ge__(self, other):
        if hasattr(other, '_thedict'):
            other = other._thedict
        return self._thedict.__ge__(other)

    def __lt__(self, other):
        if hasattr(other, '_thedict'):
            other = other._thedict
        return self._thedict.__lt__(other)

    def __le__(self, other):
        if hasattr(other, '_thedict'):
            other = other._thedict
        return self._thedict.__le__(other)

    def __hash__(self):
        """This just raises a TypeError."""
        self._thedict.__hash__()

    def __iter__(self):
        """Return an ordered iterator for the oDict."""
        return dIter(self)

    def iteritems(self):
        """Return an ordered iterator over the the oDict - returning (key, value) tuples."""
        return dIter(self, -1)

    def iterkeys(self):
        """Return an ordered iterator over the keys the oDict."""
        return dIter(self)

    def itervalues(self):
        """Return an ordered iterator over the the values of the oDict - ordered by key."""
        return dIter(self, 1)

    def __str__(self):
        """An oDict version of __str__ """
        return 'oDict(' + self._thedict.__str__() + ')'


from pprint import pprint

errkeys = list(errno.errorcode.keys())
errkeys.sort()
for k in errkeys:
	print("%s - %s" % (k, os.strerror(k)))

sys.exit()

"""
db = pg_driver.connect(
	user = 'admin',
	password = '7fadf353697e41b7f8552ccd13f4a9153d13753716a7f2ce46778fe70c3bb6d1b97980ede797d245646a14473126e6d8',
	host = '127.0.0.1',
	port = 5432,
	database = 'kas_dev'
	)
"""

C = pg_driver.default.ip4(
	user = 'admin',
	password = '7fadf353697e41b7f8552ccd13f4a9153d13753716a7f2ce46778fe70c3bb6d1b97980ede797d245646a14473126e6d8',
	host = '127.0.0.1',
	port = 5432,
	database = 'kas_dev'
	)
db = C()
db.connect()


#db.execute('DECLARE the_cursor_id CURSOR WITH HOLD FOR SELECT login FROM person WHERE id=20909;')
db.execute('DECLARE the_cursor_id CURSOR WITH HOLD FOR SELECT 1::text;')
cursor = db.cursor_from_id('the_cursor_id')
assert (cursor.read()[0][0] == '1')

#print (cursor.read())
cursor.close()

sys.exit(0)


rows = db.prepare('SELECT id, environment_name, aws_account_number FROM environment WHERE (deleted IS NOT NULL AND deleted=0) OR deleted IS NULL;')
for row in rows:
	if(row[0] == '' or row[0] is None):
		print ('bad_data - id: %s, name: %s' % (row[0], row[1]))
	else:
		pass
		# print ('row: ', row[2])



sys.exit(0)
