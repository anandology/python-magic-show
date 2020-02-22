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
    def __init__(self, env):
        self.env = env

    def __add__(self, x): return Expr(self.env, operator.__add__, self, x)
    def __mul__(self, x): return Expr(self.env, operator.__mul__, self, x)
    def __sub__(self, x): return Expr(self.env, operator.__sub__, self, x)
    def __div__(self, x): return Expr(self.env, operator.__div__, self, x)

    def __radd__(self, x): return Expr(self.env, operator.__add__, x, self)
    def __rmul__(self, x): return Expr(self.env, operator.__mul__, x, self)
    def __rsub__(self, x): return Expr(self.env, operator.__sub__, x, self)
    def __rdiv__(self, x): return Expr(self.env, operator.__div__, x, self)

    def __rshift__(self, x): return Iter(self.env, self, x)
    def __rrshift__(self, x): return Iter(self.env, x, self)

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
        super().__init__(env)
        self.name = name

    def resolve(self):
        return self.env.resolve(self.name)

    def _repr(self):
        return "`{}".format(self.name)

class Expr(Promise):
    """Expression on a symbol.
    """
    def __init__(self, env, op, left, right):
        super().__init__(env)
        self.op = op
        self.left = left
        self.right= right

    def resolve(self):
        return self.op(resolve(self.left), resolve(self.right))

    def _repr(self):
        op = {
            operator.__add__: '+',
            operator.__sub__: '-',
            operator.__mul__: '*'
        }[self.op]

        return "({} {} {})".format(_repr(self.left), op, _repr(self.right))

class LazyFunction:
    def __init__(self, env, func):
        self.env = env
        self.func = func

    def __call__(self, *a, **kw):
        return LazyResult(self.env, self.func, a, kw)

class LazyResult(Promise):
    def __init__(self, env, func, a, kw):
        super().__init__(env)
        self.func = func
        self.a = a
        self.kw = kw

    def resolve(self):
        a = resolve(self.a)
        kw = resolve(self.kw)
        return self.func(*a, *kw)

    def _repr(self):
        return "<LazyResult {} {} {}>".format(self.func, self.a, self.kw)

class Iter:
    def __init__(self, env, head, tail):
        self.env = env
        self._head = head
        self._tail = tail

    def __add__(self, other):
        def add():
            nonlocal other
            other = resolve(other)
            head = resolve(self._head) + resolve(other._head)
            return Iter(self.env, head, self._tail + other._tail)
        return LazyResult(self.env, add, (), {})

    def __iter__(self):
        yield resolve(self._head)
        yield from resolve(self._tail)

    def resolve(self):
        return self

    def _repr(self):
        return "[{} {}]".format(_repr(self._head), _repr(self._tail))

    __repr__ = _repr

def resolve(x):
    if isinstance(x, (list, tuple)):
        return [resolve(v) for v in x]
    elif isinstance(x, dict):
        return {resolve(k): resolve(v) for k, v in x.items()}
    elif isinstance(x, Iter):
        return x
    elif isinstance(x, Promise):
        return resolve(x.resolve())
    else:
        return x

def _repr(x):
    if isinstance(x, Promise):
        return x._repr()
    else:
        return repr(x)

def take(n, values):
    values = iter(resolve(values))
    return [next(values) for i in range(n)]

def tail(values):
    values = resolve(values)
    if isinstance(values, Iter):
        return values._tail
    else:
        raise ValueError("Not an Iter")

ENV = LazyEnv()
BUILTINS['take'] = LazyFunction(ENV, take)
BUILTINS['tail'] = LazyFunction(ENV, tail)

def lazy_exec(code):
    exec(code, ENV, ENV)

def lazy_eval(code):
    return eval(code, ENV, ENV)

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
