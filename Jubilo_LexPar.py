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
pEspeciales = [] #pila que almacena los identificadores de las funciones especiales usadas en el programa

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
obejotaName = 'obejota.jub'
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
currentVar = '' #string para obtener mediante id el nombre de la variable actual
currentFunctionType = "void";
negativeConstant = False
currentContParameters = 0 #Cantidad de parametros para la funcion actualmente siendo compilada
currentContVars = 0 #Cantidad de variables para la funcion actualmente siendo compilada
flagRetorno = False #bandera para detectar cuando una funcion debe o no tener valor de retorno
yaSeRetorno = False #Bandera para saber si ya se regreso en la funcion actual

'''
Variables para el manejo de arreglos y matrices
'''
flagDimensionada = False #Bandera para detecar cuando una variable es dimensionada (arreglo o matriz)
contRenglones = 0 #contador para los renglones de una funcion
contColumnas = 0 #contador para las columnas de una funcion
acumuladoR = 1 #ira acumulando valor para ser m0
dirBase = 0 #guarda la direccion base de una variable dimensionada (Que es igual al limite inferior)
currentConsForArray = [] #acumulara las constantes de asignacion para un arreglo

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
#Tome el ultimo elemento de la Pila de memorias
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

BATCH_SIZE = 1000 #tamano del espacio de memoria entre diferentes tipos de datos

'''
Espacios de memoria:
+++++++++++++++++++++++
+globales enteras     + batch_size
+---------------------+
+globales flotantes   + batch_size
+---------------------+
+globales booleanas   + batch_size
+++++++++++++++++++++++
+locales enteras      + batch_size
+---------------------+
+locales flotantes    + batch_size
+---------------------+
+locales booleanas    + batch_size
+++++++++++++++++++++++
+temp enteras         + batch_size
+---------------------+
+temp flotantes       + batch_size
+---------------------+
+temp booleanas       + batch_size
+++++++++++++++++++++++
+constantes enteras   + batch_size
+---------------------+
+constantes flotantes + batch_size
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
#index_boolConstantes = index_stringConstantes = true
#index_boolConstantes = index_stringConstantes + 1 = false

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
        pushOperando(constante)
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
        pushOperando(constante)
        pushMemoria(dict_Float[constante])
        pushTipo('float')
    elif type(constante) == str:
        if constante == 'true':
            pushOperando(constante)
            pushMemoria(index_stringConstantes)
            pushTipo('bool')
        elif constante == 'false':
            pushOperando(constante)
            pushMemoria(index_stringConstantes + 1)
            pushTipo('bool')
        else:
            if constante not in dict_String:
                if cont_StringConst < index_stringConstantes:
                    dict_String[constante] = cont_StringConst
                    cont_StringConst = cont_StringConst + 1
                    printAuxQuad('addConstant', 'string', constante, dict_String[constante])
                else:
                    printErrorOutOfBounds('constantes','Strings')
            pushOperando(constante)
            pushMemoria(dict_String[constante])
            pushTipo('string')
    else:
        sys.exit("Error: Tipo de variable desconocida.");

'''
#Obtiene una constante como direccion de memoria, si no esta ya declarada la agrega
'''
def asMemConstant(constante):
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
        return(dict_Int[constante])

    elif type(constante) == float:
        if constante not in dict_Float:
            if cont_FloatConst < index_floatConstantes:
                dict_Float[constante] = cont_FloatConst
                cont_FloatConst = cont_FloatConst + 1
                printAuxQuad('addConstant', 'float', constante, dict_Float[constante])
            else:
                printErrorOutOfBounds('constantes','Flotantes')
        return(dict_Float[constante])

    elif type(constante) == str:
        if constante == 'true':
            return(index_stringConstantes)
        if constante == 'false':
            return(index_stringConstantes + 1)
        else:
            if constante not in dict_String:
                if cont_StringConst < index_stringConstantes:
                    dict_String[constante] = cont_StringConst
                    cont_StringConst = cont_StringConst + 1
                    printAuxQuad('addConstant', 'string', constante, dict_String[constante])
                else:
                    printErrorOutOfBounds('constantes','Strings')
            return(dict_String[constante])
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
    sys.exit()
    return

#Regresa un mensaje de error en caso de que el retorno de una funcion sea incorrecto
def printReturnError():
    print('Error: La funcion intenta retornar un valor que no coincide con su tipo')
    sys.exit()
    return

#Funcion para desplegar como quedaria
def printAuxQuad(quad_operator, quad_leftOper, quad_rightOper, quad_result):
    auxQuad = (quad_operator, quad_leftOper, quad_rightOper, quad_result)
    pushQuad(auxQuad)
    print(">>> Quadruplo: ('{}','{}','{}','{}')".format(quad_operator, quad_leftOper, quad_rightOper, quad_result))

#Funcino para desplegar los cuadruplos de manera bonita y con index
def printQuadsInFormat():
    #print('##### PILAS AL MOMENTO: #####')
    #print("operandos: ",pOperandos)
    #print("pTipos: ",pTipos)
    #print("pMemorias: ", pMemorias)
    #print("pOepradres: ",pOperadores)
    print("##### Cuadruplos al momento: #####")
    count = 0
    file = open(obejotaName,"w+")
    for quad in arregloQuads:
        print("{}.\t{},\t{},\t{},\t{}".format(count,quad[0],quad[1],quad[2],quad[3]))
        count = count + 1

        file.write(str(quad) + '\n')
    file.close()
    print("##### YAY, compilado #####")

#List of language tokens
tokens = [
    'PROGRAM','VOID','MAIN','ID','FUNC','COMMENT', #palabras de programa
    'PRINT','READ','RETURN','IF','ELSE','WHILE', #palabras de programa, condiciones y ciclos
    'INT_TYPE','FLOAT_TYPE','BOOL_TYPE', #tipos de datos
    'PLUS_OP','MINUS_OP','MULT_OP','DIV_OP','EQUAL_OP', #operadores
    'EQUAL_LOG','LESS_LOG','LEQUAL_LOG','GREAT_LOG', #operadores logicos
    'GEQUAL_LOG','DIFF_LOG','OR_LOG','AND_LOG', #operadores logicos
    'LPAREN','RPAREN','LBRACK','RBRACK','LCURLY','RCURLY', #simbolos para conjuntos
    'COMMA','SEMIC','COLON', #simbolos para conjuntos
    'ARRANGE','ZEROS','ONES','SUM','FACT', #funciones especiales
    'MEAN','MEDIAN','MODE','STDEV','VAR', #funciones especiales
    'COVARIANCE','CORRELATION', 'SORT','TRANSPOSE', #funciones especiales
    'EXPORTCSV', 'PLOTHIST','PLOTLINE', #funciones especiales
    'EXCHANGE','LINEAREG', 'RANDINT','RANDFLOAT', #funciones especiales
    'FLOAT_CTE','INT_CTE','BOOL_CTE','STRING_CTE', #constantes
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
    r'\"[a-zA-Z0-9_\.\_]*\"'
    t.value = str(t.value)
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
    elif t.value == 'exportcsv':
        t.type = 'EXPORTCSV'
    elif t.value == 'plothist':
        t.type = 'PLOTHIST'
    elif t.value == 'plotline':
        t.type = 'PLOTLINE'
    elif t.value == 'exchange':
        t.type = 'EXCHANGE'
    elif t.value == 'lineareg':
        t.type = 'LINEAREG'
    elif t.value == 'randint':
        t.type = 'RANDINT'
    elif t.value == 'randfloat':
        t.type = 'RANDFLOAT'
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
    programa : PROGRAM ID COLON vars_loop pnGotoMain function main
    '''
    print("Programa \"", p[2], "\" terminado.")
    printAuxQuad('ENDPROGRAM', p[2], '', '') #Se agrega un cuadruplo para indicar que acabo el programa
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
                   | vars_array SEMIC pnReclamarMemoriaDim
    '''

#Asignacion de constante a una variable declarada
def p_vars_assign(p):
    '''
    vars_assign : EQUAL_OP pnQuadGenSec1 full_exp
    '''

#Creacion de variable de tipo arreglo o matriz
def p_vars_array(p):
    '''
    vars_array : LBRACK pnDetectDimensionada INT_CTE pnGetColumnas RBRACK vars_array_predicate
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
    vars_array_assign : EQUAL_OP LBRACK constante pnGetConsForArray constante_loop RBRACK pnAssignConsToArray
    '''

#Permite agregar varias constantes a la declaracion del arreglo
def p_constante_loop(p):
    '''
    constante_loop : empty
                   | COMMA constante pnGetConsForArray constante_loop
    '''

#Cuando se tienen dos pares de [] lo convierte en una matriz
def p_vars_matrix(p):
    '''
    vars_matrix : LBRACK INT_CTE pnGetRenglones RBRACK vars_matrix_predicate
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
    vars_matrix_assign : EQUAL_OP LBRACK array array_loop RBRACK pnAssignConsToMatrix
    '''

#Estructura de un arreglo, con minimo un dato y posibles mas
def p_array(p):
    '''
    array : LBRACK constante pnGetConsForArray constante_loop RBRACK
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
    '''
    p[0] = p[1]

def p_constante(p):
    '''
    constante : BOOL_CTE pnQuadGenCteBool
              | STRING_CTE pnQuadGenCteString
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
    main : VOID MAIN pnFillGotoMain LPAREN RPAREN pnCreateFunctionMain bloque pnEndProc
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
             | vars
             | func_call
             | sfunc_call
             | ciclo
             | retorno
    '''
    print("Creado estatuto de:", p[1])

def p_func_call(p):
    '''
    func_call : func SEMIC
    '''
    p[0] = 'func_call'

def p_func(p):
    '''
    func : ID LPAREN pnQuadGenExp6 pnQuadEra params RPAREN pnQuadGenExp7 pnQuadGoSub
    '''

def p_func2(p):
    '''
    func2 : ID LPAREN pnQuadGenExp6 pnQuadEra params RPAREN pnQuadGenExp7 pnQuadGoSub2
    '''

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
    p[0] = 'Sfunc'

def p_asignacion(p):
    '''
    asignacion : ID pnQuadGenExp1 asignacion_predicate EQUAL_OP pnQuadGenSec1 full_exp  SEMIC pnQuadGenSec2
    '''
    p[0] = "Asignacion"

def p_asignacion_predicate(p):
    '''
    asignacion_predicate : empty
                         | LBRACK pnDetectDimensionada pnQuadGenExp6 full_exp RBRACK pnQuadGenExp7 asignacion_array_predicate
    '''

def p_asignacion_array_predicate(p):
    '''
    asignacion_array_predicate : empty pnAccessArray
                               | LBRACK pnQuadGenExp6 full_exp RBRACK pnQuadGenExp7 pnAccessMatrix
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
    retorno : RETURN pnQuadGenExp6 full_exp pnQuadGenExp7 pnQuadRetorno SEMIC
            | RETURN pnQuadRetorno SEMIC
    '''

def p_var_cte(p):
    '''
    var_cte : sfunc_operando
            | constante
            | func2
            | ID pnQuadGenExp1 var_cte_predicate
    '''

def p_var_cte_predicate(p):
    '''
    var_cte_predicate : asignacion_predicate
                      | LPAREN full_exp full_exp_loop RPAREN
    '''

def p_sfunc_operando(p):
    '''
    sfunc_operando : FACT npSpecialFunctionId spfunc_params pnValidateFact
                   | SUM npSpecialFunctionId LPAREN ID pnValidateId RPAREN
                   | MEAN npSpecialFunctionId LPAREN ID  pnValidateId RPAREN
                   | MEDIAN npSpecialFunctionId LPAREN ID pnValidateId RPAREN
                   | MODE npSpecialFunctionId LPAREN ID pnValidateId RPAREN
                   | STDEV npSpecialFunctionId LPAREN ID pnValidateId RPAREN
                   | VAR npSpecialFunctionId LPAREN ID pnValidateId RPAREN
                   | COVARIANCE npSpecialFunctionId LPAREN ID COMMA ID  pnValidateId2 RPAREN
                   | CORRELATION npSpecialFunctionId LPAREN ID COMMA ID pnValidateId2 RPAREN
    '''

def p_sfunc(p):
    '''
    sfunc : ID MINUS_OP GREAT_LOG pnAddSpecialFunctionVar ARRANGE npSpecialFunctionId LPAREN constante COMMA constante RPAREN pnValidateArrange
          | ID MINUS_OP GREAT_LOG pnAddSpecialFunctionVar ZEROS npSpecialFunctionId LPAREN INT_CTE RPAREN pnValidateZerosAndOnes
          | ID MINUS_OP GREAT_LOG pnAddSpecialFunctionVar ONES npSpecialFunctionId LPAREN INT_CTE RPAREN pnValidateZerosAndOnes
          | ID MINUS_OP GREAT_LOG pnAddSpecialFunctionVar RANDINT npSpecialFunctionId LPAREN constante COMMA constante COMMA INT_CTE RPAREN pnValidateRands
          | ID MINUS_OP GREAT_LOG pnAddSpecialFunctionVar RANDFLOAT npSpecialFunctionId LPAREN constante COMMA constante COMMA INT_CTE RPAREN pnValidateRands
          | SORT npSpecialFunctionId LPAREN ID pnValidateSortTranspose RPAREN
          | TRANSPOSE npSpecialFunctionId LPAREN ID pnValidateSortTranspose RPAREN
          | PLOTHIST npSpecialFunctionId LPAREN ID COMMA INT_CTE pnValidatePlotHist RPAREN
          | PLOTLINE npSpecialFunctionId LPAREN ID COMMA ID pnValidatePlotLine RPAREN
          | LINEAREG npSpecialFunctionId LPAREN ID COMMA ID pnValidatePlotLine RPAREN
          | EXPORTCSV npSpecialFunctionId LPAREN STRING_CTE COMMA ID pnValidateExportCsv RPAREN
          | EXCHANGE npSpecialFunctionId LPAREN ID COMMA ID pnValidateExchange RPAREN
    '''

def p_spfunc_params(p):
    '''
    spfunc_params : LPAREN pnQuadGenExp6 full_exp RPAREN pnQuadGenExp7
    '''

def p_spfunc_two_params(p):
    '''
    spfunc_two_params : LPAREN pnQuadGenExp6 full_exp COMMA pnQuadGenExp7 pnQuadGenExp6 full_exp RPAREN pnQuadGenExp7
    '''

def p_spfunc_three_params(p):
    '''
    spfunc_three_params : spfunc_two_params
                        | LPAREN full_exp COMMA full_exp COMMA full_exp RPAREN
    '''

def p_empty(p):
    '''
    empty :
    '''
    p[0] = None


def p_error(p):
    print ("Syntax error in line " + str(lexer.lineno))
    print("ERROR DE SINTAXIS EN: ",p)
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
    global flagDimensionada
    global currentVar
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

    #Calcular si la variable es dimensionada
    isDimensionada = dirFunciones.isVarDimensionada(currentFunction, varId)
    if isDimensionada == -1: #No esta en ese contexto, buscar en globales
        isDimensionada = dirFunciones.isVarDimensionada(GLOBAL_CONTEXT, varId)

    if isDimensionada == 1:
        flagDimensionada = True
        currentVar = varId
    elif isDimensionada == 0:
        flagDimensionada = False
    else:
        flagDimensionada = False
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
    global currentVar
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
    currentVar = varId
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
    global currentVar
    currentVar = ''

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
    global flagRetorno #Bandera para saber si el contexto(funcion) actual ocupa un retorno
    currentContParameters = 0 #Se reinician los contadores de parametros y variables para la funcion
    currentContVars = 0
    currentFunction = p[-1] #Current function = id de la funcion que se quiere crear
    currentFunctionType = str(p[-2])
    dirFunciones.add_function(currentFunction, currentFunctionType, currentContParameters, nextQuad())
    #Checar  si el tipo es VOID o no, para saber si la funcion ocupa un retorno de valor forzoso
    if dirFunciones.diccionario[currentFunction]['tipo'] == 'void':
        flagRetorno = False;
    else:
        flagRetorno = True;

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
    global flagRetorno
    global yaSeRetorno
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

    if yaSeRetorno == False: #No se ha regresado nada
        sys.exit("Error. Se ocupa crear un Retorno en todas las funciones.")
        return
    printAuxQuad('ENDPROC', '', '', '')
    flagRetorno = False
    yaSeRetorno = False

#Valida que la funcion a llamar exista en el directorio de funciones y genera la accion ERA
def p_pnQuadEra(p):
    '''
    pnQuadEra :
    '''
    global pFunciones
    global pArgumentos

    function = p[-3] #toma el nombre de la funcion
    print("HUEVOOOOS", function)
    # 1. Verify that the procedure exists into the DirFunc
    if function in dirFunciones.diccionario:
        pFunciones.append(function) #añade la funcion a la pila de funciones
        #print(pFunciones)
        # 2. Generate action ERA size
        printAuxQuad('ERA', function, '', '') #genera cuadruplo ERA con el nombre de a funcion
        pArgumentos.append(0) #en este momento ha recibido 0 argumentos para la llamada a funcion
        #print(pArgumentos)

    else:
        print('ERROR. Funcion {} no declarada.'.format(function))
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
            print("Error, El parametro {} no coinciden en la funcion {}".format(param, function))
            sys.exit()
            return
    else:
        print("Error, demasiados argumentos")
        sys.exit()
        return
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
        #printAuxQuad('GOSUB', function, nextQuad()+1, dirFunciones.diccionario[function][3
        quadStartFunc = dirFunciones.diccionario[function]['quadCont']
        printAuxQuad('GOSUB', function, nextQuad()+1, quadStartFunc)
    else:
        print ('ERROR. La cantidad de argumentos no es la esperada para la funcion {}.'.format(function))
        sys.exit()
        return

def p_pnQuadGoSub2(p):
    '''
    pnQuadGoSub2 :
    '''
    global pFunciones
    global pArgumentos
    args = pArgumentos.pop()
    function = pFunciones.pop()

    if not dirFunciones.exist_function(function):
        print('Error. La funcion {} no existe en el directorio de funciones'.format(function))
        sys.exit()
        return

    tipoFunction = dirFunciones.diccionario[function]['tipo'];
    memFunction = nextTemporalAvail(tipoFunction) #Crear una variable temporal donde guardar el resultado de la funcino
    # 5. Verify that the last parameter points to null
    if args == dirFunciones.diccionario[function]['cantParametros']:
        # 6. Generate action GOSUB, procedure-name, '', initial address
        quadStartFunc = dirFunciones.diccionario[function]['quadCont']
        #(GOSUB, nombre de funcion, cuadruplo para saber a donde regresar, cuadruplo donde empieza el codigo de la fx )
        printAuxQuad('GOSUB', function, nextQuad()+1, quadStartFunc)
        #General quad con asignar el resultado de la func en un temporal
        printAuxQuad('=', function, '', memFunction)
        #Pushear a las pilas el resultado temporal de la Funcion
        pushOperando(function)
        pushMemoria(memFunction)
        pushTipo(tipoFunction)
    else:
        print ('ERROR. La cantidad de argumentos no es la esperada para la funcion {}.'.format(function))
        sys.exit()
        return


def p_pnQuadRetorno(p):
    '''
    pnQuadRetorno :
    '''
    global currentFunction
    global flagRetorno #SAber si tengo que regresar un valor o no
    global yaSeRetorno

    if not flagRetorno:
        if p[-1] == 'return':
            #Si no tengo regresar nada y no le estoy mandando nada
            printAuxQuad('RETURN', '', '', '')
            yaSeRetorno = True
        else:
            printReturnError()
    else: #si si tengo que regresar algo
        operandoRet = popOperandos()
        tipoRet = popTipos()
        memRet = popMemorias()
        #si los tipos son correctos se crea el cuadruplo con el operando regresado
        if dirFunciones.diccionario[currentFunction]['tipo'] == tipoRet:
            printAuxQuad('RETURN', '', '', memRet)
            yaSeRetorno = True
        else:
            #Si no es correcto los tipos, se genera un error
            printReturnError()

#Funcion que guarda el id de una funcion especial de Jubilo
def p_npSpecialFunctionId(p):
    '''
    npSpecialFunctionId :
    '''
    global pEspeciales
    nombreSFunc = str(p[-1])
    pEspeciales.append(nombreSFunc)

#Valida una funcion de un solo parametro de entrada, este parametro es de tipo full exp
#Genera el cuadruplo para realizar la funcion
def p_pnValidateFact(p):
    '''
    pnValidateFact :
    '''
    global funcValida
    specialFunction = pEspeciales.pop() #obtiene el nombre string de la funcion especial
    param = popOperandos() #resultado obtenido en FULL_EXP
    tipoParam = popTipos() #tipo de dato del resultado obtenido en FULL_EXP
    memParam = popMemorias() #posicion de memoria de lo que se obtuvo en FULL_EXP
    #VALIDACIONES PARA QUE LA FUNCION PUEDA FUNCIONAR
    tipoFunction = funcValida.get_tipo(specialFunction, tipoParam, '') #revisa en el cubo semantico
    if tipoFunction == 'error': #la funcion no se puede hacer con el tipo de parametro enviado
        printTypeMismatch()
    else: #la funcion es de tipo 'INT' y se procede con la funcion
        resultTemporal = nextTemporalAvail(tipoFunction)
        printAuxQuad(specialFunction, memParam, '', resultTemporal)
        pushTipo(tipoFunction) #guarda el tipo de resultado de la funcion especial
        pushOperando(resultTemporal) #creo que no necesito esto aqui
        pushMemoria(resultTemporal)

#Valida una funcion de un solo parametro de entrada, este parametro es de tipo ID arreglo
def p_pnValidateId(p):
    '''
    pnValidateId :
    '''
    global currentFunction
    nombreId = str(p[-1]) #nombre de la id
    specialFunction = pEspeciales.pop() #obtiene el nombre string de la funcion especial

    if dirFunciones.exist_var(currentFunction, nombreId):
        dims = dirFunciones.getDimensiones(currentFunction, nombreId)
        if (dims[0] == 0 or dims[1] > 0): #toma los casos en los que no es un arreglo o es una matriz
            print('Error. Se esperaba un parametro de tipo arreglo')
            sys.exit()
            return
        tipoId = dirFunciones.search_varType(currentFunction, nombreId)
        #en este if ya se sabe que el id es un arreglo y procede a hacer la validacion respecto a la funcion
        tipoFunction = funcValida.get_tipo(specialFunction, tipoId, '') #revisa en el cubo semantico
        if tipoFunction == 'error':
            printTypeMismatch()
        else:
            pushTipo(tipoFunction) #guarda el tipo del resultado que se debe obtener con la funcion especiales
            resultTemporal = nextTemporalAvail(tipoFunction)
            pushMemoria(resultTemporal)
            pushOperando(specialFunction)
            varMemPos = dirFunciones.search_memPos(currentFunction, nombreId)
            #QUAD(sum, posicion de memoria del argumento array, cantidad de valores en el array, direccion para el resultado de la fx)
            printAuxQuad(specialFunction, varMemPos, dims[0], resultTemporal)
    elif dirFunciones.exist_var(GLOBAL_CONTEXT, nombreId):
        dims = dirFunciones.getDimensiones(GLOBAL_CONTEXT, nombreId)
        if (dims[0] == 0 or dims[1] > 0): #toma los casos en los que no es un arreglo o es una matriz
            print('Error. Se esperaba un parametro de tipo arreglo')
            sys.exit()
            return
        tipoId = dirFunciones.search_varType(currentFunction, nombreId)
        #en este if ya se sabe que el id es un arreglo y procede a hacer la validacion respecto a la funcion
        tipoFunction = funcValida.get_tipo(GLOBAL_CONTEXT, tipoId, '') #revisa en el cubo semantico
        if tipoFunction == 'error':
            printTypeMismatch()
        else:
            pushTipo(tipoFunction) #guarda el tipo del resultado que se debe obtener con la funcion especiales
            resultTemporal = nextTemporalAvail(tipoFunction)
            pushMemoria(resultTemporal)
            pushOperando(specialFunction)
            varMemPos = dirFunciones.search_memPos(GLOBAL_CONTEXT, nombreId)
            printAuxQuad(specialFunction, varMemPos, dims[0], resultTemporal)
    else:
        print('Error. La variable ID = {} no ha sido declarada.'.format(nombreId))
        sys.exit()
        return

#Valida los parametros de una funciones especial con dos parametros de entrada
def p_pnValidateId2(p):
    '''
    pnValidateId2 :
    '''
    global currentFunction
    global pEspeciales
    specialFunction = pEspeciales.pop()
    nombreX = str(p[-1])
    nombreY = str(p[-3])
    #Si exsite X en actual
    if dirFunciones.exist_var(currentFunction, nombreX):
        dimsX = dirFunciones.getDimensiones(currentFunction, nombreX)
        tipoX = dirFunciones.search_varType(currentFunction, nombreX)
        varMemPosX = dirFunciones.search_memPos(currentFunction, nombreX)
        #Si existe Y en actual
        if dirFunciones.exist_var(currentFunction, nombreY):
            dimsY = dirFunciones.getDimensiones(currentFunction, nombreY)
            tipoY = dirFunciones.search_varType(currentFunction, nombreY)
            varMemPosY = dirFunciones.search_memPos(currentFunction, nombreY)
        #Si no, existe Y en global
        elif dirFunciones.exist_var(GLOBAL_CONTEXT, nombreY):
            dimsY = dirFunciones.getDimensiones(GLOBAL_CONTEXT, nombreY)
            tipoY = dirFunciones.search_varType(GLOBAL_CONTEXT, nombreY)
            varMemPosY = dirFunciones.search_memPos(GLOBAL_CONTEXT, nombreY)
        else:
            print('Error. La variable ID = {} no existe en ninguna parte.'.format(nombreY))
            sys.exit()
            return
    #Si existe X en global
    elif dirFunciones.exist_var(GLOBAL_CONTEXT, nombreX):
        dimsX = dirFunciones.getDimensiones(GLOBAL_CONTEXT, nombreX)
        tipoX = dirFunciones.search_varType(GLOBAL_CONTEXT, nombreX)
        varMemPosX = dirFunciones.search_memPos(GLOBAL_CONTEXT, nombreX)
        #Si existe Y en actual
        if dirFunciones.exist_var(currentFunction, nombreY):
            dimsY = dirFunciones.getDimensiones(currentFunction, nombreY)
            tipoY = dirFunciones.search_varType(currentFunction, nombreY)
            varMemPosY = dirFunciones.search_memPos(currentFunction, nombreY)
        #Si no, existe Y en global
        elif dirFunciones.exist_var(GLOBAL_CONTEXT, nombreY):
            dimsY = dirFunciones.getDimensiones(GLOBAL_CONTEXT, nombreY)
            tipoY = dirFunciones.search_varType(GLOBAL_CONTEXT, nombreY)
            varMemPosY = dirFunciones.search_memPos(GLOBAL_CONTEXT, nombreY)
        else:
            print('Error. La variable ID = {} no existe en ninguna parte.'.format(nombreY))
            sys.exit()
            return
    else:
        print('Error. La variable ID = {} no existe en ninguna parte.'.format(nombreX))
        sys.exit()
        return

    if (dimsX[0] == 0 or dimsX[1] > 0 or dimsY[0] == 0 or dimsY[1] > 0):
        print('Error. Se esperaban dos parametros de tipo arreglo')
        sys.exit()
        return
    tipoFunction = funcValida.get_tipo(specialFunction, tipoX, tipoY)
    if tipoFunction == 'error':
        printTypeMismatch()
    else:
        resultTemporal = nextTemporalAvail(tipoFunction)
        printAuxQuad(specialFunction, varMemPosY, dimsY[0], '')
        printAuxQuad(specialFunction, varMemPosX, dimsX[0], resultTemporal)
        pushOperando(specialFunction)
        pushMemoria(resultTemporal)
        pushTipo(tipoFunction)

#Punto neuralgico para el sort de un arreglo, no se crea espacio de memoria pues se modifica el que se manda por param
def p_pnValidateSortTranspose(p):
    '''
    pnValidateSortTranspose :
    '''
    global currentFunction
    global pEspeciales
    specialFunction = pEspeciales.pop()
    currentId = p[-1]
    auxContext = ''
    if dirFunciones.exist_var(currentFunction, currentId):
        auxContext = currentFunction
    elif dirFunciones.exist_var(GLOBAL_CONTEXT, currentId):
        auxContext = GLOBAL_CONTEXT
    else:
        print('Error. La variable ID = {} no existe en ninguna parte.'.format(currentId))
        sys.exit()
        return

    dimsVar = dirFunciones.getDimensiones(auxContext, currentId)
    typeVar = dirFunciones.search_varType(auxContext, currentId)
    memVar = dirFunciones.search_memPos(auxContext, currentId) #Memoria base
    if dimsVar[0] == 0: #Si no es un arreglo, petar
        print('Error. Se esperaba un parametro dimensionado')
        sys.exit()
        return
    else:
        tipoFunction = funcValida.get_tipo(specialFunction, typeVar, '')
        if tipoFunction == 'error':
            printTypeMismatch()
        else:
            #Quad(Sort, de donde empieza el arreglo, cuanto dura el arreglo o matriz)
            if dimsVar[1] == 0: #No Es matriz
                printAuxQuad(specialFunction, memVar, dimsVar[0], '')
            else: #si es matriz, mandar un quad con sort, donde empieza el arreglo, columnas, renglones
                auxCasillas = dimsVar[0] * dimsVar[1]
                printAuxQuad(specialFunction, memVar, dimsVar[0], dimsVar[1])

#Punto neuralgico para desplegar un histograma en base a un arreglo de datos y una constante entera #bins
def p_pnValidatePlotHist(p):
    '''
    pnValidatePlotHist :
    '''
    global currentFunction
    global pEspeciales
    global dirFunciones
    specialFunction = pEspeciales.pop()
    numBins = p[-1]
    currentId = p[-3]
    auxContext = ''
    if dirFunciones.exist_var(currentFunction, currentId):
        auxContext = currentFunction
    elif dirFunciones.exist_var(GLOBAL_CONTEXT, currentId):
        auxContext = GLOBAL_CONTEXT
    else:
        print('Error. La variable ID = {} no existe en ninguna parte.'.format(currentId))
        sys.exit()
        return

    dimsVar = dirFunciones.getDimensiones(auxContext, currentId)
    typeVar = dirFunciones.search_varType(auxContext, currentId)
    memVar = dirFunciones.search_memPos(auxContext, currentId) #Memoria base
    if dimsVar[0] == 0 or dimsVar[1] > 0: #Si no es un arreglo, petar
        print('Error. Se esperaba un parametro arreglo.')
        sys.exit()
        return
    else: #si es un arreglo
        tipoFunction = funcValida.get_tipo(specialFunction, typeVar, 'int')
        if tipoFunction == 'error':
            printTypeMismatch()
        else:
            #Quad(Plot Hist, memPos inicial del arreglo, tamano del arreglo, memPos Bins)
            binsMem = asMemConstant(numBins) #Obtener direccion de memoria de la constante
            printAuxQuad(specialFunction, memVar, dimsVar[0], binsMem)

#Punto neuralgico para desplegar una grafica lineal o la regresion lineal en base a dos arreglos
def p_pnValidatePlotLine(p):
    '''
    pnValidatePlotLine :
    '''
    global currentFunction
    global pEspeciales
    global dirFunciones
    specialFunction = pEspeciales.pop()
    paramY = p[-1]
    paramX = p[-3]
    auxContextX = ''
    auxContextY = ''
    if dirFunciones.exist_var(currentFunction, paramY):
        auxContextY = currentFunction
    elif dirFunciones.exist_var(GLOBAL_CONTEXT, paramY):
        auxContextY = GLOBAL_CONTEXT
    else:
        print('Error. La variable ID = {} no existe en ninguna parte.'.format(paramY))
        sys.exit()
        return
    if dirFunciones.exist_var(currentFunction, paramX):
        auxContextX = currentFunction
    elif dirFunciones.exist_var(GLOBAL_CONTEXT, paramX):
        auxContextX = GLOBAL_CONTEXT
    else:
        print('Error. La variable ID = {} no existe en ninguna parte.'.format(paramX))
        sys.exit()
        return

    dimsVarX = dirFunciones.getDimensiones(auxContextX, paramX)
    typeVarX = dirFunciones.search_varType(auxContextX, paramX)
    memVarX = dirFunciones.search_memPos(auxContextX, paramX) #Memoria base de X
    dimsVarY = dirFunciones.getDimensiones(auxContextY, paramY)
    typeVarY = dirFunciones.search_varType(auxContextY, paramY)
    memVarY = dirFunciones.search_memPos(auxContextY, paramY) #Memoria base de Y
    if dimsVarX[0] == 0 or dimsVarY[0] == 0 or dimsVarX[1] > 0 or dimsVarY[1] > 0: #Alguno de los dos parametros no es arreglo
        sys.exit("Error. Se esperan dos parametros de tipo arreglo para la funcion {}.".format(specialFunction))
        return
    if dimsVarX[0] != dimsVarY[0]: #Los arreglos mandados como parametro no son del mismo tamano
        sys.exit("Error. Los parametros de tipo arreglo para la funcion {} deben ser del mismo tamano.".format(specialFunction))
        return
    tipoFunction = funcValida.get_tipo(specialFunction, typeVarX, typeVarY)
    #print("LOS TIPOS DE LAS COSAS SON: ", specialFunction, typeVarX, typeVarY)
    if tipoFunction == 'error':
        printTypeMismatch()
    else:
        #Quad(plot line, donde empieza arr1, donde empieza arr2, tamano del arreglo)
        printAuxQuad(specialFunction, memVarX, memVarY, dimsVarX[0])

#Punto neuralgico para el export de csv
def p_pnValidateExportCsv(p):
    '''
    pnValidateExportCsv :
    '''
    global currentFunction
    global pEspeciales
    global dirFunciones
    specialFunction = pEspeciales.pop()
    paramName = str(p[-3])
    paramId = p[-1]
    auxContext = ''
    if dirFunciones.exist_var(currentFunction, paramId):
        auxContext = currentFunction
    elif dirFunciones.exist_var(GLOBAL_CONTEXT, paramId):
        auxContext = GLOBAL_CONTEXT
    else:
        print('Error. La variable ID = {} no existe en ninguna parte.'.format(paramId))
        sys.exit()
        return
    if len(paramName) <= 6 or paramName[-5:-1] != ".csv":
        print('Error. Se necesita un nombre de archivo de al menos un caracter con terminacion ".csv" para la funcion {}, se tiene nombre {}.'.format(specialFunction, paramName))
        sys.exit()
        return

    dimsVar = dirFunciones.getDimensiones(auxContext, paramId)
    typeVar = dirFunciones.search_varType(auxContext, paramId)
    memVar = dirFunciones.search_memPos(auxContext, paramId) #Memoria base de X
    if dimsVar[0] == 0: #El id que se recibio no es una variabl dimensionada
        sys.exit("Error. Se esperaba una variable dimensionada para la funcion {}.".format(specialFunction))
        return
    tipoFunction = funcValida.get_tipo(specialFunction, 'string', typeVar)
    if tipoFunction == 'error':
        printTypeMismatch()
    else:
        #Se ocupa verificar que sea un arreglo o una matriz, para definir que tantos espacios checar
        if dimsVar[1] > 0: #Es una matriz
            #Quad(export csv, dirBase, 'nombre', 'col x reng')
            strColReng = str(dimsVar[0]) + '/' + str(dimsVar[1])
            printAuxQuad(specialFunction, memVar, paramName, strColReng)
        else: #Es un arreglo
            #Quad(export csv, dirBase, 'nombre', 'col')
            printAuxQuad(specialFunction, memVar, paramName, dimsVar[0])

def p_pnValidateExchange(p):
    '''
    pnValidateExchange :
    '''
    global currentFunction
    global pEspeciales
    global dirFunciones
    specialFunction = pEspeciales.pop()
    paramX = p[-3]
    paramY = p[-1]
    auxContextX = ''
    auxContextY = ''
    if dirFunciones.exist_var(currentFunction, paramY):
        auxContextY = currentFunction
    elif dirFunciones.exist_var(GLOBAL_CONTEXT, paramY):
        auxContextY = GLOBAL_CONTEXT
    else:
        print('Error. La variable ID = {} no existe en ninguna parte.'.format(paramY))
        sys.exit()
        return
    if dirFunciones.exist_var(currentFunction, paramX):
        auxContextX = currentFunction
    elif dirFunciones.exist_var(GLOBAL_CONTEXT, paramX):
        auxContextX = GLOBAL_CONTEXT
    else:
        print('Error. La variable ID = {} no existe en ninguna parte.'.format(paramX))
        sys.exit()
        return

    dimsVarX = dirFunciones.getDimensiones(auxContextX, paramX)
    typeVarX = dirFunciones.search_varType(auxContextX, paramX)
    memVarX = dirFunciones.search_memPos(auxContextX, paramX) #Memoria base de X
    dimsVarY = dirFunciones.getDimensiones(auxContextY, paramY)
    typeVarY = dirFunciones.search_varType(auxContextY, paramY)
    memVarY = dirFunciones.search_memPos(auxContextY, paramY) #Memoria base de Y

    #Hacer el intercambio de valores de una variable a otra, pudiendo ser variables dimensioandas de mismo tamaño
    if dimsVarX[0] == 0: #X no es dimensionada
        if dimsVarY[0] != 0: #Pero Y si es dimensionada
            sys.exit("Error. Para la funcion {}, se necesitan dos variables de las mismas dimensiones.".format(specialFunction))
            return
        else: #X no es dim y Y tampoco
            #Validar que sean del mismo tipo
            tipoFunction = funcValida.get_tipo(specialFunction, typeVarX, typeVarY)
            if tipoFunction == 'error':
                printTypeMismatch()
            else:
                #Print quad(sp func, dirbase x, dir base y, 'single')
                printAuxQuad(specialFunction, memVarX, memVarY, 'single')
    else: #X si es dimensionada
        if dimsVarX[0] != dimsVarY[0] or dimsVarX[1] != dimsVarY[1]: #Pero Y no es de la misma dimension
            sys.exit("Error. Para la funcion {}, se necesitan dos variables de las mismas dimensiones.".format(specialFunction))
            return
        else: #Ambas son dimensionadas y de igual dimension
            tipoFunction = funcValida.get_tipo(specialFunction, typeVarX, typeVarY)
            if tipoFunction == 'error':
                printTypeMismatch()
            else:
                #Print quad(sp func, dirbase x, dir base y, 'single')
                auxStrCasillas = str(dimsVarX[0]) +'/' + str(dimsVarX[1])
                printAuxQuad(specialFunction, memVarX, memVarY, auxStrCasillas)

#Valida el caso especial de la funcion arrange, cuyos dos Full_EXP deben ser de tipo entero
def p_pnValidateArrange(p):
    '''
    pnValidateArrange :
    '''
    global currentFunction
    global currentVar
    #global currentType
    global dirFunciones

    specialFunction = pEspeciales.pop()
    param2 = popOperandos()
    param1 = popOperandos()
    tipoParam2 = popTipos()
    tipoParam1 = popTipos()
    memParam2 = popMemorias()
    memParam1 = popMemorias()

    tipoFunction = funcValida.get_tipo(specialFunction, tipoParam1, tipoParam2) #busca validacion en cubo semantico
    if tipoFunction == 'error':
        printTypeMismatch()
    else:
        memToReclaim = param2 - param1
        if memToReclaim > 0:
            varInitialMemory = nextMemoryAvail(currentFunction, tipoFunction)
            dirFunciones.add_varToFunction(currentFunction, currentVar, tipoFunction, 0, memToReclaim, varInitialMemory)
            print(specialFunction, param1, param2)
            printAuxQuad(specialFunction, memParam1, memParam2, varInitialMemory)
            #Reclamar memoria para variable dimensionada
            updateMemoryPointer(currentFunction, tipoFunction, memToReclaim - 1)
        else:
            print('Error. El limite superior debe ser mayor al limite inferior')
            sys.exit()
            return
    currentVar = ''
    #currentType = ''

def p_pnValidateZerosAndOnes(p):
    '''
    pnValidateZerosAndOnes :
    '''
    global currentFunction
    global currentVar
    global dirFunciones
    arrSize = p[-2]
    specialFunction = pEspeciales.pop()
    tipoFunction = funcValida.get_tipo(specialFunction, 'int', '')
    if tipoFunction == 'error':
        printTypeMismatch()
    else:
        if arrSize <= 0:
            sys.exit("Error. Se necesita un tamano mayor a 0 para la funcion {}.".format(specialFunction))
            return
        else:
            varInitialMemory = nextMemoryAvail(currentFunction, tipoFunction)
            dirFunciones.add_varToFunction(currentFunction, currentVar, tipoFunction, 0, arrSize, varInitialMemory)
            printAuxQuad(specialFunction, arrSize, '', varInitialMemory)
            updateMemoryPointer(currentFunction, tipoFunction, arrSize - 1)
    currentVar = ''

def p_pnValidateRands(p):
    '''
    pnValidateRands :
    '''
    global currentFunction
    global currentVar
    global dirFunciones
    global funcValida
    arrSize = p[-2]
    specialFunction = pEspeciales.pop()
    param2 = popOperandos()
    param1 = popOperandos()
    tipoParam2 = popTipos()
    tipoParam1 = popTipos()
    memParam2 = popMemorias()
    memParam1 = popMemorias()

    if tipoParam1 == tipoParam2:
        tipoFunction = funcValida.get_tipo(specialFunction, tipoParam1, 'int')
        if tipoFunction == 'error':
            print("tipos: ", specialFunction, tipoParam1, tipoParam2 )
            printTypeMismatch()
        else:
            if arrSize <= 0:
                sys.exit("Error. Se necesita un tamano mayor a 0 para la funcion {}.".format(specialFunction))
                return
            else:
                varInitialMemory = nextMemoryAvail(currentFunction, tipoFunction)
                dirFunciones.add_varToFunction(currentFunction, currentVar, tipoFunction, 0, arrSize, varInitialMemory)
                aux =  str(memParam1) + '/' + str(memParam2)
                printAuxQuad(specialFunction, aux, arrSize, varInitialMemory)
                updateMemoryPointer(currentFunction, tipoFunction, arrSize - 1)
    else:
        sys.exit("Error. Los limites superior e inferior deben ser del mismo tipo para la funcion {}.".format(specialFunction))
        return
    currentVar = ''

#Funcion para detectar que la variable actual variable es dimensionada
def p_pnDetectDimensionada(p):
    '''
    pnDetectDimensionada :
    '''
    global flagDimensionada
    flagDimensionada = True
    #Se tienen cosas que no se ocupan en las pilas
    varTipo = popTipos()
    varId = popOperandos()
    varMem = popMemorias()

#Funcion que recibe el numero de columnas
def p_pnGetColumnas(p):
    '''
    pnGetColumnas :
    '''
    global acumuladoR
    global contColumnas
    global dirFunciones
    global currentFunction
    global currentVar
    columnas = p[-1]
    if columnas > 0:
        acumuladoR = columnas #Equivale a R * (Ls - Li, que es 0)
        contColumnas = columnas
        #Actualizar variable y ponerle columnas
        dirFunciones.update_dimensions(currentFunction, currentVar, 0, columnas)
    else:
        #print('ERROR. Index invalido')
        sys.exit('ERROR. Index invalido, cantidad de columnas debe ser mayor a 0')
        return

#Funcion que recibe el numero de filas
def p_pnGetRenglones(p):
    '''
    pnGetRenglones :
    '''
    global acumuladoR
    global contRenglones
    global dirFunciones
    global currentFunction
    global currentVar
    renglones = p[-1]
    if renglones > 0:
        acumuladoR = acumuladoR * renglones
        contRenglones = renglones
        #Actualizar variable y ponerle renglones
        dirFunciones.update_dimensions(currentFunction, currentVar, renglones, -1) #Se manda columnas -1 cuando no se actualizan las columnas
    else:
        sys.exit('ERROR. Index invalido, cantidad de renglones debe ser mayor a cero.')
        return

#Funcion que ya ha recibido los renglones y columnas de una variable dimensionada
#Actualiza R y reclama la memoria necesaria para la variable dimensionada
def p_pnReclamarMemoriaDim(p):
    '''
    pnReclamarMemoriaDim :
    '''
    global acumuladoR
    global dirFunciones
    global currentFunction
    global currentVar
    global flagDimensionada
    global currentConsForArray
    cantValores = acumuladoR - 1
    acumuladoR = 1
    flagDimensionada = False
    currentType = dirFunciones.search_varType(currentFunction, currentVar)
    updateMemoryPointer(currentFunction, currentType, cantValores) #Reclamar memoria para variable dimensionada
    currentConsForArray = [] #Reiniciar las posibles constantes a asignar

#Funcion que recibe las constantes para una asignacion de arreglo
def p_pnGetConsForArray(p):
    '''
    pnGetConsForArray :
    '''
    global currentFunction
    global currentVar
    global currentConsForArray
    consToAdd = p[-1] #popOperando
    currentType = dirFunciones.search_varType(currentFunction, currentVar) #popType
    if currentType == 'int' or currentType == 'float':
        if type(consToAdd) == int or type(consToAdd) == float:
            currentConsForArray.append(consToAdd)
        else:
            printTypeMismatch()
    else: #el arreglo es de booleanos, quien hace un arreglo un arreglo de booleanos tho?
        if type(consToAdd) == 'bool':
            currentConsForArray.append(consToAdd)
        else:
            printTypeMismatch()

#Funcion que asigna los espacios de memoria para cada constante de un arreglo que fue asignado
def p_pnAssignConsToArray(p):
    '''
    pnAssignConsToArray :
    '''
    global currentFunction
    global currentVar
    global currentConsForArray
    global contColumnas
    #Si tengo el mismo numero de constantes a asignar, que el numero de columnas, las asigno
    if len(currentConsForArray) == contColumnas:
        memInicial = dirFunciones.search_memPos(currentFunction, currentVar)
        auxConsType = []
        auxConsId = []
        auxConsMem = []
        for index in range(contColumnas):
            auxConsType.append(popTipos())
            auxConsId.append(popOperandos())
            auxConsMem.append(popMemorias())

        for index in range(contColumnas):
            auxCons = auxConsMem.pop()
            auxMem = memInicial + index
            printAuxQuad('=', auxCons, '', auxMem) #Quadruplo para asignar los valores
    elif len(currentConsForArray) < contColumnas:
        print ('Error. No hay suficientes constantes para asignarse al arreglo {}, se tienen {}, se ocupan {}.'.format(currentVar, len(currentConsForArray), contColumnas))
        sys.exit()
        return
    elif len(currentConsForArray) > contColumnas:
        print('Error. Demasiadas constantes {} para asignarse al arreglo {} de tamano {}.'.format(len(currentConsForArray), currentVar, contColumnas))
        sys.exit()
        return

#Funcion que asigna los espacios de memoria para cada constante de una matriz que fue asignado
def p_pnAssignConsToMatrix(p):
    '''
    pnAssignConsToMatrix :
    '''
    global currentFunction
    global currentVar
    global currentConsForArray
    global contColumnas
    global contRenglones
    cantCasillas = contColumnas * contRenglones #Cantidad de casillas que tengo que asignar

    if len(currentConsForArray) == cantCasillas:
        memInicial = dirFunciones.search_memPos(currentFunction, currentVar)
        auxConsType = []
        auxConsId = []
        auxConsMem = []
        for index in range(cantCasillas):
            auxConsType.append(popTipos())
            auxConsId.append(popOperandos())
            auxConsMem.append(popMemorias())

        for index in range(cantCasillas):
            consMem = auxConsMem.pop()
            auxMem = memInicial + index
            printAuxQuad('=', consMem, '', auxMem) #Quadruplo para asignar los valores
    elif len(currentConsForArray) < cantCasillas:
        print ('Error. No hay suficientes constantes para asignarse a la matriz {}, se tienen {}, se ocupan {}.'.format(currentVar, len(currentConsForArray), cantCasillas))
        sys.exit()
        return
    elif len(currentConsForArray) > cantCasillas:
        print('Error. Demasiadas constantes {} para asignarse a la matriz {} de tamano {}.'.format(len(currentConsForArray), currentVar, cantCasillas))
        sys.exit()
        return

#Funcion para accesar a un indice de un arreglo
def p_pnAccessArray(p):
    '''
    pnAccessArray :
    '''
    global flagDimensionada #esta y currentVar se asignan en pnQuadGenExp1
    global currentVar #Variable que se esta tomando en cuenta
    global currentFunction
    auxId = popOperandos() #Elemento del index_intGlobales
    auxMem = popMemorias() #Posicion de memoria que tiene lo que
    auxType = popTipos() #Estas 3 cosas tambien se meten en pnQuadGenExp1

    if flagDimensionada: #Checar que si sea una variable dimensionada
        #checar que el indice que se quiere acceder resulte en un entero
        if auxType != 'int': #No resulta en entero
            print("Error. Se esperaba un entero para acceder en el arreglo {}.".format(currentVar))
            sys.exit()
            return

        #Obtiene las dimensiones de la variable (Que es el limite superior) - Regresa arr[columnas, renglones]
        varDims = dirFunciones.getDimensiones(currentFunction, currentVar)
        if varDims == -1: #Si no existe buscar en contexto global
            varDims = dirFunciones.getDimensiones(GLOBAL_CONTEXT, currentVar)
            if varDims == -1:
                print('ERROR. No se puede acceder por index a una variable no dimensionada')
                sys.exit()
                return

        #Cuadruplo para verificar si el index esta dentro de los limites del arreglo varDims
        printAuxQuad('VERIFICA', auxMem, 0, varDims[0])

        #Obtener memoria base de la variable
        varMemPos = dirFunciones.search_memPos(currentFunction, currentVar)
        if not varMemPos:
            varMemPos = dirFunciones.search_memPos(GLOBAL_CONTEXT, currentVar)
        #Si tampoco se encuentra en el contexto global, no existe la variable
        if varMemPos < 0:
            print("Error: Variable ", varId , " no declarada. :", varMemPos)
            sys.exit("Error: Variable {} no declarada.".format(varId))
            return

        #Buscar el tipo de la variable en su contexto para pushearlo, sino la encuentra buscar en globales
        currentVarTipo = dirFunciones.search_varType(currentFunction, currentVar)
        if not currentVarTipo:
            currentVarTipo = dirFunciones.search_varType(GLOBAL_CONTEXT, currentVar)
        #Si tampoco se encuentra en el contexto global, no existe la variable
        if not currentVarTipo:
            print("Error: Variable ", varId , " no declarada. 1")
            sys.exit("Error: Variable {} no declarada.".format(currentVar))
            return

        #Calcular memoria del indice, creando un cuadruplo de la suma de la direccion de memoria base con el contenido de auxMem
        contenidoDeAuxMem = '(' + str(auxMem) + ')'
        temporalAccessMem = nextTemporalAvail('int')
        printAuxQuad('+', varMemPos, contenidoDeAuxMem, temporalAccessMem)
        #No se le suma memoria base, porque es 0
        #Pushear indice a las pilas
        contenidoDeTempAccessMem = '(' + str(temporalAccessMem) + ')'
        pushOperando(currentVar)
        pushMemoria(contenidoDeTempAccessMem)
        pushTipo(currentVarTipo)
        flagDimensionada = False #regresa la bandera a falso para detectar futuras variables dimensionadas
        currentVar = ''

    else:
        print('ERROR. No se puede acceder por index a una variable no dimensionada')
        sys.exit()
        return

#Funcion para accesar a un indice de una matriz
def p_pnAccessMatrix(p):
    '''
    pnAccessMatrix :
    '''
    global flagDimensionada #Esta y currentVar se asignan en pnQuadGenExp1
    global currentVar #Variable que se esta tomando en cuenta
    global currentFunction #Contexto actual
    rengId = popOperandos() #Index para renglones
    rengMem = popMemorias()
    rengType = popTipos()
    colId = popOperandos() #Index para columnas
    colMem = popMemorias()
    colType = popTipos()

    if flagDimensionada: #Checar que si sea una variable dimensionada
        #Checar que ambos indices que se quieren acceder resulten en enteros
        if colType != 'int':
            print("Error. Se esperaba un entero para acceder a las columnas de la matriz {}.".format(currentVar))
            if rengType != 'int':
                print("Error. Se esperaba un entero para acceder a los renglones de la matriz {}.".format(currentVar))
            sys.exit()
            return
        if rengType != 'int':
            print("Error. Se esperaba un entero para acceder a los renglones de la matriz {}.".format(currentVar))
            sys.exit()
            return

        #Obtiene las dimensiones de la variable (Que son los limites superiores) - Regresa arr[columnas, renglones]
        varDims = dirFunciones.getDimensiones(currentFunction, currentVar)
        if varDims == -1: #Si no existe buscar en contexto global
            varDims = dirFunciones.getDimensiones(GLOBAL_CONTEXT, currentVar)
            if varDims == -1:
                print('ERROR. No se puede acceder por index a una variable no dimensionada')
                sys.exit()
                return

        #Cuadruplo para verificar si los indices estan dentro de lo permitido
        printAuxQuad('VERIFICA', colMem, 0, varDims[0]) #columnas
        printAuxQuad('VERIFICA', rengMem, 0, varDims[1]) #renglones

        #Obtener memoria base de la variable dimensionada
        varMemPos = dirFunciones.search_memPos(currentFunction, currentVar)
        if not varMemPos:
            varMemPos = dirFunciones.search_memPos(GLOBAL_CONTEXT, currentVar)
        #Si tampoco se encuentra en el contexto global, no existe la variable
        if varMemPos < 0:
            print("Error: Variable ", varId , " no declarada. :", varMemPos)
            sys.exit("Error: Variable {} no declarada.".format(varId))
            return

        #Buscar el tipo de la variable en su contexto para pushearlo, sino la encuentra buscar en globales
        currentVarTipo = dirFunciones.search_varType(currentFunction, currentVar)
        if not currentVarTipo:
            currentVarTipo = dirFunciones.search_varType(GLOBAL_CONTEXT, currentVar)
        #Si tampoco se encuentra en el contexto global, no existe la variable
        if not currentVarTipo:
            print("Error: Variable ", varId , " no declarada. 1")
            sys.exit("Error: Variable {} no declarada.".format(currentVar))
            return

        #Calcular memoria del indice, creando un cuadruplo de la suma de la direccion base
        # mas (cantidadRenglones * tamanoCol + cantidadColumnas)
        temporalAccessMem = nextTemporalAvail('int')
        # cantidadRenglones * tamanoCol
        printAuxQuad('*', rengMem, asMemConstant(varDims[0]), temporalAccessMem)
        # temporalAccessMem + cantidadColumnas
        temporalAccessMem2 = nextTemporalAvail('int')
        printAuxQuad('+', temporalAccessMem, colMem, temporalAccessMem2)
        # (temporalAccessMem2) + dirBase
        temporalAccessMem3 = nextTemporalAvail('int')
        contenidoDeAuxMem = '(' + str(temporalAccessMem2) + ')'
        printAuxQuad('+', varMemPos, contenidoDeAuxMem, temporalAccessMem3)

        #Pushear indice de memoria a las pilas
        contenidoDeTempAccessMem = '(' + str(temporalAccessMem3) + ')'
        pushOperando(currentVar)
        pushMemoria(contenidoDeTempAccessMem)
        pushTipo(currentVarTipo)
        flagDimensionada = False #regresa la bandera a falso para detectar futuras variables dimensionadas
        currentVar = ''
    else:
        print('ERROR. No se puede acceder por index a una variable no dimensionada')
        sys.exit()
        return

def p_pnAddSpecialFunctionVar(p):
    '''
    pnAddSpecialFunctionVar :
    '''
    #global currentType
    global currentVar
    #currentType = p[-4] #tipo variable special func
    currentVar = p[-3] #id variable special func

#Defining Lexer & Parser
parser = yacc.yacc()
lexer = lex.lex()

'''
MAIN EJECUCION
'''
name = './test_files/test3.txt'

#Num of arguments para ejecucion
arguments = len(sys.argv) - 1
if arguments >= 1:
    name = sys.argv[1]
if arguments == 2:
    obejotaName = sys.argv[2]

with open(name, 'r') as archive:
    s = archive.read()
print(name)
parser.parse(s)
