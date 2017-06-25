from lexer import MyLexer
import ply.yacc as yacc
import ast

class MyParser(object):


    precedence = (
        ('left', 'OR'),
        ('left', 'AND'),
        ('left', 'EQ', 'NE'),
        ('left', 'GT', 'GEQ', 'LT', 'LEQ'),
        ('left', 'PLUS', 'MINUS'),
        ('left', 'TIMES', 'DIVIDE', 'MODULO'),
    )

    def p_program(self, p):
        'program : statement_list'
        p[0] = ast.Program(p[1])

    def p_statement_list(self, p):
        '''statement_list : statement
                          | statement_list statement
        '''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[2]]


    def p_statement(self, p):
        '''statement : declaration_statement
                     | synonym_statement
                     | newmode_statement
                     | procedure_statement
                     | action_statement
        '''
        p[0] = p[1]

    def p_declaration_statement(self, p):
        '''declaration_statement : DCL declaration_list SEMI'''
        p[0] = ast.DeclarationStatement(p[2])
        p[0].lineno = p.lineno(1)

    def p_declaration_list(self, p):
        '''declaration_list : declaration
                            | declaration_list COMMA declaration
        '''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[3]]


    def p_declaration(self, p):
        '''declaration : identifier_list mode 
                       | identifier_list mode initialization
        '''
        if len(p) == 3:
            p[0] = ast.Declaration(p[1], p[2])
        else:
            p[0] = ast.Declaration(p[1], p[2], p[3])
        p[0].lineno = p[2].lineno


    def p_initialization(self, p):
        '''initialization : EQUALS expression
        '''
        p[0] = p[2]
        p[0].lineno = p.lineno(1)


    def p_identifier_list(self, p):
        '''identifier_list : identifier
                           | identifier_list COMMA identifier
        '''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[3]]

    def p_identifier(self, p):
        '''identifier : ID '''
        p[0] = ast.Identifier(p[1])
        p[0].lineno = p.lineno(1)


    def p_synonym_statement(self, p):
        ''' synonym_statement : SYN synonym_list SEMI
        '''
        p[0] = ast.SynonymStatement(p[2])
        p[0].lineno = p.lineno(1)


    def p_synonym_list(self, p):
        ''' synonym_list : synonym_definition 
                         | synonym_list COMMA synonym_definition
        '''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[3]]


    def p_synonym_definition(self, p):
        ''' synonym_definition : identifier_list mode EQUALS constant_expression
                               | identifier_list EQUALS constant_expression
        '''
        if len(p) == 5:
            p[0] = ast.SynonymDefinition(p[1], p[4], p[2])
            p[0].lineno = p[2].lineno
        else:
            p[0] = ast.SynonymDefinition(p[1], p[3])
            p[0].lineno = p.lineno(2)


    def p_constant_expression(self, p):
        ''' constant_expression : expression
        '''
        p[0] = p[1]


    def p_newmode_statement(self, p):
        ''' newmode_statement : TYPE newmode_list SEMI
        '''
        p[0] = ast.NewModeStatement(p[2])
        p[0].lineno = p.lineno(1)


    def p_newmode_list(self, p):
        ''' newmode_list : mode_definition 
                         | newmode_list COMMA mode_definition
        '''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[3]]
        

    def p_mode_definition(self, p):
        ''' mode_definition : identifier_list EQUALS mode
        '''
        p[0] = ast.ModeDefinition(p[1], p[3])
        p[0].lineno = p.lineno(2)


    def p_mode(self, p):
        ''' mode : identifier
                 | discrete_mode
                 | reference_mode
                 | composite_mode
        '''
        p[0] = ast.Mode(p[1])
        p[0].lineno = p[1].lineno


    def p_discrete_mode(self, p):
        ''' discrete_mode : integer_mode
                          | boolean_mode
                          | character_mode
                          | discrete_range_mode
        '''
        p[0] = ast.DiscreteMode(p[1])
        p[0].lineno = p[1].lineno


    def p_integer_mode(self, p):
        ''' integer_mode : INT
        '''
        p[0] = ast.IntegerMode()
        p[0].lineno = p.lineno(1)


    def p_boolean_mode(self, p):
        ''' boolean_mode : BOOL
        '''
        p[0] = ast.BooleanMode()
        p[0].lineno = p.lineno(1)


    def p_character_mode(self, p):
        ''' character_mode : CHAR
        '''
        p[0] = ast.CharacterMode()
        p[0].lineno = p.lineno(1)


    def p_discrete_range_mode(self, p):
        ''' discrete_range_mode : identifier LPAREN literal_range RPAREN
                                | discrete_mode LPAREN literal_range RPAREN
        '''
        p[0] = ast.DiscreteRangeMode(p[1], p[3])
        p[0].lineno = p[1].lineno

    def p_literal_range(self, p):
        ''' literal_range : expression COLON expression
        '''
        p[0] = ast.LiteralRange(p[1], p[3])
        p[0].lineno = p[1].lineno


    def p_reference_mode(self, p):
        ''' reference_mode : REF mode
        '''
        p[0] = ast.ReferenceMode(p[2])
        p[0].lineno = p.lineno(1)

    def p_composite_mode(self, p):
        ''' composite_mode : string_mode
                           | array_mode
        '''
        p[0] = p[1]

    def p_string_mode(self, p):
        ''' string_mode : CHARS LBRACKET integer_literal RBRACKET
        '''
        p[0] = ast.StringMode(p[3])
        p[0].lineno = p.lineno(1)


    def p_array_mode(self, p):
        ''' array_mode : ARRAY LBRACKET list_index_mode RBRACKET mode
        '''
        p[0] = ast.ArrayMode(p[3], p[5])
        p[0].lineno = p.lineno(1)

    def p_list_index_mode(self, p):
        ''' list_index_mode : index_mode
                            | list_index_mode COMMA index_mode
        '''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[3]]

    def p_index_mode(self, p):
        ''' index_mode : discrete_mode
                       | literal_range
        '''
        p[0] = p[1]


    def p_location(self, p):
        ''' location : identifier
                     | dereferenced_reference
                     | array_element
                     | array_slice
                     | call_action
        '''
        """
                     | string_slice
                     | string_element
        """
        p[0] = ast.Location(p[1])
        p[0].lineno = p[1].lineno

    def p_dereferenced_reference(self, p):
        ''' dereferenced_reference : location ARROW
        '''
        p[0] = ast.DereferencedReference(p[1])
        p[0].lineno = p.lineno(2)

    """
    def p_string_element(self, p):
        ''' string_element : identifier LBRACKET start_element RBRACKET
        '''
        p[0] = ast.StringElement(p[1], p[3])


    def p_start_element(self, p):
        ''' start_element : expression
        '''
        p[0] = p[1]


    def p_string_slice(self, p):
        ''' string_slice : identifier LBRACKET left_element COLON right_element RBRACKET 
        '''
        p[0] = ast.StringSlice(p[1], p[3], p[5])


    def p_left_element(self, p):
        ''' left_element : expression
        '''
        p[0] = p[1]


    def p_right_element(self, p):
        ''' right_element : expression
        '''
        p[0] = p[1]
    """

    def p_array_element(self, p):
        ''' array_element : array_location LBRACKET expression_list RBRACKET
        '''
        p[0] = ast.ArrayElement(p[1], p[3])
        p[0].lineno = p[1].lineno


    def p_expression_list(self, p):
        ''' expression_list : expression
                            | expression_list COMMA expression
        '''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[3]]


    def p_array_slice(self, p):
        ''' array_slice : array_location LBRACKET expression COLON expression RBRACKET
        '''
        p[0] = ast.ArraySlice(p[1], p[3], p[5])
        p[0].lineno = p[1].lineno


    def p_array_location(self, p):
        ''' array_location : location
        '''
        p[0] = p[1]


    def p_primitive_value(self, p):
        ''' primitive_value : literal
                            | value_array_element
                            | value_array_slice
                            | parenthesized_expression
        '''
        p[0] = ast.PrimitiveValue(p[1])
        p[0].lineno = p[1].lineno


    def p_literal(self, p):
        ''' literal : integer_literal
                    | boolean_literal
                    | character_literal
                    | empty_literal
                    | character_string_literal
        '''
        p[0] = p[1]
        p[0].lineno = p[1].lineno


    def p_integer_literal(self, p):
        ''' integer_literal : ICONST
        '''
        p[0] = ast.IntegerLiteral(int(p[1]))
        p[0].lineno = p.lineno(1)


    def p_boolean_literal(self, p):
        ''' boolean_literal : FALSE
                            | TRUE
        '''
        p[0] = ast.BooleanLiteral(p[1])
        p[0].lineno = p.lineno(1)


    def p_character_literal(self, p):
        ''' character_literal : CCONST
        '''
        p[0] = ast.CharacterLiteral(p[1])
        p[0].lineno = p.lineno(1)


    def p_empty_literal(self, p):
        ''' empty_literal : NULL
        '''
        p[0] = ast.EmptyLiteral()
        p[0].lineno = p.lineno(1)


    def p_character_string_literal(self, p):
        ''' character_string_literal : SCONST
        '''
        p[0] = ast.CharacterStringLiteral(p[1])
        p[0].lineno = p.lineno(1)


    def p_value_array_element(self, p):
        ''' value_array_element : array_primitive_value LBRACKET expression_list RBRACKET
        '''
        p[0] = ast.ValueArrayElement(p[1], p[3])
        p[0].lineno = p[1].lineno


    def p_value_array_slice(self, p):
        ''' value_array_slice : array_primitive_value LBRACKET expression COLON expression RBRACKET
        '''
        p[0] = ast.ValueArraySlice(p[1], p[3], p[5])
        p[0].lineno = p[1].lineno


    def p_array_primitive_value(self, p):
        ''' array_primitive_value : primitive_value
        '''
        p[0] = p[1]


    def p_parenthesized_expression(self, p):
        ''' parenthesized_expression : LPAREN expression RPAREN
        '''
        p[0] = ast.ParenthesizedExpression(p[2])
        p[0].lineno = p.lineno(1)


    def p_expression(self, p):
        ''' expression : operand0
                       | conditional_expression
        '''
        p[0] = ast.Expression(p[1])
        p[0].lineno = p[1].lineno


    def p_conditional_expression(self, p):
        ''' conditional_expression : IF boolean_expression then_expression else_expression FI
                                   | IF boolean_expression then_expression elsif_expression else_expression FI
        '''
        if len(p) == 6:
            p[0] = ast.ConditionalExpression(p[2], p[3], p[4])
        else:
            p[0] = ast.ConditionalExpression(p[2], p[3], p[5], p[4])
        p[0].lineno = p.lineno(1)


    def p_boolean_expression(self, p):
        ''' boolean_expression : expression
        '''
        p[0] = ast.BooleanExpression(p[1])
        p[0].lineno = p[1].lineno


    def p_then_expression(self, p):
        ''' then_expression : THEN expression
        '''
        p[0] = ast.ThenExpression(p[2])
        p[0].lineno = p.lineno(1)


    def p_else_expression(self, p):
        ''' else_expression : ELSE expression
        '''
        p[0] = ast.ElseExpression(p[2])
        p[0].lineno = p.lineno(1)


    def p_elsif_expression(self, p):
        ''' elsif_expression : ELSIF boolean_expression then_expression
                             | elsif_expression ELSIF boolean_expression then_expression
        '''
        if len(p) == 4:
            p[0] = ast.ElsifExpression(p[2], p[3])
            p[0].lineno = p.lineno(1)
        else:
            p[0] = ast.ElsifExpression(p[3], p[4], p[1])
            p[0].lineno = p[1].lineno


    def p_operand0(self, p):
        ''' operand0 : operand1
                     | operand0 operator1 operand1
        '''
        if len(p) == 2:
            p[0] = p[1]
            #p[0] = ast.Operand1(p[1])
        else:
            p[0] = ast.Operand0(p[3], p[1], p[2])
            p[0].lineno = p[1].lineno


    def p_operator1(self, p):
        ''' operator1 : relational_operator
                      | membership_operator
        '''
        p[0] = p[1]


    def p_relational_operator(self, p):
        ''' relational_operator : AND
                                | OR 
                                | EQ 
                                | NE
                                | GT
                                | GEQ
                                | LT
                                | LEQ
        '''
        p[0] = ast.Operator(p[1])
        p[0].lineno = p.lineno(1)


    def p_membership_operator(self, p):
        ''' membership_operator : IN
        '''
        p[0] = ast.Operator(p[1])
        p[0].lineno = p.lineno(1)


    def p_operand1(self, p):
        ''' operand1 : operand2
                     | operand1 arithmetic_additive_operator operand2
                     | operand1 string_concatenation_operator operand2
        '''
        if len(p) == 2:
            #p[0] = ast.Operand2(p[1])
            p[0] = p[1]
        else:
            p[0] = ast.Operand1(p[3], p[1], p[2])
            p[0].lineno = p[1].lineno


    def p_arithmetic_additive_operator(self, p):
        ''' arithmetic_additive_operator : PLUS
                                         | MINUS
        '''
        p[0] = ast.Operator(p[1])
        p[0].lineno = p.lineno(1)


    def p_string_concatenation_operator(self, p):
        ''' string_concatenation_operator : LAND
        '''
        p[0] = ast.Operator(p[1])
        p[0].lineno = p.lineno(1)


    def p_operand2(self, p):
        ''' operand2 : operand3 
                     | operand2 arithmetic_multiplicative_operator operand3
        '''
        if len(p) == 2:
            #p[0] = ast.Operand3(p[1])
            p[0] = p[1]
        else:
            p[0] = ast.Operand2(p[3], p[1], p[2])
            p[0].lineno = p[1].lineno


    def p_arithmetic_multiplicative_operator(self, p):
        ''' arithmetic_multiplicative_operator : TIMES
                                               | DIVIDE
                                               | MODULO 
        '''
        p[0] = ast.Operator(p[1])
        p[0].lineno = p.lineno(1)

    def p_operand3(self, p):
        ''' operand3 : operand4
                     | monadic_operator operand4
        '''
        if len(p) == 2:
            #p[0] = ast.Operand4(p[1]) 
            p[0] = p[1]
        else:
            p[0] = ast.Operand3(p[2], p[1])
            p[0].lineno = p[1].lineno


    def p_monadic_operator(self, p):
        ''' monadic_operator : MINUS
                             | NOT 
        '''
        p[0] = ast.Operator(p[1])
        p[0].lineno = p.lineno(1)


    def p_operand4(self, p):
        ''' operand4 : location
                     | referenced_location
                     | primitive_value
        '''
        #p[0] = ast.Operand4(p[1])
        p[0] = p[1]


    def p_referenced_location(self, p):
        ''' referenced_location : ARROW location
        '''
        p[0] = ast.ReferencedLocation(p[2])
        p[0].lineno = p.lineno(1)


    def p_action_statement(self, p):
        ''' action_statement : action SEMI
                             | identifier COLON action SEMI
        '''
        if len(p) == 3:
            p[0] = ast.ActionStatement(p[1])
            p[0].lineno = p[1].lineno
        else:
            p[0] = ast.ActionStatement(p[3], p[1])
            p[0].lineno = p[1].lineno


    def p_action(self, p):
        ''' action : bracketed_action
                   | assignment_action
                   | call_action
                   | exit_action
                   | return_action
                   | result_action
        '''
        p[0] = ast.Action(p[1])
        p[0].lineno = p[1].lineno


    def p_bracketed_action(self, p):
        ''' bracketed_action : if_action
                             | do_action
        '''
        p[0] = ast.BracketedAction(p[1])
        p[0].lineno = p[1].lineno


    def p_assignment_action(self, p):
        ''' assignment_action : location assigning_operator expression
        '''
        p[0] = ast.AssignmentAction(p[1], p[2], p[3])
        p[0].lineno = p[1].lineno


    def p_assigning_operator(self, p):
        ''' assigning_operator : EQUALS
                               | PLUS EQUALS
                               | MINUS EQUALS
                               | TIMES EQUALS
                               | DIVIDE EQUALS
                               | MODULO EQUALS
                               | LAND EQUALS
        '''
        if len(p) == 2:
            p[0] = ast.AssigningOperator(p[1])
        else:
            p[0] = ast.AssigningOperator(p[2], p[1])
        p[0].lineno = p.lineno(1)

    def p_if_action(self, p):
        ''' if_action : IF boolean_expression then_clause FI
                      | IF boolean_expression then_clause else_clause FI
        '''
        if len(p) == 5:
            p[0] = ast.IfAction(p[2], p[3])
        else:
            p[0] = ast.IfAction(p[2], p[3], p[4])
        p[0].lineno = p.lineno(1)


    def p_then_clause(self, p):
        ''' then_clause : THEN action_statement_list
        '''
        p[0] = ast.ThenClause(p[2])
        p[0].lineno = p.lineno(1)

    def p_action_statement_list(self, p):
        '''action_statement_list : action_statement
                                 | action_statement_list action_statement
        '''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[2]]

    def p_else_clause(self, p):
        ''' else_clause : ELSE action_statement_list
                        | ELSIF boolean_expression then_clause 
                        | ELSIF boolean_expression then_clause else_clause
        '''
        if len(p) == 3:
            p[0] = ast.ElseClause('else', p[2])
        elif len(p) == 4:
            p[0] = ast.ElseClause('elsif', p[2], p[3])
        else:
            p[0] = ast.ElseClause('elsif', p[2], p[3], p[4])
        p[0].lineno = p.lineno(1)


    def p_do_action(self, p):
        ''' do_action : DO action_statement_list OD
                      | DO control_part SEMI action_statement_list OD
        '''
        if len(p) == 4:
            p[0] = ast.DoAction(p[2])
        else:
            p[0] = ast.DoAction(p[4], p[2])
        p[0].lineno = p.lineno(1)


    def p_control_part(self, p):
        ''' control_part : for_control 
                         | for_control while_control
                         | while_control
        '''
        if len(p) == 2:
            p[0] = ast.ControlPart(p[1])
        else:
            p[0] = ast.ControlPart(p[1], p[2])
        p[0].lineno = p[1].lineno


    def p_for_control(self, p):
        ''' for_control : FOR iteration
        '''
        p[0] = ast.ForControl(p[2])
        p[0].lineno = p.lineno(1)


    def p_iteration(self, p):
        ''' iteration : step_enumeration
                      | range_enumeration
        '''
        p[0] = p[1] 
        #ast.Iteration(p[1])
        #p[0].lineno = p[1].lineno


    def p_step_enumeration(self, p):
        ''' step_enumeration : identifier EQUALS start_value end_value
                             | identifier EQUALS start_value step_value end_value
                             | identifier EQUALS start_value DOWN end_value
                             | identifier EQUALS start_value step_value DOWN end_value
        '''
        if len(p) == 5:
            p[0] = ast.StepEnumeration(p[1], p[3], p[4])
        elif len(p) == 6:
            if p[4] == 'down':
                p[0] = ast.StepEnumeration(p[1], p[3], p[5], decreasing=True)
            else:
                p[0] = ast.StepEnumeration(p[1], p[3], p[5], step=p[4])
        else:
            p[0] = ast.StepEnumeration(p[1], p[3], p[6], step=p[4], decreasing=True)
        p[0].lineno = p[1].lineno


    def p_start_value(self, p):
        ''' start_value : expression
        '''
        p[0] = p[1]


    def p_step_value(self, p):
        ''' step_value : BY expression
        '''
        p[0] = p[2]


    def p_end_value(self, p):
        ''' end_value : TO expression
        '''
        p[0] = p[2]


    def p_range_enumeration(self, p):
        # discrete_mode changed to discrete_range_mode
        ''' range_enumeration : identifier IN discrete_range_mode 
                              | identifier DOWN IN discrete_range_mode
        '''
        if len(p) == 4:
            p[0] = ast.RangeEnumeration(p[1], p[3])
        else:
            p[0] = ast.RangeEnumeration(p[1], p[4], decreasing=True)
        p[0].lineno = p[1].lineno


    def p_while_control(self, p):
        ''' while_control : WHILE boolean_expression
        '''
        p[0] = ast.WhileControl(p[2])
        p[0].lineno = p.lineno(1)


    def p_call_action(self, p):
        ''' call_action : procedure_call
                        | builtin_call
        '''
        p[0] = ast.CallAction(p[1])
        p[0].lineno = p[1].lineno


    def p_procedure_call(self, p):
        ''' procedure_call : identifier LPAREN  RPAREN
                           | identifier LPAREN parameter_list RPAREN
        '''
        if len(p) == 4:
            p[0] = ast.ProcedureCall(p[1])
        else:
            p[0] = ast.ProcedureCall(p[1], p[3])
        p[0].lineno = p[1].lineno

    def p_parameter_list(self, p):
        ''' parameter_list : parameter
                           | parameter_list COMMA parameter
        '''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[3]]


    def p_parameter(self, p):
        ''' parameter : expression
        '''
        p[0] = p[1]


    def p_exit_action(self, p):
        ''' exit_action : EXIT identifier
        '''
        p[0] = ast.ExitAction(p[2])
        p[0].lineno = p.lineno(1)


    def p_return_action(self, p):
        ''' return_action : RETURN 
                          | RETURN result
        '''
        if len(p) == 2:
            p[0] = ast.ReturnAction()
        else:
            p[0] = ast.ReturnAction(p[2])
        p[0].lineno = p.lineno(1)

    def p_result_action(self, p):
        ''' result_action : RESULT result
        '''
        p[0] = ast.ResultAction(p[2])
        p[0].lineno = p.lineno(1)


    def p_result(self, p):
        ''' result : expression
        '''
        p[0] = p[1]


    def p_builtin_call(self, p):
        ''' builtin_call : builtin_name LPAREN RPAREN
                         | builtin_name LPAREN parameter_list RPAREN
        '''
        if len(p) == 4:
            p[0] = ast.BuiltInCall(p[1])
        else:
            p[0] = ast.BuiltInCall(p[1], p[3])
        p[0].lineno = p.lineno(2)



    def p_builtin_name(self, p):
        ''' builtin_name : ABS
                         | ASC
                         | NUM
                         | UPPER
                         | LOWER
                         | LENGTH
                         | READ
                         | PRINT
        '''
        p[0] = p[1]


    def p_procedure_statement(self, p):
        ''' procedure_statement : identifier COLON procedure_definition SEMI
        '''
        p[0] = ast.ProcedureStatement(p[1], p[3])
        p[0].lineno = p[1].lineno


    def p_procedure_definition(self, p):
        ''' procedure_definition : PROC LPAREN RPAREN SEMI statement_list END
                                 | PROC LPAREN formal_parameter_list RPAREN SEMI statement_list END
                                 | PROC LPAREN RPAREN result_spec SEMI statement_list END
                                 | PROC LPAREN formal_parameter_list RPAREN result_spec SEMI statement_list END
        '''
        if len(p) == 7:
            p[0] = ast.ProcedureDefinition(p[5])
        elif len(p) == 8:
            if p[3] == ')':
                p[0] = ast.ProcedureDefinition(p[6], result_spec=p[4])
            else:
                p[0] = ast.ProcedureDefinition(p[6], formal_parameter_list=p[3])
        else:
            p[0] = ast.ProcedureDefinition(p[7], result_spec=p[5], formal_parameter_list=p[3])
        p[0].lineno = p.lineno(1)


    def p_formal_parameter_list(self, p):
        ''' formal_parameter_list : formal_parameter 
                                  | formal_parameter_list COMMA formal_parameter
        '''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[3]]


    def p_formal_parameter(self, p):
        ''' formal_parameter : identifier_list parameter_spec
        '''
        p[0] = ast.FormalParameter(p[1], p[2])
        p[0].lineno = p[1].lineno


    def p_parameter_spec(self, p):
        ''' parameter_spec : mode 
                           | mode LOC
        '''
        if len(p) == 2:
            p[0] = ast.ParameterSpec(p[1])
        else:
            p[0] = ast.ParameterSpec(p[1], loc=True)
        p[0].lineno = p[1].lineno


    def p_result_spec(self, p):
        ''' result_spec : RETURNS LPAREN mode RPAREN
                        | RETURNS LPAREN mode LOC RPAREN
        '''
        if len(p) == 5:
            p[0] = ast.ResultSpec(p[3])
        else:
            p[0] = ast.ResultSpec(p[3], loc=True)
        p[0].lineno = p.lineno(1)


    # Error rule for syntax errors
    def p_error(self, p):
        print (p)
        print("Syntax error in input!")

    def __init__(self):
        self.mylex = MyLexer()
        self.mylex.build()           
        self.tokens = self.mylex.tokens
        self.myparser = myparser = yacc.yacc(module=self)

    def parse(self, codigo):
        return self.myparser.parse(input=codigo, lexer=self.mylex)

