import sys
from node import *

# x: a propositional formula
# returns implication free form of x
def impl_free(x):
  if isinstance(x, Liter):
    return x
  elif isinstance(x, Impl):
    left = impl_free(x.left)
    right = impl_free(x.right)
    return Or(Not(left), right)
  elif isinstance(x, RevImpl):
    left = impl_free(x.left)
    right = impl_free(x.right)
    return Or(Not(right), left)
  elif isinstance(x, Equiv):
    left = impl_free(x.left)
    right = impl_free(x.right)
    return And(Or(Not(left), right), Or(Not(right), left))
  elif isinstance(x, Not):
    return Not(impl_free(x.left))
  else:
    left = impl_free(x.left)
    right = impl_free(x.right)
    return x.__class__(left, right)

# x: implication free formula
# returns negation normal form of x
def nnf(x):
  if isinstance(x, Liter):
    return x
  elif isinstance(x, Not) and isinstance(x.left, Not):
    return nnf(x.left.left)
  elif isinstance(x, Not) and isinstance(x.left, And):
    return Or(nnf(Not(x.left.left)), nnf(Not(x.left.right)))
  elif isinstance(x, Not) and isinstance(x.left, Or):
    return And(nnf(Not(x.left.left)), nnf(Not(x.left.right)))
  elif isinstance(x, Not):
    return Not(nnf(x.left))
  else:
    return x.__class__(nnf(x.left), nnf(x.right))

# a, b: cnf formulas
# distributes (a OR b)
def distr(a, b):
  if isinstance(a, And):
    return And(distr(a.left, b), distr(a.right, b))
  elif isinstance(b, And):
    return And(distr(a, b.left), distr(a, b.right))
  else:
    return Or(a, b)

# x: imlication free and negation normal form formula
# returns conjunctive normal form of x
def cnf(x):
  if isinstance(x, Liter):
    return x
  elif isinstance(x, And):
    return And(cnf(x.left), cnf(x.right))
  elif isinstance(x, Or):
    return distr(cnf(x.left), cnf(x.right))
  elif isinstance(x, Not):
    return Not(cnf(x.left))
  else:
    raise Exception('not implfree or nnf')