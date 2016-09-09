import types

def cursor2csv(cursor, headers=True):
    """ converts a cursor into a file-like object which contains all of
    the records in the cursor as a CSV file.

    The cursor should be a regular tuple cursor, not a dict cursor.
    """
    t = tempfile.TemporaryFile()
    writer = csv.writer(t)
    if headers:
        writer.writerow([d[0] for d in cursor.description])
    writer.writerows(cursor)
    t.seek(0)

class data_registry(dict):
    default = None

    def __getattr_(self, key):
        return self[key]

    def reg(self, name):
        def update(p, n):
            if not hasattr(p, '__registry__'):
                p.__registry__ = {}
            self[n] = p
            p[n] = self
            return p

        if isinstance(name, types.FunctionType):
            return update(name, name.__name__)
        else:
            return lambda p: update(p, name)

class slots(dict):
    # Provide blank slots for those that are not explicitly created
    def __getitem__(self, key):
        try:
            return dict.__getitem__(self, key)
        except KeyError:
            dict.__setitem__(self, key, [])
            return dict.__getitem__(self, key)


def fix_decor_attrs(*decors):
    """ Given a list of decorators, this decorator insures that the
    final function will have the proper attributes like __doc__
    and __dict__

    Example:
        @fix_decor_attrs(
            my_decor1,
            my_decor2)
        def my_proc(cool):
            pass
    """
    def decor(func):
        # emulate decorator syntax
        seed = func
        dlist = list(decors)
        dlist.reverse()
        for f in dlist:
            odoc = seed.__doc__
            odict = seed.__dict__
            seed = f(seed)
            if not seed.__doc__:
                seed.__doc__ = odoc
            # Make a choice. Do we overwrite
            for k, v in odict:
                if k not in seed.__dict__:
                    seed.__dict__[k] = v
        seed.__name__ = func.__name__
        return seed
    return decor
