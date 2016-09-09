import re, md5
from func import apply_all

def is_ssn(str):
    return re.match(r'^\d{3}-\d{2}-\d{4}$', str)

def is_phone_number_alt1(str):
    return re.match(r'^\(\d{3}\) \d{3}-\d{4}$', str)

def is_phone_number_alt2(str):
    return re.match(r'^\d{3}-\d{3}-\d{4}$', str)

def is_phone_number_alt3(str):
    return re.match(r'^\d{3}\.\d{3}\.\d{4}$', str)

is_phone_number = apply_all([
	is_phone_number_alt1,
	is_phone_number_alt2,
	is_phone_number_alt3]
)

def str2var(s):
    """ Converts an arbitrary string to a valid python variable name """
    return s.replace(" ", "").replace("-", "_")

def randstr(min, max):
    """ randstr(min, max) -> string

    Generates a pseduo-random string between min and max length
    """
    mid = (max - min)/2
    return md5.new(str(time.time()+random.random())).hexdigest()[random.randint(min, mid):random.randint(mid+1,max)]

def seq_repr(name, seq):
    """ seq_repr(str name, seq seq) ->

        provide a generic representation string for a sequence type. This
        procedure is useful when defining your own sequence types and you
        wish to have a unique __repr__ for your type.
    """
    return "<%s : [%s]>" % (name, ", ".join([repr(x) for x in seq]))

def valid_pyid(s):
    return bool(re.match("^[A-Za-z_][A-Za-z0-9_]*$", s))
