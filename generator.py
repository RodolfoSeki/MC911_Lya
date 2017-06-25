from visitor import *

class memEnvironment(object):
    def __init__(self):
        self.stack = []
        self.modeStack = []

    def push(self, enclosure):
        self.stack.append(SymbolTable(decl=enclosure))
        self.modeStack.append(SymbolTable(decl=enclosure))

    def pop(self):
        self.stack.pop()
        self.modeStack.pop()

    def peek(self):
        return self.stack[-1]

    def scope_level(self):
        return len(self.stack) - 1

    def add_local(self, name, value):
        self.peek().add(name, value)
        print("Added {} = {}".format(name, value))
        print(self.stack)

    def add_mode(self, name, mode):
        self.modeStack[-1].add(name, mode)

    def lookup(self, name):
        for i, scope in enumerate(reversed(self.stack), 1):
            hit = scope.lookup(name)
            if hit is not None:
                return self.scope_level() - i + 1, hit
        print('Stack state')
        print(self.stack)
        print('Looking for ' + name)
        return None

    def lookup_mode(self, name):
        for scope in reversed(self.modeStack):
            hit = scope.lookup(name)
            if hit is not None:
                return hit
        print('Mode Stack state')
        print(self.modeStack)
        print('Looking for ' + name)
        return None

    def find(self, name):
        if name in self.stack[-1]:
            return True
        else:
            return False

class NodeGenerator(object):

    def generate(self, node):
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
            self.environment.add_mode(identifier.repr, node.mode)

        if node.value is not None:
            if node.mode.type == [char_type, string_type]:
                self.generate(node.value)
                for identifier in node.id_list:
                    disp, off = self.environment.lookup(identifier.repr)
                    self.code.append(('ldr', disp, off))
                    self.code.append(('sts', len(self.H) - 1))      
            else:
                for identifier in node.id_list:
                    self.generate(node.value)
                    disp, off = self.environment.lookup(identifier.repr)
                    self.code.append(('stv', disp, off))


    def generate_IntegerLiteral(self, node):
        self.code.append(('ldc', node.const))   

    def generate_BooleanLiteral(self, node):
        if node.val.lower() == 'true':
            self.code.append(('ldc', True))        
        else:
            self.code.append(('ldc', False))        

    def generate_CharacterLiteral(self, node):
        self.code.append(('ldc', node.val))     

    def generate_CharacterStringLiteral(self, node):
        #self.code.append(('ldc', len(self.H)))  
        self.H.append(eval(node.string))

    def generateBinaryExp(self, node, left, right, op):
        self.generate(left)
        self.generate(right)
        if op == None:
            return 
        if op == '+':
            self.code.append(('add',))     
        elif op == '-':
            self.code.append(('sub',))     
        elif op == '*':
            self.code.append(('mul',))     
        elif op == '/':
            self.code.append(('div',))     
        elif op == '%':
            self.code.append(('mod',))     
        elif op == '<':
            self.code.append(('les',))     
        elif op == '<=':
            self.code.append(('leq',))     
        elif op == '>':
            self.code.append(('grt',))     
        elif op == '>=':
            self.code.append(('gre',))     
        # TODO: array e string
        elif op == '==':
            self.code.append(('equ',))     
        elif op == '!=':
            self.code.append(('neq',))     
        #TODO membership operators

    def generateUnaryExp(self, node, op, val):
        self.generate(val)
        if op == None:
            return 

        if op == '-':
            self.code.append(('neg',))     
        elif op == '!':
            self.code.append(('not',))     

    def generate_Identifier(self, node):
        disp, off = self.environment.lookup(node.name)
        type_ = self.environment.lookup_mode(node.name)

        # Location
        if hasattr(type_, 'loc'):
            self.code.append(('lrv', disp, off))
        # Composite mode
        elif len(type_.type) > 1:
            #if node.type[-1] in [array_type]:
             self.code.append(('ldr', disp, off))
             #self.code.append(('lmv', node.mode.size))
        # Primitive Value
        else:
            self.code.append(('ldv', disp, off))
        node.size = type_.size

        
    '''
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

    def generate_DiscreteRangeMode(self, node):
        self.generate(node.name)
        self.generate(node.literal_range)
        node.type = node.name.type
        node.repr = node.name.repr + '(' + node.literal_range.repr + ')'

    '''

    def generate_LiteralRange(self, node):
        self.generate(node.lower)


    def generate_Location(self, node):
        '''
        if node.loc_type.__class__.__name__ == 'Identifier':
            if len(node.loc_type.type) == 1: # Primitive Type
                disp, off = self.environment.lookup(node.loc_type.repr)
                self.code.append(('ldv', disp, off))
            else:
                disp, off = self.environment.lookup(node.loc_type.repr)
                self.code.append(('ldr', disp, off))
            #    mode = self.environment.lookup_mode(node.loc_type.repr)
            #    self.code.append(('lmv', mode.size))
        else:
            self.generate(node.loc_type)
        '''
        self.generate(node.loc_type)
        node.size = node.loc_type.size
        
    '''
    def generate_DereferencedReference(self, node):
        self.generate(node.loc)
        node.type = node.loc.type[0:-1]
        node.repr = node.loc.repr + '->'

    ''' 

    def generate_ArrayElement(self, node):
        self.generate(node.loc)
        mode = self.environment.lookup_mode(node.loc.repr)
        arrayMode = mode.mode
        for expr, range_, size in reversed(list(zip(node.expr_list, arrayMode.index_mode_list, arrayMode.sizes))):
            self.generate(expr)
            self.generate(range_)
            self.code.append(('sub',))
            self.code.append(('idx', size))
        self.code.append(('grc',))
        node.size = arrayMode.sizes[len(node.expr_list) - 1]

    ''' 
    
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
        

    def generate_EmptyLiteral(self, node):
        node.type = [pointer_type]
        node.repr = node.val
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

    '''

    def generate_ConditionalExpression(self, node):
        self.generate(node.if_expr)
        self.code.append(('jof', node.next))
        node.then_expr.exit = node.exit
        node.else_expr.exit = node.exit
        self.generate(node.then_expr)
        self.code.append(('lbl', node.next))
        if node.elsif_expr is not None:
            node.elsif_expr.exit = node.exit
            self.generate(node.elsif_expr)
        self.generate(node.else_expr)
        self.code.append(('lbl', node.exit))

    def generate_ThenExpression(self, node):
        self.generate(node.expr)
        self.code.append(('jmp', node.exit))
    
    def generate_ElsifExpression(self, node):
        self.generate(node.bool_expr)
        self.code.append(('jof', node.next))
        node.then_expr.exit = node.exit
        self.generate(node.then_expr)
        self.code.append(('lbl', node.next))
        if node.elsif_expr:
            node.elsif_expr.exit = node.exit
            self.generate(node.elsif_expr)
        
    def generate_Operand0(self, node):
        self.generateBinaryExp(node, node.operand0, node.operand1, node.operator.op)

    def generate_Operand1(self, node):
        self.generateBinaryExp(node, node.operand1, node.operand2, node.operator.op)

    def generate_Operand2(self, node):
        self.generateBinaryExp(node, node.operand2, node.operand3, node.operator.op)

    def generate_Operand3(self, node):
        self.generateUnaryExp(node, node.operator.op, node.operand_or_literal)


    '''
    def generate_ReferencedLocation(self, node):
        self.generate(node.location)
        disp, off = self.environment.lookup(identifier.repr)
                    self.code.append(('ldr', disp, off))
                    self.code.append(('sts', len(self.H) - 1))      
        self.code.append(('ldr', node.const))   

        node.repr = '->' + node.location.repr

    def generate_ActionStatement(self, node):
        if node.label:
            print(node.label)

    '''

    def generate_AssignmentAction(self, node):
        if node.location.loc_type.__class__.__name__ == 'Identifier':
            self.generate(node.expression)
            disp, off = self.environment.lookup(node.location.loc_type.repr)
            self.code.append(('stv', disp, off))
        else:
            self.generate(node.location)
            if self.code[-1] == ('grc',):
                self.code.pop()
            self.generate(node.expression)
            self.code.append(('smv', 1))

    def generate_IfAction(self, node):
        self.generate(node.if_exp)
        self.code.append(('jof', node.next))
        node.then_exp.exit = node.exit
        self.generate(node.then_exp)
        self.code.append(('lbl', node.next))
        if node.else_exp:
            node.else_exp.exit = node.exit
            self.generate(node.else_exp)
        self.code.append(('lbl', node.exit))

    def generate_ThenClause(self, node):
        for statement in node.action_statement_list:
            self.generate(statement)
        self.code.append(('jmp', node.exit))
    
    def generate_ElseClause(self, node):
        if node.else_type == 'else':
            for stmt in node.bool_or_statement_list: 
                self.generate(stmt)
            self.code.append(('jmp', node.exit))
        else:
            self.generate(node.bool_or_statement_list)
            self.code.append(('jof', node.next))
            node.then_exp.exit = node.exit
            self.generate(node.then_exp)
            self.code.append(('lbl', node.next))
            if node.else_exp:
                node.else_exp.exit = node.exit
                self.generate(node.else_exp)

    def generate_DoAction(self, node):
        # Check if needs to initialize variable
        if hasattr(node.ctrl_part, 'initialized'):
            self.generate(node.ctrl_part) # first call initialize variable
        node.ctrl_part.initialized = True

        self.code.append(('lbl', node.start))
        for stmt in node.action_statement_list: 
            self.generate(stmt)
        
        node.ctrl_part.exit = node.exit
        self.generate(node.ctrl_part)
        self.code.append(('jmp', node.start))
        self.code.append(('lbl', node.exit))

    def generate_ControlPart(self, node):
        node.ctrl1.exit = node.exit
        self.generate(node.ctrl1)
        if node.initialized and node.ctrl2:
            node.ctrl2.exit = node.exit
            self.generate(node.ctrl2)

    def generate_ForControl(self, node):
        if not node.initialized:
            self.generate(node.iteration) 
            node.initialized = True
        else:
            disp, off = self.environment.lookup(node.counter.name)
            # Compare
            self.code.append(('ldv', disp, off))
            self.generate(node.end)
            if node.decreasing:
                self.code.append(('grt',))
            else:
                self.code.append(('les',))
            self.code.append(('jof', node.exit))

            # Increase/Decrease step 
            self.code.append(('ldv', disp, off))
            self.generate(node.step)
            if not node.step:
                self.code.append(('ldc', 1))
            if node.decreasing:
                self.code.append(('sub',))
            else:
                self.code.append(('add',))
            self.code.append(('stv', disp, off))



    def generate_StepEnumeration(self, node):
        disp, off = self.environment.lookup(node.counter.name)
        # Initialize counter 
        if not node.initialized:
            self.generate(node.start)
            self.code.append(('stv', disp, off))
            node.initialized = True
        else:
            print("Shouldn't enter here")
            # Compare
            self.code.append(('ldv', disp, off))
            self.generate(node.end)
            if node.decreasing:
                self.code.append(('grt',))
            else:
                self.code.append(('les',))

            # Increase/Decrease step 
            self.code.append(('ldv', disp, off))
            if node.step:
                self.generate(node.step)
            else:
                self.code.append(('ldc', 1))
            if node.decreasing:
                self.code.append(('sub',))
            else:
                self.code.append(('add',))
            self.code.append(('stv', disp, off))

    def generate_RangeEnumeration(self, node):
        disp, off = self.environment.lookup(node.counter.name)

        # Initialize counter as range lower or upper
        if not node.initialized:
            if node.decreasing:
                self.generate(node.upper)
            else:
                self.generate(node.lower)
            self.code.append(('stv', disp, off))
            node.initialized = True
        else:
            print("Shouldn't enter here")
            # Compare
            self.code.append(('ldv', disp, off))
            self.generate(node.end)
            if node.decreasing:
                self.code.append(('grt',))
            else:
                self.code.append(('les',))

            # Increase/Decrease step 
            self.code.append(('ldv', disp, off))
            if node.step:
                self.generate(node.step)
            else:
                self.code.append(('ldc', 1))
            if node.decreasing:
                self.code.append(('sub',))
            else:
                self.code.append(('add',))
            self.code.append(('stv', disp, off))
        self.generate(node.counter)
        self.generate(node.mode)

    def generate_WhileControl(self, node):
        self.generate(node.bool_exp)
        self.code.append(('jof', node.exit))

    def generate_CallAction(self, node):
        self.generate(node.call)
        node.size = node.call.size

    def generate_ProcedureCall(self, node):

        for param, param_type in zip(node.param_list, node.parameter_types):
            formal_type, isloc, formal_name = param_type # Formal parameter info

            # Constant
            if param.expr.__class__.__name__ is "PrimitiveValue":

                if isloc:
                    disp, off = self.environment.lookup(param.expr.val.repr)
                    self.code.append(('ldr', disp, off))
                else:
                    self.generate(param) # load constant value or add string to H

                # Constant string
                if param.expr.val.__class__.__name__ is "CharacterStringLiteral":
                    if isloc:
                        self.code.append(('ldc', len(self.H) - 1))
                    else:
                        # TODO: Copy Constant String ex:"example"
                        print("Can only pass character string literal as loc")
                        #self.code.append(('ldr', disp, off))
                        #self.code.append(('sts', len(self.H) - 1))      

            # Location or reference_location
            else:
                # Array location
                if param.expr.loc_type.__class__.__name__ == 'Identifier':
                    self.generate(param) # load reference array
                    if not isloc: # copy array
                        self.code.append(('lmv', param.size))

                # Array Element or Slice
                else:
                    self.generate(param)
                    self.code.append(('lmv', param.size))

            
            disp, label = self.environment.lookup(node.name.name)
            #self.code.append(('cfu', label))

            node.size = node.result_spec.mode.size if node.result_spec else 0

    def generate_BuiltInCall(self, node):
        node.size = 1

        func_name = node.name
        
        if func_name == 'print':
            for param in node.param_list:
                if param.expr.__class__.__name__ is "PrimitiveValue":
                    self.generate(param)
                    if param.type == [char_type, string_type]:
                        self.code.append(('prc', len(self.H) - 1))
                    elif param.type == [int_type]:
                        self.code.append(('prv',0))
                    elif param.type == [char_type]:
                        self.code.append(('prv',1))
                    else:
                        print("ERROR")
                        
                else:
                    if param.type == [char_type, string_type]:
                        disp, off = self.environment.lookup(param.repr)
                        self.code.append(('ldr', disp, off))
                        self.code.append(('prs', ))
                    elif param.type == [int_type]:
                        self.generate(param)
                        self.code.append(('prv',0))
                    elif param.type == [char_type]:
                        self.generate(param)
                        self.code.append(('prv',1))
                    elif param.type[-1] == array_type:
                        self.generate(param.expr)
                        if self.code[-1] == ('grc',):
                            self.code.pop()
                        assert (param.expr.__class__.__name__ == 'Location'), "Print multiple values should receive array"
                        self.code.append(('lmv', param.expr.size))
                        self.code.append(('prt', param.expr.size))
                    else:
                        print("ERROR2")

        elif func_name == 'read':
            for param in node.param_list:
                if param.type == [char_type, string_type]:
                    disp, off = self.environment.lookup(param.repr)
                    self.code.append(('ldr', disp, off))
                    self.code.append(('rds', ))
                elif param.expr.loc_type.__class__.__name__ == 'Identifier':
                    disp, off = self.environment.lookup(param.repr)
                    self.code.append(('rdv', ))
                    self.code.append(('stv', disp, off))
                elif param.expr.loc_type.__class__.__name__ == 'ArrayElement':
                    self.generate(param)
                    if self.code[-1] == ('grc',):
                        self.code.pop()
                    self.code.append(('rdv', ))
                    self.code.append(('smv', 1))
    
    def generate_ProcedureStatement(self, node):
        node.procedure_def.label = node.label
        self.generate(node.procedure_def)

    def generate_ProcedureDefinition(self, node):
        self.code.append(('jmp', node.exit))
        self.code.append(('lbl', node.start))
        self.environment.add_local(node.label.name, node.start)

        node.symtab = self.environment.peek()
        self.environment.push(node)
        node.environment = self.environment

        self.code.append(('enf', node.environment.scope_level()))
        if node.offset > 0:
            self.code.append(('alc', node.offset))      

        offset = -1 #PC 
        if node.result_spec: # Espaço para return
            offset -= node.result_spec.mode.size

        for param in reversed(node.formal_parameter_list):
            for identifier in param.id_list:
                offset -= param.param_spec.mode.size
                node.environment.add_local(identifier.name, offset)
                if param.loc:
                    param.param_spec.mode.loc = True
                node.environment.add_mode(identifier.name, param.param_spec.mode)

        # Generate all of the statements
        for stmt in node.stmt_list: 
            self.generate(stmt)

        if node.offset > 0:
            self.code.append(('dlc', node.offset))      

        self.code.append(('lbl', node.ret))
        self.code.append(('ret', node.environment.scope_level(), len(node.formal_parameter_list)))

        self.environment.pop()
        self.code.append(('lbl', node.exit))

    '''
    def generate_FormalParameter(self, node):
        self.generate(node.param_spec)
        for identifier in node.id_list:
            if node.loc:
                identifier.loc = True
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
