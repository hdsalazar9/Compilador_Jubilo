#Hector David Salazar Schz, A01207471.
#Melanie Vielma Saldana, A00818905.
#Diseno de compiladores Ago-Dic 2019. ITESM.
#Jubilo
import ply.lex as lex
import ply.yacc as yacc
import sys
from Jubilo_CuboSemantico import *
from Jubilo_CuboSemantico_SFuncs import *
from Jubilo_DirFunc import *

'''
Objetos para la generacion de cuadruplos
'''
dirFunciones = Jubilo_DirFunc() #Toma el objeto de clase DirFunc para validar la existecia de funciones
operValida = Jubilo_CuboSemantico() # Toma el objeto de clase CuboSemantico para validar operaciones
funcValida = Jubilo_CuboSemantico_SFuncs() #Toma el objeto de clase CuboSemanticoSFuncs para validar funciones

'''
Pilas para la generacion de cuadruplos
'''
pOperandos = [] # pila que almacena operandos de la expresion
pOperadores = [] # pila que almacena operadores de la expresion
pTipos = [] # pila que almacena los tipos de los operandos de la expresion

'''
Variables para validacion de funciones
'''
currentFunction = 'globals' # string nombre de funcion actual

'''
Funciones para simular y manejar pilas (push, pop, top)
'''
#Toma el ultimo elemento de Pila de Operandos
def popOperandos():
    global pOperandos
    return pOperandos.pop()

#Toma el ultimo elemento de Pila de Operandos
def popOperadores():
    global pOperadores
    return pOperadores.pop()

#Toma el ultimo elemento de Pila de Tipos
def popTipos():
    global pTipos
    return pTipos.pop()

#Simula push stack para anadir nuevo operando
def pushOperando(operando):
    global pOperandos
    pOperandos.append(operando)

#Simula push stack para anadir nuevo operador
def pushOperador(operador):
    global pOperadores
    pOperadores.append(operador)

#Simula push stack para anadir nuevo tipo
def pushTipo(tipo):
    global pTipos
    pTipos.append(tipo)












#List of language tokens
tokens = [
    'PROGRAM','VOID','MAIN','ID','FUNC','COMMENT', #palabras de programa
    'PRINT','READ','RETURN','IF','ELSE','WHILE', #palabras de programa, condiciones y ciclos
    'INT_TYPE','FLOAT_TYPE','BOOL_TYPE','CHAR_TYPE','STRING_TYPE', #tipos de datos
    'PLUS_OP','MINUS_OP','MULT_OP','DIV_OP','EQUAL_OP', #operadores
    'EQUAL_LOG','LESS_LOG','LEQUAL_LOG','GREAT_LOG', #operadores logicos
    'GEQUAL_LOG','DIFF_LOG','OR_LOG','AND_LOG', #operadores logicos
    'LPAREN','RPAREN','LBRACK','RBRACK','LCURLY','RCURLY', #simbolos para conjuntos
    'COMMA','SEMIC','COLON', #simbolos para conjuntos
    'ARRANGE','ZEROS','ONES','SUM','FACT', #funciones especiales
    'MEAN','MEDIAN','MODE','STDEV','VAR', #funciones especiales
    'COVARIANCE','CORRELATION', 'SORT','TRANSPOSE', #funciones especiales
    'READCSV','EXPORTCSV', 'PLOTHIST','PLOTLINE', #funciones especiales
    'EXCHANGE','LINEAREG', 'RANDINT','RANDFLOAT', #funciones especiales
    'RANDINTMAT','RANDFLOATMAT', #funciones especiales
    'FLOAT_CTE','INT_CTE','BOOL_CTE','CHAR_CTE','STRING_CTE' #constantes
]

#Defining token Reg Expressions
t_PLUS_OP = r'\+'
t_MINUS_OP = r'-'
t_MULT_OP = r'\*'
t_DIV_OP = r'/'
t_EQUAL_OP = r'\='
t_EQUAL_LOG = r'\=\='
t_LESS_LOG = r'\<'
t_LEQUAL_LOG = r'\<\='
t_GREAT_LOG = r'\>'
t_GEQUAL_LOG = r'\>\='
t_DIFF_LOG = r'\!\='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACK = r'\['
t_RBRACK = r'\]'
t_LCURLY = r'\{'
t_RCURLY = r'\}'
t_COMMA = r'\,'
t_SEMIC = r'\;'
t_COLON = r'\:'
t_ignore = ' \t\n'

def t_FLOAT_CTE(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_INT_CTE(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_STRING_CTE(t):
    r'\"[a-z][a-zA-Z0-9_]*\"'
    t.value = str(t.value)
    return t

def t_CHAR_CTE(t):
    r'\'[a-z][a-zA-Z0-9_]\''
    t.value = chr(t.value)
    return t

def t_COMMENT(t):
    r'\~.*'
    return t

#Recognizing string literals
def t_ID(t):
    r'[a-z][a-zA-Z0-9_]*'
    if t.value == 'program':
        t.type = 'PROGRAM'
    elif t.value == 'void':
        t.type = 'VOID'
    elif t.value == 'main':
        t.type = 'MAIN'
    elif t.value == 'func':
        t.type = 'FUNC'
    elif t.value == 'print':
        t.type = 'PRINT'
    elif t.value == 'read':
        t.type = 'READ'
    elif t.value == 'if':
        t.type = 'IF'
    elif t.value == 'else':
        t.type = 'ELSE'
    elif t.value == 'while':
        t.type = 'WHILE'
    elif t.value == 'int':
        t.type = 'INT_TYPE'
    elif t.value == 'float':
        t.type = 'FLOAT_TYPE'
    elif t.value == 'bool':
        t.type = 'BOOL_TYPE'
    elif t.value == 'char':
        t.type = 'CHAR_TYPE'
    elif t.value == 'string':
        t.type = 'STRING_TYPE'
    elif t.value == 'true' or t.value == 'TRUE':
        t.type = 'BOOL_CTE'
    elif t.value == 'false' or t.value == 'FALSE':
        t.type = 'BOOL_CTE'
    elif t.value == 'or' or t.value == 'OR':
        t.type = 'OR_LOG'
    elif t.value == 'and' or t.value == 'AND':
        t.type = 'AND_LOG'
    elif t.value == 'arrange':
        t.type = 'ARRANGE'
    elif t.value == 'zeros':
        t.type = 'ZEROS'
    elif t.value == 'ones':
        t.type = 'ONES'
    elif t.value == 'sum':
        t.type = 'SUM'
    elif t.value == 'fact':
        t.type = 'FACT'
    elif t.value == 'mean':
        t.type = 'MEAN'
    elif t.value == 'median':
        t.type = 'MEDIAN'
    elif t.value == 'mode':
        t.type = 'MODE'
    elif t.value == 'stdev':
        t.type = 'STDEV'
    elif t.value == 'var':
        t.type = 'VAR'
    elif t.value == 'sort':
        t.type = 'SORT'
    elif t.value == 'transpose':
        t.type = 'TRANSPOSE'
    elif t.value == 'covariance':
        t.type = 'COVARIANCE'
    elif t.value == 'correlation':
        t.type = 'CORRELATION'
    elif t.value == 'readcsv':
        t.type = 'READCSV'
    elif t.value == 'exportcsv':
        t.type = 'EXPORTCSV'
    elif t.value == 'plothist':
        t.type = 'PLOTHIST'
    elif t.value == 'plotline':
        t.type = 'PLOTLINE'
    elif t.value == 'exchange':
        t.type = 'EXCHANGE'
    elif t.value == 'linear':
        t.type = 'LINEAREG'
    elif t.value == 'randint':
        t.type = 'RANDINT'
    elif t.value == 'randfloat':
        t.type = 'RANDFLOAT'
    elif t.value == 'randintmat':
        t.type = 'RANDINTMAT'
    elif t.value == 'randfloatmat':
        t.type = 'RANDFLOATMAT'
    elif t.value == 'return':
        t.type == 'RETURN'
    else:
        t.type = 'ID'
    return t

#Generic Error
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)



#Grammar Rules por Parser

#Declaracion de id programa inicial
def p_programa(p):
    '''
    programa : PROGRAM ID COLON vars function main
    '''
    print("Programa \"", p[2], "\" terminado.")

#Declaracion de variables, puede ser recursivo y declarar varias variables
def p_vars(p):
    '''
    vars : type ID vars_predicate vars
         | empty
    '''
    print("Variable", "de tipo ", " creada.")

#Predicados posibles para la declaracion de variables
def p_vars_predicate(p):
    '''
    vars_predicate : pnVarSimple SEMIC
                   | vars_assign SEMIC
                   | vars_array SEMIC
    '''

#Asignacion de constante a una variable declarada
def p_vars_assign(p):
    '''
    vars_assign : EQUAL_OP constante
    '''

#Creacion de variable de tipo arreglo o matriz
def p_vars_array(p):
    '''
    vars_array : LBRACK INT_CTE RBRACK vars_array_predicate
    '''

#Predicados posibles para la declaracion de arreglos
def p_vars_array_predicate(p):
    '''
    vars_array_predicate : empty
                         | vars_array_assign
                         | vars_matrix
    '''

#Asignacion de [constantes] a un arreglo declarado
def p_vars_array_assign(p):
    '''
    vars_array_assign : EQUAL_OP LBRACK constante constante_loop RBRACK
    '''

#Permite agregar varias constantes a la declaracion del arreglo
def p_constante_loop(p):
    '''
    constante_loop : empty
                   | COMMA constante constante_loop
    '''

#Cuando se tienen dos pares de [] lo convierte en una matriz
def p_vars_matrix(p):
    '''
    vars_matrix : LBRACK INT_CTE RBRACK vars_matrix_predicate
    '''

#Predicados posibles para la declaracion de matrices
def p_vars_matrix_predicate(p):
    '''
    vars_matrix_predicate : empty
                          | vars_matrix_assign
    '''

#Asignacion de variables a la matriz desde declaracion
def p_vars_matrix_assign(p):
    '''
    vars_matrix_assign : EQUAL_OP LBRACK array array_loop RBRACK
    '''

#Estructura de un arreglo, con minimo un dato y posibles mas
def p_array(p):
    '''
    array : LBRACK constante constante_loop RBRACK
    '''

#Asignacion de mas de un arreglo a una posible lista de arreglos (matriz)
def p_array_loop(p):
    '''
    array_loop : empty
               | COMMA array array_loop
    '''

#Declaracion de funciones del usuario
def p_function(p):
    '''
    function : empty
             | FUNC type ID LPAREN function_predicate RPAREN vars bloque function
    '''

def p_function_predicate(p):
    '''
    function_predicate : func_params
                       | empty
    '''

def p_func_params(p):
    '''
    func_params : type ID func_params_loop
    '''

def p_func_params_loop(p):
    '''
    func_params_loop : COMMA func_params
                     | empty
    '''

def p_type(p):
    '''
    type : INT_TYPE
         | FLOAT_TYPE
         | BOOL_TYPE
         | CHAR_TYPE
         | STRING_TYPE
    '''
    p[0] = p[1]

def p_constante(p):
    '''
    constante : BOOL_CTE
              | STRING_CTE
              | CHAR_CTE
              | MINUS_OP constante_num
              | constante_num
    '''

def p_constante_num(p):
    '''
    constante_num : INT_CTE
                  | FLOAT_CTE
    '''

def p_main(p):
    '''
    main : VOID MAIN LPAREN RPAREN bloque
    '''
    global dirFunciones
    global currentFunction
    currentFunction = 'main'
    #Creacion de main en el directorio de funciones, con cero parametros
    dirFunciones.add_function(currentFunction, p[1], 0)

def p_bloque(p):
    'bloque : LCURLY bloque_predicate RCURLY'
    print("Bloque creado.")

def p_bloque_predicate(p):
    '''
    bloque_predicate : estatuto bloque_predicate
                     | empty
    '''

def p_estatuto(p):
    '''
    estatuto : asignacion
             | condicion
             | escritura
             | lectura
             | sfunc_call
             | ciclo
             | retorno
    '''
    print("Creado estatuto de:", p[1])

def p_sfunc_call(p):
    '''
    sfunc_call : sfunc SEMIC
    '''

def p_asignacion(p):
    '''
    asignacion : ID asignacion_predicate EQUAL_OP full_exp SEMIC
    '''
    p[0] = "Asignacion"

def p_asignacion_predicate(p):
    '''
    asignacion_predicate : empty
                         | LBRACK full_exp RBRACK asignacion_array_predicate
    '''

def p_asignacion_array_predicate(p):
    '''
    asignacion_array_predicate : empty
                               | LBRACK full_exp RBRACK
    '''

def p_condicion(p):
    'condicion : IF LPAREN full_exp RPAREN bloque condicion_else SEMIC'
    p[0] = "Condicion"

def p_condicion_else(p):
    '''
    condicion_else : ELSE bloque
                   | empty
    '''

def p_escritura(p):
    'escritura : PRINT LPAREN full_exp full_exp_loop RPAREN SEMIC'
    p[0] = "Escritura"

def p_full_exp_loop(p):
    '''
    full_exp_loop : empty
                  | COMMA full_exp full_exp_loop
    '''

def p_lectura(p):
    '''
    lectura : READ LPAREN ID asignacion_predicate RPAREN SEMIC
    '''

def p_ciclo(p):
    '''
    ciclo : WHILE LPAREN full_exp RPAREN bloque SEMIC
    '''

def p_full_exp(p):
    '''
    full_exp : expresion
             | log_exp
    '''

def p_log_exp(p):
    '''
    log_exp : OR_LOG
            | AND_LOG
    '''

def p_expresion(p):
    '''
    expresion : exp
              | exp expresion_operador exp
    '''
    print("Expresion creada.")

def p_expresion_operador(p):
    '''
    expresion_operador : LESS_LOG
                       | GREAT_LOG
                       | LEQUAL_LOG
                       | GEQUAL_LOG
                       | EQUAL_LOG
                       | DIFF_LOG
    '''

def p_exp(p):
    '''
    exp : termino exp_predicate
    '''

def p_exp_predicate(p):
    '''
    exp_predicate : PLUS_OP exp
                  | MINUS_OP exp
                  | empty
    '''

def p_termino(p):
    'termino : factor termino_predicate'

def p_termino_predicate(p):
    '''
    termino_predicate : DIV_OP termino
                      | MULT_OP termino
                      | empty
    '''

def p_factor(p):
    '''
    factor : var_cte
           | LPAREN full_exp RPAREN
    '''

def p_retorno(p):
    '''
    retorno : RETURN full_exp SEMIC
    '''

def p_var_cte(p):
    '''
    var_cte : sfunc
            | constante
            | ID pnQuadGen1 var_cte_predicate
    '''

def p_var_cte_predicate(p):
    '''
    var_cte_predicate : asignacion_predicate
                      | LPAREN full_exp full_exp_loop RPAREN
    '''

def p_sfunc(p):
    '''
    sfunc : ARRANGE spfunc_two_params
          | ZEROS spfunc_params
          | ONES spfunc_params
          | SUM spfunc_params
          | FACT spfunc_params
          | MEAN spfunc_params
          | MEDIAN spfunc_params
          | MODE spfunc_params
          | STDEV spfunc_params
          | VAR spfunc_params
          | SORT spfunc_params
          | TRANSPOSE spfunc_params
          | READCSV spfunc_params
          | PLOTHIST spfunc_params
          | COVARIANCE spfunc_two_params
          | CORRELATION spfunc_two_params
          | EXPORTCSV spfunc_two_params
          | PLOTLINE spfunc_two_params
          | EXCHANGE spfunc_two_params
          | LINEAREG spfunc_two_params
          | RANDINT spfunc_three_params
          | RANDFLOAT spfunc_three_params
          | RANDINTMAT spfunc_four_params
          | RANDFLOATMAT spfunc_four_params
    '''

def p_spfunc_params(p):
    '''
    spfunc_params : LPAREN full_exp RPAREN
    '''

def p_spfunc_two_params(p):
    '''
    spfunc_two_params : LPAREN full_exp COMMA full_exp RPAREN
    '''

def p_spfunc_three_params(p):
    '''
    spfunc_three_params : spfunc_two_params
                        | LPAREN full_exp COMMA full_exp COMMA full_exp RPAREN
    '''

def p_spfunc_four_params(p):
    '''
    spfunc_four_params : LPAREN full_exp COMMA full_exp COMMA full_exp COMMA full_exp RPAREN
    '''

def p_empty(p):
    'empty : '
    p[0] = None

def p_error(p):
    print("Syntax error at '%s'" % p)


##Funciones de generacion de cuadruplos
'''
Punto neuralgico de anadir id a pOper y pType
'''
def p_pnQuadGen1(p):
    '''
        pnQuadGen1 :
    '''
    global currentFunction
    global dirFunciones
    global pOperandos
    global pTipos
    varId = p[-1]
    pushOperador(varId)
    varTipo = dirFunciones.search_varType(currentFunction, varId)
    pushTipo(varTipo)
    print(pOperadores)
    print(pTipos)

'''
Punto neuralgico recepcion de variable y su anadidura a su variable
'''
def p_pnVarSimple(p):
    '''
        pnVarSimple :
    '''
    varTipo = p[-2]
    varId = p[-1]
    global currentFunction
    global dirFunciones
    #Agregar variable simple a directorio de funciones en current function
    dirFunciones.add_varToFunction(currentFunction, varId, varTipo, 0, 0)


#Defining Lexer & Parser
parser = yacc.yacc()
lexer = lex.lex()

#Testing of parser
while True:

    #Input of lines of code
    print("Jubilo >")
    try:
        s = input("> ")
    except EOFError:
        break
    parser.parse(s)
