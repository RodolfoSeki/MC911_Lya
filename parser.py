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

