def check_attrs(obj, attrs):
    """ ensures that the object has the given attributes and that they are not
    False
    """
    bad = []
    for a in attrs:
        try:
            v = getattr(obj, a)
        except AttributeError:
            bad.append(a)
        else:
            if not v:
                bad.append(a)
    return bad
