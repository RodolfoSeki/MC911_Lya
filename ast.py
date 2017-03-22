import sys

class Node(object):

    def children(self):
        return []

    def show(self, buf=sys.stdout, offset=0):
        #buf.write(', '.join([(n, getattr(self, n)) for n in self.attr_names]))
        buf.write(' '*offset)
        buf.write(type(self).__name__ + '\n')

        for child in self.children():
            child.show(buf, offset + 2)



class Program(Node):
    def __init__(self, stmt_list):
        self.stmt_list = stmt_list

    def children(self):
        return self.stmt_list
            
class DeclarationStatement(Node):
    def __init__(self, dcl_list):
        self.dcl_list = dcl_list

    def children(self):
        return self.dcl_list

class Declaration(Node):
    def __init__(self, id_list, mode, init = None):
        self.id_list = id_list
        self.mode = mode
        self.init = init

class Identifier(Node):
    def __init__(self, x):
        self.x = x

class DiscreteMode(Node):
    def __init__(self, x):
        self.x = x

class Expression(Node):
    def __init__(self, x):
        self.x = x

class Operand0(Node):
    def __init__(self, x):
        self.x = x

class Operand1(Node):
    def __init__(self, x):
        self.x = x

class Operand2(Node):
    def __init__(self, left, operator=None, right=None):
        self.left = left
        self.operator = None
        self.right = right

class Operand3(Node):
    def __init__(self, x):
        self.x = x


