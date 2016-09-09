"""
Generic sequence manipulation routines.

These procedures perform transformations and other operations on sequences.
"""
import fnmatch

def flatten(a):
    """Flatten a list."""
    def bounce(thing):
        """Bounce the 'thing' until it stops being a callable."""
        while callable(thing):
            thing = thing()
        return thing
        
    def flatten_k(a, k):
        """CPS/trampolined version of the flatten function.  The original
        function, before the CPS transform, looked like this:
    
        def flatten(a):
            if not isinstance(a,(tuple,list)): return [a]
            if len(a)==0: return []
            return flatten(a[0])+flatten(a[1:])
    
        The following code is not meant for human consumption.
        """
        
        ## We removed to ONLY check for lists and not tuples
        if not isinstance(a,list):
            return lambda: k([a])
        if len(a)==0:
            return lambda: k([])
        def k1(v1):
            def k2(v2):
                return lambda: k(v1 + v2)
            return lambda: flatten_k(a[1:], k2)
        return lambda: flatten_k(a[0], k1)
    
    return bounce(flatten_k(a, lambda x: x))
    
def assoc_list(l1, l2):
    """ assoc_list(list l1, list l2) -> dict
    
    Creates a dictionary where each key is an item in l1 and the value is the
    element in l2 that has the same position.
    Assigns None to values in the return dict where there is no corresponding
    index found in l2.
    """
    d = {}
    for i in range(len(l1)):
        try:
            d[l1[i]] = l2[i]
        except IndexError:
            d[l1[i]] = None

def xor_seq(seq):
    """ xor_seq(list seq) -> bool

    Performs and exclusive or on each item in the sequence. Only returns True
    iff one value in the sequence is True.
    """
    return reduce(lambda x, y: x ^ y, seq)
    
def pack(*seqs):
	""" pack together each sequence in the arg list into one list """
	ret = []
	max = 0
	for s in seqs:
		if len(s) > max:
			max = len(s)
	for i in range(max):
		t = []
		for j in range(len(seqs)):
			try:
				t.append(seqs[j][i])
			except IndexError:
				t.append(None)
		ret.append(t)
	return ret

def grep(lst, pattern):
    """ grep(lst, pattern) -> list

    Filters elements from lst like the grep command
    """
    if pattern.find('*') != -1:
        return fnmatch.filter(lst, pattern)
    else:
        return filter(lambda s: s.find(pattern) != -1, lst)

def unique(lst):
    """ This should probably not be used because of py2.3's sets. """
    t = {}
    for x in lst:
        t[x] = 1
    return t.keys()

def unique_ordered(vals):
    new = []
    for val in vals:
        if val not in new:
            new.append(val)
    return new
