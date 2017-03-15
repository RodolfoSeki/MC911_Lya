import ply.lex as lex
import sys

class MyLexer(object):

    # Dict of reserved words
    reserved = {
            'array' : 'ARRAY', 
            'by' : 'BY', 
            'chars' : 'CHARS', 
            'dcl' : 'DCL', 
            'do' : 'DO', 
            'down' : 'DOWN', 
            'else' : 'ELSE', 
            'elsif' : 'ELSIF', 
            'end' : 'END', 
            'exit' : 'EXIT', 
            'fi' : 'FI',
            'for' : 'FOR', 
            'if' : 'IF', 
            'in' : 'IN', 
            'loc' : 'LOC', 
            'od' : 'OD', 
            'print' : 'PRINT',
            'proc' : 'PROC', 
            'ref' : 'REF', 
            'result' : 'RESULT', 
            'return' : 'RETURN', 
            'returns' : 'RETURNS',
            'syn' : 'SYN', 
            'then' : 'THEN', 
            'to' : 'TO', 
            'type' : 'TYPE', 
            'while' : 'WHILE',
            'abs' : 'ABS',
            'asc' : 'ASC',
            'bool' : 'BOOL',
            'char' : 'CHAR',
            'false' : 'FALSE',
            'int' : 'INT',
            'length' : 'LENGTH',
            'lower' : 'LOWER',
            'null' : 'NULL',
            'num' : 'NUM',
            'print' : 'PRINT',
            'read' : 'READ',
            'true' : 'TRUE',
            'upper' : 'UPPER'
    }


    # List of token names.   This is always required
    tokens = [
            'ID',
            'ICONST',
            'CCONST',
            'SCONST',
            'PLUS', 
            'MINUS',
            'TIMES',
            'DIVIDE',
            'MODULO',
            'EQUALS',
            'SEMI',
            'ARROW',
            'LPAREN',
            'RPAREN',
            'LBRACKET',
            'RBRACKET',
            'AND',
            'OR',
            'EQ',
            'NE',
            'GT',
            'GEQ',
            'LT',
            'LEQ',
            'COLON',
            'COMMA',
            'NOT'
            ] + list(reserved.values())

    # Regular expression rules for simple tokens
    t_PLUS = r'\+'
    t_MINUS = r'-'
    t_TIMES = r'\*'
    t_DIVIDE = r'/'
    t_MODULO = r'%'
    t_EQUALS = r'='
    t_SEMI = r';'
    t_ARROW = r'->'
    t_LPAREN  = r'\('
    t_RPAREN  = r'\)'
    t_LBRACKET = r'\['
    t_RBRACKET = r'\]'
    t_AND = r'&&'
    t_OR = r'\|\|'
    t_EQ = r'=='
    t_NE = r'!='
    t_GT = r'>'
    t_GEQ = r'>='
    t_LT = r'<'
    t_LEQ = r'<='
    t_COLON = r':'
    t_COMMA = r'\,'
    t_NOT = r'!'

    # A regular expression rule with some action code
    # Note addition of self parameter since we're in a class
    def t_ICONST(self,t):
        r'\d+'
        return t

    def t_CCONST(self,t):
        r'\'[^\\]\'|\'\^\(\d+\)\'|\'\\[nt\\]\''
        if "^(" in t.value:
            t.value = int(t.value[3:-2])
        elif '\\' in t.value:
            if t.value[2] == 'n':
                t.value = 10
            elif t.value[2] == 't':
                t.value = 11
            else:
                t.value = 92 
        else:
            t.value = ord(t.value[1])
        return t

    def t_ID(self,t):
        r'[A-Za-z_][\w_]*'
        t.type = MyLexer.reserved.get(t.value, 'ID')
        return t

    def t_SCOMMENT(self, t):
        r'\/\/.*\n'
        pass

    def t_COMMENT(self, t):
        r'\/\*(.|\n)*\*\/'
        pass

    def t_SCONST(self, t):
        #r'\"([^\"]*)\"'
        r'\"(\\.|[^\\"])*\"'
        return t

    # Define a rule so we can track line numbers
    def t_newline(self,t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    # A string containing ignored characters (spaces and tabs)
    t_ignore  = ' \t'

    # Error handling rule
    def t_error(self,t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    def t_commenterror(self,t):
        r'\/\*.*'
        print ('{}: Unterminated comment'.format(t.lexer.lineno))
        pass

    def t_stringerror(self,t):
        r'\".*\n'
        print ('{}: Unterminated string'.format(t.lexer.lineno))
        t.lexer.skip(1)

    def t_badescape(self,t):
        r'\a|\r|\f|\v'
        print ("{}: Bad string escape code '{}'".format(t.lexer.lineno, t.value))
        t.lexer.skip(1)

    # Build the lexer
    def build(self,**kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

    # Test it output
    def input(self,data):
        self.lexer.input(data)

    def token(self):
        tok = self.lexer.token()
        return tok
'''
# Build the lexer and try it out
m = MyLexer()
m.build()           # Build the lexer

# Open file
f = open(sys.argv[1])
codigo = ''.join(f.readlines())
m.test(codigo)     # Test it

'''
