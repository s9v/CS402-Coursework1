from node import *

# x: cnf formula
# checks whether x is valid
def valid(x):
  if isinstance(x, Liter):
    return False
  elif isinstance(x, Not):
    return False
  elif isinstance(x, Or):
    v = or_literals(x)
    for l in v:
      if l[0] != '-' and ('-'+l) in v:
        return True
    return False
  else:
    return valid(x.left) and valid(x.right)

# x: disjunction of one or more literals (possibly negated)
# helper for valid(), returns list of literals in the formula
def or_literals(x):
  if isinstance(x, Liter):
    return [x.left]
  elif isinstance(x, Not):
    return ['-' + or_literals(x.left)[0]]
  elif isinstance(x, Or):
    v = or_literals(x.left)
    v.extend(or_literals(x.right))
    return v
  else:
    raise Exception('should be only Liter, Not or Or')