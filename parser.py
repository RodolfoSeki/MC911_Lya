# Yacc example

import ply.yacc as yacc
from lexer import MyLexer
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

    def p_expression_plus(self, p):
        'expression : expression PLUS term'
        p[0] = p[1] + p[3]

    def p_expression_minus(self, p):
        'expression : expression MINUS term'
        p[0] = p[1] - p[3]

    def p_expression_term(self, p):
        'expression : term'
        p[0] = p[1]

    def p_term_times(self, p):
        'term : term TIMES factor'
        p[0] = p[1] * p[3]

    def p_term_div(self, p):
        'term : term DIVIDE factor'
        p[0] = p[1] / p[3]

    def p_term_factor(self, p):
        'term : factor'
        p[0] = p[1]

    def p_factor_num(self, p):
        'factor : ICONST'
        p[0] = int(p[1])

    def p_factor_id(self, p):
        'factor : ID'
        p[0] = p[1]

    def p_factor_expr(self, p):
        'factor : LPAREN expression RPAREN'
        p[0] = p[2]


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
print p.parse(codigo)
f.close()

