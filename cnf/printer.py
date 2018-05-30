from node import *

opers = {
  And: '&',
  Or: '|',
  Impl: '>',
  RevImpl: '<',
  Equiv: '='
}

# prints tree x in polish notation
def print_polish(x):
  if isinstance(x, Liter):
    print(x.left + " ", end='')
  elif isinstance(x, Not):
    print("- ", end='')
    print_polish(x.left)
  else:
    print(opers[x.__class__]+" ", end='')
    print_polish(x.left)
    print_polish(x.right)

# prints tree x in infix notation
def print_infix(x):
  if isinstance(x, Liter):
    print(x.left + " ", end='')
  elif isinstance(x, Not):
      print("- ", end='')
      print_infix(x.left)
  else:
    print('( ', end='')
    print_infix(x.left)
    print(opers[x.__class__]+" ", end='')
    print_infix(x.right)
    print(') ', end='')

# prints tree x in infix notation with parentheses only around OR operations
def print_cnf(x):
  if isinstance(x, Liter):
    print(x.left + " ", end='')
  elif isinstance(x, Not):
      print("- ", end='')
      print_cnf(x.left)
  else:
    if isinstance(x, And) and isinstance(x.left, Or):
      print('( ', end='')
      print_cnf(x.left)
      print(') ', end='')
    else:
      print_cnf(x.left)

    print(opers[x.__class__]+" ", end='')

    if isinstance(x, And) and isinstance(x.right, Or):
      print('( ', end='')
      print_cnf(x.right)
      print(') ', end='')
    else:
      print_cnf(x.right)