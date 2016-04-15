import errors as ERRORS

def unrepr(s):
    if not s:
        return s
    try:
        return Builder().build(getObj(s))
    except:
        return s

def label2name(label):
    reps = [('-','_'),(' ','_')]
    for rep in reps:
        label = label.replace(rep[0],rep[1])
    return label.lower()

# public domain "unrepr" implementation, found on the web and then improved.
def getObj(s):
    s = "a=" + s
    p = compiler.parse(s)
    return p.getChildren()[1].getChildren()[0].getChildren()[1]

class Builder:

    def build(self, o):
        m = getattr(self, 'build_' + o.__class__.__name__, None)
        if m is None:
            raise UnknownType(o.__class__.__name__)
        return m(o)

    def build_List(self, o):
        return map(self.build, o.getChildren())

    def build_Const(self, o):
        return o.value

    def build_Dict(self, o):
        d = {}
        i = iter(map(self.build, o.getChildren()))
        for el in i:
            d[el] = i.next()
        return d

    def build_Tuple(self, o):
        return tuple(self.build_List(o))

    def build_Name(self, o):
        if o.name == 'None':
            return None
        if o.name == 'True':
            return True
        if o.name == 'False':
            return False

        raise ERRORS.UnknownType(o.name)

    def build_Add(self, o):
        real, imag = map(self.build_Const, o.getChildren())
        try:
            real = float(real)
        except TypeError:
            raise ERRORS.UnknownType('Add')
        if not isinstance(imag, complex) or imag.real != 0.0:
            raise ERRORS.UnknownType('Add')
        return real+imag

    def build_Getattr(self, o):
        parent = self.build(o.expr)
        return getattr(parent, o.attrname)
