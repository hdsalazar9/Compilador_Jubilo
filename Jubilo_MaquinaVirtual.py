#Hector David Salazar Schz, A01207471.
#Melanie Vielma Saldana, A00818905.
#Diseno de compiladores Ago-Dic 2019. ITESM.
#Jubilo
import sys
import numpy as np
import statistics as stats
import math
import matplotlib.pyplot as plt

from Jubilo_MemoriaVirtual import *

#### Inicializacion de objetos de memoria para global y main ####
CONST_STRING_GLOBALES ='globales'
CONST_STRING_LOCALES = 'locales'
CONST_STRING_TEMPORALES = 'temporales'
CONST_STRING_CONSTANTES = 'constantes'
GLOBAL_CONTEXT = 'globals'
MAIN_CONTEXT = 'main'
m_Global = MemoriaVirtual(GLOBAL_CONTEXT)
m_Main = MemoriaVirtual(MAIN_CONTEXT)

### Inicializacion de variables para maquina virtual ###
obejota = open('./obejota_files/obejota1.jub')
quadList = [] #almacena cuadruplos despues de lectura de obejota
quadIndex = 0 #almacena el index del cuadruplo que se esta ejecutando en este momento
nextQuadIndex = -1 #almacena el siguiente index de cuadruplo a ejecutar
quad = () #Almacena el objeto del cuadruplo que se esta ejecutando en este momento
valoresRetorno = [] #Pila para acumular los valores de retorno de las funciones de usuario
pilaGosub = [] #Pila para las llamadas de funciones de usuario, saber a donde regresar


#Pila de ejecucion de memorias
pilaEjecucion = []
pilaTemporal = []
currentEjecucion = '' #Objeto de memoria virtual que se esta ejecutando actualmente
#Push/pop para pilas
def pushMemEjecucion(memoria):
	global pilaEjecucion
	pilaEjecucion.append(memoria)
def popMemEjecucion():
	global pilaEjecucion
	return pilaEjecucion.pop()
def topMemEjecucion():
	global pilaEjecucion
	last = len(pilaEjecucion) - 1
	if (last < 0):
		return 'empty'
	return pilaEjecucion[last]

def pushMemTemporal(memoria):
	global pilaTemporal
	pilaTemporal.append(memoria)
def popMemTemporal():
	global pilaTemporal
	return pilaTemporal.pop()
def topMemTemporal():
	global pilaTemporal
	last = len(pilaTemporal) - 1
	if (last < 0):
		return 'empty'
	return pilaTemporal[last]

def pushValRetorno(val):
	global valoresRetorno
	valoresRetorno.append(val)
def popValRetorno():
	global valoresRetorno
	return valoresRetorno.pop()

def pushGosub(val):
	global pilaGosub
	pilaGosub.append(val)
def popGosub():
	global pilaGosub
	return pilaGosub.pop()

pushMemEjecucion(m_Main)

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
Funcion que regresa el tipo de dato encontrado en el cuadruplo segun la direccion de memoria
'''
def getType(mem):
	global currentEjecucion
	type = ''
	try:
		if mem[0] == '{': #Si la memoria se refiere a una direccion de memoria, ignorarlo
			mem = getValor(currentEjecucion, mem[1:-1], getType(mem[1:-1]))
	except:
		pass
	mem = int(mem)
	if (mem >= 0 and mem < index_intGlobales) or (mem >= index_boolGlobales and mem < index_intLocales) or (mem >= index_boolLocales and mem < index_intTemporales) or (mem >= index_boolTemporales and mem < index_intConstantes):
		type = 'int'
	if (mem >= index_boolGlobales and mem < index_floatGlobales) or (mem >= index_intLocales and mem < index_floatLocales) or (mem >= index_intTemporales and mem < index_floatTemporales) or (mem >= index_intConstantes and mem < index_floatConstantes):
		type = 'float'
	if (mem >= index_floatGlobales and mem < index_boolGlobales) or (mem >= index_floatLocales and mem < index_boolLocales) or (mem >= index_floatTemporales and mem < index_boolTemporales) or mem == index_stringConstantes or mem == (index_stringConstantes+1):
		type = 'bool'
	if (mem >= index_floatConstantes and mem < index_stringConstantes):
		type = 'string'
	return type

def getSection(mem):
	global currentEjecucion
	section = ''
	try:
		if mem[0] == '{': #Si la memoria se refiere a una direccion de memoria, ignorarlo
			mem = getValor(currentEjecucion, mem[1:-1], getType(mem[1:-1]))
	except:
		pass
	mem = int(mem)
	if (mem >= 0 and mem < index_boolGlobales):
		section = CONST_STRING_GLOBALES
	if (mem >= index_boolGlobales and mem < index_boolLocales):
		section = CONST_STRING_LOCALES
	if (mem >= index_boolLocales and mem < index_boolTemporales):
		section = CONST_STRING_LOCALES #Se guardan las temporales en la memoria de locales
	if (mem >= index_boolTemporales and mem <= (index_stringConstantes + 1)):
		section = CONST_STRING_GLOBALES #Guardaremos las constantes en el contexto de globales
	return section
'''
Funcion que regresa el valor del dato encontrado en el cuadruplo segun la direccion de memoria
'''
def getValor(objMemVirt, memoryAddress, memoryType):
	global m_Global
	#Checar si la memoryAddress se trata de una referencia a otra mem memoryAddress
	try:
		if memoryAddress[0] == '{' and memoryAddress[-1] == '}':
			memoryAddress = getValor(objMemVirt, memoryAddress[1:-1], getType(memoryAddress[1:-1]))
			memoryType = getType(memoryAddress)
	except:
		pass
	auxValor = -1
	auxSection = getSection(memoryAddress) #Saber por la memoria a que contexto pertenece global o local
	if auxSection == CONST_STRING_GLOBALES:
		try: #Obtener el valor de la memoria actual (objMemVirt)
			auxValor = m_Global.getValueFromMemory(str(memoryAddress),str(memoryType))
		except:
			print("Unexpected error:", sys.exc_info()[0], quadIndex)
			print("Error. Se quiere acceder a una variable no inicializada.",auxSection,memoryAddress, quadIndex)
			sys.exit()
	elif auxSection == CONST_STRING_LOCALES:
		try:
			auxValor = objMemVirt.getValueFromMemory(str(memoryAddress), str(memoryType))
		except:
			print("Unexpected error:", sys.exc_info()[0], quadIndex)
			print("Error. Se quiere acceder a una variable no inicializada.",auxSection,memoryAddress, quadIndex)
			sys.exit()
	else:
		print("Error fatal. No se encuentra esa seccion de memoria.")
		sys.exit()
	#print("auxValor",auxValor)
	return auxValor

'''
Funcion que llena un espacio de memoria con un valor
'''
def fillValor(objMemVirt, memoryAddress, memoryType, value):
	global m_Global
	try:
		if memoryAddress[0] == '{' and memoryAddress[-1] == '}': #Saber por la memoria a que contexto pertenece global o local
			memoryAddress = getValor(objMemVirt, memoryAddress[1:-1], getType(memoryAddress[1:-1]))
			memoryType = getType(memoryAddress)
	except:
		pass
	memoryType = str(memoryType)
	auxSection = getSection(memoryAddress)
	if auxSection == CONST_STRING_GLOBALES: #anadir el valor a globales
		m_Global.fillMemory(memoryAddress, memoryType, value)
	elif auxSection == CONST_STRING_LOCALES: #anadir el valor a locales
		objMemVirt.fillMemory(memoryAddress, memoryType, value)
	else:
		print("Error fatal. No se encuentra esa seccion de memoria.")
		sys.exit()

'''
Funcion principal de la maquina virtual
Ejecuta los cuadruplos que lee del archivo obejota : codigo objeto
'''
def ejecucion():
	global quad
	global quadList
	global valoresRetorno
	global m_Global #Para guardar constantes
	global currentEjecucion
	global nextQuadIndex
	global quadIndex

	currentEjecucion = topMemEjecucion(); #Es top porque aun no hay necesidad de sacarlo
	quad = quadList[quadIndex]
	nextQuadIndex = -1 #Aun no se sabe el siguiente cuadruplo

	'''
	Receta de cocina para leer cuadruplo:
	1. Obtiene los tipos de datos de los dos operandos
	2. Obtiene el valor de los dos operandos
	3. Condicionales para los datos validos, convierte el operador al tipo de dato que es
	4. hace la operacion del cuadruplo
	'''
	if quad[0] == 'ENDPROGRAM': #Fin del programa
		#probablemente deberia limpiar algunas pilas o algo asi
		print("Jubi > Fin de ejecucion del programa {}, vuelva pronto :)".format(str(quad[1])))
		return
	elif quad[0] == 'GOTO':
		nextQuadIndex = int(quad[3])
	elif quad[0] == 'GOTOF':
		tipo1 = getType(quad[1])
		auxBool = getValor(currentEjecucion, quad[1], tipo1)
		#print("Deberia de hacer gotof",auxBool)
		if not auxBool: #si si evalua en falso, ir al quad que diga el [3]
			nextQuadIndex = int(quad[3])
	#Adding de Constantes a la memoria de global
	elif quad[0] == 'addConstant':
		#('addConstant', 'int', 0, 9001)
		#print("quiero poner: ",m_Global, quad[3], str(quad[1]), quad[2])
		fillValor(m_Global, quad[3], quad[1], quad[2])
	#Operadores aritmeticos
	elif quad[0] == '+':
		try:
			if quad[1][0] == '~':
				tipo1 = 'int'
				op1 = int(quad[1][1:])
			else:
				tipo1 = getType(quad[1])
				op1 = getValor(currentEjecucion, quad[1], tipo1)
		except:
			tipo1 = getType(quad[1])
			op1 = getValor(currentEjecucion, quad[1], tipo1)
			pass
		tipo2 = getType(quad[2])
		op2 = getValor(currentEjecucion, quad[2], tipo2)
		#Castea el valor encontrado en la direccion de currentEjecucion al tipo que le corresponde
		if tipo1 == 'int':
			op1 = int(op1)
		if tipo2 == 'int':
			op2 = int(op2)
		if tipo1 == 'float':
			op1 = float(op1)
		if tipo2 == 'float':
			op2 = float(op2)
		res = op1 + op2
		fillValor(currentEjecucion, quad[3], getType(quad[3]), res)
	elif quad[0] == '-':
		tipo1 = getType(quad[1])
		tipo2 = getType(quad[2])
		op1 = getValor(currentEjecucion, quad[1], tipo1)
		op2 = getValor(currentEjecucion, quad[2], tipo2)
		#Castea el valor encontrado en la direccion de currentEjecucion al tipo que le corresponde
		if tipo1 == 'int':
			op1 = int(op1)
		if tipo2 == 'int':
			op2 = int(op2)
		if tipo1 == 'float':
			op1 = float(op1)
		if tipo2 == 'float':
			op2 = float(op2)
		res = op1 - op2
		fillValor(currentEjecucion, quad[3], getType(quad[3]), res)
	elif quad[0] == '*':
		tipo1 = getType(quad[1])
		tipo2 = getType(quad[2])
		op1 = getValor(currentEjecucion, quad[1], tipo1)
		op2 = getValor(currentEjecucion, quad[2], tipo2)
		#Casting if needed
		if tipo1 == 'int':
			op1 = int(op1)
		if tipo2 == 'int':
			op2 = int(op2)
		if tipo1 == 'float':
			op1 = float(op1)
		if tipo2 == 'float':
			op2 = float(op2)
		res = op1 * op2
		fillValor(currentEjecucion, quad[3], getType(quad[3]), res)
	elif quad[0] == '/':
		tipo1 = getType(quad[1])
		tipo2 = getType(quad[2])
		op1 = getValor(currentEjecucion, quad[1], tipo1)
		op2 = getValor(currentEjecucion, quad[2], tipo2)
		#Casting if needed
		if tipo1 == 'int':
			op1 = int(op1)
		if tipo2 == 'int':
			op2 = int(op2)
		if tipo1 == 'float':
			op1 = float(op1)
		if tipo2 == 'float':
			op2 = float(op2)
		res = op1 / op2
		fillValor(currentEjecucion, quad[3], getType(quad[3]), res)
	#Asignacion
	elif quad[0] == '=':
		auxTipo = ''
		auxValor = 0
		try:
			auxTipo = getType(quad[1])
			auxValor = getValor(currentEjecucion, quad[1], auxTipo)
		except:
			#print("Unexpected error:", sys.exc_info()[0], quadIndex)
			auxTipo = getType(quad[3])
			auxValor = valoresRetorno.pop()
		fillValor(currentEjecucion, quad[3], auxTipo, auxValor)
	#Operadores relacionales
	elif quad[0] == '<':
		tipo1 = getType(quad[1])
		tipo2 = getType(quad[2])
		op1 = getValor(currentEjecucion, quad[1], tipo1)
		op2 = getValor(currentEjecucion, quad[2], tipo2)
		if tipo1 == 'int':
			op1 = int(op1)
		if tipo2 == 'int':
			op2 = int(op2)
		if tipo1 == 'float':
			op1 = float(op1)
		if tipo2 == 'float':
			op2 = float(op2)
		if op1 < op2:
			res = True
		else:
			res = False
		fillValor(currentEjecucion, quad[3], getType(quad[3]), res)
	elif quad[0] == '>':
		tipo1 = getType(quad[1])
		tipo2 = getType(quad[2])
		op1 = getValor(currentEjecucion, quad[1], tipo1)
		op2 = getValor(currentEjecucion, quad[2], tipo2)

		if tipo1 == 'int':
			op1 = int(op1)
		if tipo2 == 'int':
			op2 = int(op2)
		if tipo1 == 'float':
			op1 = float(op1)
		if tipo2 == 'float':
			op2 = float(op2)
		if op1 > op2:
			res = True
		else:
			res = False
		fillValor(currentEjecucion, quad[3], getType(quad[3]), res)
	elif quad[0] == '<=':
		tipo1 = getType(quad[1])
		tipo2 = getType(quad[2])
		op1 = getValor(currentEjecucion, quad[1], tipo1)
		op2 = getValor(currentEjecucion, quad[2], tipo2)
		if tipo1 == 'int':
			op1 = int(op1)
		if tipo2 == 'int':
			op2 = int(op2)
		if tipo1 == 'float':
			op1 = float(op1)
		if tipo2 == 'float':
			op2 = float(op2)
		if op1 <= op2:
			res = True
		else:
			res = False
		fillValor(currentEjecucion, quad[3], getType(quad[3]), res)
	elif quad[0] == '>=':
		tipo1 = getType(quad[1])
		tipo2 = getType(quad[2])
		op1 = getValor(currentEjecucion, quad[1], tipo1)
		op2 = getValor(currentEjecucion, quad[2], tipo2)
		if tipo1 == 'int':
			op1 = int(op1)
		if tipo2 == 'int':
			op2 = int(op2)
		if tipo1 == 'float':
			op1 = float(op1)
		if tipo2 == 'float':
			op2 = float(op2)
		if op1 >= op2:
			res = True
		else:
			res = False
		fillValor(currentEjecucion, quad[3], getType(quad[3]), res)
	elif quad[0] == '==':
		tipo1 = getType(quad[1])
		tipo2 = getType(quad[2])
		op1 = getValor(currentEjecucion, quad[1], tipo1)
		op2 = getValor(currentEjecucion, quad[2], tipo2)
		if tipo1 == 'int':
			op1 = int(op1)
		if tipo2 == 'int':
			op2 = int(op2)
		if tipo1 == 'float':
			op1 = float(op1)
		if tipo2 == 'float':
			op2 = float(op2)
		if op1 == op2:
			res = True
		else:
			res = False
		fillValor(currentEjecucion, quad[3], getType(quad[3]), res)
	elif quad[0] == '!=':
		tipo1 = getType(quad[1])
		tipo2 = getType(quad[2])
		op1 = getValor(currentEjecucion, quad[1], tipo1)
		op2 = getValor(currentEjecucion, quad[2], tipo2)
		if tipo1 == 'int':
			op1 = int(op1)
		if tipo2 == 'int':
			op2 = int(op2)
		if tipo1 == 'float':
			op1 = float(op1)
		if tipo2 == 'float':
			op2 = float(op2)
		if op1 != op2:
			res = True
		else:
			res = False
		fillValor(currentEjecucion, quad[3], getType(quad[3]), res)
	#Operadores logicos
	elif quad[0] == '||':
		tipo1 = getType(quad[1])
		tipo2 = getType(quad[2])
		op1 = getValor(currentEjecucion, quad[1], tipo1)
		op2 = getValor(currentEjecucion, quad[2], tipo2)
		if op1 == op2 and op1 == False and op2 == False:
			res = False
		else:
			res = True
		fillValor(currentEjecucion, quad[3], getType(quad[3]), res)
	elif quad[0] == '&&':
		tipo1 = getType(quad[1])
		tipo2 = getType(quad[2])
		op1 = getValor(currentEjecucion, quad[1], tipo1)
		op2 = getValor(currentEjecucion, quad[2], tipo2)
		if op1 == op2 and op1 == True:
			res = True
		else:
			res = False
		fillValor(currentEjecucion, quad[3], getType(quad[3]), res)
	#Print & Read
	elif quad[0] == 'print':
		tipo1 = getType(quad[1])
		op1 = getValor(currentEjecucion, quad[1], tipo1)
		if tipo1 == 'string':
			print("Jubi > {}".format(str(op1[1:-1])))
		else:
			print("Jubi > {}".format(str(op1)))
		#currentEjecucion.printMV()
	elif quad[0] == 'read':
		op1 = input("Jubi > ")
		try:
			int(op1)
			tipo1 = 'int'
		except:
			try:
				float(op1)
				tipo1 = 'float'
			except:
				try:
					str(op1)
					if op1 == "true" or op1 == "false":
						tipo1 = 'bool'
					else:
						tipo1 = 'string'
				except:
					print("Unexpected error:", sys.exc_info()[0], quadIndex)
		if tipo1 == getType(quad[1]):
			fillValor(currentEjecucion, quad[1], getType(quad[1]), op1)
		else:
			print("Error. Tipos de read incorrectos, se recibio un {} para una memoria de {}.".format(tipo1, getType(quad[1])))
			sys.exit()
			return
	#Calcular la memoria para los arrays
	elif quad[0] == 'VERIFICA':
		#Checar si el siguiente tambien es un verifica que significaria un array
		auxQuad = quadList[quadIndex + 1]
		if auxQuad[0] == 'VERIFICA': #se trata de una matriz
			#quad varifica 1
			#auxQuad verifica 2
			tipo1 = getType(quad[1])
			op1 = getValor(currentEjecucion, quad[1], tipo1)
			tipo2 = getType(auxQuad[1])
			op2 = getValor(currentEjecucion, auxQuad[1], tipo2)
			try: #Verificar los limites
				op1 = int(op1)
				op2 = int(op2)
				lim_inf1 = int(quad[2])
				lim_sup1 = int(quad[3])
				lim_inf2 = int(auxQuad[2])
				lim_sup2 = int(auxQuad[3])
			except:
				print("Unexpected error:", sys.exc_info()[0], quadIndex)
				sys.exit()
				return
			if op1 < lim_inf1 or op1 >= lim_sup1:
				print("JubiError > El indice para columnas {} no esta dentro de los limites {} a {}.".format(op1, lim_inf1, lim_sup1))
				sys.exit()
				return
			if op2 < lim_inf2 or op2 >= lim_sup2: #No esta dentro de los indices
				print("JubiError > El indice para renglones {} no esta dentro de los limites {} a {}.".format(op2, lim_inf2, lim_sup2))
				sys.exit()
				return
			#Saltarse los quads comidos
			nextQuadIndex = quadIndex + 2
		elif auxQuad[0] == '+':
			tipo1 = getType(quad[1])
			op1 = getValor(currentEjecucion, quad[1], tipo1)
			try:
				op1 = int(op1)
				lim_inf = int(quad[2])
				lim_sup = int(quad[3])
			except:
				print("Unexpected error:", sys.exc_info()[0], quadIndex)
				sys.exit()
				return
			if op1 < lim_inf or op1 >= lim_sup: #No esta dentro de los indices
				print("JubiError > El indice {} no esta dentro de los limites {} a {}.".format(op1, lim_inf, lim_sup))
				sys.exit()
				return
			#cuadruplo que tendra la suma de memoria y un index
			tipo2 = getType(auxQuad[2])
			op2 = getValor(currentEjecucion, auxQuad[2], tipo2)
			memToAdd = int(auxQuad[1]) + int(op2)
			#print("Quiero acceder a index: ",memToAdd)
			#Anadir la memoria calculada
			fillValor(currentEjecucion, auxQuad[3], getType(auxQuad[3]), memToAdd)
			#Saltarse el quad de suma que nos estamos comiendo
			nextQuadIndex = quadIndex + 2
		else:
			print("Error en el acomodo de los cuadruplos...")
			sys.exit()
			return
	#Quadruplos de funciones de usuario
	elif quad[0] == 'GOSUB':
		currentEjecucion = popMemTemporal()
		pushMemEjecucion( currentEjecucion )
		pushGosub(quad[2]) #Saber a donde regresar despues
		nextQuadIndex = int(quad[3]) #Ir a ejecutar esa funcion dentro de los cuadruplos
	elif quad[0] == 'ERA':
		#Agregar una nueva memoria a la pila de memorias
		nameFunc = str(quad[1])
		newMemory = MemoriaVirtual(nameFunc)
		pushMemTemporal(newMemory)
	elif quad[0] == 'ENDPROC':
		popMemEjecucion() #Ya se acabo de procesar esa funcion
		nextQuadIndex = int(popGosub())
	elif quad[0] == 'RETURN':
		if quad[3] != '':
			auxOp = getValor(currentEjecucion, quad[3], getType(quad[3]))
			pushValRetorno(auxOp)
		popMemEjecucion()
		nextQuadIndex = int(popGosub());
	elif quad[0] == 'PARAMETER':
		#Los parametros son las primeras casillas de una funcion entonces
		#asignar en las primeras casillas de variables los parametros
		parameterType = getType(quad[1])
		parameterVal = getValor(currentEjecucion, quad[1], parameterType)
		#Memoria temporal de la funcion a donde se mandan los parametros
		auxMem = topMemTemporal()
		#Vars locales empiezan en index = index_boolGlobales
		#Obtener en donde guardar el parametro
		parameterMem = auxMem.nextToSaveParam(parameterType, index_boolGlobales, BATCH_SIZE)
		fillValor(auxMem, parameterMem, getType(parameterMem), parameterVal)

	#Quadruplos de Funciones especiales de Jubilo
	elif quad[0] == 'fact':
		tipo = getType(quad[1])
		param = getValor(currentEjecucion, quad[1], tipo)
		if int(param) < 0:
			print('Error. No se puede calcular el factorial de un entero negativo')
			sys.exit()
			return
		else:
			param = math.factorial(int(param))
			auxTipo = getType(quad[3])
			fillValor(currentEjecucion, quad[3], auxTipo , param)

	elif quad[0] == 'sum':
		arreglo = [] #almacenara todas las constantes del arreglo
		memPosBase = int(quad[1]) #toma como entero la memoria base del arreglo
		columnas = int(quad[2])
		for x in range (columnas):
			auxValor = getValor(currentEjecucion, memPosBase+x, getType(memPosBase+x))
			arreglo.append(float(auxValor))
		auxTipo = getType(quad[3])
		fillValor(currentEjecucion, quad[3], auxTipo, np.sum(arreglo))
	elif quad[0] == 'mean':
		arreglo = []
		memPosBase = int(quad[1])
		columnas = int(quad[2])
		for x in range(columnas):
			auxValor = getValor(currentEjecucion, memPosBase+x, getType(memPosBase+x))
			arreglo.append(float(auxValor))
		auxTipo = getType(quad[3])
		fillValor(currentEjecucion, quad[3], auxTipo, np.mean(arreglo))
	elif quad[0] == 'median':
		arreglo = []
		memPosBase = int(quad[1])
		columnas = int(quad[2])
		for x in range(columnas):
			auxValor = getValor(currentEjecucion, memPosBase+x, getType(memPosBase+x))
			arreglo.append(float(auxValor))
		auxTipo = getType(quad[3])
		fillValor(currentEjecucion, quad[3], auxTipo, np.median(arreglo))
	elif quad[0] == 'mode':
		arreglo = []
		memPosBase = int(quad[1])
		columnas = int(quad[2])
		for x in range(columnas):
			auxValor = getValor(currentEjecucion, memPosBase+x, getType(memPosBase+x))
			arreglo.append(float(auxValor))
		auxTipo = getType(quad[3])
		try:
			res = stats.mode(arreglo)
			fillValor(currentEjecucion, quad[3], auxTipo, res)
		except:
			print("Jubi > El arreglo no tiene una moda definida, se regresa el ultimo valor.")
			fillValor(currentEjecucion, quad[3], auxTipo, auxValor)
	elif quad[0] == 'stdev':
		arreglo = []
		memPosBase = int(quad[1])
		columnas = int(quad[2])
		for x in range(columnas):
			auxValor = getValor(currentEjecucion, memPosBase+x, getType(memPosBase+x))
			arreglo.append(float(auxValor))
		auxTipo = getType(quad[3])
		fillValor(currentEjecucion, quad[3], auxTipo, np.std(arreglo))
	elif quad[0] == 'var':
		arreglo = []
		memPosBase = int(quad[1])
		columnas = int(quad[2])
		for x in range(columnas):
			auxValor = getValor(currentEjecucion, memPosBase+x, getType(memPosBase+x))
			arreglo.append(float(auxValor))
		auxTipo = getType(quad[3])
		fillValor(currentEjecucion, quad[3], auxTipo, np.var(arreglo))
	elif quad[0] == 'covariance':
		quad2 = quadList[quadIndex + 1]
		arreglo1 = []
		memPosBase1 = int(quad[1])
		columnas1 = int(quad[2])
		arreglo2 = []
		memPosBase2 = int(quad2[1])
		columnas2 = int(quad2[2])
		for x in range(min(columnas1, columnas2)):
			auxValor1 = getValor(currentEjecucion, memPosBase1+x, getType(memPosBase1+x))
			auxValor2 = getValor(currentEjecucion, memPosBase2+x, getType(memPosBase2+x))
			arreglo1.append(auxValor1)
			arreglo2.append(auxValor2)

		res = np.cov(np.array(arreglo1).astype(np.float), np.array(arreglo2).astype(np.float), bias=True)[0][1]
		auxTipo = getType(quad2[3])
		fillValor(currentEjecucion, quad2[3], auxTipo, res)
		#compensar el quad comido por esta funcion
		nextQuadIndex = quadIndex + 2
	elif quad[0] == 'correlation':
		quad2 = quadList[quadIndex + 1]
		arreglo1 = []
		memPosBase1 = int(quad[1])
		columnas1 = int(quad[2])
		arreglo2 = []
		memPosBase2 = int(quad2[1])
		columnas2 = int(quad2[2])
		for x in range(min(columnas1, columnas2)):
			auxValor1 = getValor(currentEjecucion, memPosBase1+x, getType(memPosBase1+x))
			auxValor2 = getValor(currentEjecucion, memPosBase2+x, getType(memPosBase2+x))
			arreglo1.append(auxValor1)
			arreglo2.append(auxValor2)
		res = np.correlate(np.array(arreglo1).astype(np.float), np.array(arreglo2).astype(np.float))
		auxTipo = getType(quad2[3])
		fillValor(currentEjecucion, quad2[3], auxTipo, res[0])
		#compensar el quad comido por esta funcion
		nextQuadIndex = quadIndex + 2
	#Funciones especiales de creacion de arreglos
	elif quad[0] == 'arrange':
		lim_inf = getValor(currentEjecucion, quad[1], getType(quad[1]))
		lim_sup = getValor(currentEjecucion, quad[2], getType(quad[2]))
		arreglo = np.arange(int(lim_inf),int(lim_sup))
		for x in range(len(arreglo)):
			fillValor(currentEjecucion, int(quad[3])+x, getType(int(quad[3])+x), arreglo[x])

	elif quad[0] == 'zeros':
		size = int(quad[1])
		arreglo = np.zeros(size)
		for x in range(len(arreglo)):
			fillValor(currentEjecucion, int(quad[3])+x, getType(int(quad[3])+x), arreglo[x])

	elif quad[0] == 'ones':
		size = int(quad[1])
		arreglo = np.ones(size)
		for x in range(len(arreglo)):
			fillValor(currentEjecucion, int(quad[3])+x, getType(int(quad[3])+x), arreglo[x])

	elif quad[0] == 'randint':
		limites = quad[1]
		lim_inf = limites[0:limites.find('/')]
		lim_inf = getValor(currentEjecucion, lim_inf, getType(lim_inf))
		lim_sup = limites[limites.find('/')+1:]
		lim_sup = getValor(currentEjecucion, lim_sup, getType(lim_sup))
		lim_inf = float(lim_inf)
		lim_sup = float(lim_sup)
		cuantos = int(quad[2])
		donde = int(quad[3])
		resArray = np.random.randint(lim_inf, lim_sup, size=cuantos)
		for x in range(cuantos):
			fillValor(currentEjecucion, donde+x, getType(donde+x), resArray[x])
	elif quad[0] == 'randfloat':
		limites = quad[1]
		lim_inf = limites[0:limites.find('/')]
		lim_inf = getValor(currentEjecucion, lim_inf, getType(lim_inf))
		lim_sup = limites[limites.find('/')+1:]
		lim_sup = getValor(currentEjecucion, lim_sup, getType(lim_sup))
		lim_inf = float(lim_inf)
		lim_sup = float(lim_sup)
		cuantos = int(quad[2])
		donde = int(quad[3])
		#(b - a) * random_sample() + a
		resArray = (lim_sup - lim_inf) * np.random.random_sample(cuantos) + lim_inf
		for x in range(cuantos):
			fillValor(currentEjecucion, donde+x, getType(donde+x), resArray[x])
	#Sort & Transpose
	elif quad[0] == 'sort':
		memPosBase = int(quad[1])
		columnas= int(quad[2])
		if quad[3] == '':
			renglones = 0
		else:
			renglones=int(quad[3])
		auxArray = []
		if renglones == 0: #Es un arreglo
			for x in range(columnas -1):
				auxArray.append(getValor(currentEjecucion, memPosBase+x, getType(memPosBase+x)))
		else:
			for x in range(renglones -1):
				for y in range(columnas -1):
					s = memPosBase+y+x*columnas
					auxArray.append(getValor(currentEjecucion, s, getType(s)))
		narray = np.array(auxArray)
		sortedArray = np.sort(narray)
		if renglones == 0: #Es un arreglo
			for x in range(columnas -1):
				fillValor(currentEjecucion, memPosBase+x, getType(memPosBase+x), sortedArray[x])
		else:
			for x in range(renglones -1):
				for y in range(columnas -1):
					s = memPosBase+y+x*columnas
					fillValor(currentEjecucion, s, getType(s), sortedArray[x][y])

	elif quad[0] == 'transpose':
		''' No puedo :/
		#Algoritmo obtenido de:
		#https://www.programiz.com/python-programming/examples/transpose-matrix
		memoriaBase=int(quad[1])
		columnas= int(quad[2])
		if quad[3] == '':
			filas = 1
		else:
			filas=int(quad[3])
		matTemp=[]
		arrTemp=[]
		for fila in range(filas -1):
			arrTemp=[]
			for columna in range(columnas -1):
				x=memoriaBase+fila+columna*filas
				arrTemp.append(getValor(currentEjecucion, x, getType(quad[1])))
			matTemp.append(arrTemp)
		for fila in range(filas -1):
			for columna in range(columnas -1):
				x=memoriaBase+columna+fila*columnas
				fillValor(currentEjecucion, x, getType(quad[1]), matTemp[columna][fila])
		'''


	#Habiendo revisado el cuadruplo ir al siguiente cuadruplo a ejecutar
	#Que si nextQuadIndex sigue en -1, deberia ser el siguiente
	if nextQuadIndex != -1:
		quadIndex = nextQuadIndex
	else: #Solo se ejecuta el siguiente quad
		quadIndex = quadIndex + 1
	#Volver a llamar a la funcion de ejecucion hasta que termine el programa
	ejecucion()

'''
Lee el archivo obejota. EJEMPLO (+,a,b,t1) -> +,a,b,t1
line : string del archivo obejota
python replace syntax -> string.replace('old substring', 'new substring')
python split syntax -> string.split('separator')
'''
for line in obejota:
	line = line.replace('(','')
	line = line.replace(')','')
	line = line.replace('\n','')
	line = line.replace('\'','')
	line = line.replace(' ','')

	quad = tuple(line.split(','))
	auxQuad = (1,1,1,1)
	quad = (quad[0], quad[1], quad[2], quad[3])
	quadList.append(quad)
ejecucion() #llamada a funcion para ejecutar cuadruplo por cuadruplo generado despues de lectura de obejota
