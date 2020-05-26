from UserDict import UserDict

__all__ = ['cldict', 'default_dict', 'default_set_dict', 'odict']

class default_dict(dict):
    def __init__(self, other={}, default=None):
        dict.__init__(self, other)
        self.default = default
    
    def __getitem__(self, key):
        try:
            return dict.__getitem__(self, key)
        except KeyError:
            return self.default

class default_set_dict(dict):
    def __init__(self, other={}, default=None):
        dict.__init__(self, other)
        self.default = default
    
    def __getitem__(self, key):
        try:
            v = dict.__getitem__(self, key)
        except KeyError:
            self[key] = self.default
            v = dict.__getitem__(self, key)
        return v

class cldict(object):
    """A class dictionary easily lets a class masquerade as a dictionary.
    This is very useful for lazy evaluation of values.
    You can pass in another class_dict into the constructor and
    the dictionary will be lazily merged with its parent, thereby
    creating a lazy dictionary chain.
    """
    def __init__(self, data={}, parent={}):
        self.data = data
        if isinstance(parent, dict) or isinstance(parent, UserDict):
            self.update(parent)
            self.parent = None
        elif isinstance(parent, cldict):
            self.parent = parent
        else:
            raise TypeError, "class_dict's only accept dictionaries or other class dict's"

    def __cmp__(self, other):
        #TODO: WRONG WRONG
        if isinstance(dict, DS):
            return cmp(self.data, dict.data)
        else:
            return cmp(self.data, dict)

    def __len__(self):
        if self.parent:
            return len(self.data) + len(self._dict_methods()) + len(self.parent)
        else:
            return len(self.data) + len(self._dict_methods())

    def __call__(self, *a):
        return [self[x] for x in a]
    
    def __attr_get(self, key):
        try:
            attr = getattr(self, 'g_%s' % key)
        except AttributeError:
            if self.parent is not None:
                return self.parent[key]
            else:
                raise KeyError, key
        else:
            return attr()

    def __getitem__(self, name):
        try:
            return self.data[name]
        except KeyError:
            return self.__attr_get(name)

    def __attr_set(self, key):
        try:
            return getattr(self, 's_%s' % key)
        except AttributeError:
            if self.parent is not None:
                return self.parent.__attr_set(key)
            else:
                raise

    def __setitem__(self, key, item):
        try:
            attr = self.__attr_set(key)
        except AttributeError:
            self.data[key] = item
        else:
            attr(item)
    
    def __attr_del(self, key):
        try:
            attr = getattr(self, 'd_%s' % key)
        except AttributeError:
            if self.parent is not None:
                del self.parent[key]
            else:
                raise KeyError, key
        else:
            attr()

    def __delitem__(self, key):
        try:
            del self.data[key]
        except KeyError:
            self.__attr_del(key)

    def __iter__(self):
        return iter(self.keys())
    
    def clear(self): 
        self.data.clear()

        
    def _dict_methods(self):
        """ Retrieves the "dictionary hook" methods that an object supports """
        return [s[2:] for s in dir(self) if s.startswith("g_")]

    def keys(self):
        k = self.data.keys()
        k.extend(self._dict_methods())
        if self.parent:
            k.extend(self.parent.keys())
        return unique_list(*k)
    
    def has_key(self, key):
        return key in self
    
    def items(self):
        return [(key, self[key]) for key in self]
    
    def values(self):
        return [self[key] for key in self]

    def get(self, key, failobj=None):
        try:
            return self[key]
        except KeyError:
            return failobj
    
    def setdefault(self, key, failobj=None):
        if not self.has_key(key):
            self[key] = failobj
        return self[key]

    def popitem(self):
        return self.data.popitem()

    def __contains__(self, key):
        return key in self.keys()

    def update(self, other):
        for k in other:
            self[k] = other[k]
            
    def copy(self):
        if self.__class__ is DS:
            return DS(self.data)
        import copy
        data = self.data
        try:
            self.data = {}
            c = copy.copy(self)
        finally:
            self.data = data
        c.update(self)
        return c

    def copyFrom(self, ds):
        map(lambda s: self.__setitem__(s, ds[s]), ds.keys())

class odict(UserDict):
    def __init__(self, dict = None):
        self._keys = []
        UserDict.__init__(self, dict)

    def __getattr__(self, attr):
        try:
            return self[attr]
        except KeyError:
            raise AttributeError, attr

    def __delitem__(self, key):
        UserDict.__delitem__(self, key)
        self._keys.remove(key)

    def __setitem__(self, key, item):
        UserDict.__setitem__(self, key, item)
        if key not in self._keys: self._keys.append(key)

    def clear(self):
        UserDict.clear(self)
        self._keys = []

    def copy(self):
        dict = UserDict.copy(self)
        dict._keys = self._keys[:]
        return dict

    def items(self):
        return zip(self._keys, self.values())

    def keys(self):
        return self._keys

    def __iter__(self):
        return iter(self._keys)

        
    def popitem(self):
        try:
            key = self._keys[-1]
        except IndexError:
            raise KeyError('dictionary is empty')

        val = self[key]
        del self[key]

        return (key, val)

    def setdefault(self, key, failobj = None):
        UserDict.setdefault(self, key, failobj)
        if key not in self._keys: self._keys.append(key)

    def update(self, dict):
        UserDict.update(self, dict)
        for key in dict.keys():
            if key not in self._keys: self._keys.append(key)

    def values(self):
        return map(self.get, self._keys)

    def __repr__(self):
        return "{%s}" % ", ".join(["%r : %r" % v for v in self.items()])

class attr_proxy_dict(object):
    """ Provides a dict interface to an automatically resolving sub attribute
    of values.

    """
    def __init__(self, obj, attr):
        self.__subject__ = obj
        self.__attr__ = attr

    def __getattr__(self, v):
        attr = getattr(self.__subject__, v)
        if hasattr(attr, self.__attr__):
            return getattr(attr, self.__attr__)
        else:
            return attr

    def __getitem__(self, v):
        attr = self.__subject__.__getitem__(v)
        if hasattr(attr, self.__attr__):
            return getattr(attr, self.__attr__)
        else:
            return attr

    def get(self, v, default=None):
        attr = self.__subject__.get(v, default)
        if attr is default:
            return attr
        if hasattr(attr, self.__attr__):
            return getattr(attr, self.__attr__)
        else:
            return attr

    def keys(self):
        return self.__subject__.keys()

