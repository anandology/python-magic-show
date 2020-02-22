"""
lazy.py
~~~~~~~~

Lazy evaluation in Python.

USAGE:

    $ python lazy.py
    ...
    (InteractiveConsole)
    >>> x = 1
    >>> y = x + 1
    >>> x = 10
    >>> y
    11
"""
import sys
import operator

BUILTINS = dict(__builtins__.__dict__)

class LazyEnv(dict):
    """Python dictionary for lazy evaluation.
    """
    def __getitem__(self, key):
        """Accessing any item from the LazyEnv returns a symbol with that name.
        """
        if key in BUILTINS:
            return BUILTINS[key]
        return Symbol(self, key)

    def resolve(self, name):
        """Resolves the symbol into its actual value.
        """
        return super().__getitem__(name)

    def __repr__(self):
        return "<LazyEnv>"

class Promise:
    """Promise is promise for a value in the future.

    The `resolve` method returns the value of this promise.
    """
    def __add__(self, x): return Expr(self.env, operator.__add__, self, x)
    def __mul__(self, x): return Expr(self.env, operator.__mul__, self, x)
    def __sub__(self, x): return Expr(self.env, operator.__sub__, self, x)
    def __div__(self, x): return Expr(self.env, operator.__div__, self, x)

    def __radd__(self, x): return Expr(self.env, operator.__add__, x, self)
    def __rmul__(self, x): return Expr(self.env, operator.__mul__, x, self)
    def __rsub__(self, x): return Expr(self.env, operator.__sub__, x, self)
    def __rdiv__(self, x): return Expr(self.env, operator.__div__, x, self)

    def resolve(self):
        raise NotImplementedError()

    def __str__(self):
        return str(resolve(self))

    def __repr__(self):
        return repr(resolve(self))

class Symbol(Promise):
    """Symbol represents a variable that is resolved lazily
    when the value is accessed.
    """
    def __init__(self, env, name):
        self.env = env
        self.name = name

    def resolve(self):
        return self.env.resolve(self.name)

class Expr(Promise):
    """Expression on a symbol.
    """
    def __init__(self, env, op, left, right):
        self.env = env
        self.op = op
        self.left = left
        self.right= right

    def resolve(self):
        return self.op(resolve(self.left), resolve(self.right))

def resolve(x):
    if isinstance(x, (list, tuple)):
        return [resolve(v) for v in x]
    elif isinstance(x, dict):
        return {resolve(k): resolve(v) for k, v in x.items()}
    elif isinstance(x, Promise):
        return resolve(x.resolve())
    else:
        return x

def lazy_exec(code, env=None):
    if env is None:
        env = LazyEnv()
    exec(code, env, env)

def lazy_eval(code):
    env = LazyEnv()
    return eval(code, env, env)

def main():
    if len(sys.argv) > 1:
        f = sys.argv[1]
        code = open(f).read()
        lazy_exec(code)
    else:
        from code import InteractiveConsole
        console = InteractiveConsole(LazyEnv())
        console.runcode("import readline")
        console.interact()

if __name__ == "__main__":
    main()
