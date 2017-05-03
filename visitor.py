class NodeVisitor(object):

    def visit(self,node):
        """
        Execute a method of the form visit_NodeName(node) where
        NodeName is the name of the class of a particular node.
        """
        if node:
            method = 'visit_' + node.__class__.__name__
#            if hasattr(self, method):
#                print('Specific visitor ' + method)
#            else:
#                print('Generic_visit for ' + node.__class__.__name__)
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
        for child in node.children():
            self.visit(child)
            if hasattr(child, 'type'):
                node.type = child.type
            if hasattr(child, 'repr'):
                node.repr = child.repr
            else:
                node.repr = node.__class__.__name__
            if hasattr(child, 'syn'):
                node.syn = child.syn

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
pointer_type = Type("addr", [], ['==', '!='])
none_type = Type("none", [], [])
array_type = Type("array", [], ['==', '!='])
syn_type = Type("syn", [], [])

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
        print('New scope for {}'.format(enclosure.__class__.__name__))
    def pop(self):
        self.stack.pop()
        print ('End scope')
    def peek(self):
        return self.stack[-1]
    def scope_level(self):
        return len(self.stack)
    def add_local(self, name, value):
        self.peek().add(name, value)
        print('Name {} with type {} was added to scope {}'.format(name, value, self.scope_level()))
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
        if op not in val.type[-1].unaryop:
            print('Error, {} is not supported for {}'.format(op, val.type[-1]))
        return val.type

    def raw_type_binary(self, node, op, left, right):
        if left.type != right.type:
            if not( left.type[-1] == right.type[-1] == pointer_type and right.type == [pointer_type]):
                print('Error, {} {} {} is not supported'.format(left.type[-1] , op, right.type[-1]))
                return left.type
        if op not in left.type[-1].binop:
            print('Error, {} is not supported for {}'.format(op, left.type[-1]))
        if op not in right.type[-1].binop:
            print('Error, {} is not supported for {}'.format(op, right.type[-1]))
        if op.upper() in ('&&', '||', '>', '<', '>=', '<=', 'IN', '!=', '=='):
            return [bool_type]
        return left.type

    def visitBinaryExp(self, node, left, right, op):
        self.visit(left)
        self.visit(right)
        if op == None:
            node.type = left.type if left is not None else right.type
            node.repr = left.repr if left is not None else right.repr
            return 

        node.type = self.raw_type_binary(node, op, left, right)
        
        if hasattr(left, 'syn') and hasattr(right, 'syn'):
            node.syn = True
        node.repr = ' '.join([left.repr, op, right.repr])
    
    def visitUnaryExp(self, node, op, val):
        self.visit(val)
        if op == None:
            node.type = val.type
            node.repr = val.repr
            return 

        node.type = self.raw_type_unary(node, op, val)
        if hasattr(val, 'syn'):
            node.syn = True
        node.repr = ''.join([op, val.repr])

    def visit_Program(self, node):
        self.environment.push(node)
        node.environment = self.environment
        node.symtab = self.environment.peek()
        # Visit all of the statements
        for stmt in node.stmt_list: 
            self.visit(stmt)

    def visit_Declaration(self, node):
        self.visit(node.mode)
        self.visit(node.value)
        if node.value is not None:
            if node.mode.type != node.value.type:
                if not( node.mode.type[-1] == node.value.type[-1] == pointer_type and node.value.type == [pointer_type]):
                    print('Error, {} is not {}'.format(node.value.repr, node.mode.repr))

        for identifier in node.id_list:
            identifier.type = node.mode.type
            identifier.repr = identifier.name
            if self.environment.find(identifier.repr):
                print('Error, {} already declared'.format(identifier.repr))
            self.environment.add_local(identifier.repr, node.mode.type)

    def visit_Identifier(self, node):
        node.repr = node.name
        node.type = self.environment.lookup(node.repr)
        if node.type is None:
            print('Error, {} used but not declared'.format(node.repr))
            node.type = [none_type]
            return
        if node.type[-1] == syn_type:
            node.syn = True
            node.type = node.type[0:-1]
                
    def visit_SynonymDefinition(self, node):
        self.visit(node.mode)
        self.visit(node.constant_exp)
        if not hasattr(node.constant_exp, 'syn'):
            print('Error, in synonym definition, {} is not constant'.format(node.constant_exp.repr))

        if node.mode is not None:
            if node.mode.type != node.constant_exp.type:
                if not (node.mode.type[-1] == pointer_type and node.constant_exp.type == [pointer_type]):
                    print('Error, {} is not {}'.format(node.constant_exp.repr, node.mode.repr))
            
        for identifier in node.id_list:
            identifier.type = node.constant_exp.type + [syn_type]
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
            self.environment.add_local(identifier.repr, identifier.type)

    def visit_IntegerMode(self, node):
        node.type = [int_type]
        node.repr = 'INT'

    def visit_BooleanMode(self, node):
        node.type = [bool_type]
        node.repr = 'BOOL'

    def visit_CharacterMode(self, node):
        node.type = [char_type]
        node.repr = 'CHAR'

    def visit_DiscreteRangeMode(self, node):
        self.visit(node.name)
        self.visit(node.literal_range)
        node.type = node.name.type
        node.repr = node.name.repr + '(' + node.literal_range.repr + ')'

    def visit_LiteralRange(self, node):
        self.visit(node.lower)
        self.visit(node.upper)
        if node.lower.type[-1] != int_type:
            print('Error, literal range lower bound cannot be {}'.format(lower.type))
        if node.upper.type[-1] != int_type:
            print('Error, literal range upper bound cannot be {}'.format(upper.type))

        node.type = node.lower.type
        node.repr = node.lower.repr + ':' + node.upper.repr

    def visit_ReferenceMode(self, node):
        self.visit(node.mode)
        node.type = node.mode.type + [pointer_type]
        node.repr = "REF " + node.mode.repr
        
    def visit_StringMode(self, node):
        self.visit(node.length)
        if node.length.type[-1] != int_type:
            print('Error, string length cannot be {}'.format(node.length.type[-1]))

        node.type = [char_type, string_type]
        node.repr = 'CHARS [{}]'.format(node.length.repr)

    def visit_ArrayMode(self, node):
        self.visit(node.mode)
        node.type = []
        node.type += node.mode.type
        
        for index_mode in node.index_mode_list:
            self.visit(index_mode)
            node.type +=  [array_type]
        
        node.repr = 'ARRAY [{}] {}'.format(', '.join([index_mode.repr for index_mode in node.index_mode_list]), node.mode.repr)

    def visit_DereferencedReference(self, node):
        self.visit(node.loc)
        node.type = node.loc.type[0:-1]
        node.repr = node.loc.repr + '->'

    
    def visit_StringElement(self, node):
        self.visit(node.ident)
        self.visit(node.element)
        if node.element.type[-1] != int_type:
            print('Error, index {} should be int'.format(element.repr))
            
        node.type = node.ident.type[0:-1] # element type
        node.repr = '{}[{}]'.format(node.ident.repr, node.element.repr)
        
    def visit_StringSlice(self, node):
        self.visit(node.loc)
        self.visit(node.left)
        self.visit(node.right)
        
        if node.left.type[-1] != int_type:
            print('Error, {} should be int'.format(left.repr))
            
        if node.right.type[-1] != int_type:
            print('Error, {} should be int'.format(right.repr))
        
        node.type = node.loc.type
        node.repr = '{}[{}:{}]'.format(node.loc.repr, node.left.repr, node.right.repr)
    
    def visit_ArrayElement(self, node):
        self.visit(node.loc)
        
        for exp in node.expr_list:
            self.visit(exp)
            if exp.type[-1] != int_type:
                print('Error, index {} should be int'.format(exp.repr))

        if len(node.expr_list) == 1:
            node.type = node.loc.type[0:-1] # element type
        else:
            node.type = node.loc.type
        node.repr = '{}[{}]'.format(node.loc.repr, ', '.join([exp.repr for exp in node.expr_list]))
    
    def visit_ArraySlice(self, node):
        self.visit(node.loc)
        self.visit(node.left)
        self.visit(node.right)
        
        if node.left.type[-1] != int_type:
            print('Error, {} should be int'.format(left.repr))
            
        if node.right.type[-1] != int_type:
            print('Error, {} should be int'.format(right.repr))
            
        node.type = node.loc.type
        node.repr = '{}[{}:{}]'.format(node.loc.repr, node.left.repr, node.right.repr)
        

    def visit_IntegerLiteral(self, node):
        node.type = [int_type]
        node.syn = True
        node.repr = node.const

    def visit_BooleanLiteral(self, node):
        node.type = [bool_type]
        node.repr = node.val
        node.syn = True

    def visit_CharacterLiteral(self, node):
        node.type = [char_type]
        node.repr = "'" + chr(node.val) + "'"
        node.syn = True
        
    def visit_EmptyLiteral(self, node):
        node.type = [pointer_type]
        node.repr = node.val
        node.syn = True
        
    def visit_CharacterStringLiteral(self, node):
        node.type = [char_type, string_type]
        node.repr = node.string
        node.syn = True
        
    def visit_ValueArrayElement(self, node):
        self.visit(node.value)
        
        for exp in node.exp_list:
            self.visit(exp)
            if exp.type[-1] != int_type:
                print('Error, index {} should be int'.format(exp.repr))

        if len(node.exp_list) == 1:
            node.type = node.value.type[0:-1] # element type
        else:
            node.type = node.value.type

        node.repr = '{}[{}]'.format(node.value.repr, ', '.join([exp.repr for exp in node.exp_list]))
    
    def visit_ValueArraySlice(self, node):
        self.visit(node.value)
        self.visit(node.lower)
        self.visit(node.upper)
        
        if node.lower.type[-1] != int_type:
            print('Error, {} should be int'.format(lower.repr))
            
        if node.upper.type[-1] != int_type:
            print('Error, {} should be int'.format(upper.repr))
            
        node.type = node.value.type
        node.repr = '{}[{}:{}]'.format(node.value.repr, node.lower.repr, node.upper.repr)
    
    def visit_ConditionalExpression(self, node):
        self.visit(node.if_expr)
        self.visit(node.then_expr)
        self.visit(node.else_expr)
        self.visit(node.elsif_expr)

        node.type = node.then_expr.type
        node.repr = 'Conditional Expression'
        
    def visit_ElsifExpression(self, node):
        self.visit(node.bool_expr)
        self.visit(node.then_expr)
        self.visit(node.elsif_expr)

        node.type = node.then_expr.type
        node.repr = 'Elsif Expression'

    def visit_Operand0(self, node):
        self.visitBinaryExp(node, node.operand0, node.operand1, node.operator.op)

    def visit_Operand1(self, node):
        self.visitBinaryExp(node, node.operand1, node.operand2, node.operator.op)

    def visit_Operand2(self, node):
        self.visitBinaryExp(node, node.operand2, node.operand3, node.operator.op)

    def visit_Operand3(self, node):
        self.visitUnaryExp(node, node.operator.op, node.operand_or_literal)

    def visit_ReferencedLocation(self, node):
        self.visit(node.location)
        node.type = node.location.type + [pointer_type]
        node.repr = '->' + node.location.repr

    def visit_ActionStatement(self, node):
        if node.label:
            node.label.repr = node.label.name
            if self.environment.find(node.label.name):
                print('Error, {} already declared'.format(node.label.repr))
            self.environment.add_local(node.label.repr, [none_type])
        self.visit(node.action)
        # node.type = node.action.type
        node.repr = node.action.repr

    def visit_AssignmentAction(self, node):
        self.visit(node.expression)
        self.visit(node.location)
        left = node.location
        right = node.expression
        if hasattr(left, 'syn'):
            print("Error, can't reassign constant value {}".format(left.repr))
        if left.type != right.type:
            if left.type and right.type:
                if not(left.type[-1] == right.type[-1] == pointer_type and right.type == [pointer_type]):
                    print("Error, can't assign {} to {}".format(right.type, left.type))
        #node.type = left.type
        node.repr = ' '.join([left.repr, node.assigning_op.op, right.repr])

    def visit_ThenClause(self, node):
        self.environment.push(node)
        node.environment = self.environment
        node.symtab = self.environment.peek()
        for stmt in node.action_statement_list: 
            self.visit(stmt)
        self.environment.pop()
    
    def visit_ElseClause(self, node):
        self.environment.push(node)
        node.environment = self.environment
        node.symtab = self.environment.peek()
        if node.else_type == 'else':
            for stmt in node.bool_or_statement_list: 
                self.visit(stmt)
        else:
            self.visit(node.then_exp)
            self.visit(node.else_exp)
            
        self.environment.pop()

    def visit_DoAction(self, node):
        self.environment.push(node)
        node.environment = self.environment
        node.symtab = self.environment.peek()

        self.visit(node.ctrl_part)

        for stmt in node.action_statement_list: 
            self.visit(stmt)
            
        self.environment.pop()

    def visit_ControlPart(self, node):
        self.environment.push(node)
        node.environment = self.environment
        node.symtab = self.environment.peek()

        self.visit(node.ctrl1)
        self.visit(node.ctrl2)

        self.environment.pop()

    def visit_StepEnumeration(self, node):
        self.visit(node.counter)
        self.visit(node.start)
        self.visit(node.end)
        self.visit(node.step)

        if node.counter.type[-1] != int_type:
            print('Error, loop counter {} must be of type int'.format(node.counter.repr))
        if node.start.type[-1] != int_type:
            print('Error, loop start value {} must be of type int'.format(node.start.repr))
        if node.end.type[-1] != int_type:
            print('Error, loop end value {} must be of type int'.format(node.end.repr))
        if node.step and node.step.type[-1] != int_type:
            print('Error, loop step value {} must be of type int'.format(node.step.repr))

    def visit_RangeEnumeration(self, node):
        self.visit(node.counter)
        self.visit(node.mode)
        if node.mode.type[-1] != int_type:
            print('Error, range value {} must be of type int'.format(node.mode.repr))

    def visit_WhileControl(self, node):
        self.visit(node.bool_exp)
        if node.bool_exp.type[-1] != bool_type:
            print('Error, while control {} must be of type bool'.format(node.bool_exp.repr))

    def visit_ProcedureCall(self, node):
        self.visit(node.name)
        for param in node.param_list: 
            self.visit(param)
            
        node.type = node.name.type
        node.repr = node.name.repr.upper() + '(' + ', '.join([param.repr for param in node.param_list]) + ')'
        ## ajustar tipo e checar parametros

    def visit_BuiltInCall(self, node):
        returnType = {
                'ABS':int_type, 
                'ASC':int_type, 
                'LENGTH':int_type, 
                'LOWER':string_type, 
                'UPPER':string_type, 
                'NUM':int_type,
                'PRINT':int_type,
                'READ':int_type
                }

        # check if one parameter only
        if node.name.upper() in ('ABS', 'NUM', 'LENGTH', 'LOWER', 'UPPER', 'ASC'):
            if len(node.param_list) > 1:
                print('Error, {} expects one argument'.format(node.name.upper()))

        node.type = [returnType[node.name.upper()]]
        for param in node.param_list: 
            self.visit(param)
        node.repr = node.name.upper() + '(' + ', '.join([param.repr for param in node.param_list]) + ')'

    def visit_ProcedureStatement(self, node):

        self.visit(node.procedure_def.result_spec)
        if self.environment.find(node.label.name):
            print('Error, {} name already used'.format(node.label.name))
        self.environment.add_local(node.label.name, node.procedure_def.result_spec.type if node.procedure_def.result_spec else [none_type])

        self.visit(node.procedure_def)
        node.repr = node.label.name + ' : ' + node.procedure_def.repr 

    def visit_ProcedureDefinition(self, node):
        self.environment.push(node)
        node.environment = self.environment
        node.symtab = self.environment.peek()

        for param in node.formal_parameter_list:
            self.visit(param)

        for stmt in node.stmt_list:
            self.visit(stmt)

        self.environment.pop()

        node.type = node.result_spec.type if node.result_spec else none_type
        
        node.repr = 'PROC (' + ', '.join([param.repr for param in node.formal_parameter_list]) + ')'

    def visit_FormalParameter(self, node):
        self.visit(node.param_spec)
        for identifier in node.id_list:
            self.environment.add_local(identifier.name, node.param_spec.type)
        node.repr = ', '.join([identifier.name for identifier in node.id_list]) + ' ' + node.param_spec.repr

    def visit_ParameterSpec(self, node):
        self.visit(node.mode)
        node.type = node.mode.type
        if node.loc:
            node.repr = 'LOC ' + node.mode.repr
        else:
            node.repr = node.mode.repr

    def visit_ResultSpec(self, node):
        self.visit(node.mode)
        if node.loc:
            node.type = node.mode.type + [pointer_type]
            node.repr = 'LOC ' + node.mode.repr
        else:
            node.type = node.mode.type
            node.repr = node.mode.repr
       
        
