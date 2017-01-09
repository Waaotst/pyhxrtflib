
from functools import wraps

def debug_echo(func):
    '''used on method to simply print the function name and
    parameters if self.debug_echo = True,
    the function will not execute'''
    @wraps(func)
    def deco(*args, **kwargs):
        try:
            debug = args[0].debug_echo
        except AttributeError:
            debug = False
        if debug:
            if len(args) == 1:
                to_print = []
            else:
                to_print = args[1:]
            print(func.__name__, repr(to_print), **kwargs)

        return func(*args, **kwargs)
    return deco
