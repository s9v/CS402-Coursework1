import sys
from node import *
from cnf import *
from printer import *
from valid import valid

def parse(v):
  stack = []

  for i in range(len(v)):
    if v[i] == '&':
      stack.append(And(None, None))
    elif v[i] == '|':
      stack.append(Or(None, None))
    elif v[i] == '-':
      stack.append(Not(None))
    elif v[i] == '>':
      stack.append(Impl(None, None))
    elif v[i] == '<':
      stack.append(RevImpl(None, None))
    elif v[i] == '=':
      stack.append(Equiv(None, None))
    else:
      x = Liter(v[i])

      while True:
        if isinstance(stack[-1], Not):
          stack[-1].left = x
          x = stack.pop()
        elif stack[-1].left is None:
          stack[-1].left = x
          break
        else:
          stack[-1].right = x

          if len(stack) == 1:
            break
          else:
            x = stack.pop()

  if len(stack) > 1:
    raise Exception('invalid formula')

  return stack[0]

def main():
  v = sys.argv[1].split(' ')
  x = parse(v)
  x = impl_free(x)
  x = nnf(x)
  x = cnf(x)
  print_polish(x)
  print()
  print_cnf(x)
  print()
  print('Valid' if valid(x) else 'Not Valid')

if __name__ == '__main__':
  main()