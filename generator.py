from visitor import SymbolTable

class memEnvironment(object):
    def __init__(self):
        self.stack = []

        self.root = SymbolTable()
        self.stack.append(self.root)

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
        for i, scope in enumerate(reversed(self.stack)):
            hit = scope.lookup(name)
            if hit is not None:
                return i, hit
        return None

    def find(self, name):
        if name in self.stack[-1]:
            return True
        else:
            return False

class NodeGenerator(object):

    def generate(self, node):
        """
        Execute a method of the form visit_NodeName(node) where
        NodeName is the name of the class of a particular node.
        """
        if node:
            method = 'generate_' + node.__class__.__name__
            generator = getattr(self, method, self.generic_generate)
            return generator(node)
        else:
            return None

    def generic_generate(self,node):

        for child in node.children():
            self.generate(child)
            if hasattr(child, 'type'):
                node.type = child.type
            if hasattr(child, 'repr'):
                node.repr = child.repr
            else:
                node.repr = node.__class__.__name__
            if hasattr(child, 'syn'):
                node.syn = child.syn
 

class Generator(NodeGenerator):

    def __init__(self):
        self.code = []
        self.H = []
        self.environment = memEnvironment()

    def generate_Program(self, node):
        self.environment.push(node)
        self.code.append(('stp',))      
        if node.offset > 0:
            self.code.append(('alc', node.offset))      

            # Generate all of the statements
            for stmt in node.stmt_list: 
                self.generate(stmt)

        if node.offset > 0:
            self.code.append(('dlc', node.offset))      
        
        self.code.append(('end',))
        self.environment.pop()

    def generate_Declaration(self, node):
        #TODO: reference type variable

        for identifier in node.id_list:
            self.environment.add_local(identifier.repr, identifier.offset)
        if node.value is not None:
            if isinstance(node.value, str):
                self.generate(node.value)
                for identifier in node.id_list:
                    self.code.append(('sts', len(self.H)))      
            else:
                for identifier in node.id_list:
                    self.generate(node.value)
                    self.code.append(tuple('stv', *self.environment.lookup(identifier)))


    def generate_IntegerLiteral(self, node):
        self.code.append(('ldc', node.const))   

    def generate_BooleanLiteral(self, node):
        if node.val.lower() == 'true':
            self.code.append(('ldc', True))        
        else:
            self.code.append(('ldc', False))        

    def generate_CharacterLiteral(self, node):
        self.code.append(('ldc', node.val))     

    # TODO: check
    def generate_CharacterStringLiteral(self, node):
        #self.code.append(('ldc', len(self.H)))  
        self.H.append(node.val)

    # TODO: 3 types of print
                

    '''
    def generate_ProcedureCall(self, node):
        if node.offset > 0:
            self.code.append(('alc', node.offset))      

            # load parameters
            for param, loc in reversed(node.parameter_types): 
                if loc or array_type in param:
                    self.code.append(('ldr', node.))      
                else:
                    self.code.append(('ldc', node.))      
            
        self.code.append(('enf', node.))      
    '''



'''
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

    def generateBinaryExp(self, node, left, right, op):
        self.generate(left)
        self.generate(right)
        if op == None:
            node.type = left.type if left is not None else right.type
            node.repr = left.repr if left is not None else right.repr
            return 

        node.type = self.raw_type_binary(node, op, left, right)
        
        if hasattr(left, 'syn') and hasattr(right, 'syn'):
            node.syn = True
        node.repr = ' '.join([left.repr, op, right.repr])
    
    def generateUnaryExp(self, node, op, val):
        self.generate(val)
        if op == None:
            node.type = val.type
            node.repr = val.repr
            return 

        node.type = self.raw_type_unary(node, op, val)
        if hasattr(val, 'syn'):
            node.syn = True
        node.repr = ''.join([op, val.repr])

    def generate_Program(self, node):
        
        self.environment.push(node)
        node.environment = self.environment
        node.symtab = self.environment.peek()
        # Visit all of the statements
        for stmt in node.stmt_list: 
            self.generate(stmt)


    def generate_Identifier(self, node):
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
        
    def generate_SynonymDefinition(self, node):
        self.generate(node.mode)
        self.generate(node.constant_exp)
        if not hasattr(node.constant_exp, 'syn'):
            print('Error at line {}, in synonym definition, {} is not constant'.format(node.lineno, node.constant_exp.repr))

        if node.mode is not None:
            if node.mode.type != node.constant_exp.type:
                if not (node.mode.type[-1] == pointer_type and node.constant_exp.type == [pointer_type]):
                    print('Error at line {}, {} is not {}'.format(node.lineno, node.constant_exp.repr, node.mode.repr))
            
        for identifier in node.id_list:
            identifier.type = node.constant_exp.type + [syn_type]
            identifier.repr = identifier.name
            if self.environment.find(identifier.repr):
                print('Error at line {}, {} already exists'.format(node.lineno, identifier.repr))
            self.environment.add_root(identifier.repr, identifier.type)
            
    def generate_ModeDefinition(self, node):
        self.generate(node.mode)

        for identifier in node.id_list:
            identifier.type = node.mode.type
            identifier.repr = identifier.name
            if self.environment.find(identifier.repr):
                print('Error at line {}, {} already exists'.format(node.lineno, identifier.repr))
            self.environment.add_local(identifier.repr, identifier.type)

    def generate_IntegerMode(self, node):
        node.type = [int_type]
        node.repr = 'INT'

    def generate_BooleanMode(self, node):
        node.type = [bool_type]
        node.repr = 'BOOL'

    def generate_CharacterMode(self, node):
        node.type = [char_type]
        node.repr = 'CHAR'

    def generate_DiscreteRangeMode(self, node):
        self.generate(node.name)
        self.generate(node.literal_range)
        node.type = node.name.type
        node.repr = node.name.repr + '(' + node.literal_range.repr + ')'

    def generate_LiteralRange(self, node):
        self.generate(node.lower)
        self.generate(node.upper)
        if node.lower.type[-1] != int_type:
            print('Error at line {}, literal range lower bound cannot be {}'.format(node.lineno, node.lower.type))
        if node.upper.type[-1] != int_type:
            print('Error at line {}, literal range upper bound cannot be {}'.format(node.lineno, node.upper.type))

        node.type = node.lower.type
        node.repr = node.lower.repr + ':' + node.upper.repr

    def generate_ReferenceMode(self, node):
        self.generate(node.mode)
        node.type = node.mode.type + [pointer_type]
        node.repr = "REF " + node.mode.repr
        
    def generate_StringMode(self, node):
        self.generate(node.length)
        if node.length.type[-1] != int_type:
            print('Error at line {}, string length cannot be {}'.format(node.lineno, node.length.type[-1]))

        node.type = [char_type, string_type]
        node.repr = 'CHARS [{}]'.format(node.length.repr)

    def generate_ArrayMode(self, node):
        self.generate(node.mode)
        node.type = []
        node.type += node.mode.type
        
        for index_mode in node.index_mode_list:
            self.generate(index_mode)
            node.type +=  [array_type]
        
        node.repr = 'ARRAY [{}] {}'.format(', '.join([index_mode.repr for index_mode in node.index_mode_list]), node.mode.repr)

    def generate_DereferencedReference(self, node):
        self.generate(node.loc)
        node.type = node.loc.type[0:-1]
        node.repr = node.loc.repr + '->'
    
    def generate_ArrayElement(self, node):
        self.generate(node.loc)
        
        if node.loc.type == [char_type, string_type]:
            if len(node.expr_list) != 1:
                print("Error at line {}, String {} must have 1 dimension".format(node.lineno, node.loc.repr))
                    
        for exp in node.expr_list:
            self.generate(exp)
            if exp.type[-1] != int_type:
                print('Error at line {}, index {} should be int'.format(node.lineno, exp.repr))

        if len(node.expr_list) >= 1:
            node.type = node.loc.type[0:-len(node.expr_list)] # element type
        if len(node.type) == 0:
            print("Error at line {}, {} is not array".format(node.lineno, node.loc.repr))
        node.repr = '{}[{}]'.format(node.loc.repr, ', '.join([exp.repr for exp in node.expr_list]))
    
    def generate_ArraySlice(self, node):
        self.generate(node.loc)
        self.generate(node.left)
        self.generate(node.right)
        
        if node.left.type[-1] != int_type:
            print('Error at line {}, {} should be int'.format(node.lineno, left.repr))
            
        if node.right.type[-1] != int_type:
            print('Error at line {}, {} should be int'.format(node.lineno, right.repr))
            
        node.type = node.loc.type
        node.repr = '{}[{}:{}]'.format(node.loc.repr, node.left.repr, node.right.repr)
        

    def generate_IntegerLiteral(self, node):
        node.type = [int_type]
        node.syn = True
        node.repr = node.const

    def generate_BooleanLiteral(self, node):
        node.type = [bool_type]
        node.repr = node.val
        node.syn = True

    def generate_CharacterLiteral(self, node):
        node.type = [char_type]
        node.repr = "'" + chr(node.val) + "'"
        node.syn = True
        
    def generate_EmptyLiteral(self, node):
        node.type = [pointer_type]
        node.repr = node.val
        node.syn = True
        
    def generate_CharacterStringLiteral(self, node):
        node.type = [char_type, string_type]
        node.repr = node.string
        node.syn = True
        
    def generate_ValueArrayElement(self, node):
        self.generate(node.value)
        
        for exp in node.exp_list:
            self.generate(exp)
            if exp.type[-1] != int_type:
                print('Error at line {}, index {} should be int'.format(node.lineno, exp.repr))

        if len(node.exp_list) == 1:
            node.type = node.value.type[0:-1] # element type
        else:
            node.type = node.value.type

        node.repr = '{}[{}]'.format(node.value.repr, ', '.join([exp.repr for exp in node.exp_list]))
    
    def generate_ValueArraySlice(self, node):
        self.generate(node.value)
        self.generate(node.lower)
        self.generate(node.upper)
        
        if node.lower.type[-1] != int_type:
            print('Error at line {}, {} should be int'.format(node.lineno, lower.repr))
            
        if node.upper.type[-1] != int_type:
            print('Error at line {}, {} should be int'.format(node.lineno, upper.repr))
            
        node.type = node.value.type
        node.repr = '{}[{}:{}]'.format(node.value.repr, node.lower.repr, node.upper.repr)
    
    def generate_ConditionalExpression(self, node):
        self.generate(node.if_expr)
        self.generate(node.then_expr)
        self.generate(node.else_expr)
        self.generate(node.elsif_expr)

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
        
    def generate_ElsifExpression(self, node):
        self.generate(node.bool_expr)
        self.generate(node.then_expr)
        self.generate(node.elsif_expr)
            
        if not(node.bool_expr.type == [bool_type] ):
            print("Error at line {}, expression {} is not type bool".format(node.lineno, node.bool_expr.repr))
        
        if (node.elsif_expr != None):
            if not(node.then_expr.type == node.elsif_expr.type ):
                print("Error at line {}, expressions {} and {} are not same type".format(node.lineno, node.then_expr.repr, node.elsif_expr.repr))
        
        
        node.type = node.then_expr.type
        node.repr = 'Elsif Expression'

    def generate_Operand0(self, node):
        self.generateBinaryExp(node, node.operand0, node.operand1, node.operator.op)

    def generate_Operand1(self, node):
        self.generateBinaryExp(node, node.operand1, node.operand2, node.operator.op)

    def generate_Operand2(self, node):
        self.generateBinaryExp(node, node.operand2, node.operand3, node.operator.op)

    def generate_Operand3(self, node):
        self.generateUnaryExp(node, node.operator.op, node.operand_or_literal)

    def generate_ReferencedLocation(self, node):
        self.generate(node.location)
        node.type = node.location.type + [pointer_type]
        node.repr = '->' + node.location.repr

    def generate_ActionStatement(self, node):
        if node.label:
            node.label.repr = node.label.name
            if self.environment.find(node.label.name):
                print('Error at line {}, {} already declared'.format(node.lineno, node.label.repr))
            self.environment.add_local(node.label.repr, [none_type])
        self.generate(node.action)
        # node.type = node.action.type
        node.repr = node.action.repr

    def generate_AssignmentAction(self, node):
        self.generate(node.expression)
        self.generate(node.location)
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

    def generate_ThenClause(self, node):
        self.environment.push(node)
        node.environment = self.environment
        node.symtab = self.environment.peek()
        for stmt in node.action_statement_list: 
            self.generate(stmt)
        self.environment.pop()
    
    def generate_ElseClause(self, node):
        self.environment.push(node)
        node.environment = self.environment
        node.symtab = self.environment.peek()
        if node.else_type == 'else':
            for stmt in node.bool_or_statement_list: 
                self.generate(stmt)
        else:
            self.generate(node.then_exp)
            self.generate(node.else_exp)
            
        self.environment.pop()

    def generate_DoAction(self, node):
        self.environment.push(node)
        node.environment = self.environment
        node.symtab = self.environment.peek()

        self.generate(node.ctrl_part)

        for stmt in node.action_statement_list: 
            self.generate(stmt)
            
        self.environment.pop()

    def generate_ControlPart(self, node):
        self.environment.push(node)
        node.environment = self.environment
        node.symtab = self.environment.peek()

        self.generate(node.ctrl1)
        self.generate(node.ctrl2)

        self.environment.pop()

    def generate_StepEnumeration(self, node):
        self.generate(node.counter)
        self.generate(node.start)
        self.generate(node.end)
        self.generate(node.step)

        if node.counter.type[-1] != int_type:
            print('Error at line {}, loop counter {} must be of type int'.format(node.lineno, node.counter.repr))
        if node.start.type[-1] != int_type:
            print('Error at line {}, loop start value {} must be of type int'.format(node.lineno, node.start.repr))
        if node.end.type[-1] != int_type:
            print('Error at line {}, loop end value {} must be of type int'.format(node.lineno, node.end.repr))
        if node.step and node.step.type[-1] != int_type:
            print('Error at line {}, loop step value {} must be of type int'.format(node.lineno, node.step.repr))

    def generate_RangeEnumeration(self, node):
        self.generate(node.counter)
        self.generate(node.mode)
        if node.mode.type[-1] != int_type:
            print('Error at line {}, range value {} must be of type int'.format(node.lineno, node.mode.repr))

    def generate_WhileControl(self, node):
        self.generate(node.bool_exp)
        if node.bool_exp.type[-1] != bool_type:
            print('Error at line {}, while control {} must be of type bool'.format(node.lineno, node.bool_exp.repr))

    def generate_ProcedureCall(self, node):
        self.generate(node.name)

        for param in node.param_list: 
            self.generate(param)
            
        node.type = node.name.type
        node.repr = node.name.repr.upper() + '(' + ', '.join([param.repr for param in node.param_list]) + ')'
        ## checar parametros

    def generate_BuiltInCall(self, node):

        node.type = [int_type]
        for param in node.param_list: 
            self.generate(param)
        node.repr = node.name.upper() + '(' + ', '.join([param.repr for param in node.param_list]) + ')'

    def generate_ProcedureStatement(self, node):

        self.generate(node.procedure_def.result_spec)
        if self.environment.find(node.label.name):
            print('Error at line {}, {} name already used'.format(node.lineno, node.label.name))
        self.environment.add_local(node.label.name, node.procedure_def.result_spec.type if node.procedure_def.result_spec else [none_type])

        self.generate(node.procedure_def)
        node.repr = node.label.name + ' : ' + node.procedure_def.repr 

    def generate_ProcedureDefinition(self, node):
        self.environment.push(node)
        node.environment = self.environment
        node.symtab = self.environment.peek()

        for param in node.formal_parameter_list:
            self.generate(param)

        for stmt in node.stmt_list:
            self.generate(stmt)

        self.environment.pop()

        node.type = node.result_spec.type if node.result_spec else none_type
        
        node.repr = 'PROC (' + ', '.join([param.repr for param in node.formal_parameter_list]) + ')'

    def generate_FormalParameter(self, node):
        self.generate(node.param_spec)
        for identifier in node.id_list:
            self.environment.add_local(identifier.name, node.param_spec.type)
        node.repr = ', '.join([identifier.name for identifier in node.id_list]) + ' ' + node.param_spec.repr

    def generate_ParameterSpec(self, node):
        self.generate(node.mode)
        node.type = node.mode.type
        if node.loc:
            node.repr = 'LOC ' + node.mode.repr
        else:
            node.repr = node.mode.repr

    def generate_ResultSpec(self, node):
        self.generate(node.mode)
        node.type = node.mode.type
        if node.loc:
            node.repr = 'LOC ' + node.mode.repr
        else:
            node.repr = node.mode.repr
''' 
