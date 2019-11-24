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
dirVars = Jubilo_TablaVars()
operValida = Jubilo_CuboSemantico() # Toma el objeto de clase CuboSemantico para validar operaciones
funcValida = Jubilo_CuboSemantico_SFuncs() #Toma el objeto de clase CuboSemanticoSFuncs para validar funciones

'''
Pilas para la generacion de cuadruplos
'''
pOperandos = [] # pila que almacena operandos de la expresion
pOperadores = [] # pila que almacena operadores de la expresion
pMemorias = [] #pila que almacena las direcciones de memoria de la expresion
pTipos = [] # pila que almacena los tipos de los operandos de la expresion
pSaltos = [] # pila que almacena los indices de saltos para condiciones y ciclos
pFunciones = [] # pila que almacena los indices de ubicacion de las funciones del programa
pArgumentos = [] # pila que almacena cantidad de argumentos de una funcion

'''
Manejo de cuadruplos
'''
arregloQuads = [] #arreglo para guardar todos los cuadruplos generados

'''
Diccionario de constantes:
Enteras, Flotantes, String
'''
dict_Int = {}
dict_Float = {}
dict_String = {}


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
currentFunctionType = "void";
negativeConstant = False
currentContParameters = 0 #Cantidad de parametros para la funcion actualmente siendo compilada
currentContVars = 0 #Cantidad de variables para la funcion actualmente siendo compilada
retornoFlag = False #bandera para detectar cuando una funcion debe o no tener valor de retorno

'''
Variables para el manejo de arreglos y matrices
'''
reng = 0 #contador para los renglones de una funcion
col = 0 #contador para las columnas de una funcion
R = 1 #ira acumulando valor para ser m0
base = 0 #guarda la direccion base de una variable dimensionada




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

#
def popMemorias():
    global pMemorias
    return pMemorias.pop()

#Toma el ultimo elemento de Pila de Tipos
def popTipos():
    global pTipos
    return pTipos.pop()

#Toma el ultimo elemento de Pila de Saltos
def popSaltos():
    global pSaltos
    return pSaltos.pop()

#Simula pop stack para remover el ultimo quadruplo
def popQuad(quad):
    global arregloQuads
    return arregloQuads.pop()

#Simula push stack para anadir nuevo operando
def pushOperando(operando):
    global pOperandos
    pOperandos.append(operando)

#Simula push stack para anadir nuevo operador
def pushOperador(operador):
    global pOperadores
    pOperadores.append(operador)

#Simula push stack para anadir nueva posicion de memoria
def pushMemoria(memoria):
    global pMemorias
    pMemorias.append(memoria)

#Simula push stack para anadir nuevo tipo
def pushTipo(tipo):
    global pTipos
    pTipos.append(tipo)

#Simula push stack para anadir nuevo salto
def pushSalto(salto):
    global pSaltos
    pSaltos.append(salto)

#Simula push stack para anadir nuevo quadruplo
def pushQuad(quad):
    global arregloQuads
    arregloQuads.append(quad)

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

#Obtiene el indice del siguiente cuadruplo del arreglo de cuadruplos
def nextQuad():
    global arregloQuads
    return len(arregloQuads)

'''
Manejo de memoria para la funcion nextTemporalAvail: toma el siguiente temporal en
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
+---------------------+
+constantes string    + batch_size
+++++++++++++++++++++++
'''
#Declaracion de inicio de espacio de memoria por tipo de memoria
index_intGlobales = BATCH_SIZE
index_floatGlobales = index_intGlobales + BATCH_SIZE
index_boolGlobales = index_floatGlobales + BATCH_SIZE

index_intLocales = index_boolGlobales + BATCH_SIZE
index_floatLocales = index_intLocales + BATCH_SIZE
index_boolLocales = index_floatLocales + BATCH_SIZE

index_intTemporales = index_boolLocales + BATCH_SIZE
index_floatTemporales = index_intTemporales + BATCH_SIZE
index_boolTemporales = index_floatTemporales + BATCH_SIZE

index_intConstantes = index_boolTemporales + BATCH_SIZE
index_floatConstantes = index_intConstantes + BATCH_SIZE
index_stringConstantes = index_floatConstantes + BATCH_SIZE

'''
Variables para manejar cambios de contexto
'''
#Declaracion de inicio de index de memoria para globales
cont_IntGlobal = 0
cont_FloatGlobal = index_intGlobales
cont_BoolGlobal  = index_floatGlobales

#Declaracion de inicio de index de memoria para locales
cont_IntLocal = index_boolGlobales
cont_FloatLocal = index_intLocales
cont_BoolLocal = index_floatLocales

'''
Obtiene el siguiente espacio de memoria disponible para una variable local o global
nextMemoryAvail
'''
def nextMemoryAvail(scope, tipo):
    global cont_IntGlobal
    global cont_FloatGlobal
    global cont_BoolGlobal
    global cont_IntLocal
    global cont_FloatLocal
    global cont_BoolLocal

    memPos = -1

    #Obtener memoria para una global
    if scope == GLOBAL_CONTEXT:
        if tipo == 'int':
            if cont_IntGlobal < index_intGlobales:
                memPos = cont_IntGlobal
                cont_IntGlobal += 1
            else:
                printErrorOutOfBounds('globales','Enteras')
        elif tipo == 'float':
            if cont_FloatGlobal < index_floatGlobales:
                memPos = cont_FloatGlobal
                cont_FloatGlobal +=  1
            else:
                printErrorOutOfBounds('globales','Flotantes')
        elif tipo == 'bool':
            if cont_BoolGlobal < index_boolGlobales:
                memPos = cont_BoolGlobal
                cont_BoolGlobal +=  1
            else:
                printErrorOutOfBounds('globales','Booleanas')
    #OBtener memoria para una variable local
    else:
        if tipo == 'int':
            if cont_IntLocal < index_intLocales:
                memPos = cont_IntLocal
                cont_IntLocal += 1
            else:
                printErrorOutOfBounds('locales','Enteras')
        elif tipo == 'float':
            if cont_FloatLocal < index_floatLocales:
                memPos = cont_FloatLocal
                cont_FloatLocal +=  1
            else:
                printErrorOutOfBounds('locales','Flotantes')
        elif tipo == 'bool':
            if cont_BoolLocal < index_boolLocales:
                memPos = cont_BoolLocal
                cont_BoolLocal +=  1
            else:
                printErrorOutOfBounds('locales','Booleanas')
    return memPos

'''
Modificador de memoria para el manejo de arreglos
updateMemoryPointer(scope de la declaracion del arreglo, tipo del arreglo, cantidad de valores en el arreglo)
'''
def updateMemoryPointer(scope, tipo, cont):
    global cont_IntGlobal
    global cont_FloatGlobal
    global cont_BoolGlobal
    global cont_IntLocal
    global cont_FloatLocal
    global cont_BoolLocal

    if scope == GLOBAL_CONTEXT:
        if tipo == 'int':
            cont_IntGlobal += cont
            if cont_IntGlobal > index_intGlobales:
                print ('Overflow int globales')
        if tipo == 'float':
            cont_FloatGlobal += cont
            if cont_FloatGlobal > index_floatGlobales:
                print('Overflow float globales')
        if tipo == 'bool':
            cont_BoolGlobal += cont
            if cont_BoolGlobal > index_boolGlobales:
                print('Overflow bool globales')
    else:
        if tipo == 'int':
            cont_IntLocal += cont
            if cont_IntLocal > index_intLocales:
                print('Overflow int locales')
        if tipo == 'float':
            cont_FloatLocal += cont
            if cont_FloatLocal > index_floatLocales:
                print('Overflow float locales')
        if tipo == 'bool':
            cont_BoolLocal += cont
            if cont_BoolLocal > index_boolLocales:
                print('Overflow bool locales')

#Declaracion de inicio de index de memoria para temporales
cont_IntTemp = index_boolLocales
cont_FloatTemp = index_intTemporales
cont_BoolTemp = index_floatTemporales

#Obtiene el siguiente temporal de la pila simulada de temporales
def nextTemporalAvail(tipo):
    global cont_IntTemp
    global cont_FloatTemp
    global cont_BoolTemp

    if tipo == 'int':
        if cont_IntTemp < index_intTemporales:
            avail = cont_IntTemp
            cont_IntTemp = cont_IntTemp + 1
        else:
            printErrorOutOfBounds('temporales','Enteras')

    elif tipo == 'float':
        if cont_FloatTemp < index_floatTemporales:
            avail = cont_FloatTemp
            cont_FloatTemp = cont_FloatTemp + 1
        else:
            printErrorOutOfBounds('temporales','Flotantes')

    elif tipo == 'bool':
        if cont_BoolTemp < index_boolTemporales:
            avail = cont_BoolTemp
            cont_BoolTemp = cont_BoolTemp + 1
        else:
           printErrorOutOfBounds('temporales','Boleanas')
    else:
        avail = -1
        #En teoria nunca deberia llegar aqui D:!
        print("Error: Tipo de variable desconocida.")
    return avail

#Declaracion de inicio de index de memoria para constantes
cont_IntConst = index_boolTemporales
cont_FloatConst = index_intConstantes
cont_StringConst = index_floatConstantes

#Checa si la constante se encuentra en el diccionario de constantes y si no, lo guarda
#Y lo agrega a la pila de operandos
#Se crea un cuadruplo de tipo:
# addConstant, Tipo de constante, Constante, direccion de memoria (aka el valor del diccionario)
def pushConstant(constante):
    global dict_Int
    global dict_Float
    global dict_String
    global cont_IntConst
    global cont_FloatConst
    global cont_StringConst

    if type(constante) == int:
        if constante not in dict_Int:
            if cont_IntConst < index_intConstantes:
                dict_Int[constante] = cont_IntConst
                cont_IntConst = cont_IntConst + 1
                printAuxQuad('addConstant', 'int', constante, dict_Int[constante])
            else:
                printErrorOutOfBounds('constantes','Enteras')
        pushOperando(dict_Int[constante])
        pushMemoria(dict_Int[constante])
        pushTipo('int')

    elif type(constante) == float:
        if constante not in dict_Float:
            if cont_FloatConst < index_floatConstantes:
                dict_Float[constante] = cont_FloatConst
                cont_FloatConst = cont_FloatConst + 1
                printAuxQuad('addConstant', 'float', constante, dict_Float[constante])
            else:
                printErrorOutOfBounds('constantes','Flotantes')
        pushOperando(dict_Float[constante])
        pushMemoria(dict_Float[constante])
        pushTipo('float')

    elif type(constante) == str:
        if constante == 'true' or constante == 'false':
            pushOperando(constante)
            pushMemoria(index_stringConstantes)
            pushTipo('bool')
        else:
            if constante not in dict_String:
                if cont_StringConst < index_stringConstantes:
                    dict_String[constante] = cont_StringConst
                    cont_StringConst = cont_StringConst + 1
                    printAuxQuad('addConstant', 'string', constante, dict_String[constante])
                else:
                    printErrorOutOfBounds('constantes','Strings')
            pushOperando(dict_String[constante])
            pushMemoria(dict_String[constante])
            pushTipo('string')

    else:
        sys.exit("Error: Tipo de variable desconocida.");

'''
Funciones para desplegar mensajes genericos como errores o infos
'''
#Funcion para mostrar un mensaje de error cuando se llena los maximos posibles valores temporales
def printErrorOutOfBounds(tipoMemoria,tipoDato):
    print("Error: Memoria llena; demasiadas {} de tipo {}.".format(tipoMemoria,tipoDato))
    sys.exit()

#Funcion para mostrar un mensaje de error generico entre un operador
#y dos operandos junto con su tipo
def printErrorOperacionInvalida(rOp, rTy, lOp, lTy, Op):
    print("Error: Imposible realizar operacion {} con operadores ({} de tipo {}) y ({} de tipo {}).".format(Op, rOp, rTy, lOp, lTy))

def printTypeMismatch():
    print('Error: Tipo de dato incorrecto')

#Regresa un mensaje de error en caso de que el retorno de una funcion sea incorrecto
def printReturnError():
    print('Error: La funcion intenta retornar un valor que no coincide con su tipo')

#Funcion para desplegar como quedaria
def printAuxQuad(quad_operator, quad_leftOper, quad_rightOper, quad_result):
    auxQuad = (quad_operator, quad_leftOper, quad_rightOper, quad_result)
    pushQuad(auxQuad)
    print(">>> Quadruplo: ('{}','{}','{}','{}')".format(quad_operator, quad_leftOper, quad_rightOper, quad_result))

#Funcino para desplegar los cuadruplos de manera bonita y con index
def printQuadsInFormat():
    print("##### Cuadruplos al momento: #####")
    count = 0
    for quad in arregloQuads:
        print("{}.\t{},\t{},\t{},\t{}".format(count,quad[0],quad[1],quad[2],quad[3]))
        count = count + 1

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
    'FLOAT_CTE','INT_CTE','BOOL_CTE','CHAR_CTE','STRING_CTE', #constantes
    'NEW_LINE'
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
    r'\"[a-zA-Z0-9_]*\"'
    t.value = str(t.value)
    return t

def t_CHAR_CTE(t):
    r'\'[a-zA-Z0-9_]\''
    t.value = chr(t.value)
    return t

def t_COMMENT(t):
    r'\~.*'
    return t

def t_NEW_LINE(t):
    r'\n'
    t.lexer.lineno += 1
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
    elif t.value == 'true':
        t.type = 'BOOL_CTE'
    elif t.value == 'false':
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
        t.type = 'RETURN'
    else:
        t.type = 'ID'
    return t

#Generic Error
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

'''
###Grammar Rules por Parser###
'''
#Declaracion de id programa inicial
def p_programa(p):
    '''
    programa : PROGRAM ID COLON vars vars_loop pnGotoMain function main
    '''
    print("Programa \"", p[2], "\" terminado.")
    printQuadsInFormat()

#Declaracion de variables, puede ser recursivo y declarar varias variables
def p_vars(p):
    '''
    vars : type ID pnVarSimple vars_predicate
    '''

#Permite que en el inicio de un programa pueda crear varias variables globales
def p_vars_loop(p):
    '''
    vars_loop : vars vars_loop
              | empty
    '''

#Predicados posibles para la declaracion de variables
def p_vars_predicate(p):
    '''
    vars_predicate : SEMIC pnVarSimple2
                   | vars_assign SEMIC pnQuadGenSec2
                   | vars_array SEMIC
    '''

#Asignacion de constante a una variable declarada
def p_vars_assign(p):
    '''
    vars_assign : EQUAL_OP pnQuadGenSec1 full_exp
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
             | FUNC function_auxTypeId LPAREN function_predicate RPAREN pnInsertParams bloque pnEndProc function
    '''

def p_function_auxTypeId(p):
    '''
    function_auxTypeId : VOID ID pnTipoIdFuncion
                       | type ID pnTipoIdFuncion
    '''

def p_function_predicate(p):
    '''
    function_predicate : func_params
                       | empty
    '''

def p_func_params(p):
    '''
    func_params : type ID pnTipoIdParam func_params_loop
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
    #TODO: Probablemente el VOID no deberia estar ahi...
    p[0] = p[1]

def p_constante(p):
    '''
    constante : BOOL_CTE pnQuadGenCteBool
              | STRING_CTE pnQuadGenCteString
              | CHAR_CTE pnQuadGenCteChar
              | MINUS_OP pnNegConst constante_num
              | constante_num
    '''
    #Correcion para que funcione incluso cuando es un número negativo
    if p[1] == '-':
        p[0] = -1 * p[3]
    else:
        p[0] = p[1]

    global negativeConstant
    negativeConstant = False

def p_constante_num(p):
    '''
    constante_num : INT_CTE pnQuadGenCteInt
                  | FLOAT_CTE pnQuadGenCteFloat
    '''
    p[0] = p[1]

def p_main(p):
    '''
    main : VOID MAIN pnFillGotoMain LPAREN RPAREN pnCreateFunctionMain bloque
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
             | func_call
             | sfunc_call
             | ciclo
             | retorno
             | vars
    '''
    print("Creado estatuto de:", p[1])

def p_func_call(p):
    '''
    func_call : ID LPAREN pnQuadEra params RPAREN pnQuadGoSub SEMIC

    '''
    p[0] = 'func_call'

def p_params(p):
    '''
    params : paramsaux
           | empty
    '''

def p_paramsaux(p):
    '''
    paramsaux : full_exp COMMA pnAgregaParam paramsaux
              | full_exp pnAgregaParam
    '''

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
    ciclo : WHILE pnQuadGenCycle1 LPAREN full_exp RPAREN pnQuadGenCycle2 bloque SEMIC pnQuadGenCycle3
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
    exp : termino pnQuadGenExp4 exp_predicate
    '''

def p_exp_predicate(p):
    '''
    exp_predicate : PLUS_OP pnQuadGenExp2 exp
                  | MINUS_OP pnQuadGenExp2 exp
                  | empty pnQuadGenExp4
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
    retorno : RETURN full_exp pnQuadRetorno SEMIC
            | RETURN pnQuadRetorno SEMIC
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
    sfunc : ARRANGE npSpecialFunctionId spfunc_two_params
          | ZEROS npSpecialFunctionId spfunc_params pnValidateParam
          | ONES npSpecialFunctionId spfunc_params pnValidateParam
          | SUM npSpecialFunctionId LPAREN ID pnValidateId RPAREN
          | FACT npSpecialFunctionId spfunc_params pnValidateParam
          | MEAN npSpecialFunctionId LPAREN ID  pnValidateId RPAREN
          | MEDIAN npSpecialFunctionId LPAREN ID pnValidateId RPAREN
          | MODE npSpecialFunctionId LPAREN ID pnValidateId RPAREN
          | STDEV npSpecialFunctionId LPAREN ID pnValidateId RPAREN
          | VAR npSpecialFunctionId LPAREN ID pnValidateId RPAREN
          | SORT npSpecialFunctionId spfunc_params
          | TRANSPOSE npSpecialFunctionId spfunc_params
          | READCSV npSpecialFunctionId spfunc_params
          | PLOTHIST npSpecialFunctionId spfunc_params
          | COVARIANCE npSpecialFunctionId spfunc_two_params
          | CORRELATION npSpecialFunctionId spfunc_two_params
          | EXPORTCSV npSpecialFunctionId spfunc_two_params
          | PLOTLINE npSpecialFunctionId spfunc_two_params
          | EXCHANGE npSpecialFunctionId spfunc_two_params
          | LINEAREG npSpecialFunctionId spfunc_two_params
          | RANDINT npSpecialFunctionId spfunc_three_params
          | RANDFLOAT npSpecialFunctionId spfunc_three_params
          | RANDINTMAT npSpecialFunctionId spfunc_four_params
          | RANDFLOATMAT npSpecialFunctionId spfunc_four_params
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
    print("ERROR LOCO EN: ",p)
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
    global currentContVars
    global currentContParameters
    currentFunction = 'main'
    dirFunciones.add_function(currentFunction, 'void', 0, nextQuad())
    currentContParameters = 0 #Se reinician los contadores de parametros y variables para la funcion
    currentContVars = 0

'''
Agrega el cuadruplo necesario para ir a main, que es lo primero que se ejecuta
'''
def p_pnGotoMain(p):
    '''
    pnGotoMain :
    '''
    printAuxQuad('GOTO', '', '', '')
    pushSalto(nextQuad() - 1)

'''
Rellena el GOTO Main con el cuádruplo donde inicia
'''
def p_pnFillGotoMain(p):
    '''
    pnFillGotoMain :
    '''
    global arregloQuads
    arregloQuads[popSaltos()] = ('GOTO', '', '', nextQuad())

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
        print("Error: Variable ", varId , " no declarada. 1")
        sys.exit("Error: Variable {} no declarada.".format(varId))
        #TODO: Deberiamos handlear el hecho de que no este declarada y no tronar el sistema
        return

    #Buscar la direccion de la memoria en su contexto, sino la encuentra buscar en globales
    varMemPos = dirFunciones.search_memPos(currentFunction, varId)
    if not varMemPos:
        varMemPos = dirFunciones.search_memPos(GLOBAL_CONTEXT, varId)
    #Si tampoco se encuentra en el contexto global, no existe la variable
    if varMemPos < 0:
        print("Error: Variable ", varId , " no declarada. :", varMemPos)
        sys.exit("Error: Variable {} no declarada.".format(varId))
        #TODO: Deberiamos handlear el hecho de que no este declarada y no tronar el sistema
        return

    pushOperando(varId)
    pushMemoria(varMemPos)
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
        quad_rightMem = popMemorias()
        quad_leftOper = popOperandos()
        quad_leftType = popTipos()
        quad_leftMem = popMemorias()
        quad_operator = popOperadores()
        global operValida
        quad_resultType = operValida.get_tipo(quad_leftType, quad_rightType, quad_operator)
        print("Intentar obtener quad de {}, {}, {}, result: {}".format(quad_leftType, quad_rightType, quad_operator, quad_resultType))
        if quad_resultType == 'error':
            printErrorOperacionInvalida(quad_rightOper, quad_rightType, quad_leftOper, quad_leftType, quad_operator)
        else:
            #quad_result = direccion de memoria donde se guardara el tipo de dato
            quad_resultIndex = nextTemporalAvail(quad_resultType)
            printAuxQuad(quad_operator, quad_leftMem, quad_rightMem, quad_resultIndex)
            pushOperando(quad_resultIndex)
            pushMemoria(quad_resultIndex)
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
        quad_rightMem = popMemorias()
        quad_leftOper = popOperandos()
        quad_leftType = popTipos()
        quad_leftMem = popMemorias()
        quad_operator = popOperadores()
        global operValida
        quad_resultType = operValida.get_tipo(quad_leftType, quad_rightType, quad_operator)
        print("Intentar obtener quad de {}, {}, {}, result: {}".format(quad_leftType, quad_rightType, quad_operator, quad_resultType))
        if quad_resultType == 'error':
            printErrorOperacionInvalida(quad_rightOper, quad_rightType, quad_leftOper, quad_leftType, quad_operator)
        else:
            #quad_result = direccion de memoria donde se guardara el tipo de dato
            quad_resultIndex = nextTemporalAvail(quad_resultType)
            printAuxQuad(quad_operator, quad_leftMem, quad_rightMem, quad_resultIndex)
            pushOperando(quad_resultIndex)
            pushMemoria(quad_resultIndex)
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
        quad_leftMem = popMemorias()
        quad_leftOper = popOperandos()
        quad_leftType = popTipos()
        quad_leftMem = popMemorias()
        quad_operator = popOperadores()
        global operValida
        quad_resultType = operValida.get_tipo(quad_leftType, quad_rightType, quad_operator)
        print("Intentar obtener quad de {}, {}, {}, result: {}".format(quad_leftType, quad_rightType, quad_operator, quad_resultType))
        if quad_resultType == 'error':
            printErrorOperacionInvalida(quad_rightOper, quad_rightType, quad_leftOper, quad_leftType, quad_operator)
        else:
            #quad_result = direccion de memoria donde se guardara el tipo de dato
            quad_resultIndex = nextTemporalAvail(quad_resultType)
            printAuxQuad(quad_operator, quad_leftMem, quad_rightMem, quad_resultIndex)
            pushOperando(quad_resultIndex)
            pushMemoria(quad_resultIndex)
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
        quad_rightMem = popMemorias()
        quad_leftOper = popOperandos()
        quad_leftType = popTipos()
        quad_leftMem = popMemorias()
        quad_operator = popOperadores()
        global operValida
        quad_resultType = operValida.get_tipo(quad_leftType, quad_rightType, quad_operator)
        print("Intentar obtener quad de {}, {}, {}, result: {}".format(quad_leftType, quad_rightType, quad_operator, quad_resultType))
        if quad_resultType == 'error':
            printErrorOperacionInvalida(quad_rightOper, quad_rightType, quad_leftOper, quad_leftType, quad_operator)
        else:
            #quad_result = direccion de memoria donde se guardara el tipo de dato
            quad_resultIndex = nextTemporalAvail(quad_resultType)
            printAuxQuad(quad_operator, quad_leftMem, quad_rightMem, quad_resultIndex)
            pushOperando(quad_resultIndex)
            pushMemoria(quad_resultIndex)
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
        quad_rightMem = popMemorias()
        quad_leftOper = popOperandos() #A quien se lo voy a asignar
        quad_leftType = popTipos()
        quad_leftMem = popMemorias()
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
                printAuxQuad(quad_operator, quad_rightMem, '', quad_leftMem)
        else:
            print("Error: Intenando asignar a una no variable, de tipo: ", quad_leftType)


'''
Punto neuralgico para meter read o print a la pila de operadores
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
        quad_rightMem = popMemorias()
        quad_operator = popOperadores()
        global operValida
        quad_resultType = operValida.get_tipo(quad_operator, quad_rightType, '')
        #print("Intentar obtener quad de {}, {}, {}, result: {}".format(quad_leftType, quad_rightType, quad_operator, quad_resultType))
        if quad_resultType == 'error':
            printErrorOperacionInvalida(quad_rightOper, quad_rightType, '', '', quad_operator)
        else:
            printAuxQuad(quad_operator, quad_rightMem, '', quad_operator)
            pushOperando(quad_rightOper)
            pushMemoria(quad_rightOper)
            pushTipo(quad_resultType)
'''
Genera el cuadruplo GOTOF para la condicion IF despues de recibir la expresion boleana a evaluar
'''
def p_pnQuadGenCond1(p):
    '''
    pnQuadGenCond1 :
    '''
    quad_memPos = popMemorias()
    quad_resultType = popTipos()
    if quad_resultType == 'error':
        printTypeMismatch()
    else:
        result = popOperandos()
        printAuxQuad('GOTOF', result, '', '')
        pushSalto(nextQuad() - 1)

'''
Rellena el cuadruplo para que el programa sepa cuando terminar la condicion
'''
def p_pnQuadGenCond2(p):
    '''
    pnQuadGenCond2 :
    '''
    global arregloQuads
    end = popSaltos()
    auxQuad = (arregloQuads[end][0], arregloQuads[end][1], arregloQuads[end][2], nextQuad())
    arregloQuads[end] = auxQuad

'''
Genera el cuadruplo GOTO para la condicion ELSE y rellena el cuadruplo
para que el programa sepa a donde saltar en caso de obtener falso
'''
def p_pnQuadGenCond3(p):
    '''
    pnQuadGenCond3 :
    '''
    global arregloQuads
    printAuxQuad('GOTO', '', '','')
    false = popSaltos()
    pushSalto(nextQuad() - 1)
    auxQuad = (arregloQuads[false][0], arregloQuads[false][1], arregloQuads[false][2], nextQuad())
    arregloQuads[false] = auxQuad
'''
Mete el siguiente cuadruplo a la pila de saltos, a donde regresara
al final del ciclo
'''
def p_pnQuadGenCycle1(p):
    '''
    pnQuadGenCycle1 :
    '''
    pushSalto(nextQuad())

'''
Genera el cuadruplo GOTOF para que el programa sepa a donde debe ir
si la evaluacion de la expresion resulta falsa
'''
def p_pnQuadGenCycle2(p):
    '''
    pnQuadGenCycle2 :
    '''
    quad_memPos = popMemorias()
    quad_resultType = popTipos()
    if quad_resultType == 'error':
        printTypeMismatch()
    else:
        result = popOperandos()
        printAuxQuad('GOTOF', result, '', '')
        pushSalto(nextQuad()-1)
'''
Genera el cuadruplo GOTO para que el programa sepa a donde regresar una vez
terminado el statement. Rellena los GOTOs generados en pnQuadGenCycle2 y
pnQuadGenCycle3.
'''
def p_pnQuadGenCycle3(p):
    '''
    pnQuadGenCycle3 :
    '''
    end = popSaltos()
    retorno = popSaltos()
    printAuxQuad('GOTO', retorno, '','')
    auxQuad = (arregloQuads[end][0], arregloQuads[end][1], arregloQuads[end][2], nextQuad())
    arregloQuads[end] = auxQuad

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
    global currentContVars
    print("tipo: ", p[-2])
    print("nombre: ", p[-1])
    #Obtener el siguiente apuntador de memoria donde guardar esa madre
    #si lees esto elda tqm
    memPos = nextMemoryAvail(currentFunction, varTipo)
    #Agregar variable simple a directorio de funciones en current function
    dirFunciones.add_varToFunction(currentFunction, varId, varTipo, 0, 0, memPos)
    #Agregar variable y su tipo a la pila por si se llega a utilizar
    pushTipo(varTipo)
    pushOperando(varId)
    pushMemoria(memPos)
    currentContVars = currentContVars + 1 #Incrementa el contador de variables

'''
Punto neuralgico de que no se le asignara nada a esa variable
'''
def p_pnVarSimple2(p):
    '''
    pnVarSimple2 :
    '''
    varTipo = popTipos()
    varId = popOperandos()
    varMem = popMemorias()

'''
Puntos neuralgicos para recepcion de constantes y meter su valor en pila de operandos
'''
def p_pnQuadGenCteBool(p):
    '''
    pnQuadGenCteBool :
    '''
    pushConstant(p[-1])

def p_pnQuadGenCteString(p):
    '''
    pnQuadGenCteString :
    '''
    pushConstant(p[-1])

def p_pnQuadGenCteChar(p):
    '''
    pnQuadGenCteChar :
    '''
    pushConstant(p[-1])

'''
Punto neuralgico si es que se trata de una constante negativa
'''
def p_pnNegConst(p):
    '''
    pnNegConst :
    '''
    global negativeConstant
    negativeConstant = True

def p_pnQuadGenCteInt(p):
    '''
    pnQuadGenCteInt :
    '''
    if negativeConstant:
        pushConstant(-1 * p[-1])
    else:
        pushConstant(p[-1])

def p_pnQuadGenCteFloat(p):
    '''
    pnQuadGenCteFloat :
    '''
    if negativeConstant:
        pushConstant(-1.0 * p[-1])
    else:
        pushConstant(p[-1])

'''
Puntos neuralgicos para la creacion de funciones y sus respectivas inicializaciones
'''
#Inicializacion de variables para conteo de parametros y variables de la nueva funcion
def p_pnTipoIdFuncion(p):
    '''
    pnTipoIdFuncion :
    '''
    global currentFunction
    global currentFunctionType
    global currentContVars
    global currentContParameters #Numero de parametros que tendra la funcion
    global retornoFlag #Bandera para saber si el contexto(funcion) actual ocupa un retorno
    currentContParameters = 0 #Se reinician los contadores de parametros y variables para la funcion
    currentContVars = 0
    currentFunction = p[-1] #Current function = id de la funcion que se quiere crear
    currentFunctionType = str(p[-2])
    dirFunciones.add_function(currentFunction, currentFunctionType, currentContParameters, nextQuad())
    #Checar  si el tipo es VOID o no, para saber si la funcion ocupa un retorno de valor forzoso
    if dirFunciones.diccionario[currentFunction]['tipo'] == 'void':
        retornoFlag = False;
    else:
        retornoFlag = True;

#Agrega los tipos y ids de las variables parametros encontradas, luego incrementa el contador de parametros
def p_pnTipoIdParam(p):
    '''
    pnTipoIdParam :
    '''
    global currentFunction
    global currentContParameters
    currentContParameters += 1
    #Agregar cada parametro como variable dentro de la tabla de variables de la funcion
    varTipo = p[-2]
    varId = p[-1]
    memPos = nextMemoryAvail(currentFunction, varTipo)
    #Se agrega en el contexto local, con el tipo y id definidos, y siendo no dimensionada
    dirFunciones.add_varToFunction(currentFunction, varId, varTipo, 0, 0, memPos)

#Funcion para actualizar el numero de parametros de una funcion ya definida
def p_pnInsertParams(p):
    '''
    pnInsertParams :
    '''
    global dirFunciones
    global currentFunction
    global currentContParameters
    dirFunciones.update_functionParams(currentFunction, currentContParameters)


#Genera la accion para finalizar la funcion
def p_pnEndProc(p):
    '''
    pnEndProc :
    '''
    global retornoFlag

    #Reset de apuntadores de memoria local
    global cont_IntLocal
    global cont_FloatLocal
    global cont_BoolLocal
    cont_IntLocal = index_boolGlobales
    cont_FloatLocal = index_intLocales
    cont_BoolLocal = index_floatLocales
    #Reset de apuntadores de memoria temporal
    global cont_IntTemp
    global cont_FloatTemp
    global cont_BoolTemp
    cont_IntTemp = index_boolLocales
    cont_FloatTemp = index_intTemporales
    cont_BoolTemp = index_floatTemporales

    printAuxQuad('ENDPROC', '', '', '')
    retornoFlag = False

#Valida que la funcion a llamar exista en el directorio de funciones y genera la accion ERA
def p_pnQuadEra(p):
    '''
    pnQuadEra :
    '''
    global pFunciones
    global pArgumentos

    function = p[-2] #toma el nombre de la funcion
    # 1. Verify that the procedure exists into the DirFunc
    if function in dirFunciones.diccionario:
        pFunciones.append(function) #añade la funcion a la pila de funciones
        #print(pFunciones)
        # 2. Generate action ERA size
        printAuxQuad('ERA', function, '', '') #genera cuadruplo ERA con el nombre de a funcion
        pArgumentos.append(0) #en este momento ha recibido 0 argumentos para la llamada a funcion
        #print(pArgumentos)

    else:
        print('ERROR. Function not declared')
        sys.exit()
        return

def p_pnAgregaParam(p):
    '''
    pnAgregaParam :
    '''
    global pArgumentos
    global pFunciones
    global currentFunction
    # 3. Obtain Argument and ArgumentType
    argument = popOperandos()
    argumentType = popTipos()
    argumentMem = popMemorias()
    function = pFunciones.pop()
    args = pArgumentos.pop() + 1
    pArgumentos.append(args)
    param = 'param' + str(args)
    #print(param)

    functionParams = dirFunciones.diccionario[function]['cantParametros'] #toma la cantidad de parametros de la funcion referenciada
    print(functionParams)
    lista = dirFunciones.listTypes(function)
    if functionParams >= args:
        if lista[args-1] == argumentType:
            printAuxQuad('PARAMETER', argumentMem, '', param)
        else:
            print("Error, los parametros no coinciden")
    else:
        print("Error, demasiados argumentos")
        sys.exit()

    pFunciones.append(function)


def p_pnQuadGoSub(p):
    '''
    pnQuadGoSub :
    '''
    global pFunciones
    global pArgumentos
    args = pArgumentos.pop()
    function = pFunciones.pop()
    # 5. Verify that the last parameter points to null
    if args == dirFunciones.diccionario[function]['cantParametros']:
        # 6. Generate action GOSUB, procedure-name, '', initial address
        printAuxQuad('GOSUB', function, '', nextQuad()+1)
        #printAuxQuad('GOSUB', function, nextQuad()+1, dirFunciones.diccionario[function][3])
    else:
        print ('ERROR. Argument mysmatch')
        sys.exit()
        return

def p_pnQuadRetorno(p):
    '''
    pnQuadRetorno :
    '''
    global currentFunction
    global retornoFlag #SAber si tengo que regresar un valor o no

    if not retornoFlag:
        if p[-1] == 'return':
            #Si no tengo regresar nada y no le estoy mandando nada
            printAuxQuad('RETURN', '', '', '')
        else:
            printReturnError()
    else: #si si tengo que regresar algo
        operandoRet = popOperandos()
        tipoRet = popTipos()
        memRet = popMemorias()
        #si los tipos son correctos se crea el cuadruplo con el operando regresado
        if dirFunciones.diccionario[currentFunction]['tipo'] == tipoRet:
            printAuxQuad('RETURN', '', '', memRet)
        else:
            #Si no es correcto los tipos, se genera un error
            printReturnError()

#Funcion que guarda el id de una funcion especial de Jubilo
def p_npSpecialFunctionId(p):
    '''
    npSpecialFunctionId :
    '''
    nombreSFunc = str(p[-1])
    pushOperador(nombreSFunc)


#Valida una funcion de un solo parametro de entrada, este parametro es de tipo full exp
#Genera el cuadruplo para realizar la funcion
def p_pnValidateParam(p):
    '''
    pnValidateParam :
    '''
    #se usan las pilas de operandos y operadores porque el parametro de la funcion es de tipo full exp
    specialFunction = popOperadores()
    param = popOperandos()
    tipoParam = popTipos()
    memParam = popMemorias()
    tipoFunction = funcValida.get_tipo(specialFunction, tipoParam, '') #revisa en el cubo semantico
    resultTemporal = nextTemporalAvail(tipoFunction)
    if tipoFunction == 'error':
        printTypeMismatch()
    else:
        pushTipo(tipoFunction) #guarda el tipo de resultado de la funcion especial
        pushOperando(resultTemporal)
        pushMemoria(resultTemporal)
        printAuxQuad(specialFunction, memParam, '', resultTemporal)

#Valida una funcion de un solo parametro de entrada, este parametro es de tipo ID
def p_pnValidateId(p):
    '''
    pnValidateId :
    '''
    nombreId = str(p[-1])
    specialFunction = popOperadores()

    #pendiente porque esto necesita la implementacion de arreglitos

#Defining Lexer & Parser
parser = yacc.yacc()
lexer = lex.lex()

'''
Para probar el parser desde archivo
'''
name = './test_files/test1.txt'

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
