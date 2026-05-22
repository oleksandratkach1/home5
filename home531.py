from math import gcd

class Rational:
    def __init__(self, n=0, d=1):
        if isinstance(n, str):
            n, d = (int(x) for x in n.split('/')) if '/' in n else (int(n), 1)
        if d < 0:
            n, d = -n, -d
        g = gcd(abs(n), abs(d))
        self.n, self.d = n // g, d // g

    def _to_r(self, other):
        return other if isinstance(other, Rational) else Rational(other)

    def __add__(self, other):
        o = self._to_r(other)
        return Rational(self.n * o.d + o.n * self.d, self.d * o.d)

    def __radd__(self, other): return self.__add__(other)

    def __sub__(self, other):
        o = self._to_r(other)
        return Rational(self.n * o.d - o.n * self.d, self.d * o.d)

    def __rsub__(self, other): return self._to_r(other).__sub__(self)

    def __mul__(self, other):
        o = self._to_r(other)
        return Rational(self.n * o.n, self.d * o.d)

    def __rmul__(self, other): return self.__mul__(other)

    def __truediv__(self, other):
        o = self._to_r(other)
        return Rational(self.n * o.d, self.d * o.n)

    def __rtruediv__(self, other): return self._to_r(other).__truediv__(self)

    def __call__(self): return self.n / self.d

    def __getitem__(self, key): return self.n if key == 'n' else self.d

    def __setitem__(self, key, val):
        if key == 'n': self.n = val
        else: self.d = val

    def __repr__(self): return str(self.n) if self.d == 1 else f"{self.n}/{self.d}"


def evaluate(expr):
    tokens = expr.split()
    vals = [Rational(*map(int, t.split('/'))) if '/' in t else Rational(int(t)) for t in tokens[::2]]
    ops = tokens[1::2]

    i = 0
    while i < len(ops):
        if ops[i] in ('*', '/'):
            vals[i] = vals[i] * vals[i+1] if ops[i] == '*' else vals[i] / vals[i+1]
            vals.pop(i+1)
            ops.pop(i)
        else:
            i += 1

    result = vals[0]
    for op, val in zip(ops, vals[1:]):
        result = result + val if op == '+' else result - val
    return result


with open("numbers.txt", "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if line:
            r = evaluate(line)
            print(f"{line}\n= {r} ≈ {r():.6f}\n")