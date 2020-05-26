from functional import *

__all__ = ['apply_all', 'apply_seq_values', 'filter_call']

def apply_all(funcs, reducer=any):
    """     apply_all(list funcs, func reducer) -> variable

    Given a list of functions(funcs) and a reducer function, this function
    returns a function that applies all of its arguments to each function
    in funcs. The resulting list of function results is then passed to reducer.
    The results of reducer are returned from the created function.
    """
    def _(*a, **k):
       return reducer(map(
              lambda x: x(*a, **k), funcs
       ))
    return _

def apply_seq_values(dict):
    """ apply_seq_values(dict) -> list

    transforms a dict into a list, applying the keys to each element in each
    list of values
    """
    trans = []
    for k, v in dict.items():
        trans = trans + [func(*k) for func in v]
    return trans

def filter_call(search, *arg, **kwd):
    """ f(list search, *a, **k) -> list

    Given a list of functions[search], apply the arguments
    to each function. If the results of the call are not False,
    then append them to the result list.
    """
    ret = []
    for f in search:
        result = f(*arg, **kwd)
        if result:
            ret.append(result)
    return ret
