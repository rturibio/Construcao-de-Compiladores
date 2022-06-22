# Trabalho Final - reconhecedor de estruturas em C

from ply import *

# Palavras reservadas <palavra>:<TOKEN>
reserved = {
    'if' : 'IF',
    'else' : 'ELSE',
    'for' : 'FOR',
    'while' : 'WHILE',
    'main' : 'MAIN',
    'int' : 'INT',
    'return' : 'RETURN',
    'void' : 'VOID',
}

# Demais TOKENS
tokens = [
    'EQUALS', 'GREATER', 'LESS', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'POWER',
    'LPAREN', 'RPAREN', 'LT', 'LE', 'GT', 'GE', 'NE',
    'GREATEQ', 'LESSEQ', 'EQEQ', 'NOTEQ', 'AND','TRUE','FALSE',
    'COMMA', 'SEMI', 'INTEGER', 'FLOAT', 'STRING','OR','DOUBLE','CHAR',
    'ID', 'NEWLINE', 'SEMICOLON', 'RBRACES', 'LBRACES'
] + list(reserved.values())

t_ignore = ' \t'

def t_REM(t):
    r'REM .*'
    return t

# Definição de Identificador com expressão regular r'<expressão>'
def t_ID(t):
    r'[a-zA-Z][a-zA-Z0-9]*'
    t.type = reserved.get(t.value,'ID')    # Check for reserved words
    return t

t_EQUALS = r'='
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_POWER = r'\^'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_RBRACES = r'\}'
t_LBRACES = r'\{'
t_SEMICOLON = r'\;'
t_LT = r'<'
t_LE = r'<='
t_GT = r'>'
t_GE = r'>='
t_NE = r'!='
t_COMMA = r'\,'
t_SEMI = r';'
t_INTEGER = r'\d+'
t_FLOAT = r'((\d*\.\d+)(E[\+-]?\d+)?|([1-9]\d*E[\+-]?\d+))'
t_STRING = r'\".*?\"'

def t_NEWLINE(t):
    r'\n'
    t.lexer.lineno += 1
    return t

def t_error(t):
    print("Illegal character %s" % t.value[0])
    t.lexer.skip(1)

# Constroi o analisador léxico
lexer = lex.lex()

#precedence = (
#        ('left', 'PLUS', 'MINUS' ),
#        ('left', 'TIMES', 'DIVIDE' ),
#        ('right', 'UMINUS'),
#    )

precedence = (
    ('left','AND','OR'),
    ('left','GREATER','LESS', 'GREATEQ', 'LESSEQ', 'EQEQ', 'NOTEQ'),
    ('left','PLUS','MINUS'),
    ('left','TIMES','DIVIDE'),
    ('right','UMINUS'),
    )

names = {}

def p_estrutura_inicial(p):
    "programa : INT MAIN LPAREN RPAREN LBRACES code RBRACES"

def p_code(p):
        '''code : statement SEMICOLON
                | statement SEMICOLON code
                | statement IF expression LPAREN code RPAREN
                | statement IF expression LPAREN code RPAREN ELSE LBRACES code RBRACES'''

#def p_statement(p):
#    '''
#   statement : if_statement
#              |  if_else_statement
#    '''
#    p[0] = p[1]

#def p_if_statement(p):
#    '''
#    statement : IF expression LPAREN basicblock RPAREN
#    '''
#    p[0] = IfStatement(p[2], p[4], None, lineno=p.lineno(1))

#def p_if_else_statement(p):
#    '''
#    statement : IF expression LPAREN code RPAREN ELSE LBRACES code RBRACES
#    '''
#    p[0] = IfStatement(p[2], p[4], p[8], lineno=p.lineno(1))
    
def p_statement_assing(p):
        'statement : ID EQUALS expression'
        names[p[1]] = p[3]

def p_statement_expr(p):
        'statement : expression'
        print(p[1])

def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression'''
    if p[2] == 'PLUS':
        p[0] = p[1] + p[3]
    elif p[2] == 'MINUS':
        p[0] = p[1] - p[3]
    elif p[2] == 'TIMES':
        p[0] = p[1] * p[3]
    elif p[2] == 'DIVIDE':
        p[0] = p[1] / p[3]

def p_expression_uminus(p):
    "expression : '-' expression %prec UMINUS"
    p[0] = -p[2]

def p_expression_group(p):
    "expression : LPAREN expression RPAREN"
    p[0] = p[2]

def p_expression_number(p):
    "expression : INTEGER"
    "expression : FLOAT"
    p[0] = p[1]

def p_expression_double(p):
    'expression : DOUBLE'
    p[0] = p[1]

def p_expression_char(p):
    'expression : CHAR'
    p[0] = p[1]

def p_expression_logop(P):
    '''expression : expression GREATER expression
                  | expression LESS expression
                  | expression GREATEQ expression
                  | expression LESSEQ expression
                  | expression EQEQ expression
                  | expression NOTEQ expression
                  | expression AND expression
                  | expression OR expression'''
    if p[2] == '>'  : p[0] = p[1] > p[3]
    elif p[2] == '<': p[0] = p[1] < p[3]
    elif p[2] == '>=': p[0] = p[1] >= p[3]
    elif p[2] == '<=': p[0] = p[1] <= p[3]
    elif p[2] == '==': p[0] = p[1] == p[3]
    elif p[2] == '!=': p[0] = p[1] != p[3]
    elif p[2] == '&': p[0] = p[1] and p[3]
    elif p[2] == '|': p[0] = p[1] or p[3]

def p_expression_name(p):
    "expression : ID"
    try:
        p[0] = names[p[1]]
    except LookupError:
        print("Undefined name '%s'" % p[1])
        p[0] = 0
        
def p_expression_bool(p):
    'expression : bool'
    p[0] = p[1]

def p_true(p):
    'bool : TRUE'
    p[0] = True

def p_false(p):
    'bool : FALSE'
    p[0] = False

def p_error(p):
    if p:
        print("Syntax error in input at token '%s'" % p.value)
    else:
        print("EOF","Syntax error. No more input.")

#import ply.yacc as yacc
#yacc.yacc()
        
# string de teste
data = '''

int main()
{
    float a;
    int b, resultado;
     a = 4.0;
     b = 6;
     if(a>= 10){
         resultado = a -  b;
     }else{
         resultado = a +  b;
     }
}

            '''

# string de teste como entrada do analisador léxico
lexer.input(data)

# Tokenização
for tok in lexer:
     print(tok)

import ply.yacc as yacc
yacc.yacc()

print(data)

## Se comentar para os erros !!!!
yacc.parse(data)
