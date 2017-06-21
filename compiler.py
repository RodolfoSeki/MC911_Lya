# Yacc example

import ply.yacc as yacc
import ast
from parser import MyParser
from visitor import Visitor
from generator import Generator
from virtualMachine import VirtualMachine
import sys

# Get the token map from the lexer.  This is required.
p = MyParser()
f = open(sys.argv[1])
codigo = ''.join(f.readlines())
f.close()
ast = p.parse(codigo)
#print(ast.show())
visitor = Visitor()
visitor.visit(ast)
print(ast.showDecorated())

print('------ Generating Code ------')
generator = Generator()
generator.generate(ast)
print('------ Code generated ------')
print('H:', generator.H)
print('Code:', generator.code)
print('----------------------------')

print('------ Running Code ------')
vm = VirtualMachine(generator.code, string_list = generator.H)
vm.run()
print('----------------------------')

