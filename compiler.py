# Yacc example

import ply.yacc as yacc
import ast
from parser import MyParser
from visitor import Visitor
from generator import Generator
from virtualMachine import VirtualMachine
import sys

if len(sys.argv) < 2 or '--help' in sys.argv:
    print('''Como rodar:
                ./python3 compiler.py <path_to_lya_file> <options>

             Options:
                --input : Imprime o codigo de entrada
                --tree  : Imprime a arvore decorada na tela
                --code  : Imprime o codigo gerado pelo compilador
                --run   : Executa o codigo
                --debug : Opção para mostrar instruções e stack durante a execução do código
          ''')
    exit()

# Get the token map from the lexer.  This is required.
p = MyParser()
f = open(sys.argv[1])
codigo = ''.join(f.readlines())
f.close()


if '--input' in sys.argv:
    print('---------- Input -----------')
    print(codigo)
    print('----------------------------')

ast = p.parse(codigo)
#print(ast.show())
visitor = Visitor()
visitor.visit(ast)
if '--tree' in sys.argv:
    print(ast.showDecorated())

generator = Generator()
generator.generate(ast)
if '--code' in sys.argv:
    print('------ Code generated ------')
    print('H:', generator.H)
    print('Code:', generator.code)
    print('----------------------------')

if '--run' in sys.argv:
    print('------ Running Code ------')
    vm = VirtualMachine(generator.code, string_list = generator.H, verbose='--debug' in sys.argv)
    vm.run()
    print('----------------------------')

