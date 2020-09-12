from lark import Lark
from lark.visitors import Interpreter

import operator as op
import math
import os

def get_parser():
    p = "grammar.lark"
    p = os.path.join(os.path.dirname(__file__), p)
    with open(p,"r") as f:
        raw = f.read()
    return Lark(raw, start="expression", parser="lalr")
    

class UndefinedFunction(ValueError):
    pass

class UndefinedVariable(ValueError):
    pass

class BaseEnviroment:
    variables = {} 
    pseudo_functions =  {
        "pi":lambda: math.pi,
        "e":lambda: math.e
    }

    functions =  {        
        #math (pure computations)
        "asin":math.asin,
        "atan":math.atan,
        "cos":math.cos,
        "acos":math.acos,
        "sin":math.sin,
        "tan":math.tan,

        "exp":math.exp,
        "ln": math.log,
        "log":lambda b,e:math.log(e,b),

        "abs":abs,
        "floor":math.floor,
        "ceil":math.ceil,

        "ifelse":lambda c,i,e: i if c else e,
        "cond":lambda c,i,e: i if c else e,
    }

    def __getitem__(self, key):
        key = key.lower()
        if key in self.functions:
            return self.functions[key]

        #pseudo variable
        if key in self.pseudo_functions:
            return self.pseudo_functions[key]()

        if key in self.variables:
            return self.variables[key]

        raise KeyError(key)

    def __setitem__(self, key, value):
        key = key.lower()
        self.variables[key] = value

    def __contains__(self, key):
        key = key.lower()
        return (
            key in self.functions or
            key in self.pseudo_functions or
            key in self.variables
        )

    def clear(self):
        t = self.variables
        self.variables = {}
        return t

class ExpressionInterpreter(Interpreter):
    _env = BaseEnviroment()
    #cast types
    def int(self, tree):
        return int(tree.children[0])
    
    def float(self, tree):
        return float(tree.children[0])
    
    def str(self, tree):
        return str(tree.children[0])

    #return variable value
    def var(self, tree):
        name = tree.children[0]
        try:
            return self._env[name]
        except KeyError:            
            raise UndefinedVariable(name)

    def assign(self, tree):
        name = tree.children[0]
        v = self.visit(tree.children[1])
        self._env[name] = v
        return v

    def fn_call(self, tree):
        name, *args = tree.children
        args = [self.visit(c) for c in args]
        try:
            return self._env[name](*args)
        except KeyError:            
            raise UndefinedFunction(name)

    def _op(self, tree, fn):
        args = [self.visit(c) for c in tree.children]
        #TODO: investigare
        args = [a[0] if hasattr(a,'__getitem__') else a for a in args ]
        try:
            return fn(*args)
        except:
            return fn(args)

    def op_sum(self, tree):
        return self._op(tree, op.add)

    def op_mul(self, tree):
        return self._op(tree, op.mul)

    def op_sub(self, tree):
        return self._op(tree, op.sub)

    def op_div(self, tree):
        return self._op(tree, op.truediv)
    
    def op_mod(self, tree):
        return self._op(tree, op.mod)
    
    def op_and(self, tree):
        return self._op(tree, op.and_)
        
    def op_or(self, tree):
        return self._op(tree, op.or_)
        
    def op_eq(self, tree):
        return 1 if self._op(tree, op.eq) else 0

    def op_neq(self, tree):
        return 1 if self._op(tree, op.ne) else 0
        
    def op_gt(self, tree):
        return 1 if self._op(tree, op.gt) else 0

    def op_gt_or_eq(self, tree):
        return 1 if self._op(tree, op.ge) else 0

    def op_lt(self, tree):
        return 1 if self._op(tree, op.lt) else 0
    
    def op_lt_or_eq(self, tree):
        return 1 if self._op(tree, op.le) else 0

    def op_not(self, tree):
        return 1 if self._op(tree, op.not_) else 0
    
    def op_negate(self, tree):
        return 1 if self._op(tree, op.neg) else 0

    pass

def scopose(trigger):
    out = []
    for subt in trigger:
        #is a list
        if hasattr(subt, 'append'):
            out.append(scopose(subt)) 
        else:
            if "&&" in subt:
                out.extend([scopose([e]) for e in subt.split("&&")])
            elif "||" in subt:
                out.append([scopose([e]) for e in subt.split("||")])
            else:
                if subt.startswith("("):
                    subt = subt.strip()[1:-1]
                out.append(subt)

    return out
