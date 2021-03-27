from inspect import signature
import re

# TODO(rageply) Add clearer logic to the nr of input arguments, ex: R_(3) should only be joined to sets that treat 3d coords, ie customize the self.nr_args.

class setlang:
    def __init__(self, expr): 
        self.nr_args = len(signature(expr).parameters)
        if self.nr_args > 1:
            self.constraints = [lambda x : expr(*x)]
        else:
            self.constraints  = [expr]

    def __iadd__(self, expr):
        assert(len(signature(expr).parameters) == self.nr_args)
        if self.nr_args > 1:
            self.constraints += [lambda x : expr(*x)]
        else:
            self.constraints  += [expr]
            
        return self
        
    def __contains__(self, args, _recursive=False):
        if type(args) is list and self.nr_args == 1 and not _recursive: 
            for arg in args:
                if not self.__contains__(arg,_recursive=True):
                    return False
            else:
                return True
        else:
            for expr in self.constraints:
                if not expr(args):
                    return False
            else:
                return True

# TODO(rageply) let them modify ordinary sets as well.
 
    def __add__(self, other):
        assert(self.nr_args == other.nr_args)
        return setlang(lambda x : x in self or x in other)
    
    def __sub__(self, other):
        assert(self.nr_args == other.nr_args)
        return setlang(lambda x : x in self and x not in other)

    def __rand__(self, other):
        assert(self.nr_args == other.nr_args)
        return setlang(lambda x : x in self and x in other)
                

    def __invert__(self):
        return setlang(lambda x : x not in self)


def set_range(a, b):
    return setlang(lambda x : a <= x <= b)

# Helper sets
NN = setlang(lambda x : type(x) is int and x >= 0)
ZZ = setlang(lambda x : type(x) is int)
RR = setlang(lambda x : x in ZZ or type(x) is float)
RRpos = setlang(lambda x : x in RR and x >= 0)
RRneg = setlang(lambda x : x in RR and x < 0)
CC = setlang(lambda x : x in RR or type(x) is complex)

OO = setlang(lambda x : False)
UU = setlang(lambda x : True)

meta_set = setlang(lambda x : type(x) is setlang)


def D_(r2):
    return setlang(lambda x : sum([ xi * xi for xi in x]) == r2)

def C_(r2):
    return setlang(lambda x : sum([ xi * xi for xi in x]) < r2)

def RR_(n):
    return setlang(lambda x : len(x) == n and list(x) in RR)




    
    # Main idea: eval("lambda " + user unput expression). So
    # A = {x : x < 2} gets interpreted as
    # key = "A", expr = "x : x < 2" and realised as 
    # variable_space.update({key : eval("lambda " + expr)})
    # then when another statement is made, it will
    # replace substrings seperated by whitespace or 
    # special characters that is in the variable_space key
    # set and evaluate that expression. So
    # 1 in R
    # R is seperated by whitespace AND is a key, replace the 
    # string such that it equals 1 in "variable_space[\"A\"]"
    # and output the results in the terminal
    # match single element
    # ((\".+\")|([0-9]+\.[0-9]+)|([0-9]+))
    # match tuple
    # (\( *((\".+\")|([0-9]+\.[0-9]+)|([0-9]+))( *, *((\".+\")|([0-9]+\.[0-9]+)|([0-9]+)))+ *\))
    # match list
    # (\[ *((\".+\")|([0-9]+\.[0-9]+)|([0-9]+))( *, *((\".+\")|([0-9]+\.[0-9]+)|([0-9]+)))+ *\])
    # match all
    # (((\".+\")|([0-9]+\.[0-9]+)|([0-9]+))|(\( *((\".+\")|([0-9]+\.[0-9]+)|([0-9]+))( *, *((\".+\")|([0-9]+\.[0-9]+)|([0-9]+)))+ *\))|(\[ *((\".+\")|([0-9]+\.[0-9]+)|([0-9]+))( *, *((\".+\")|([0-9]+\.[0-9]+)|([0-9]+)))+ *\]))

# SETLANG_append_workspace = { fname : (open(fname,"a"), "".join(["{\"{}\": {\"set\": {}, \"parsed\": \"{}\", \"orig\":\"{}\"}}".format(k,v["set"],v["parsed"],v["orig"]) for k,v in _pm.items()])) in SETLANG_write_and_close }