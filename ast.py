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

class Mode(Node):
    def __init__(self, mode):
        self.mode = mode 

    def children(self):
        listchildren = []
        if self.mode is not None: listchildren.append(self.mode)
        return listchildren
        
    attr_names = ()

class ModeName(Node):
    def __init__(self, identifier):
        self.identifier = identifier

    attr_names = ('identifier')

class DiscreteMode(Node):
    def __init__(self, name):
        self.name = name

    def children(self):
        listchildren = []
        if self.name is not None: listchildren.append(self.name)
        return listchildren

    attr_names = ()

class IntegerMode(Node):
    def __init__(self):
        self.name = 'int'

    attr_names = ('name',)

class CharMode(Node):
    def __init__(self):
        self.name = 'char'

    attr_names = ('name',)

class BooleanMode(Node):
    def __init__(self):
        self.name = 'bool'

    attr_names = ('name',)

class DiscreteRangeMode(Node):
    def __init__(self, name, literal_range):
        self.name = name
        self.literal_range

    def children(self):
        listchildren = []
        if self.name is not None: listchildren.append(self.name)
        if self.literal_range is not None: listchildren.append(self.literal_range)
        return listchildren

    attr_names = ()

class LiteralRange(Node):
    def __init__(self, lower, upper):
        self.lower = lower 
        self.upper = upper

    def children(self):
        listchildren = []
        if self.lower is not None: listchildren.append(self.lower)
        if self.upper is not None: listchildren.append(self.upper)
        return listchildren

    attr_names = ()

class ReferenceMode(Node):
    def __init__(self, mode):
        self.mode = mode

    def children(self):
        listchildren = []
        if self.mode is not None: listchildren.append(self.mode)
        return listchildren

    attr_names = ()

class ReferenceMode(Node):
    def __init__(self, mode):
        self.mode = mode

    def children(self):
        listchildren = []
        if self.mode is not None: listchildren.append(self.mode)
        return listchildren

    attr_names = ()

class StringMode(Node):
    def __init__(self, length):
        self.length = length

    attr_names = ('length',)

class ArrayMode(Node):
    def __init__(self, index_mode_list, mode):
        self.index_mode_list = index_mode_list
        self.mode = mode

    def children(self):
        listchildren = []
        for index_mode in self.index_mode_list:
            listchildren.append(index_mode)
        if self.mode is not None: listchildren.append(self.mode)
        return listchildren

    attr_names = ()

class Location(Node):
    def __init__(self, loc_type):
        self.loc_type = loc_type

    def children(self):
        listchildren = []
        if self.loc_type is not None: listchildren.append(self.loc_type)
        return listchildren

    attr_names = ()

class DereferencedReference(Node):
    def __init__(self, loc):
        self.loc = loc

    def children(self):
        listchildren = []
        if self.loc is not None: listchildren.append(self.loc)
        return listchildren

    attr_names = ()

class StringSlice(Node):
    def __init__(self, loc, left, right):
        self.loc = loc
        self.left = loc
        self.right = loc

    def children(self):
        listchildren = []
        if self.loc is not None: listchildren.append(self.loc)
        if self.left is not None: listchildren.append(self.left)
        if self.right is not None: listchildren.append(self.right)
        return listchildren

    attr_names = ()

class ArrayElement(Node):

    def __init__(self, loc, expr_list):
        self.loc = loc
        self.expr_list = expr_list

    def children(self):
        listchildren = []
        if self.loc is not None: listchildren.append(self.loc)
        for expr in self.expr_list:
            listchildren.append(expr)
        return listchildren

    attr_names = ()

class ArraySlice(Node):

    def __init__(self, loc, left, right):
        self.loc = loc
        self.left = left  
        self.right = right

    def children(self):
        listchildren = []
        if self.loc is not None: listchildren.append(self.loc)
        if self.left is not None: listchildren.append(self.left)
        if self.right is not None: listchildren.append(self.right)
        return listchildren

    attr_names = ()

class PrimitiveValue(Node):

    def __init__(self, val):
        self.val = val

    def children(self):
        listchildren = []
        if self.val is not None: listchildren.append(self.val)
        return listchildren

    attr_names = ()


class IntegerLiteral(Node):
    def __init__(self, const):
        self.const = const

    attr_names = ('const',)

class BooleanLiteral(Node):
    def __init__(self, val):
        self.val= val

    attr_names = ('val',)

class CharacterLiteral(Node):
    def __init__(self, val):
        self.val= val

    attr_names = ('val',)

class EmptyLiteral(Node):
    def __init__(self):
        self.val='NULL'

    attr_names = ('val',)

class CharacterStringLiteral(Node):
    def __init__(self, string):
        self.string = string

    attr_names = ('string',)

### value_array_element

class Expression(Node):
    def __init__(self, expr):
        self.expr = expr 

    def children(self):
        listchildren = []
        if self.expr is not None: listchildren.append(self.expr)
        return listchildren

    attr_names = ()

class ConditionalExpression(Node):
    def __init__(self, if_expr, then_expr, elsif_expr=None, else_expr):
        self.if_expr = if_expr
        self.then_expr = then_expr 
        self.elsif_expr = elsif_expr
        self.else_expr = else_expr

    def children(self):
        listchildren = []
        if self.if_expr is not None: listchildren.append(self.if_expr)
        if self.then_expr is not None: listchildren.append(self.then_expr)
        if self.elsif_expr is not None: listchildren.append(self.elsif_expr)
        if self.else_expr is not None: listchildren.append(self.else_expr)
        return listchildren

    attr_names = ()

class BooleanExpression(Node):
    def __init__(self, expr):
        self.expr = expr 

    def children(self):
        listchildren = []
        if self.expr is not None: listchildren.append(self.expr)
        return listchildren

    attr_names = ()

class ThenExpression(Node):
    def __init__(self, expr):
        self.expr = expr 

    def children(self):
        listchildren = []
        if self.expr is not None: listchildren.append(self.expr)
        return listchildren

    attr_names = ()

class ElseExpression(Node):
    def __init__(self, expr):
        self.expr = expr 

    def children(self):
        listchildren = []
        if self.expr is not None: listchildren.append(self.expr)
        return listchildren

    attr_names = ()

class ElsifExpression(Node):
    def __init__(self, bool_expr, then_expr, elsif_expr=None):
        self.bool_expr = bool_expr
        self.then_expr = then_expr
        self.elsif_expr = elsif_expr

    def children(self):
        listchildren = []
        if self.bool_expr is not None: listchildren.append(self.bool_expr)
        if self.then_expr is not None: listchildren.append(self.then_expr)
        if self.elsif_expr is not None: listchildren.append(self.elsif_expr)
        return listchildren

    attr_names = ()

class Operand0(Node):
    def __init__(self, operand1, operand0=None, operator=None):
        self.operand1 = operand1
        self.operand0 = operand0
        self.operator = operator

    def children(self):
        listchildren = []
        if self.operand1 is not None: listchildren.append(self.operand1)
        if self.operand0 is not None: listchildren.append(self.operand0)
        if self.operator is not None: listchildren.append(self.operator)
        return listchildren
    
    attr_names = ()

class Operator1(Node):
    def __init__(self, op):
        self.op= op

    attr_names = ('op',)

class Operand1(Node):
    def __init__(self, operand2, operand1=None, operator=None):
        self.operand2 = operand2
        self.operand1 = operand1
        self.operator = operator

    def children(self):
        listchildren = []
        if self.operand2 is not None: listchildren.append(self.operand2)
        if self.operand1 is not None: listchildren.append(self.operand1)
        if self.operator is not None: listchildren.append(self.operator)
        return listchildren

    attr_names = ()

class Operator2(Node):
    def __init__(self, op):
        self.op= op

    attr_names = ('op',)

class Operand2(Node):
    def __init__(self, operand3, operand2=None, operator=None):
        self.operand3 = operand3
        self.operand2 = operand2
        self.operator = operator

    def children(self):
        listchildren = []
        if self.operand3 is not None: listchildren.append(self.operand3)
        if self.operand2 is not None: listchildren.append(self.operand2)
        if self.operator is not None: listchildren.append(self.operator)
        return listchildren

    attr_names = ()


class Operand3(Node):
    def __init__(self, operand_or_literal, operator=None):
        self.operand_or_literal = operand_or_literal
        self.operator = operator

    def children(self):
        listchildren = []
        if self.operand_or_literal is not None: listchildren.append(self.operand_or_literal)
        if self.operator is not None: listchildren.append(self.operator)
        return listchildren

    attr_names = ()

class Operand4(Node):
    def __init__(self, operand):
        self.operand = operand

    def children(self):
        listchildren = []
        if self.operand is not None: listchildren.append(self.operand)
        return listchildren

    attr_names = ()


