import sys

def toRed(prt): return("\033[91m{}\033[00m" .format(prt))
def toGreen(prt): return("\033[92m{}\033[00m" .format(prt))
def toYellow(prt): return("\033[93m{}\033[00m" .format(prt))
def toCyan(prt): return("\033[96m{}\033[00m" .format(prt))
def toBold(prt): return("'\033[1m{}\033[00m" .format(prt))
def toLightGray(prt): return("\033[97m{}\033[00m" .format(prt))

class Node(object):

    def children(self):
        return []

    def show(self, buf=sys.stdout, offset=0):
        buf.write(' '*offset)
        buf.write(type(self).__name__)
        buf.write(': ' + ', '.join(['{}={}'.format(k, getattr(self, k)) for k in self.attr_names]) + '\n')

        for child in self.children():
            try:
                child.show(buf, offset + 2)
            except:
                print (' '*offset + "Error at: " + self.__class__.__name__)
                print (child)
                raise

    def showDecorated(self, buf=sys.stdout, offset=0):
        buf.write(' '*offset)
        buf.write(toBold(type(self).__name__))
        buf.write(': ' + ', '.join(['{}={}'.format(k, getattr(self, k)) for k in self.attr_names]))
        if len(self.attr_names) < 1:
            if 'type' in dir(self):
                buf.write('   ' + 'type=' + str(getattr(self, 'type')))
            if 'offset' in dir(self):
                buf.write('   ' + 'offset=' + str(getattr(self, 'offset')))
            if 'size' in dir(self):
                buf.write('   ' + 'size=' + str(getattr(self, 'size')))
            if 'next' in dir(self):
                buf.write('   ' + 'next=' + str(getattr(self, 'next')))
            if 'exit' in dir(self):
                buf.write('   ' + 'exit=' + str(getattr(self, 'exit')))
            if 'repr' in dir(self):
                buf.write('   ' + toGreen(getattr(self, 'repr')))
            buf.write('\n')
        else:
            buf.write('\n')


        for child in self.children():
            try:
                child.showDecorated(buf, offset + 2)
            except:
                print (' '*offset + "Error at: " + self.__class__.__name__)
                print (child)
                raise

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

class SynonymStatement(Node):
    def __init__(self, synonym_list):
        self.synonym_list = synonym_list 

    def children(self):
        listchildren = []
        for synonym in self.synonym_list:
            listchildren.append(synonym)
        return listchildren

    attr_names = ()

class SynonymDefinition(Node):
    def __init__(self, id_list, constant_exp, mode=None):
        self.id_list = id_list
        self.constant_exp = constant_exp
        self.mode = mode

    def children(self):
        listchildren = []
        if self.constant_exp is not None: listchildren.append(self.constant_exp)
        if self.mode is not None: listchildren.append(self.mode)
        for identifier in self.id_list:
            listchildren.append(identifier)
        return listchildren

    attr_names = ()


class NewModeStatement(Node):
    def __init__(self, mode_list):
        self.mode_list = mode_list 

    def children(self):
        listchildren = []
        for mode in self.mode_list:
            listchildren.append(mode)
        return listchildren
        
    attr_names = ()

class ModeDefinition(Node):
    def __init__(self, id_list, mode):
        self.id_list = id_list
        self.mode = mode

    def children(self):
        listchildren = []
        for identifier in self.id_list:
            listchildren.append(identifier)
        if self.mode is not None: listchildren.append(self.mode)
        return listchildren

    attr_names = ()

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

class CharacterMode(Node):
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
        self.literal_range = literal_range

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

class StringMode(Node):
    def __init__(self, length):
        self.length = length

    def children(self):
        listchildren = []
        if self.length is not None: listchildren.append(self.length)
        return listchildren
    attr_names = ()

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

class StringElement(Node):
    def __init__(self, ident, element):
        self.ident = ident
        self.element = element

    def children(self):
        listchildren = []
        if self.ident is not None: listchildren.append(self.ident)
        if self.element is not None: listchildren.append(self.element)
        return listchildren

    attr_names = ()

class StringSlice(Node):
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
        self.val = val

    attr_names = ('val',)

class EmptyLiteral(Node):
    def __init__(self):
        self.val='NULL'

    attr_names = ('val',)

class CharacterStringLiteral(Node):
    def __init__(self, string):
        self.string = string

    attr_names = ('string',)

class ValueArrayElement(Node):
    def __init__(self, value, exp_list):
        self.value = value 
        self.exp_list = exp_list

    def children(self):
        listchildren = []
        if self.value is not None: listchildren.append(self.value)
        for exp in self.exp_list:
            listchildren.append(exp)
        return listchildren

    attr_names = ()


class ValueArraySlice(Node):
    def __init__(self, value, lower, upper):
        self.value = value 
        self.lower = lower
        self.upper = upper

    def children(self):
        listchildren = []
        if self.value is not None: listchildren.append(self.value)
        if self.lower is not None: listchildren.append(self.lower)
        if self.upper is not None: listchildren.append(self.upper)
        return listchildren

    attr_names = ()

class ParenthesizedExpression(Node):
    def __init__(self, expr):
        self.expr = expr 

    def children(self):
        listchildren = []
        if self.expr is not None: listchildren.append(self.expr)
        return listchildren

    attr_names = ()

class Expression(Node):
    def __init__(self, expr):
        self.expr = expr 

    def children(self):
        listchildren = []
        if self.expr is not None: listchildren.append(self.expr)
        return listchildren

    attr_names = ()

class ConditionalExpression(Node):
    def __init__(self, if_expr, then_expr, else_expr, elsif_expr=None, ):
        self.if_expr = if_expr
        self.then_expr = then_expr 
        self.else_expr = else_expr
        self.elsif_expr = elsif_expr

    def children(self):
        listchildren = []
        if self.if_expr is not None: listchildren.append(self.if_expr)
        if self.then_expr is not None: listchildren.append(self.then_expr)
        if self.else_expr is not None: listchildren.append(self.else_expr)
        if self.elsif_expr is not None: listchildren.append(self.elsif_expr)
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
        if self.operand0 is not None: listchildren.append(self.operand0)
        if self.operand1 is not None: listchildren.append(self.operand1)
        if self.operator is not None: listchildren.append(self.operator)
        return listchildren
    
    attr_names = ()

class Operator(Node):
    def __init__(self, op):
        self.op = op

    attr_names = ('op',)


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


class ReferencedLocation(Node):
    def __init__(self, location):
        self.location = location

    def children(self):
        listchildren = []
        if self.location is not None: listchildren.append(self.location)
        return listchildren

    attr_names = ()


class ActionStatement(Node):
    def __init__(self, action, label=None):
        self.action = action
        self.label = label

    def children(self):
        listchildren = []
        if self.action is not None: listchildren.append(self.action)
        if self.label is not None: listchildren.append(self.label)
        return listchildren

    attr_names = ()


class Action(Node):
    def __init__(self, action):
        self.action = action

    def children(self):
        listchildren = []
        if self.action is not None: listchildren.append(self.action)
        return listchildren

    attr_names = ()

class BracketedAction(Node):
    def __init__(self, action):
        self.action = action

    def children(self):
        listchildren = []
        if self.action is not None: listchildren.append(self.action)
        return listchildren

    attr_names = ()

class AssignmentAction(Node):
    def __init__(self, location, assigning_op, expression):
        self.location = location
        self.assigning_op = assigning_op
        self.expression = expression

    def children(self):
        listchildren = []
        if self.location is not None: listchildren.append(self.location)
        if self.assigning_op is not None: listchildren.append(self.assigning_op)
        if self.expression is not None: listchildren.append(self.expression)
        return listchildren

    attr_names = ()

class AssigningOperator(Node):
    def __init__(self, assignm_symbl, cld_dyadic_op=''):
        self.op = cld_dyadic_op + assignm_symbl

    attr_names = ('op',)

class IfAction(Node):
    def __init__(self, if_exp, then_exp, else_exp=None):
        self.if_exp = if_exp
        self.then_exp = then_exp
        self.else_exp = else_exp

    def children(self):
        listchildren = []
        if self.if_exp is not None: listchildren.append(self.if_exp)
        if self.then_exp is not None: listchildren.append(self.then_exp)
        if self.else_exp is not None: listchildren.append(self.else_exp)
        return listchildren

    attr_names = ()

class ThenClause(Node):
    def __init__(self, action_statement_list):
        self.action_statement_list = action_statement_list

    def children(self):
        listchildren = []
        for statement in self.action_statement_list:
            listchildren.append(statement)
        return listchildren

    attr_names = ()

class ElseClause(Node):
    def __init__(self, else_type , bool_or_statement_list, then_exp=None, else_exp=None):
        self.else_type = else_type
        self.bool_or_statement_list = bool_or_statement_list
        self.then_exp = then_exp
        self.else_exp = else_exp

    def children(self):
        listchildren = []
        if self.else_type == 'else': 
            for statement in self.bool_or_statement_list:
                listchildren.append(statement)
        else:
            if self.bool_or_statement_list is not None: listchildren.append(self.bool_or_statement_list)
            if self.then_exp is not None: listchildren.append(self.then_exp)
            if self.else_exp is not None: listchildren.append(self.else_exp)
        return listchildren

    attr_names = ()

class DoAction(Node):
    def __init__(self, action_statement_list, ctrl_part=None):
        self.action_statement_list = action_statement_list
        self.ctrl_part = ctrl_part

    def children(self):
        listchildren = []
        if self.ctrl_part is not None: listchildren.append(self.ctrl_part)
        for statement in self.action_statement_list:
            listchildren.append(statement)
        return listchildren

    attr_names = ()

class ControlPart(Node):
    def __init__(self, ctrl1, ctrl2=None):
        self.ctrl1= ctrl1
        self.ctrl2= ctrl2

    def children(self):
        listchildren = []
        if self.ctrl1 is not None: listchildren.append(self.ctrl1)
        if self.ctrl2 is not None: listchildren.append(self.ctrl2)
        return listchildren

    attr_names = ()


class ForControl(Node):
    def __init__(self, iteration):
        self.iteration = iteration 

    def children(self):
        listchildren = []
        if self.iteration is not None: listchildren.append(self.iteration)
        return listchildren

    attr_names = ()


'''
class Iteration(Node):
    def __init__(self, enum):
        self.enum = enum

    def children(self):
        listchildren = []
        if self.enum is not None: listchildren.append(self.enum)
        return listchildren

    attr_names = ()
'''


class StepEnumeration(Node):
    def __init__(self, counter, start, end, step=None, decreasing=False):
        self.counter = counter
        self.start = start
        self.end = end 
        self.step = step
        self.decreasing = decreasing

    def children(self):
        listchildren = []
        if self.counter is not None: listchildren.append(self.counter)
        if self.start is not None: listchildren.append(self.start)
        if self.end is not None: listchildren.append(self.end)
        if self.step is not None: listchildren.append(self.step)
        return listchildren

    attr_names = ('decreasing', )

class RangeEnumeration(Node):
    def __init__(self, counter, mode, decreasing=False):
        self.counter = counter
        self.mode = mode 
        self.decreasing = decreasing

    def children(self):
        listchildren = []
        if self.counter is not None: listchildren.append(self.counter)
        if self.mode is not None: listchildren.append(self.mode)
        return listchildren

    attr_names = ('decreasing', )

class WhileControl(Node):
    def __init__(self, bool_exp):
        self.bool_exp = bool_exp

    def children(self):
        listchildren = []
        if self.bool_exp is not None: listchildren.append(self.bool_exp)
        return listchildren

    attr_names = ()

class CallAction(Node):
    def __init__(self, call):
        self.call = call

    def children(self):
        listchildren = []
        if self.call is not None: listchildren.append(self.call)
        return listchildren

    attr_names = ()


class ProcedureCall(Node):
    def __init__(self, name, param_list=[]):
        self.name = name
        self.param_list = param_list

    def children(self):
        listchildren = []
        if self.name is not None: listchildren.append(self.name)
        for param in self.param_list:
            listchildren.append(param)
        return listchildren

    attr_names = ()

class ExitAction(Node):
    def __init__(self, label):
        self.label = label  

    def children(self):
        listchildren = []
        if self.label is not None: listchildren.append(self.label)
        return listchildren

    attr_names = ()

class ReturnAction(Node):
    def __init__(self, exp=None):
        self.exp = exp 

    def children(self):
        listchildren = []
        if self.exp is not None: listchildren.append(self.exp)
        return listchildren

    attr_names = ()

class ResultAction(Node):
    def __init__(self, result):
        self.result = result 

    def children(self):
        listchildren = []
        if self.result is not None: listchildren.append(self.result)
        return listchildren

    attr_names = ()

class BuiltInCall(Node):
    def __init__(self, name, param_list=[]):
        self.name = name
        self.param_list = param_list

    def children(self):
        listchildren = []
        for param in self.param_list:
            listchildren.append(param)
        return listchildren

    attr_names = ('name', )
    
class ProcedureStatement(Node):
    def __init__(self, label, procedure_def):
        self.label = label
        self.procedure_def = procedure_def

    def children(self):
        listchildren = []
        if self.label is not None: listchildren.append(self.label)
        if self.procedure_def is not None: listchildren.append(self.procedure_def)
        return listchildren

    attr_names = ()


class ProcedureDefinition(Node):
    def __init__(self, stmt_list, result_spec=None, formal_parameter_list=[]):
        self.stmt_list = stmt_list
        self.result_spec = result_spec
        self.formal_parameter_list = formal_parameter_list

    def children(self):
        listchildren = []
        if self.result_spec is not None: listchildren.append(self.result_spec)
        for formal_parameter in self.formal_parameter_list:
            listchildren.append(formal_parameter)
        for statement in self.stmt_list:
            listchildren.append(statement)
        return listchildren

    attr_names = ()

class FormalParameter(Node):
    def __init__(self, id_list, param_spec):
        self.id_list = id_list
        self.param_spec = param_spec

    def children(self):
        listchildren = []
        if self.param_spec is not None: listchildren.append(self.param_spec)
        for identifier in self.id_list:
            listchildren.append(identifier)
        return listchildren

    attr_names = ()


class ParameterSpec(Node):
    def __init__(self, mode, loc=False):
        self.mode = mode 
        self.loc = loc 

    def children(self):
        listchildren = []
        if self.mode is not None: listchildren.append(self.mode)
        return listchildren

    attr_names = ('loc', )


class ResultSpec(Node):
    def __init__(self, mode, loc=False):
        self.mode = mode 
        self.loc = loc 

    def children(self):
        listchildren = []
        if self.mode is not None: listchildren.append(self.mode)
        return listchildren

    attr_names = ('loc', )

