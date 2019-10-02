#Héctor David Salazar Schz, A01207471.
#Diseño de compiladores Ago-Dic 2019. ITESM.
#Lexer y Parser - Jubilo
import ply.lex as lex
import ply.yacc as yacc
import sys

#List of tokens
tokens = [
    'PROGRAM','ID','SEMIC',
    'VAR','DOT','DOUBLEDOT',
    'LBRACK','RBRACK','INT_T','FLOAT_T',
    'GRET','LEST','DIFT',
    'EQUAL','LPAREN','RPAREN','PRINT',
    'CTE_STR','PLUSOP','MINUSOP',
    'DIVOP','MULTOP','IF','ELSE',
    'CTE_INT','CTE_FLO'
]

#Defining token Reg Expressions
t_SEMIC = r'\;'
t_DOT = r'\.'
t_DOUBLEDOT = r'\:'
t_LBRACK = r'\{'
t_RBRACK = r'\}'
t_DIFT = r'\<\>'
t_GRET = r'\>'
t_LEST = r'\<'
t_EQUAL = r'='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_PLUSOP = r'\+'
t_MINUSOP = r'-'
t_DIVOP = r'/'
t_MULTOP = r'\*'
t_ignore = ' \t\n'

def t_CTE_FLO(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_CTE_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t

#Recognizing string literals
def t_ID(t):
    r'[a-z][a-zA-Z0-9_]*'
    if t.value == 'program':
        t.type = 'PROGRAM'
    elif t.value == 'var':
        t.type = 'VAR'
    elif t.value == 'print':
        t.type = 'PRINT'
    elif t.value == 'cte.string':
        t.type = 'CTE_STR'
    elif t.value == 'if':
        t.type = 'IF'
    elif t.value == 'else':
        t.type = 'ELSE'
    elif t.value == 'int':
        t.type = 'INT_T'
    elif t.value == 'float':
        t.type = 'FLOAT_T'
    else:
        t.type = 'ID'
    return t

#Generic Error
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

#Grammar Rules por Parser
def p_programa(p):
    '''
    programa : PROGRAM ID DOUBLEDOT bloque
             | PROGRAM ID DOUBLEDOT vars bloque
    '''
    print("Programa \"", p[2], "\" terminado.")

def p_vars(p):
    'vars : VAR vars_2 DOUBLEDOT tipo SEMIC vars_1'
    print("Variable", p[2], "de tipo ", p[4], " creada.")

def p_vars_1(p):
    '''
    vars_1 : vars_2 DOUBLEDOT tipo SEMIC vars_1
           | empty
    '''
    if(len(p) > 2):
        print("Variable", p[1], "de tipo ", p[3], " creada.")

def p_vars_2(p):
    '''
    vars_2 : ID DOT vars_2
           | ID
    '''
    p[0] = p[1]

def p_tipo(p):
    '''
    tipo : INT_T
         | FLOAT_T
    '''
    p[0] = p[1]

def p_bloque(p):
    'bloque : LBRACK bloque_1 RBRACK'
    print("Bloque creado.")

def p_bloque_1(p):
    '''
    bloque_1 : estatuto bloque_1
             | empty
    '''

def p_estatuto(p):
    '''
    estatuto : asignacion
             | condicion
             | escritura
    '''
    print("Creado estatuto de:", p[1])

def p_asignacion(p):
    'asignacion : ID EQUAL expresion SEMIC'
    p[0] = "Asignacion"

def p_escritura(p):
    'escritura : PRINT LPAREN escritura_1 RPAREN SEMIC'
    p[0] = "Escritura"

def p_escritura_1(p):
    '''
    escritura_1 : expresion
                | CTE_STR
                | expresion DOT escritura_1
                | CTE_STR DOT escritura_1
    '''

def p_condicion(p):
    'condicion : IF LPAREN expresion RPAREN bloque condicion_else'
    p[0] = "Condicion"

def p_condicion_else(p):
    '''
    condicion_else : ELSE bloque
                   | empty
    '''

def p_expresion(p):
    'expresion : exp expresion_operador'
    print("Expresion creada.")

def p_expresion_operador(p):
    '''
    expresion_operador : DIFT exp
                       | LEST exp
                       | GRET exp
                       | empty
    '''

def p_exp(p):
    'exp : termino exp_1'

def p_exp_1(p):
    '''
    exp_1 : PLUSOP exp
          | MINUSOP exp
          | empty
    '''

def p_termino(p):
    'termino : factor termino_1'

def p_termino_1(p):
    '''
    termino_1 : DIVOP termino
              | MULTOP termino
              | empty
    '''

def p_factor(p):
    '''
    factor : factor_1
           | factor_2
    '''

def p_factor_1(p):
    'factor_1 : LPAREN expresion RPAREN'

def p_factor_2(p):
    'factor_2 : factor_3 varc'

def p_factor_3(p):
    '''
    factor_3 : PLUSOP
             | MINUSOP
             | empty
    '''

def p_varc(p):
    '''
    varc : ID
         | CTE_FLO
         | CTE_INT
    '''

def p_empty(p):
    'empty : '
    p[0] = None

def p_error(p):
    print("Syntax error at '%s'" % p)

#Defining Parser
parser = yacc.yacc()

#Lexer example
#util = "program bbcita: var uah: float; { uah = 45.45; print(uah); if(23<2){print(true);}else{print(false);}}"
#Defining the Lexer
lexer = lex.lex()
#lexer.input(util)

#Testing of parser
while True:
    # tok = lexer.token()
    # if not tok:
    #     break;
    # print(tok)

    #Input of lines of code
    try:
        s = input("Patito > ")
    except EOFError:
        break
    parser.parse(s)
