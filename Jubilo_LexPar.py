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
pSaltos = [] #pila que almacena los indices de saltos para condiciones y ciclos

'''
Manejo de cuadruplos
'''
arregloCuads = [] #arreglo para guardar todos los cuadruplos generados

'''
Constantes
'''
GLOBAL_CONTEXT = 'globals'
OPERADORES_SUMARESTA = ['+','-']
OPERADORES_MULTDIV = ['*','/']
OPERADORES_RELACIONALES = ['>', '<', '>=', '<=', '==', '!=']
OPERADORES_LOGICOS = ['&&', '||']
OPERADOR_ASIGNACION = ['=']
OPERADOR_SECUENCIAL = ['read', 'print']

'''
Variables para validacion de funciones
'''
currentFunction = GLOBAL_CONTEXT # string nombre de funcion actual


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

#Toma el ultimo elemento de Pila de Saltos
def popSaltos():
    global pSaltos
    return pSaltos.pop()

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

#Simula push stack para anadir nuevo salto
def pushSalto(salto):
    global pSaltos
    pSaltos.append(salto)

#Obtiene el ultimo operando ingresado a la pila de operandos
def topOperador():
    global pOperadores
    last = len(pOperadores) - 1
    if (last < 0):
        return 'empty'
    return pOperadores[last]

#Obtiene el ultimo tipo ingresado a la pila de tipos
def topTipo():
    global pTipos
    last = len(pTipos) - 1
    if(last < 0):
        return 'empty'
    return pTipos[last]

'''
Manejo de memoria para funcion funcion nextAvail: toma el siguiente temporal en
la pila para la generacion de cuadruplos
'''

BATCH_SIZE = 100 #tamano del espacio de memoria entre diferentes tipos de datos

'''
Espacios de memoria:
+++++++++++++++++++++++
+globales enteras     + batch_size
+---------------------+
+globales flotantes   + batch_size
+---------------------+
+globales booleanas   + batch_size
+---------------------+
+globales character   + batch_size
+++++++++++++++++++++++
+locales enteras      + batch_size
+---------------------+
+locales flotantes    + batch_size
+---------------------+
+locales booleanas    + batch_size
+---------------------+
+locales character    + batch_size
+++++++++++++++++++++++
+temp enteras         + batch_size
+---------------------+
+temp flotantes       + batch_size
+---------------------+
+temp booleanas       + batch_size
+---------------------+
+temp character       + batch_size
+++++++++++++++++++++++
+constantes enteras   + batch_size
+---------------------+
+constantes flotantes + batch_size
+---------------------+
+constantes booleanas + batch_size
+---------------------+
+constantes character + batch_size
+++++++++++++++++++++++
'''
#Declaracion de inicio de espacio de memoria por tipo de memoria
index_intGlobales = BATCH_SIZE
index_floatGlobales = index_intGlobales + BATCH_SIZE
index_boolGlobales = index_floatGlobales + BATCH_SIZE
index_charGlobales = index_boolGlobales + BATCH_SIZE
index_intLocales = index_charGlobales + BATCH_SIZE
index_floatLocales = index_intLocales + BATCH_SIZE
index_boolLocales = index_floatLocales + BATCH_SIZE
index_charLocales = index_boolLocales + BATCH_SIZE
index_intTemporales = index_charLocales + BATCH_SIZE
index_floatTemporales = index_intTemporales + BATCH_SIZE
index_boolTemporales = index_floatTemporales + BATCH_SIZE
index_charTemporales = index_boolTemporales + BATCH_SIZE
index_intConstantes = index_charTemporales + BATCH_SIZE
index_floatConstantes = index_intConstantes + BATCH_SIZE
index_boolConstantes = index_floatConstantes + BATCH_SIZE
index_charConstantes = index_boolConstantes + BATCH_SIZE

#Declaracion de inicio de index de memoria para temporales
cont_IntTemp = index_charLocales
cont_FloatTemp = index_intTemporales
cont_BoolTemp = index_floatTemporales
cont_CharTemp = index_boolTemporales

#Obtiene el siguiente temporal de la pila simualda de temporales
def nextAvail(tipo):
    global cont_IntTemp
    global cont_FloatTemp
    global cont_BoolTemp
    global cont_CharTemp

    if tipo == 'int':
        if cont_IntTemp < index_intTemporales:
            avail = cont_IntTemp
            cont_IntTemp = cont_IntTemp + 1
        else:
            printErrorOutOfBounds('Enteras')

    elif tipo == 'float':
        if cont_FloatTemp < index_floatTemporales:
            avail = cont_FloatTemp
            cont_FloatTemp = cont_FloatTemp + 1
        else:
            printErrorOutOfBounds('Flotantes')

    elif tipo == 'bool':
        if cont_BoolTemp < index_boolTemporales:
            avail = cont_BoolTemp
            cont_BoolTemp = cont_BoolTemp + 1
        else:
           printErrorOutOfBounds('Boleanas')

    elif tipo == 'char':
        if cont_CharTemp < index_charTemporales:
            avail = cont_CharTemp
            cont_CharTemp = cont_CharTemp + 1
        else:
            printErrorOutOfBounds('Caracter')
    else:
        avail = -1
        #En teoria nunca deberia llegar aqui D:!
        print("Error: Tipo de variable desconocida.")
    return avail

'''
Funciones para desplegar mensajes genericos como errores o infos
'''
#Funcion para mostrar un mensaje de error cuando se llena los maximos posibles valores temporales
def printErrorOutOfBounds(tipoDato):
    print("Error: Memoria llena; demasiadas temporales de tipo {}.".format(tipoDato))

#Funcion para mostrar un mensaje de error generico entre un operador
#y dos operandos junto con su tipo
def printErrorOperacionInvalida(rOp, rTy, lOp, lTy, Op):
    print("Error: Imposible realizar operacion {} con operadores ({} de tipo {}) y ({} de tipo {}).".format(Op, rOp, rTy, lOp, lTy))

def printTypeMismatch():
    print('Error: Tipo de dato incorrecto')

#Funcion para desplegar como quedaria
def printAuxQuad(quad_operator, quad_leftOper, quad_rightOper, quad_result):
    print("Quadruplo: ('{}','{}','{}','{}')".format(quad_operator, quad_leftOper, quad_rightOper, quad_result))


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
t_OR_LOG = r'\|\|'
t_AND_LOG = r'\&\&'
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
    programa : PROGRAM ID COLON vars vars_loop function main
    '''
    print("Programa \"", p[2], "\" terminado.")

#Declaracion de variables, puede ser recursivo y declarar varias variables
def p_vars(p):
    '''
    vars : type ID vars_predicate
    '''
    #print("Variable", "de tipo ", " creada.")

#Permite que en el inicio de un programa pueda crear varias variables globales
def p_vars_loop(p):
    '''
    vars_loop : vars vars_loop
              | empty
    '''

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
    main : VOID MAIN LPAREN RPAREN pnCreateFunctionMain bloque
    '''

def p_bloque(p):
    'bloque : LCURLY bloque_predicate RCURLY'
    print("Bloque creado.")

def p_bloque_predicate(p):
    '''
    bloque_predicate : empty
                     | estatuto bloque_predicate
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
             | vars
    '''
    print("Creado estatuto de:", p[1])

def p_sfunc_call(p):
    '''
    sfunc_call : sfunc SEMIC
    '''

def p_asignacion(p):
    '''
    asignacion : ID pnQuadGenExp1 asignacion_predicate EQUAL_OP pnQuadGenSec1 full_exp  SEMIC pnQuadGenSec2
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
    'condicion : IF LPAREN full_exp RPAREN pnQuadGenCond1 bloque condicion_else SEMIC pnQuadGenCond2'
    p[0] = "Condicion"

def p_condicion_else(p):
    '''
    condicion_else : ELSE pnQuadGenCond3 bloque
                   | empty
    '''

def p_escritura(p):
    'escritura : PRINT pnQuadGenSec3 LPAREN full_exp full_exp_loop RPAREN SEMIC pnQuadGenSec4'
    p[0] = "Escritura"

def p_full_exp_loop(p):
    '''
    full_exp_loop : empty
                  | COMMA full_exp full_exp_loop
    '''

def p_lectura(p):
    '''
    lectura : READ pnQuadGenSec3 LPAREN ID pnQuadGenExp1 asignacion_predicate RPAREN SEMIC pnQuadGenSec4
    '''

def p_ciclo(p):
    '''
    ciclo : WHILE LPAREN full_exp RPAREN bloque SEMIC
    '''

def p_full_exp(p):
    '''
    full_exp : expresion log_exp
    '''

def p_log_exp(p):
    '''
    log_exp : OR_LOG pnQuadGenExp10 full_exp pnQuadGenExp11
            | AND_LOG pnQuadGenExp10 full_exp pnQuadGenExp11
            | empty
    '''

def p_expresion(p):
    '''
    expresion : exp
              | exp expresion_operador pnQuadGenExp8 exp pnQuadGenExp9
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
    p[0] = p[1]

def p_exp(p):
    '''
    exp : termino  pnQuadGenExp4 exp_predicate
    '''

def p_exp_predicate(p):
    '''
    exp_predicate : PLUS_OP pnQuadGenExp2 exp
                  | MINUS_OP pnQuadGenExp2 exp
                  | empty
    '''

def p_termino(p):
    'termino : factor pnQuadGenExp5 termino_predicate '

def p_termino_predicate(p):
    '''
    termino_predicate : DIV_OP pnQuadGenExp3 termino
                      | MULT_OP pnQuadGenExp3 termino
                      | empty
    '''

def p_factor(p):
    '''
    factor : var_cte
           | LPAREN pnQuadGenExp6 full_exp RPAREN pnQuadGenExp7
    '''

def p_retorno(p):
    '''
    retorno : RETURN full_exp SEMIC
    '''

def p_var_cte(p):
    '''
    var_cte : sfunc
            | constante
            | ID pnQuadGenExp1 var_cte_predicate
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
    '''
    empty :
    '''
    p[0] = None


def p_error(p):
    print ("Syntax error in line " + str(lexer.lineno))
    sys.exit()
    return


##Puntos neuralgicos

'''
Creacion de main en el directorio de funciones, con cero parametros
'''
def p_pnCreateFunctionMain(p):
    '''
    pnCreateFunctionMain :
    '''
    global dirFunciones
    global currentFunction
    currentFunction = 'main'
    dirFunciones.add_function(currentFunction, 'void', 0)

'''
Punto neuralgico de anadir id a pOper y pType
'''
def p_pnQuadGenExp1(p):
    '''
        pnQuadGenExp1 :
    '''
    global currentFunction
    global dirFunciones
    global pOperandos
    global pTipos
    varId = p[-1]
    #Buscar el tipo de la variable en su contexto, sino la encuentra buscar en globales
    varTipo = dirFunciones.search_varType(currentFunction, varId)
    if not varTipo:
        varTipo = dirFunciones.search_varType(GLOBAL_CONTEXT, varId)
    #Si tampoco se encuentra en el contexto global, no existe la variable
    if not varTipo:
        print("Error: Variable ", varId , " no declarada.")
        return
    pushOperando(varId)
    pushTipo(varTipo)
    print("pnQuadGenExp1 poperando: ", pOperandos)
    print("pnQuadGenExp1 ptipos: ", pTipos)

'''
Punto neuralgico para anadir un + o - a la pila de operadores pOper
'''
def p_pnQuadGenExp2(p):
    '''
    pnQuadGenExp2 :
    '''
    global pOperadores
    if p[-1] not in OPERADORES_SUMARESTA:
        print("Error: Operador no esperado.")
    else:
        pushOperador(p[-1])
        print("pnQuadGenExp2 pOperadores: ", pOperadores)

'''
Punto neuralgico para anadir un * o / a la pila de operadores pOper
'''
def p_pnQuadGenExp3(p):
    '''
    pnQuadGenExp3 :
    '''
    global pOperadores
    if p[-1] not in OPERADORES_MULTDIV:
        print("Error: Operador no esperado.")
    else:
        pushOperador(p[-1])
        print("pnQuadGenExp3 pOperadores: ", pOperadores)

'''
Punto neuralgico para checar si el top de la pila de operadores es
un + o - para crear el cuadruplo de esa operacion
'''
def p_pnQuadGenExp4(p):
    '''
    pnQuadGenExp4 :
    '''
    if topOperador() in OPERADORES_SUMARESTA:
        quad_rightOper = popOperandos()
        quad_rightType = popTipos()
        quad_leftOper = popOperandos()
        quad_leftType = popTipos()
        quad_operator = popOperadores()
        global operValida
        quad_resultType = operValida.get_tipo(quad_leftType, quad_rightType, quad_operator)
        print("Intentar obtener quad de {}, {}, {}, result: {}".format(quad_leftType, quad_rightType, quad_operator, quad_resultType))
        if quad_resultType == 'error':
            printErrorOperacionInvalida(quad_rightOper, quad_rightType, quad_leftOper, quad_leftType, quad_operator)
        else:
            #quad_result = direccion de memoria donde se guardara el tipo de dato
            quad_resultIndex = nextAvail(quad_resultType)
            printAuxQuad(quad_operator, quad_leftOper, quad_rightOper, quad_resultIndex)
            pushOperando(quad_resultIndex)
            pushTipo(quad_resultType)

'''
Punto neuralgico para checar si el top de la pila de operadores es
una * o / para crear el cuadruplo de esa operacion
'''
def p_pnQuadGenExp5(p):
    '''
    pnQuadGenExp5 :
    '''
    if topOperador() in OPERADORES_MULTDIV:
        quad_rightOper = popOperandos()
        quad_rightType = popTipos()
        quad_leftOper = popOperandos()
        quad_leftType = popTipos()
        quad_operator = popOperadores()
        global operValida
        quad_resultType = operValida.get_tipo(quad_leftType, quad_rightType, quad_operator)
        print("Intentar obtener quad de {}, {}, {}, result: {}".format(quad_leftType, quad_rightType, quad_operator, quad_resultType))
        if quad_resultType == 'error':
            printErrorOperacionInvalida(quad_rightOper, quad_rightType, quad_leftOper, quad_leftType, quad_operator)
        else:
            #quad_result = direccion de memoria donde se guardara el tipo de dato
            quad_resultIndex = nextAvail(quad_resultType)
            printAuxQuad(quad_operator, quad_leftOper, quad_rightOper, quad_resultIndex)
            pushOperando(quad_resultIndex)
            pushTipo(quad_resultType)

'''
Punto neuralgico para agregar fondo falso por parentesis izquierdo
'''
def p_pnQuadGenExp6(p):
    '''
    pnQuadGenExp6 :
    '''
    pushOperador('(')

'''
Punto neuralgico para quitar fondo falso por parentesis izquierdo
'''
def p_pnQuadGenExp7(p):
    '''
    pnQuadGenExp7 :
    '''
    tipo = popOperadores()

'''
Punto neuralgico para meter un operador relacional a la pila de operadores
'''
def p_pnQuadGenExp8(p):
    '''
    pnQuadGenExp8 :
    '''
    global pOperadores
    if p[-1] not in OPERADORES_RELACIONALES:
        print("Error: Operador no esperado.")
    else:
        pushOperador(p[-1])
        print("pnQuadGenExp8 pOperadores: ", pOperadores)

'''
Punto neuralgico para checar si el top de la pila de operadores es un
> < >= <= == != para crear el cuadruplo de esa operacion
'''
def p_pnQuadGenExp9(p):
    '''
    pnQuadGenExp9 :
    '''
    if topOperador() in OPERADORES_RELACIONALES:
        quad_rightOper = popOperandos()
        quad_rightType = popTipos()
        quad_leftOper = popOperandos()
        quad_leftType = popTipos()
        quad_operator = popOperadores()
        global operValida
        quad_resultType = operValida.get_tipo(quad_leftType, quad_rightType, quad_operator)
        print("Intentar obtener quad de {}, {}, {}, result: {}".format(quad_leftType, quad_rightType, quad_operator, quad_resultType))
        if quad_resultType == 'error':
            printErrorOperacionInvalida(quad_rightOper, quad_rightType, quad_leftOper, quad_leftType, quad_operator)
        else:
            #quad_result = direccion de memoria donde se guardara el tipo de dato
            quad_resultIndex = nextAvail(quad_resultType)
            printAuxQuad(quad_operator, quad_leftOper, quad_rightOper, quad_resultIndex)
            pushOperando(quad_resultIndex)
            pushTipo(quad_resultType)

'''
Punto neuralgico para meter un operador logico a la pila de operadores
'''
def p_pnQuadGenExp10(p):
    '''
    pnQuadGenExp10 :
    '''
    global pOperadores
    if p[-1] not in OPERADORES_LOGICOS:
        print("Error: Operador no esperado.")
    else:
        pushOperador(p[-1])
        print("pnQuadGenExp10 pOperadores: ", pOperadores)

'''
Punto neuralgico para checar si el top de la pila de operadores es un && o un !!
para crear el cuadruplo de esa operacion
'''
def p_pnQuadGenExp11(p):
    '''
    pnQuadGenExp11 :
    '''
    if topOperador() in OPERADORES_LOGICOS:
        quad_rightOper = popOperandos()
        quad_rightType = popTipos()
        quad_leftOper = popOperandos()
        quad_leftType = popTipos()
        quad_operator = popOperadores()
        global operValida
        quad_resultType = operValida.get_tipo(quad_leftType, quad_rightType, quad_operator)
        print("Intentar obtener quad de {}, {}, {}, result: {}".format(quad_leftType, quad_rightType, quad_operator, quad_resultType))
        if quad_resultType == 'error':
            printErrorOperacionInvalida(quad_rightOper, quad_rightType, quad_leftOper, quad_leftType, quad_operator)
        else:
            #quad_result = direccion de memoria donde se guardara el tipo de dato
            quad_resultIndex = nextAvail(quad_resultType)
            printAuxQuad(quad_operator, quad_leftOper, quad_rightOper, quad_resultIndex)
            pushOperando(quad_resultIndex)
            pushTipo(quad_resultType)

'''
Punto neuralgico para meter = a la pila de operadores
'''
def p_pnQuadGenSec1(p):
    '''
    pnQuadGenSec1 :
    '''
    global pOperadores
    if p[-1] not in OPERADOR_ASIGNACION:
        print("Error: Operador no esperado.")
    else:
        pushOperador(p[-1])
        print("pnQuadGenSec1 pOperadores: ", pOperadores)

'''
Punto neuralgico para generar el cuadruplo de asignacion
'''
def p_pnQuadGenSec2(p):
    '''
    pnQuadGenSec2 :
    '''
    if topOperador() in OPERADOR_ASIGNACION:
        quad_rightOper = popOperandos() #Que le voy a asignar
        quad_rightType = popTipos()
        quad_leftOper = popOperandos() #A quien se lo voy a asignar
        quad_leftType = popTipos()
        quad_operator = popOperadores()
        global operValida
        global dirFunciones
        quad_resultType = operValida.get_tipo(quad_leftType, quad_rightType, quad_operator)
        print("Intentar obtener quad de {}, {}, {}, result: {}".format(quad_leftType, quad_rightType, quad_operator, quad_resultType))
        if dirFunciones.exist_var(currentFunction, quad_leftOper) or dirFunciones.exist_var(GLOBAL_CONTEXT, quad_leftOper):
            if quad_resultType == 'error':
                printErrorOperacionInvalida(quad_rightOper, quad_rightType, quad_leftOper, quad_leftType, quad_operator)
            else:
                #quad_result = direccion de memoria donde se guardara el tipo de dato
                printAuxQuad(quad_operator, quad_rightOper, '', quad_leftOper)
        else:
            print("Error: Intenando asignar a una no variable, de tipo: ", quad_leftType)


'''
Punto neuralgico para meter read  o print a la pila de operadores
'''
def p_pnQuadGenSec3(p):
    '''
    pnQuadGenSec3 : 
    '''
    global pOperadores
    if p[-1] not in OPERADOR_SECUENCIAL:
        print("Error: Operador no esperado.")
    else:
        pushOperador(p[-1])
        print("pnQuadGenSec3 pOperadores: ", pOperadores)

'''
Punto neuralgico para generar cuadruplos de lectura y escritura
'''
def p_pnQuadGenSec4(p):
    '''
    pnQuadGenSec4 :
    '''
    if topOperador() in OPERADOR_SECUENCIAL:
        quad_rightOper = popOperandos() #hace pop de read/write
        quad_rightType = popTipos()
        quad_operator = popOperadores()
        global operValida
        quad_resultType = operValida.get_tipo(quad_operator, quad_rightType, '')
        #print("Intentar obtener quad de {}, {}, {}, result: {}".format(quad_leftType, quad_rightType, quad_operator, quad_resultType))
        if quad_resultType == 'error':
            printErrorOperacionInvalida(quad_rightOper, quad_rightType, '', '', quad_operator)
        else:
            printAuxQuad(quad_operator, quad_rightOper, '', quad_operator)
            pushOperando(quad_rightOper)
            pushTipo(quad_resultType)

def p_pnQuadGenCond1(p):
    '''
    pnQuadGenCond1 :
    '''
    global arregloCuads
    quad_resultType = popTipos()
    if quad_resultType == 'error':
        printTypeMismatch()
    else:
        result = pOperandos()
        printAuxQuad('GOTOF', result, '', '')
        pushSalto(len(arregloCuads) - 1)

def p_pnQuadGenCond2(p):
    '''
    pnQuadGenCond2 :
    '''
    global arregloCuads
    end = popSaltos()

def p_pnQuadGenCond3(p):
    '''
    pnQuadGenCond3 :
    '''
    global arregloCuads
    printAuxQuad('GOTO', '', '','')



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
    print("tipo: ", p[-2])
    print("nombre: ", p[-1])
    #Agregar variable simple a directorio de funciones en current function
    dirFunciones.add_varToFunction(currentFunction, varId, varTipo, 0, 0)


#Defining Lexer & Parser
parser = yacc.yacc()
lexer = lex.lex()

'''
Para probar el parser desde archivo
'''
name = 'test1.txt'

with open(name, 'r') as archive:
    s = archive.read()
print(name)
parser.parse(s)

'''
#Testing of parser
while True:

    #Input of lines of code
    print("Jubilo >")
    try:
        s = input("> ")
    except EOFError:
        break
    parser.parse(s)
'''
