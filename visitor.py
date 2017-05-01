class NodeVisitor(object):

    def visit(self,node):
        """
        Execute a method of the form visit_NodeName(node) where
        NodeName is the name of the class of a particular node.
        """
        print('Visiting ' + node.__class__.__name__)
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
        if len(node.children()) == 1:
            self.visit(node.children()[0])
            node.type = node.children()[0].type
            node.repr = node.children()[0].repr
        else:
            print('Erro child ' + node.__class__.__name__)

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
    def __init__(self, type, unaryop, binop):
        self.type = type
        self.unaryop = unaryop
        self.binop = binop

    def __repr__(self):
        return self.type

    def __str__(self):
        return self.type

int_type = Type("int", ['-'], ['+', '-', '*', '/', '%', '==', '!=', '>', '>=', '<', '>=', '<', '<='])
bool_type = Type("bool", ['!'], ['==', '!='])
char_type = Type("char", [], [])
string_type = Type("string", [], ['+', '==', '!=', '&', '&='])
array_type = Type("array", [], ['==', '!='])

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
        if op not in left.type.unary_ops:
            print('Error, {} is not supported for {}'.format(op, val.raw_type))
        return val.type

    def raw_type_binary(self, node, op, left, right):

        if left.type != right.type:
            #error(node.lineno,
            #print("Binary operator {} does not have matching types".format(op))
            print('Error, {} {} {} is not supported'.format(left.repr, op, right.repr))
            return left.type
        if op not in left.type.binop:
            print('Error, {} is not supported for {}'.format(op, left.type))
        if op not in right.type.binop:
            print('Error, {} is not supported for {}'.format(op, right.type))
        return left.type

    def visitBinaryExp(self, node, left, right, op):
        self.visit(left)
        self.visit(right)
        if op == None:
            node.type = left.type if left is not None else right.type
            node.repr = left.repr if left is not None else right.repr
            return 

        node.type = self.raw_type_binary(node, op, left, right)
        node.repr = ' '.join([left.name, op, right.name])
    
    def visitUnaryExp(self, node, val, op):
        self.visit(val)
        if op == None:
            node.type = val.type
            node.repr = val.repr
            return 

        node.type = raw_type_unary(node, op, val)
        node.repr = ''.join([op, val.name])

    def visit_Program(self, node):
        self.environment.push(node)
        node.environment = self.environment
        node.symtab = self.environment.peek()
        # Visit all of the statements
        for stmt in node.stmt_list: 
            self.visit_Statement(stmt)

    def visit_Statement(self, node):
        for child in node.children():
            self.visit(child)

    def visit_Declaration(self, node):
        self.visit(node.mode)
        self.visit(node.value)
        if node.value is not None:
            if node.mode.type != node.value.type:
                print('Error, {} is not {}'.format(node.value.repr, node.mode.repr))

        for identifier in node.id_list:
            identifier.type = node.mode.type
            identifier.repr = identifier.name
            if self.environment.find(identifier.repr):
                print('Error, {} already declared'.format(identifier.repr))
            if node.value is not None:
                self.environment.add_local(identifier.repr, node.value.type)
            else:
                self.environment.add_local(identifier.repr, identifier.type)

    def visit_Identifier(self, node):
        node.repr = node.name
        node.type = self.environment.lookup(node.name)
        if node.type is None:
            print('Error, {} used but not declared'.format(node.repr))
                
    def visit_SynonymDefinition(self, node):
        self.visit(node.mode)
        self.visit(node.constant_exp)
        if node.mode is not None:
            if node.mode.type != node.constant_exp.type:
                print('Error, {} is not {}'.format(node.constant_exp.repr, node.mode.repr))

        for identifier in node.id_list:
            identifier.type = node.constant_exp.type
            identifier.repr = identifier.name
            if self.environment.find(identifier.repr):
                print('Error, {} already exists'.format(identifier.repr))
            self.environment.add_root(identifier.repr, identifier.type)
            
    def visit_ModeDefinition(self, node):
        self.visit(node.mode)

        for identifier in node.id_list:
            identifier.type = node.mode.type
            identifier.repr = identifier.name
            if self.environment.find(identifier.repr):
                print('Error, {} already exists'.format(identifier.repr))
            self.environment.add_root(identifier.repr, identifier.type)

    def visit_IntegerMode(self, node):
        node.type = int_type
        node.repr = 'INT'

    def visit_BooleanMode(self, node):
        node.type = bool_type
        node.repr = 'BOOL'

    def visit_CharacterMode(self, node):
        node.type = char_type
        node.repr = 'CHAR'

    def visit_DiscreteRangeMode(self, node):
        self.visit(node.name)
        self.visit(node.literal_range)
        node.type = node.name.type
        node.repr = node.name.repr + '(' + node.literal_range.repr + ')'

    def visit_LiteralRange(self, node):
        self.visit(node.lower)
        self.visit(node.upper)
        if node.lower.type != int_type:
            print('Error, literal range lower bound cannot be {}'.format(lower.type))
        if node.upper.type != int_type:
            print('Error, literal range upper bound cannot be {}'.format(upper.type))

        node.type = node.lower.type
        node.repr = node.lower.repr + ':' + node.upper.repr

    def visit_StringMode(self, node):
        self.visit(node.length)
        if node.length.type != int_type:
            print('Error, string length cannot be {}'.format(length.type))

        node.type = string_type
        node.repr = 'CHARS [{}]'.format(length.repr)

    def visit_ArrayMode(self, node):
        for index_mode in node.index_mode_list:
            self.visit(index_mode)
        self.visit(node.mode)

        node.type = array_type
        node.arrtype = mode.type
        node.repr = 'ARRAY [{}] {}'.format(', '.join(node.index_mode_list), mode)

    def visit_IntegerLiteral(self, node):
        node.type = int_type
        node.repr = node.const

    def visit_BooleanLiteral(self, node):
        node.type = bool_type
        node.repr = node.val

    def visit_CharacterLiteral(self, node):
        node.type = char_type
        node.repr = "'" + chr(node.val) + "'"
        
    def visit_EmptyLiteral(self, node):
        node.type = string_type
        node.repr = node.val

    def visit_CharacterStringLiteral(self, node):
        node.type = string_type
        node.repr = node.val

    def visit_Operand0(self, node):
        self.visitBinaryExp(node, node.operand0, node.operand1, node.operator.op)

    def visit_Operand1(self, node):
        self.visitBinaryExp(node, node.operand1, node.operand2, node.operator.op)

    def visit_Operand2(self, node):
        self.visitBinaryExp(node, node.operand2, node.operand3, node.operator.op)

    def visit_Operand3(self, node):
        self.visitUnaryExp(node, node.operator.op, node.operand)

    def visit_AssignmentAction(self, node):
        self.visit(node.expression)
        self.visit(node.location)
        left = node.location
        right = node.expression
        if left.type != right.type:
            print("Error, can't assign {} to {}".format(right.type, left.type))
        node.type = left.type
        node.repr = ' '.join([left.repr, node.assigning_op.op, right.repr])

    def visit_SynStmt(self, node):
        # Visit all of the synonyms
        for syn in node.syns:
            self.visit(syn)
    
    def visit_StringElement(self, node):
        self.visit_Identifier(node.ident)
        self.visit(node.element)
        if node.element.type != int_type:
            print('Error, {} should be int'.format(element.repr))
            
        return node.ident.type
        
    def visit_StringSlice(self, node):
        self.visit_Identifier(node.loc)
        self.visit(node.left)
        self.visit(node.right)
        
        if node.left.type != int_type:
            print('Error, {} should be int'.format(left.repr))
            
        if node.right.type != int_type:
            print('Error, {} should be int'.format(right.repr))
        
        return node.loc.type
    
    def visit_ArrayElement(self, node):
        self.visit_Identifier(node.loc)
        
        for exp in node.expr_list:
            self.visit(exp)
            if exp.type != int_type:
                print('Error, {} should be int'.format(exp.repr))
                
        return node.loc.type
    
    def visit_ArraySlice(self, node):
        self.visit_Identifier(node.loc)
        self.visit(node.left)
        self.visit(node.right)
        
        if node.left.type != int_type:
            print('Error, {} should be int'.format(left.repr))
            
        if node.right.type != int_type:
            print('Error, {} should be int'.format(right.repr))
            
        return node.loc.type
        
