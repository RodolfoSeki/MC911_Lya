import sys

class Node(object):

    def children(self):
        return []

    def show(self, buf=sys.stdout, offset=0):
        buf.write(' '*offset)
        buf.write(type(self).__name__)
        buf.write(': ' + ', '.join(['{}={}'.format(k, getattr(self, k)) for k in self.attr_names]) + '\n')

        for child in self.children():
            child.show(buf, offset + 2)

class Program(Node):
    def __init__(self, stmt_list):
        self.stmt_list = stmt_list

    def children(self):
        return self.stmt_list

    attr_names = ()
            
class DeclarationStatement(Node):
    def __init__(self, dcl_list):
        self.dcl_list = dcl_list

    def children(self):
        return self.dcl_list

    attr_names = ()

class Declaration(Node):
    def __init__(self, id_list, mode, value=None):
        self.id_list = id_list
        self.mode = mode
        self.value = value 

    def children(self):
        listchildren = []
        for identifier in self.id_list:
            listchildren.append(identifier)
        if self.mode is not None: listchildren.append(self.mode)
        if self.value is not None: listchildren.append(self.value)
        return listchildren

    attr_names = ()

class Identifier(Node):
    def __init__(self, name):
        self.name = name 

    attr_names = ('name',)

class PrimitiveMode(Node):
    def __init__(self, mode):
        self.mode = mode 

    attr_names = ('mode',)

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

    def children(self):
        listchildren = []
        if self.left is not None: listchildren.append(self.left)
        if self.right is not None: listchildren.append(self.right)
        return listchildren

    attr_names = ('operator',)

class Operand3(Node):
    def __init__(self, x):
        self.x = x


