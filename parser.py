# Yacc example

import ply.yacc as yacc
from lexer import MyLexer
import ast
import sys

# Get the token map from the lexer.  This is required.

class MyParser(object):


    precedence = (
        ('left', 'OR'),
        ('left', 'AND'),
        ('left', 'EQ', 'NE'),
        ('left', 'GT', 'GEQ', 'LT', 'LEQ'),
        ('left', 'PLUS', 'MINUS'),
        ('left', 'TIMES', 'DIVIDE', 'MODULO')
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
        '''
        #TODO completar
        p[0] = p[1]

    def p_declaration_statement(self, p):
        '''declaration_statement : DCL declaration_list SEMI'''
        p[0] = ast.DeclarationStatement(p[2])

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


    def p_initialization(self, p):
        '''initialization : EQUALS expression
        '''
        p[0] = p[2]


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

    def p_mode(self, p):
        ''' mode : discrete_mode
                 | identifier
                 | reference_mode
        '''
        # TODO completar
        p[0] = p[1]


    def p_discrete_mode(self, p):
        ''' discrete_mode : primitive_mode 
        '''
        # TODO completar
        p[0] = p[1]


    def p_primitive_mode(self, p):
        ''' primitive_mode : INT
                           | BOOL
                           | CHAR
        '''
        # TODO completar
        p[0] = ast.PrimitiveMode(p[1])
                            
    def p_expression(self, p):
        ''' expression : operand0'''
        # TODO completar
        p[0] = ast.Expression(p[1])


    def p_operand0(self, p):
        ''' operand0 : operand1 '''
        #TODO completar
        p[0] = ast.Operand0(p[1])

    def p_operand1(self, p):
        ''' operand1 : operand2 
        '''
        #TODO completar
        p[0] = ast.Operand1(p[1])

    def p_operand2(self, p):
        ''' operand2 : operand3 
                     | operand2 arithmetic_multiplicative_operator operand3
        '''
        p[0] = ast.Operand2(*p[1:])

    def p_operand3(self, p):
        ''' operand3 : ICONST
        '''
        #TODO completar
        p[0] = ast.Operand3(p[1])

    def p_arithmetic_multiplicative_operator(self, p):
        ''' arithmetic_multiplicative_operator : TIMES
                                               | DIVIDE
                                               | MODULO 
        '''
        p[0] = p[1]

    def p_statement(self, p):
        ''' statement : declaration_statement
                      | synonym_statement
                      | newmode_statement
                      | procedure_statement
                      | action_statement
        '''
        #TODO completar
        p[0] = ast.Statement()


















    def p_synonym_statement(self, p):
        ''' synonym_statement : SYN synonym_list ;
        '''
        p[0] = ast.SynonymStatement(p[2])


    def p_synonym_list(self, p):
        ''' synonym_list : synonym_definition 
                         | synonym_list synonym_definition
        '''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[2]]


    def p_synonym_definition(self, p):
        ''' synonym_definition : identifier_list mode EQUALS constant_expression
                               | identifier_list EQUALS constant_expression
        '''
        if len(p) == 5:
            p[0] = ast.SynonymDefinition(p[1], p[2], p[4])
        else:
            p[0] = ast.SynonymDefinition(p[1], None, p[4])


    def p_constante_expression(self, p):
        ''' constante_expression : expression
        '''
        p[0] = p[1]


    def p_newmode_statement(self, p):
        ''' newmode_statement : TYPE newmode_list ;
        '''
        p[0] = ast.NewmodeStatement(p[2])


    def p_newmode_list(self, p):
        ''' newmode_list : mode_definition 
                         | mode_list mode_definition
        '''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[2]]
        

    def p_mode_definition(self, p):
        ''' mode_definition : identifier_list EQUALS mode
        '''
        p[0] = p[1] + p[3]


    def p_mode(self, p):
        ''' mode : mode_name
                 | discrete_mode
                 | reference_mode
                 | composite_mode
        '''
        #TODO completar
        p[0] = ast.Mode()


    def p_discrete_mode(self, p):
        ''' discrete_mode : integer_mode
                          | boolean_mode
                          | character_mode
                          | discrete_range_mode
        '''
        #TODO completar
        p[0] = ast.DiscreteMode()


    def p_integer_mode(self, p):
        ''' integer_mode : INT
        '''
        #TODO completar
        p[0] = ast.IntegerMode()


    def p_boolean_mode(self, p):
        ''' boolean_mode : BOOL
        '''
        #TODO completar
        p[0] = ast.BooleanMode()


    def p_character_mode(self, p):
        ''' character_mode : CHAR
        '''
        #TODO completar
        p[0] = ast.CharacterMode()


    def p_discrete_range_mode(self, p):
        ''' discrete_range_mode : discrete_mode_name ( literal_range )
                                | discrete_mode ( literal_range )
        '''
        #TODO completar
        p[0] = ast.DiscreteRangeMode()


    def p_mode_name(self, p):
        ''' mode_name : identifier
        '''
        #TODO completar
        p[0] = ast.ModeName()


    def p_discrete_mode_name(self, p):
        ''' discrete_mode_name : identifier
        '''
        #TODO completar
        p[0] = ast.DiscreteModeName()


    def p_literal_range(self, p):
        ''' literal_range : lower_bound : upper_bound
        '''
        #TODO completar
        p[0] = ast.LiteralRange()


    def p_lower_bound(self, p):
        ''' lower_bound : expression
        '''
        #TODO completar
        p[0] = ast.LowerBound()


    def p_upper_bound(self, p):
        ''' upper_bound : expression
        '''
        #TODO completar
        p[0] = ast.UpperBound()


    def p_reference_mode(self, p):
        ''' reference_mode : REF mode
        '''
        #TODO completar
        p[0] = ast.ReferenceMode()


    def p_composite_mode(self, p):
        ''' composite_mode : string_mode
                           | array_mode
        '''
        #TODO completar
        p[0] = ast.CompositeMode()


    def p_string_mode(self, p):
        ''' string_mode : CHARS LBRACKET string_length RBRACKET
        '''
        #TODO completar
        p[0] = ast.StringMode()


    def p_string_length(self, p):
        ''' string_length : integer_literal
        '''
        #TODO completar
        p[0] = ast.StringLength()


    def p_array_mode(self, p):
        ''' array_mode : ARRAY LBRACKET index_mode { , index_mode }* RBRACKET element_mode
        '''
        #TODO completar
        p[0] = ast.ArrayMode()


    def p_index_mode(self, p):
        ''' index_mode : discrete_mode
                       | literal_range
        '''
        #TODO completar
        p[0] = ast.IndexMode()


    def p_element_mode(self, p):
        ''' element_mode : mode
        '''
        #TODO completar
        p[0] = ast.ElementMode()


    def p_location(self, p):
        ''' location : location_name
                     | dereferenced_reference
                     | string_element
                     | string_slice
                     | array_element
                     | array_slice
                     | call_action
        '''
        #TODO completar
        p[0] = ast.Location()


    def p_dereferenced_reference(self, p):
        ''' dereferenced_reference : location ARROW
        '''
        #TODO completar
        p[0] = ast.DereferencedReference()


    def p_string_element(self, p):
        ''' string_element : string_location LBRACKET start_element RBRACKET
        '''
        #TODO completar
        p[0] = ast.StringElement()


    def p_start_element(self, p):
        ''' start_element : integer_expression
        '''
        #TODO completar
        p[0] = ast.StartElement()


    def p_string_slice(self, p):
        ''' string_slice : string_location LBRACKET left_element : right_element RBRACKET
        '''
        #TODO completar
        p[0] = ast.StringSlice()


    def p_string_location(self, p):
        ''' string_location : identifier
        '''
        #TODO completar
        p[0] = ast.StringLocation()


    def p_left_element(self, p):
        ''' left_element : integer_expression
        '''
        #TODO completar
        p[0] = ast.LeftElement()


    def p_right_element(self, p):
        ''' right_element : integer_expression
        '''
        #TODO completar
        p[0] = ast.RightElement()


    def p_array_element(self, p):
        ''' array_element : array_location LBRACKET expression_list RBRACKET
        '''
        #TODO completar
        p[0] = ast.ArrayElement()


    def p_expression_list(self, p):
        ''' expression_list : expression { , expression }*
        '''
        #TODO completar
        p[0] = ast.ExpressionList()


    def p_array_slice(self, p):
        ''' array_slice : array_location LBRACKET lower_bound : upper_bound RBRACKET
        '''
        #TODO completar
        p[0] = ast.ArraySlice()


    def p_array_location(self, p):
        ''' array_location : location
        '''
        #TODO completar
        p[0] = ast.ArrayLocation()


    def p_primitive_value(self, p):
        ''' primitive_value : literal
                            | value_array_element
                            | value_array_slice
                            | parenthesized_expression
        '''
        #TODO completar
        p[0] = ast.PrimitiveValue()


    def p_literal(self, p):
        ''' literal : integer_literal
                    | boolean_literal
                    | character_literal
                    | empty_literal
                    | character_string_literal
        '''
        #TODO completar
        p[0] = ast.Literal()


    def p_integer_literal(self, p):
        ''' integer_literal : ICONST
        '''
        #TODO completar
        p[0] = ast.IntegerLiteral()


    def p_boolean_literal(self, p):
        ''' boolean_literal : FALSE
                            | TRUE
        '''
        #TODO completar
        p[0] = ast.BooleanLiteral()


    def p_character_literal(self, p):
        ''' character_literal : 'character'
                              | '^( integer_literal )'
        '''
        #TODO completar
        p[0] = ast.CharacterLiteral()


    def p_empty_literal(self, p):
        ''' empty_literal : NULL
        '''
        #TODO completar
        p[0] = ast.EmptyLiteral()


    def p_character_string_literal(self, p):
        ''' character_string_literal : " { character }* "
        '''
        #TODO completar
        p[0] = ast.CharacterStringLiteral()


    def p_value_array_element(self, p):
        ''' value_array_element : array_primitive_value LBRACKET expression_list RBRACKET
        '''
        #TODO completar
        p[0] = ast.ValueArrayElement()


    def p_value_array_slice(self, p):
        ''' value_array_slice : array_primitive_value LBRACKET lower_element : upper_element RBRACKET
        '''
        #TODO completar
        p[0] = ast.ValueArraySlice()


    def p_array_primitive_value(self, p):
        ''' array_primitive_value : primitive_value
        '''
        #TODO completar
        p[0] = ast.ArrayPrimitiveValue()


    def p_parenthesized_expression(self, p):
        ''' parenthesized_expression : ( expression )
        '''
        #TODO completar
        p[0] = ast.ParenthesizedExpression()


    def p_expression(self, p):
        ''' expression : operand0
                       | conditional_expression
        '''
        #TODO completar
        p[0] = ast.Expression()


    def p_conditional_expression(self, p):
        ''' conditional_expression : IF boolean_expression then_expression else_expression FI
                                   | IF boolean_expression then_expression elsif_expression else_expression FI
        '''
        #TODO completar
        p[0] = ast.ConditionalExpression()


    def p_boolean_expression(self, p):
        ''' boolean_expression : expression
        '''
        #TODO completar
        p[0] = ast.BooleanExpression()


    def p_then_expression(self, p):
        ''' then_expression : THEN expression
        '''
        #TODO completar
        p[0] = ast.ThenExpression()


    def p_else_expression(self, p):
        ''' else_expression : ELSE expression
        '''
        #TODO completar
        p[0] = ast.ElseExpression()


    def p_elsif_expression(self, p):
        ''' elsif_expression : ELSIF boolean_expression then_expression
                             | elsif_expression ELSIF boolean_expression then_expression
        '''
        #TODO completar
        p[0] = ast.ElsifExpression()


    def p_operand0(self, p):
        ''' operand0 : operand1
                     | operand0 operator1 operand1
        '''
        #TODO completar
        p[0] = ast.Operand0()


    def p_operator1(self, p):
        ''' operator1 : relational_operator
                      | membership_operator
        '''
        #TODO completar
        p[0] = ast.Operator1()


    def p_relational_operator(self, p):
        ''' relational_operator : &&
                                | 
                                | 
                                | 
                                | ==
                                | !=
                                | 
                                | =
                                | 
                                | =
        '''
        #TODO completar
        p[0] = ast.RelationalOperator()


    def p_membership_operator(self, p):
        ''' membership_operator : IN
        '''
        #TODO completar
        p[0] = ast.MembershipOperator()


    def p_operand1(self, p):
        ''' operand1 : operand2
                     | operand1 operator2 operand2
        '''
        #TODO completar
        p[0] = ast.Operand1()


    def p_operator2(self, p):
        ''' operator2 : arithmetic_additive_operator
                      | string_concatenation_operator
        '''
        #TODO completar
        p[0] = ast.Operator2()


    def p_arithmetic_additive_operator(self, p):
        ''' arithmetic_additive_operator : +
                                         | -
        '''
        #TODO completar
        p[0] = ast.ArithmeticAdditiveOperator()


    def p_string_concatenation_operator(self, p):
        ''' string_concatenation_operator : &
        '''
        #TODO completar
        p[0] = ast.StringConcatenationOperator()


    def p_operand3(self, p):
        ''' operand3 : [ monadic_operator ] operand4
                     | integer_literal
        '''
        #TODO completar
        p[0] = ast.Operand3()


    def p_monadic_operator(self, p):
        ''' monadic_operator : -
                             | !
        '''
        #TODO completar
        p[0] = ast.MonadicOperator()


    def p_operand4(self, p):
        ''' operand4 : location
                     | referenced_location
                     | primitive_value
        '''
        #TODO completar
        p[0] = ast.Operand4()


    def p_referenced_location(self, p):
        ''' referenced_location : ARROW location
        '''
        #TODO completar
        p[0] = ast.ReferencedLocation()


    def p_action_statement(self, p):
        ''' action_statement : [ label_id : ] action ;
        '''
        #TODO completar
        p[0] = ast.ActionStatement()


    def p_label_id(self, p):
        ''' label_id : identifier
        '''
        #TODO completar
        p[0] = ast.LabelId()


    def p_action(self, p):
        ''' action : bracketed_action
                   | assignment_action
                   | call_action
                   | exit_action
                   | return_action
                   | result_action
        '''
        #TODO completar
        p[0] = ast.Action()


    def p_bracketed_action(self, p):
        ''' bracketed_action : if_action
                             | do_action
        '''
        #TODO completar
        p[0] = ast.BracketedAction()


    def p_assignment_action(self, p):
        ''' assignment_action : location assigning_operator expression
        '''
        #TODO completar
        p[0] = ast.AssignmentAction()


    def p_assigning_operator(self, p):
        ''' assigning_operator : [ closed_dyadic_operator ] assignment_symbol
        '''
        #TODO completar
        p[0] = ast.AssigningOperator()


    def p_closed_dyadic_operator(self, p):
        ''' closed_dyadic_operator : arithmetic_additive_operator
                                   | arithmetic_multiplicative_operator
                                   | string_concatenation_operator
        '''
        #TODO completar
        p[0] = ast.ClosedDyadicOperator()


    def p_assignment_symbol(self, p):
        ''' assignment_symbol : =
        '''
        #TODO completar
        p[0] = ast.AssignmentSymbol()


    def p_if_action(self, p):
        ''' if_action : IF boolean_expression then_clause [ else_clause ] FI
        '''
        #TODO completar
        p[0] = ast.IfAction()


    def p_then_clause(self, p):
        ''' then_clause : THEN { action_statement }*
        '''
        #TODO completar
        p[0] = ast.ThenClause()


    def p_else_clause(self, p):
        ''' else_clause : ELSE { action_statement }*
                        | ELSIF boolean_expression then_clause [ else_clause ]
        '''
        #TODO completar
        p[0] = ast.ElseClause()


    def p_do_action(self, p):
        ''' do_action : DO [ control_part ; ] { action_statement }* OD
        '''
        #TODO completar
        p[0] = ast.DoAction()


    def p_control_part(self, p):
        ''' control_part : for_control [ while_control ]
                         | while_control
        '''
        #TODO completar
        p[0] = ast.ControlPart()


    def p_for_control(self, p):
        ''' for_control : FOR iteration
        '''
        #TODO completar
        p[0] = ast.ForControl()


    def p_iteration(self, p):
        ''' iteration : step_enumeration
                      | range_enumeration
        '''
        #TODO completar
        p[0] = ast.Iteration()


    def p_step_enumeration(self, p):
        ''' step_enumeration : loop_counter assignment_symbol start_value [ step_value ] [ DOWN ] end_value
        '''
        #TODO completar
        p[0] = ast.StepEnumeration()


    def p_loop_counter(self, p):
        ''' loop_counter : identifier
        '''
        #TODO completar
        p[0] = ast.LoopCounter()


    def p_start_value(self, p):
        ''' start_value : discrete_expression
        '''
        #TODO completar
        p[0] = ast.StartValue()


    def p_step_value(self, p):
        ''' step_value : BY integer_expression
        '''
        #TODO completar
        p[0] = ast.StepValue()


    def p_end_value(self, p):
        ''' end_value : TO discrete_expression
        '''
        #TODO completar
        p[0] = ast.EndValue()


    def p_discrete_expression(self, p):
        ''' discrete_expression : expression
        '''
        #TODO completar
        p[0] = ast.DiscreteExpression()


    def p_range_enumeration(self, p):
        ''' range_enumeration : loop_counter [ DOWN ] IN discrete_mode
        '''
        #TODO completar
        p[0] = ast.RangeEnumeration()


    def p_while_control(self, p):
        ''' while_control : WHILE boolean_expression
        '''
        #TODO completar
        p[0] = ast.WhileControl()


    def p_call_action(self, p):
        ''' call_action : procedure_call
                        | builtin_call
        '''
        #TODO completar
        p[0] = ast.CallAction()


    def p_procedure_call(self, p):
        ''' procedure_call : procedure_name ( [ parameter_list ] )
        '''
        #TODO completar
        p[0] = ast.ProcedureCall()


    def p_parameter_list(self, p):
        ''' parameter_list : parameter { , parameter }*
        '''
        #TODO completar
        p[0] = ast.ParameterList()


    def p_parameter(self, p):
        ''' parameter : expression
        '''
        #TODO completar
        p[0] = ast.Parameter()


    def p_procedure_name(self, p):
        ''' procedure_name : identifier
        '''
        #TODO completar
        p[0] = ast.ProcedureName()


    def p_exit_actiom(self, p):
        ''' exit_actiom : EXIT label_id
        '''
        #TODO completar
        p[0] = ast.ExitActiom()


    def p_return_action(self, p):
        ''' return_action : RETURN [ result ]
        '''
        #TODO completar
        p[0] = ast.ReturnAction()


    def p_result_action(self, p):
        ''' result_action : RESULT result
        '''
        #TODO completar
        p[0] = ast.ResultAction()


    def p_result(self, p):
        ''' result : expression
        '''
        #TODO completar
        p[0] = ast.Result()


    def p_builtin_call(self, p):
        ''' builtin_call : builtin_name ( [ parameter_list ] )
        '''
        #TODO completar
        p[0] = ast.BuiltinCall()


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
        #TODO completar
        p[0] = ast.BuiltinName()


    def p_procedure_statement(self, p):
        ''' procedure_statement : label_id : procedure_definition ;
        '''
        #TODO completar
        p[0] = ast.ProcedureStatement()


    def p_procedure_definition(self, p):
        ''' procedure_definition : PROC ( [ formal_parameter_list ] ) [ result_spec ]; { statement }* END
        '''
        #TODO completar
        p[0] = ast.ProcedureDefinition()


    def p_formal_parameter_list(self, p):
        ''' formal_parameter_list : formal_parameter { , formal_parameter }*
        '''
        #TODO completar
        p[0] = ast.FormalParameterList()


    def p_formal_parameter(self, p):
        ''' formal_parameter : identifier_list parameter_spec
        '''
        #TODO completar
        p[0] = ast.FormalParameter()


    def p_parameter_spec(self, p):
        ''' parameter_spec : mode [ parameter_attribute ]
        '''
        #TODO completar
        p[0] = ast.ParameterSpec()


    def p_parameter_attribute(self, p):
        ''' parameter_attribute : LOC
        '''
        #TODO completar
        p[0] = ast.ParameterAttribute()


    def p_result_spec(self, p):
        ''' result_spec : RETURNS ( mode [ result_attribute ] )
        '''
        #TODO completar
        p[0] = ast.ResultSpec()


    def p_result_attribute(self, p):
        ''' result_attribute : LOC
        '''
        #TODO completar
        p[0] = ast.ResultAttribute()


    def p_comment(self, p):
        ''' comment : bracketed_comment
                    | line_end_comment
        '''
        #TODO completar
        p[0] = ast.Comment()


    def p_bracketed_comment(self, p):
        ''' bracketed_comment : /* character_string */
        '''
        #TODO completar
        p[0] = ast.BracketedComment()


    def p_line_end_comment(self, p):
        ''' line_end_comment : // character_string end_of_line
        '''
        #TODO completar
        p[0] = ast.LineEndComment()


    def p_character_string(self, p):
        ''' character_string : { character }*
        '''
        #TODO completar
        p[0] = ast.CharacterString()



#    def p_expression_plus(self, p):
#        'expression : expression operator term'
#        p[0] = p[1] + p[3]
#
#    def p_expression_plus(self, p):
#        'expression : expression PLUS term'
#        p[0] = p[1] + p[3]
#
#    def p_expression_minus(self, p):
#        'expression : expression MINUS term'
#        p[0] = p[1] - p[3]
#
#    def p_expression_term(self, p):
#        'expression : term'
#        p[0] = p[1]
#
#    def p_term_times(self, p):
#        'term : term TIMES factor'
#        p[0] = p[1] * p[3]
#
#    def p_term_div(self, p):
#        'term : term DIVIDE factor'
#        p[0] = p[1] / p[3]
#
#    def p_term_factor(self, p):
#        'term : factor'
#        p[0] = p[1]
#
#    def p_factor_num(self, p):
#        'factor : ICONST'
#        p[0] = int(p[1])
#
#    def p_factor_id(self, p):
#        'factor : ID'
#        p[0] = p[1]
#
#    def p_factor_expr(self, p):
#        'factor : LPAREN expression RPAREN'
#        p[0] = p[2]
#

    # Error rule for syntax errors
    def p_error(self, p):
        print("Syntax error in input!")

    def __init__(self):
        self.mylex = MyLexer()
        self.mylex.build()           
        self.tokens = self.mylex.tokens
        self.myparser = myparser = yacc.yacc(module=self)

    def parse(self, codigo):
        return self.myparser.parse(input=codigo, lexer=self.mylex)

p = MyParser()
f = open(sys.argv[1])
codigo = ''.join(f.readlines())
p.parse(codigo).show()
f.close()

