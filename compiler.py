# Yacc example

import ply.yacc as yacc
from lexer import MyLexer
import ast
from parser import MyParser
from visitor import MyVisitor
import sys

# Get the token map from the lexer.  This is required.
p = MyParser()
f = open(sys.argv[1])
codigo = ''.join(f.readlines())
ast = p.parse(codigo)
print '------'
print ast
print '------'
visitor = MyVisitor(ast)
f.close()

