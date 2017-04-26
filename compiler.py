# Yacc example

import ply.yacc as yacc
import ast
from parser import MyParser
from visitor import Visitor
import sys

# Get the token map from the lexer.  This is required.
p = MyParser()
f = open(sys.argv[1])
codigo = ''.join(f.readlines())
f.close()
ast = p.parse(codigo)
print (ast.show())
visitor = Visitor()
visitor.visit(ast)
