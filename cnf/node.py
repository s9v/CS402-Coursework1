class Node:
  def __init__(self, left, right):
    self.left = left
    self.right = right

class Liter(Node):
  def __init__(self, liter):
    self.left = liter
    self.right = None

class Not(Node):
  def __init__(self, node):
    self.left = node
    self.right = None

class And(Node):
  def __init__(self, left, right):
    self.left = left
    self.right = right

class Or(Node):
  def __init__(self, left, right):
    self.left = left
    self.right = right

class Impl(Node):
  def __init__(self, left, right):
    self.left = left
    self.right = right

class RevImpl(Node):
  def __init__(self, left, right):
    self.left = left
    self.right = right

class Equiv(Node):
  def __init__(self, left, right):
    self.left = left
    self.right = right
