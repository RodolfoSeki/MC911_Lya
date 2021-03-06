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
string_type = Type("string", [], ['+', '==', '!=', '&'])
pointer_type = Type("addr", [], ['==', '!='])
none_type = Type("none", [], [])
array_type = Type("array", [], ['==', '!='])
syn_type = Type("syn", [], [])

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

class Environment(object):
    def __init__(self):
        self.stack = []
        self.function_stack = []

        self.root = SymbolTable()
        self.stack.append(self.root)

        self.function = SymbolTable()
        self.function_stack.append(self.function)
        
        
    def push(self, enclosure):
        self.stack.append(SymbolTable(decl=enclosure))
        self.function_stack.append(SymbolTable(decl=enclosure))
        #print('New scope for {}'.format(enclosure.__class__.__name__))

    def pop(self):
        self.stack.pop()
        self.function_stack.pop()
        #print ('End scope')

    def peek(self):
        return self.stack[-1]

    def scope_level(self):
        return len(self.stack)

    def add_local(self, name, value):
        self.peek().add(name, value)
        #print('Name {} with type {} was added to scope {}'.format(name, value, self.scope_level()))

    def add_root(self, name, value):
        self.root.add(name, value)

    def add_function(self, name, value):
        self.function_stack[-2].add(name, value)

    def lookup_function(self, name):
        for scope in reversed(self.function_stack):
            hit = scope.lookup(name)
            if hit is not None:
                return hit

        return None

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
        for child in node.children():
            self.visit(child)
            if hasattr(child, 'type'):
                node.type = child.type
            #if hasattr(child, 'offset'):
            #    node.offset = child.offset
            if hasattr(child, 'size'):
                node.size = child.size
            if hasattr(child, 'repr'):
                node.repr = child.repr
            #else:
            #    node.repr = node.__class__.__name__
            if hasattr(child, 'syn'):
                node.syn = child.syn
            if hasattr(child, 'syn_val'):
                node.syn_val = child.syn_val

    
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
        self.offset = []
        self.syn_values = {}
        self.label = 1

    def raw_type_unary(self, node, op, val):
        if op not in val.type[-1].unaryop:
            print('Error at line {}, {} is not supported for {}'.format(node.lineno, op, val.type[-1]))
        return val.type

    def raw_type_binary(self, node, op, left, right):
        if left.type != right.type:
            if not( left.type[-1] == right.type[-1] == pointer_type and right.type == [pointer_type]):
                print('Error at line {}, {} {} {} is not supported'.format(node.lineno, left.type[-1] , op, right.type[-1]))
                return left.type
        if op not in left.type[-1].binop:
            print('Error at line {}, {} is not supported for {}'.format(node.lineno, op, left.type[-1]))
        if op not in right.type[-1].binop:
            print('Error at line {}, {} is not supported for {}'.format(node.lineno, op, right.type[-1]))
        if op.upper() in ('&&', '||', '>', '<', '>=', '<=', 'IN', '!=', '=='):
            return [bool_type]
        return left.type

    def visitBinaryExp(self, node, left, right, op):
        self.visit(left)
        self.visit(right)
        
        if left.repr in self.syn_values:
            left.syn_val = self.syn_values[left.repr]
        if right.repr in self.syn_values:
            right.syn_val = self.syn_values[right.repr]
        
        
        if (hasattr(left, 'syn') or hasattr(left, 'syn_val')) and (hasattr(right, 'syn') or hasattr(right, 'syn_val')):
            has_syn_val = True
            if hasattr(left, 'syn_val'):
                left_val = left.syn_val
            elif left.repr.isdigit():
                left_val = int(left.repr)
            else:
                has_syn_val = False
              
            if hasattr(right, 'syn_val'):
                right_val = right.syn_val
            elif right.repr.isdigit():
                right_val = int(right.repr)
            else:
                has_syn_val = False
            
            if has_syn_val:
                if op == '+':
                    node.syn_val = left_val + right_val   
                elif op == '-':
                    node.syn_val = left_val + right_val
                elif op == '*':
                    node.syn_val = left_val + right_val
                elif op == '/':
                    node.syn_val = left_val + right_val
                elif op == '%':
                    node.syn_val = left_val % right_val
        
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
        self.offset.append(0) 
        node.scope = self.environment.scope_level()
        for stmt in node.stmt_list: 
            self.visit(stmt)
        node.offset = self.offset[-1]

    def visit_Declaration(self, node):
        self.visit(node.mode)
        self.visit(node.value)
        if node.value is not None:
            if node.mode.type != node.value.type:
                if not(node.mode.type[-1] == node.value.type[-1] == pointer_type and node.value.type == [pointer_type]):
                    print('Error at line {}, {} is not {}'.format(node.lineno, node.value.repr, node.mode.repr))

        for identifier in node.id_list:
            identifier.offset = self.offset[-1]
            self.offset[-1] += node.mode.size

            identifier.type = node.mode.type
            identifier.repr = identifier.name
            if self.environment.find(identifier.repr):
                print('Error at line {}, {} already declared'.format(node.lineno, identifier.repr))
            self.environment.add_local(identifier.repr, node.mode.type)

    def visit_Identifier(self, node):
        node.repr = node.name
        node.type = self.environment.lookup(node.repr)
        
        if node.type is None:
            print('Error at line {}, {} used but not declared'.format(node.lineno, node.repr))
            node.type = [none_type]
            self.environment.add_root(node.name, node.type)
            return
        if node.type[-1] == syn_type:
            node.syn = True
            node.type = node.type[0:-1]
        
    def visit_SynonymDefinition(self, node):
        self.visit(node.mode)
        self.visit(node.constant_exp)
        
        
        if not hasattr(node.constant_exp, 'syn'):
            print('Error at line {}, in synonym definition, {} is not constant'.format(node.lineno, node.constant_exp.repr))

        if node.mode is not None:
            if node.mode.type != node.constant_exp.type:
                if not (node.mode.type[-1] == pointer_type and node.constant_exp.type == [pointer_type]):
                    print('Error at line {}, {} is not {}'.format(node.lineno, node.constant_exp.repr, node.mode.repr))
            
        for identifier in node.id_list:
            identifier.type = node.constant_exp.type + [syn_type]
            identifier.repr = identifier.name
            if hasattr(node.constant_exp, 'syn_val'):
                self.syn_values[identifier.name] = node.constant_exp.syn_val
            else:
                self.syn_values[identifier.name] = int(node.constant_exp.expr.repr) 
                
            if self.environment.find(identifier.repr):
                print('Error at line {}, {} already exists'.format(node.lineno, identifier.repr))
            self.environment.add_root(identifier.repr, identifier.type)
            
    def visit_ModeDefinition(self, node):
        self.visit(node.mode)

        for identifier in node.id_list:
            identifier.type = node.mode.type
            identifier.size = node.mode.size
            identifier.repr = identifier.name
            if self.environment.find(identifier.repr):
                print('Error at line {}, {} already exists'.format(node.lineno, identifier.repr))
            self.environment.add_local(identifier.repr, (identifier.type, identifier.size))

    def visit_Mode(self, node):
        self.visit(node.mode)
        if hasattr(node.mode, 'size'):
            node.type = node.mode.type
            node.size = node.mode.size
        else:
            node.type, node.size = self.environment.lookup(node.mode.name)
        node.repr = node.mode.repr

    def visit_IntegerMode(self, node):
        node.type = [int_type]
        node.repr = 'INT'
        node.size = 1

    def visit_BooleanMode(self, node):
        node.type = [bool_type]
        node.repr = 'BOOL'
        node.size = 1

    def visit_CharacterMode(self, node):
        node.type = [char_type]
        node.repr = 'CHAR'
        node.size = 1

    def visit_DiscreteRangeMode(self, node):
        self.visit(node.name)
        self.visit(node.literal_range)
        node.type = node.name.type
        node.repr = node.name.repr + '(' + node.literal_range.repr + ')'
        node.size = 1
        node.lower = node.literal_range.lower
        node.upper = node.literal_range.upper

    def visit_LiteralRange(self, node):
        self.visit(node.lower)
        self.visit(node.upper)
        
        if node.lower.type[-1] != int_type:
            print('Error at line {}, literal range lower bound cannot be {}'.format(node.lineno, node.lower.type))
        if node.upper.type[-1] != int_type:
            print('Error at line {}, literal range upper bound cannot be {}'.format(node.lineno, node.upper.type))
        
        if node.upper.repr.isdigit():
          upper_val = int(node.upper.repr)
        elif node.upper.repr in self.syn_values:
          upper_val = self.syn_values[node.upper.repr]
        else:
          upper_val = int(node.upper.syn_val)
        
        node.size = 1 + upper_val - int(node.lower.repr)
        node.type = node.lower.type
        node.repr = node.lower.repr + ':' + str(upper_val)
        

    def visit_ReferenceMode(self, node):
        self.visit(node.mode)
        node.type = node.mode.type + [pointer_type]
        node.repr = "REF " + node.mode.repr
        node.size = 1
        
    def visit_StringMode(self, node):
        self.visit(node.length)
        if node.length.type[-1] != int_type:
            print('Error at line {}, string length cannot be {}'.format(node.lineno, node.length.type[-1]))

        node.size = node.length.const
        node.type = [char_type, string_type]
        node.repr = 'CHARS [{}]'.format(node.length.repr)

    def visit_ArrayMode(self, node):
        self.visit(node.mode)
        node.type = []
        node.type += node.mode.type
        node.size = node.mode.size
        node.sizes = [node.size]

        for index_mode in reversed(node.index_mode_list):
            self.visit(index_mode)
            node.type += [array_type]
            node.size *= index_mode.size
            node.sizes.append(node.size)
        node.sizes.pop()
        node.sizes = node.sizes[::-1]
        
        node.repr = 'ARRAY [{}] {}'.format(', '.join([index_mode.repr for index_mode in node.index_mode_list]), node.mode.repr)

    def visit_DereferencedReference(self, node):
        self.visit(node.loc)
        node.type = node.loc.type[0:-1]
        node.repr = node.loc.repr + '->'
    
    def visit_ArrayElement(self, node):
        self.visit(node.loc)
        
        if node.loc.type == [char_type, string_type]:
            if len(node.expr_list) != 1:
                print("Error at line {}, String {} must have 1 dimension".format(node.lineno, node.loc.repr))
                    
        for exp in node.expr_list:
            self.visit(exp)
            if exp.type[-1] != int_type:
                print('Error at line {}, index {} should be int'.format(node.lineno, exp.repr))

        if len(node.expr_list) >= 1:
            node.type = node.loc.type[0:-len(node.expr_list)] # element type
        if len(node.type) == 0:
            print("Error at line {}, {} is not array".format(node.lineno, node.loc.repr))
        node.repr = '{}[{}]'.format(node.loc.repr, ', '.join([exp.repr for exp in node.expr_list]))
    
    def visit_ArraySlice(self, node):
        self.visit(node.loc)
        self.visit(node.left)
        self.visit(node.right)
        
        if node.left.type[-1] != int_type:
            print('Error at line {}, {} should be int'.format(node.lineno, left.repr))
            
        if node.right.type[-1] != int_type:
            print('Error at line {}, {} should be int'.format(node.lineno, right.repr))
            
        node.type = node.loc.type
        node.repr = '{}[{}:{}]'.format(node.loc.repr, node.left.repr, node.right.repr)
        

    def visit_IntegerLiteral(self, node):
        node.type = [int_type]
        node.syn = True
        node.repr = str(node.const)

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
                print('Error at line {}, index {} should be int'.format(node.lineno, exp.repr))

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
            print('Error at line {}, {} should be int'.format(node.lineno, lower.repr))
            
        if node.upper.type[-1] != int_type:
            print('Error at line {}, {} should be int'.format(node.lineno, upper.repr))
            
        node.type = node.value.type
        node.repr = '{}[{}:{}]'.format(node.value.repr, node.lower.repr, node.upper.repr)
    
    def visit_ConditionalExpression(self, node):

        node.next = self.label
        self.label += 1

        for child in node.children():
            self.visit(child)

        node.exit = self.label
        self.label += 1

        '''
        self.visit(node.if_expr)
        self.visit(node.then_expr)
        self.visit(node.else_expr)
        self.visit(node.elsif_expr)
        '''

        node.type = node.then_expr.type
        
        if not(node.if_expr.type == [bool_type]):
            print('Error at line {}, condition control {} must be of type bool'.format(node.lineno, node.if_expr.repr))
        
        if (node.elsif_expr != None):
            if not(node.then_expr.type == node.else_expr.type == node.elsif_expr.type):
                print("Error at line {}, expressions {}, {} and {} are not same type".format(node.lineno, node.then_expr.repr, node.else_expr.repr, node.elsif_expr.repr))
        else:
            if not(node.then_expr.type == node.else_expr.type):
                print("Error at line {}, expressions {} and {} are not same type".format(node.lineno, node.then_expr.repr, node.else_expr.repr))
        node.repr = 'Conditional Expression'
        
    def visit_ElsifExpression(self, node):

        node.next = self.label
        self.label += 1

        self.visit(node.bool_expr)
        self.visit(node.then_expr)
        self.visit(node.elsif_expr)

        if not(node.bool_expr.type == [bool_type] ):
            print("Error at line {}, expression {} is not type bool".format(node.lineno, node.bool_expr.repr))
        
        if (node.elsif_expr != None):
            if not(node.then_expr.type == node.elsif_expr.type ):
                print("Error at line {}, expressions {} and {} are not same type".format(node.lineno, node.then_expr.repr, node.elsif_expr.repr))
        
        
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
                print('Error at line {}, {} already declared'.format(node.lineno, node.label.repr))
            self.environment.add_local(node.label.repr, [none_type])
        self.visit(node.action)
        # node.type = node.action.type
        #node.repr = node.action.repr

    def visit_AssignmentAction(self, node):
        self.visit(node.expression)
        self.visit(node.location)
        left = node.location
        right = node.expression
        if hasattr(left, 'syn'):
            print("Error at line {}, can't reassign constant value {}".format(node.lineno, left.repr))
        if left.type != right.type:
            if left.type and right.type:
                if not(left.type[-1] == right.type[-1] == pointer_type and right.type == [pointer_type]):
                    print("Error at line {}, can't assign {} of type {} to {} of type {}".format(node.lineno, right.repr, right.type, left.repr, left.type))
        if(len(node.assigning_op.op) == 2):
            if(node.assigning_op.op[0] not in right.type[-1].binop):
                print('Error at line {}, {} is not supported for {}'.format(node.lineno, node.assigning_op.op, right.type[-1]))
        #node.type = left.type
        node.repr = ' '.join([left.repr, node.assigning_op.op, right.repr])

    def visit_IfAction(self, node):
        node.next = self.label
        self.label += 1

        for child in node.children():
            self.visit(child)

        node.exit = self.label
        self.label += 1

    def visit_ElseClause(self, node):
        node.next = self.label
        self.label += 1

        if node.else_type == 'else':
            for stmt in node.bool_or_statement_list: 
                self.visit(stmt)
        else:
            self.visit(node.then_exp)
            self.visit(node.else_exp)

    def visit_DoAction(self, node):

        node.start = self.label
        self.label += 1

        self.visit(node.ctrl_part)
        for stmt in node.action_statement_list: 
            self.visit(stmt)

        node.exit = self.label
        node.ctrl_part.exit = node.exit
        self.label += 1

    def visit_ControlPart(self, node):
        for child in node.children():
            self.visit(child)
            if hasattr(child, 'initialized'):
                node.initialized = child.initialized

    def visit_ForControl(self, node):
        self.visit(node.iteration)

        node.counter = node.iteration.counter
        node.start = node.iteration.start
        node.step = node.iteration.step
        node.end = node.iteration.end
        node.initialized = node.iteration.initialized
        node.decreasing = node.iteration.decreasing
        

    def visit_StepEnumeration(self, node):
        self.visit(node.counter)
        self.visit(node.start)
        self.visit(node.end)
        self.visit(node.step)
        node.initialized = False

        if node.counter.type[-1] != int_type:
            print('Error at line {}, loop counter {} must be of type int'.format(node.lineno, node.counter.repr))
        if node.start.type[-1] != int_type:
            print('Error at line {}, loop start value {} must be of type int'.format(node.lineno, node.start.repr))
        if node.end.type[-1] != int_type:
            print('Error at line {}, loop end value {} must be of type int'.format(node.lineno, node.end.repr))
        if node.step and node.step.type[-1] != int_type:
            print('Error at line {}, loop step value {} must be of type int'.format(node.lineno, node.step.repr))

    def visit_RangeEnumeration(self, node):
        self.visit(node.counter)
        self.visit(node.mode)

        node.initialized = False
        node.start, node.end = node.mode.lower, node.mode.upper
        node.lower = node.mode.lower
        if node.decreasing: # swap
            node.start, node.end = node.end, node.start

        node.step = None
        if node.mode.type[-1] != int_type:
            print('Error at line {}, range value {} must be of type int'.format(node.lineno, node.mode.repr))

    def visit_WhileControl(self, node):
        self.visit(node.bool_exp)
        if node.bool_exp.type[-1] != bool_type:
            print('Error at line {}, while control {} must be of type bool'.format(node.lineno, node.bool_exp.repr))

    def visit_ProcedureCall(self, node):
        self.visit(node.name)
        node.parameter_types, node.result_spec = self.environment.lookup_function(node.name.repr)
        if len(node.param_list) != len(node.parameter_types):
            print('Error at line {}, function {} expects {} arguments'.format(node.lineno, node.name, len(node.parameter_types)))

        for param, param_type in zip(node.param_list, node.parameter_types):
            self.visit(param)
            if param.type != param_type[0]:
                print('Error at line {}, argument {} type {} expected to be {}'.format(node.lineno, param.repr, param.type, param_type[0]))
            
        node.type = node.name.type
        node.repr = node.name.repr + '(' + ', '.join([param.repr for param in node.param_list]) + ')'

    def visit_BuiltInCall(self, node):

        if node.name in ['upper', 'lower']:
          node.type = [char_type]
        else:
          node.type = [int_type]
          
        for param in node.param_list: 
            self.visit(param)
        node.repr = node.name.upper() + '(' + ', '.join([param.repr for param in node.param_list]) + ')'

    def visit_ProcedureStatement(self, node):

        self.visit(node.procedure_def.result_spec)
        if self.environment.find(node.label.name):
            print('Error at line {}, {} name already used'.format(node.lineno, node.label.name))
        self.environment.add_local(node.label.name, node.procedure_def.result_spec.type if node.procedure_def.result_spec else [none_type])

        node.procedure_def.name = node.label.name
        self.visit(node.procedure_def)

        #node.offset = node.procedure_def.offset
        node.repr = node.label.name + ' : ' + node.procedure_def.repr 

    def visit_ProcedureDefinition(self, node):
        self.environment.push(node)
        self.offset.append(0)
        node.environment = self.environment

        node.start = self.label
        self.label += 1

        # tuples with type and boolean Loc and id_name
        node.param_types = []

        for param in node.formal_parameter_list:
            self.visit(param)
            for ident in param.id_list:
                node.param_types += [(param.type, param.loc, ident.name)]

        self.environment.add_function(node.name, (node.param_types, node.result_spec))

        for stmt in node.stmt_list:
            self.visit(stmt)

        node.offset = self.offset[-1]
        self.environment.pop()
        self.offset.pop()

        node.ret = self.label
        self.label += 1
        node.exit = self.label
        self.label += 1

        node.type = node.result_spec.type if node.result_spec else none_type
        
        node.repr = 'PROC (' + ', '.join([param.repr for param in node.formal_parameter_list]) + ')'

    def visit_FormalParameter(self, node):
        self.visit(node.param_spec)
        node.type = node.param_spec.type
        node.loc = node.param_spec.loc
        for identifier in node.id_list:
            self.environment.add_local(identifier.name, node.type)
        
        node.repr = ', '.join([identifier.name for identifier in node.id_list]) + ' ' + node.param_spec.repr

    def visit_ParameterSpec(self, node):
        self.visit(node.mode)
        node.type = node.mode.type
        if node.loc:
            node.repr = 'LOC ' + node.mode.repr
            node.loc = True
        else:
            node.repr = node.mode.repr
            node.loc = False

    def visit_ResultSpec(self, node):
        self.visit(node.mode)
        node.type = node.mode.type
        if node.loc:
            node.repr = 'LOC ' + node.mode.repr
            node.loc = True
        else:
            node.repr = node.mode.repr
            node.loc = False
       
        
