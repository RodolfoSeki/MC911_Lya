class NodeVisitor(object):

    def visit(self,node):
        """
        Execute a method of the form visit_NodeName(node) where
        NodeName is the name of the class of a particular node.
        """
        if node:
            method = 'visit_' + node.__class__.__name__
            visitor = getattr(self, method, self.generic_visit)
            return visitor(node)
        else:
            return None

    def generic_visit(self,node):
        """
        Method executed if no applicable visit_ method can be found.
        This examines the node to see if it has _fields, is a list,
        or can be further traversed.
        """
        return visit(node)

        """
        for field in getattr(node,"_fields"):
            value = getattr(node,field,None)
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, AST):
                        self.visit(item)
            elif isinstance(value, AST):
                self.visit(value)
        """

class SymbolTable(dict):
    """
    Class representing a symbol table. It should
    provide functionality for adding and looking
    up nodes associated with identifiers.
    """
    def __init__(self, decl=None):
        super().__init__()
        self.decl = decl
    def add(self, name, value):
        self[name] = value
    def lookup(self, name):
        return self.get(name, None)
    def return_type(self):
        if self.decl:
            return self.decl.mode
        return None

class Type(object):
    def __init__(self, exprtype, string):
        self.type = exprtype
        self.name = string

class ExprType(object):
    def __init__(self, type, unaryop, binop):
        self.type = type
        self.unaryop = unaryop
        self.binop = binop

    def __repr__(self):
        return self.type

int_type = ExprType("int", ['-'], ['+', '-', '*', '/', '%', '==', '!=', '>', '>=', '<', '>=', '<', '<='])
bool_type = ExprType("bool", ['!'], ['==', '!='])
char_type = ExprType("char", [], [])
string_type = ExprType("string", [], ['+', '==', '!=', '&', '&='])

class Environment(object):
    def __init__(self):
        self.stack = []
        self.root = SymbolTable()
        self.stack.append(self.root)
        self.root.update({
            "int": int_type,
            "char": char_type,
            "string": string_type,
            "bool": bool_type
        })
    def push(self, enclosure):
        self.stack.append(SymbolTable(decl=enclosure))
    def pop(self):
        self.stack.pop()
    def peek(self):
        return self.stack[-1]
    def scope_level(self):
        return len(self.stack)
    def add_local(self, name, value):
        self.peek().add(name, value)
    def add_root(self, name, value):
        self.root.add(name, value)
    def lookup(self, name):
        for scope in reversed(self.stack):
            hit = scope.lookup(name)
            if hit is not None:
                return hit
        return None
    def find(self, name):
        if name in self.stack[-1]:
            return True
        else:
            return False

    
class Visitor(NodeVisitor):
    """
    Program Visitor class. This class uses the visitor pattern as
    described in lya_ast.py.   It’s define methods of the form
    visit_NodeName() for each kind of AST node that we want to process.
    Note: You will need to adjust the names of the AST nodes if you
    picked different names.
    """
    def __init__(self):
        self.environment = Environment()

    def raw_type_unary(self, node, op, val):
        if hasattr(val, "check_type"):
            if op not in val.check_type.unary_ops:
                error(node.lineno,
                      "Unary operator {} not supported".format(op))
            return val.check_type

    def raw_type_binary(self, node, op, left, right):
        if hasattr(left, "check_type") and hasattr(right, "check_type"):
            if left.check_type != right.check_type:
                error(node.lineno,
                "Binary operator {} does not have matching types".format(op))
                return left.check_type
            errside = None
            if op not in left.check_type.binary_ops:
                errside = "LHS"
            if op not in right.check_type.binary_ops:
                errside = "RHS"
            if errside is not None:
                error(node.lineno, "Binary operator {} not supported on {} of expression".format(op, errside))
        return left.check_type

    def visit_Program(self, node):
        self.environment.push(node)
        node.environment = self.environment
        node.symtab = self.environment.peek()
        # Visit all of the statements
        for stmt in node.stmt_list: 
            self.visitStatement(stmt)

    def visit_Statement(self, node):
        for child in node.children():
            self.visit(child)

    def visit_Declaration(self, node):
        mode = self.visit(node.mode)
        value = self.visit(node.value)
        if value != None:
            if mode.type != value.type:
                print('Error, {} is not {}'.format(value.name, mode.type))
                #### TODO acabar

    def visit_IntegerMode(self, node):
        return Type('int', int_type)



    def visit_Operand0(self, node):
        if node.operator == None:
            return self.visit(node)
        operand0 = self.visit(node.operand0)
        operand1 = self.visit(node.operand1)
        operator = node.operator.op
        if operand0.type != operand1.type:
            print('Error, {} {} {}'.format(operand0.type, operator, operand1.type))
        if operator not in operand0.type.binop:
            print('Error, {} not supported for {}'.format(operator, operand0.type))
        #TODO

    def visit_Operand1(self, node):
        if node.operator == None:
            return self.visit(node)

        operand0 = self.visit(node.operand1)
        operand1 = self.visit(node.operand2)
        operator = node.operator.op

        if operand0.type != operand1.type:
            print('Error, {} {} {}'.format(operand0.type, operator, operand1.type))
        if operator not in operand0.type.binop:
            print('Error, {} not supported for {}'.format(operator, operand0.type))

        return Type(' '.join([operand0.name, operator, operand1.name]), operand0.type)

    def visit_Operand2(self, node):
        if node.operator == None:
            return self.visit(node)

        operand0 = self.visit(node.operand2)
        operand1 = self.visit(node.operand3)
        operator = node.operator.op

        if operand0.type != operand1.type:
            print('Error, {} {} {}'.format(operand0.type, operator, operand1.type))
        if operator not in operand0.type.binop:
            print('Error, {} not supported for {}'.format(operator, operand0.type))

        return Type(' '.join([operand0.name, operator, operand1.name]), operand0.type)

    def visit_Operand3(self, node):
        if node.operator == None:
            return self.visit(node)

        operand0 = self.visit(node.operand_or_literal)
        operator = node.operator.op

        if operator not in operand0.type.unaryop:
            print('Error, {} not supported for {}'.format(operator, operand0.type))

        return Type(' '.join([operator, operand0.name]), operand0.type)

    def visit_OperandX(self, node):
        if node.operator == None:
            return self.visit(node)
        operand0 = self.visit(node.operand0)
        operand1 = self.visit(node.operand1)
        operator = node.operator.op
        if operand0.type != operand1.type:
            print('Error, {} {} {}'.format(operand0.type, operator, operand1.type))
        if operator not in operand0.type.binop:
            print('Error, {} not supported for {}'.format(operator, operand0.type))
        #TODO

    def visit_SynStmt(self, node):
        # Visit all of the synonyms
        for syn in node.syns:
            self.visit(syn)

    def visit_UnaryExpr(self,node):
        self.visit(node.expr)
        # Make sure that the operation is supported by the type
        raw_type = self.raw_type_unary(node, node.op, node.expr)
        # Set the result type to the same as the operand
        node.raw_type = raw_type

    def visit_BinaryExpr(self,node):
        # Make sure left and right operands have the same type
        # Make sure the operation is supported
        self.visit(node.left)
        self.visit(node.right)
        raw_type = self.raw_type_binary(node, node.op, node.left, node.right)
        # Assign the result type
        node.raw_type = raw_type
