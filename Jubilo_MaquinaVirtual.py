#Hector David Salazar Schz, A01207471.
#Melanie Vielma Saldana, A00818905.
#Diseno de compiladores Ago-Dic 2019. ITESM.
#Jubilo
import sys

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

def pushValRetorno(val):
	global valoresRetorno
	valoresRetorno.append(val)
def popValRetorno():
	global valoresRetorno
	return valoresRetorno.pop()

def pushGosub(val):
	global pilaGosub
	pilaGosub.append(val)
def popGosub(val):
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
	type = ''
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
	section = ''
	#print("Typo de mem: ", type(mem), mem, quadIndex)
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
	memoryType = str(memoryType)
	auxValor = -1
	auxSection = getSection(memoryAddress) #Saber por la memoria a que contexto pertenece global o local
	if auxSection == CONST_STRING_GLOBALES:
		try: #Obtener el valor de la memoria actual (objMemVirt)
			auxValor = m_Global.getValueFromMemory(str(memoryAddres), memoryType)
		except:
			print("Error. Se quiere acceder a una variable no inicializada.",auxSection,memoryAddress)
			sys.exit()
	elif auxSection == CONST_STRING_LOCALES:
		try:
			auxValor = objMemVirt.getValueFromMemory(str(memoryAddres), memoryType)
		except:
			print("Error. Se quiere acceder a una variable no inicializada.",auxSection,memoryAddress)
			sys.exit()
	else:
		print("Error fatal. No se encuentra esa seccion de memoria.")
		sys.exit()

'''
Funcion que llena un espacio de memoria con un valor
'''
def fillValor(objMemVirt, memoryAddres, memoryType, value):
	global m_Global
	memoryType = str(memoryType)
	auxSection = getSection(memoryAddres)
	if auxSection == CONST_STRING_GLOBALES: #anadir el valor a globales
		m_Global.fillMemory(memoryAddres, memoryType, value)
	elif auxSection == CONST_STRING_LOCALES: #anadir el valor a locales
		objMemVirt.fillMemory(memoryAddres, memoryType, value)
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
		if auxBool == 'false': #si si evalua en falso, ir al quad que diga el [3]
			nextQuadIndex = int(quad[3])
	#Adding de Constantes a la memoria de global
	elif quad[0] == 'addConstant':
		#('addConstant', 'int', 0, 9001)
		#print("quiero poner: ",m_Global, quad[3], str(quad[1]), quad[2])
		fillValor(m_Global, quad[3], quad[1], quad[2])
	#Operadores aritmeticos
	elif quad[0] == '+':
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
		op1 = getValor(currentEjecucion, quad[1], getType(quad[1]))
		print("Jubi > {}".format(str(op1)))
	#FALTA HACER EL DE READ
	elif quad[0] == 'read':
		print('FALTA HACER EL DE READ')
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
