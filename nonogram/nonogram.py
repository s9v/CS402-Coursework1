import os


# Nonogram solver using minisat
class NonogramSolver():
  def __init__(self, rows=[], cols=[]):
    self.R = len(rows)
    self.C = len(cols)
    self.rows = list(rows)
    self.cols = list(cols)
    self.clauses = []

  def solve(self):
    self._build_clauses()
    self._write_dimacs_file()
    return self._solve_cnf()

  def _build_clauses(self):
    # Try all values for every row
    for r in range(self.R):
      for bitmask in range(1 << self.C):
        ok = True
        n1 = 0
        ri = 0

        # Check if values corresponding to the bitmask are correct for the row
        if len(self.rows[r]) == 1 and self.rows[r][0] == 0:
          ok = (bitmask == 0)
        else:
          for c in range(self.C+1):
            if c < self.C and (bitmask & (1 << c)) > 0:
              n1 += 1
            elif n1 > 0:
              if ri >= len(self.rows[r]) or n1 != self.rows[r][ri]:
                ok = False
                break

              ri += 1
              n1 = 0

          if ri < len(self.rows[r]) and self.rows[0] != 0:
            ok = False

        # Add to clauses if the bitmask is not correct
        if not ok:
          clause = []

          for c in range(self.C):
            x = r*self.C + c + 1
            clause.append(-x if (bitmask & (1 << c)) > 0 else x)

          self.clauses.append(clause)

    # Try all values for every column
    for c in range(self.C):
      for bitmask in range(1 << self.R):
        ok = True
        n1 = 0
        ci = 0

        # Check if values corresponding to the bitmask are correct for the column
        if len(self.cols[c]) == 1 and self.cols[c][0] == 0:
          ok = (bitmask == 0)
        else:
          for r in range(self.R+1):
            if r < self.R and (bitmask & (1 << r)) > 0:
              n1 += 1
            elif n1 > 0:
              if ci >= len(self.cols[c]) or n1 != self.cols[c][ci]:
                ok = False
                break

              ci += 1
              n1 = 0

          if ci < len(self.cols[c]):
            ok = False

        # Add to clauses if the bitmask is not correct
        if not ok:
          clause = []

          for r in range(self.R):
            x = r*self.C + c + 1
            clause.append(-x if (bitmask & (1 << r)) > 0 else x)

          self.clauses.append(clause)

  def _write_dimacs_file(self):
    # Write CNF problem into DIMACS file
    with open('nonogram.dimacs', 'w') as dimacs:
      # Write problem definition
      dimacs.write("p cnf {nliterals} {nclauses}\n".format(
        nliterals=self.R*self.C, nclauses=len(self.clauses)))

      # Write clauses
      for clause in self.clauses:
        clause.append(0)
        line = ' '.join([str(x) for x in clause])
        dimacs.write(line + '\n')

  # Solve CNF problem using minisat
  def _solve_cnf(self):
    # Run minisat and output solution into "minisat.out"
    os.system('./minisat nonogram.dimacs minisat.out >/dev/null')

    # Read minisat output
    interp = []
    lines = []

    with open('minisat.out', 'r') as f:
      lines = f.readlines()
    
    if lines[0].strip() == 'UNSAT':
      return None # Problem unsatisfiable
    else:
      # If satisfiable, read satisfying interpretation
      interp = lines[1].split(' ')
      interp = list(map(int, interp))
      solution = ''

      for r in range(self.R):
        for c in range(self.C):
          x = r*self.C+c
          solution += '.' if interp[x] < 0 else '#'
        solution += '\n'

      return solution

sol = None

def main():
  # Read nonogram in CWD format
  R = int(input())
  C = int(input())

  rows = [ input().split(' ') for i in range(R)]
  rows = [list(map(int, lst)) for lst in rows]
  cols = [input().split(' ') for i in range(C)]
  cols = [list(map(int, lst)) for lst in cols]

  # Solve
  ns = NonogramSolver(rows, cols)
  solution = ns.solve()
  global sol
  sol = solution

  # Print solution
  if solution is None:
    print('Given nonogram could not be solved and probably is unsolvable :-(')
  else:
    print(solution, end='')

if __name__ == '__main__':
  main()