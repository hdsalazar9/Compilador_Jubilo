from Jubilo_LexPar import *

obejota = open('')
quadList = [] #almacena cuadruplos despues de lectura de obejota

'''
Funcion que regresa el tipo de dato encontrado en el cuadruplo segun la direccion de memoria
'''
def getTipo(address):
	tipo = 'none'
	address = int(address)
	return tipo

'''
Funcion que regresa el valor del dato encontrado en el cuadruplo segun la direccion de memoria
'''
def getValor(current, tipo, address):
	valor = 0
	return valor


'''
Funcion principal de la maquina virtual
Ejecuta los cuadruplos que lee del archivo obejota : codigo objeto
'''
def ejecucion():
	global quad
	global retorno


	'''
	Receta de cocina para leer cuadruplo: 
	1. Obtiene los tipos de datos de los dos operandos
	2. Obtiene el valor de los dos operandos
	3. Condicionales para los datos validos, convierte el operador al tipo de dato que es
	4. hace la operacion del cuadruplo
	'''
	if quad[0] == '+':
		tipo1 = getTipo(quad[1])
		tipo2 = getTipo(quad[2])
		op1 = getValor(memoria, tipo1, quad[1])
		op2 = getValor(memoria, tipo2, quad[2])

		if tipo1 == 'int':
			op1 = int(op1)
		if tipo2 == 'int':
			op2 = int(op2)
		if tipo1 == 'float':
			op1 = float(op1)
		if tipo2 == 'float':
			op2 = float(op2)
		res = op1 + op2

	if quad[0] == '-':
		tipo1 = getTipo(quad[1])
		tipo2 = getTipo(quad[2])
		op1 = getValor(memoria, tipo1, quad[1])
		op2 = getValor(memoria, tipo2, quad[2])

		if tipo1 == 'int':
			op1 = int(op1)
		if tipo2 == 'int':
			op2 = int(op2)
		if tipo1 == 'float':
			op1 = float(op1)
		if tipo2 == 'float':
			op2 = float(op2)
		res = op1 - op2

	if quad[0] == '*':
		tipo1 = getTipo(quad[1])
		tipo2 = getTipo(quad[2])
		op1 = getValor(memoria, tipo1, quad[1])
		op2 = getValor(memoria, tipo2, quad[2])

		if tipo1 == 'int':
			op1 = int(op1)
		if tipo2 == 'int':
			op2 = int(op2)
		if tipo1 == 'float':
			op1 = float(op1)
		if tipo2 == 'float':
			op2 = float(op2)
		res = op1 * op2

	if quad[0] == '/':
		tipo1 = getTipo(quad[1])
		tipo2 = getTipo(quad[2])
		op1 = getValor(memoria, tipo1, quad[1])
		op2 = getValor(memoria, tipo2, quad[2])

		if tipo1 == 'int':
			op1 = int(op1)
		if tipo2 == 'int':
			op2 = int(op2)
		if tipo1 == 'float':
			op1 = float(op1)
		if tipo2 == 'float':
			op2 = float(op2)
		res = op1 / op2

	if quad[0] == '=':
		auxValor = 0
		try:
			auxTipo = getTipo(quad[1])
			int(quad[1])
			auxValor = getValor(memoria, auxTipo, quad[1])
		except: 
			auxTipo = getTipo(quad[3])
			auxValor = retorno.pop()

	if quad[0] == '<'
		tipo1 = getTipo(quad[1])
		tipo2 = getTipo(quad[2])
		op1 = getValor(memoria, tipo1, quad[1])
		op2 = getValor(memoria, tipo2, quad[2])

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

	if quad[0] == '>'
		tipo1 = getTipo(quad[1])
		tipo2 = getTipo(quad[2])
		op1 = getValor(memoria, tipo1, quad[1])
		op2 = getValor(memoria, tipo2, quad[2])

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

	if quad[0] == '<='
		tipo1 = getTipo(quad[1])
		tipo2 = getTipo(quad[2])
		op1 = getValor(memoria, tipo1, quad[1])
		op2 = getValor(memoria, tipo2, quad[2])

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

	if quad[0] == '>='
		tipo1 = getTipo(quad[1])
		tipo2 = getTipo(quad[2])
		op1 = getValor(memoria, tipo1, quad[1])
		op2 = getValor(memoria, tipo2, quad[2])

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

	if quad[0] == '=='
		tipo1 = getTipo(quad[1])
		tipo2 = getTipo(quad[2])
		op1 = getValor(memoria, tipo1, quad[1])
		op2 = getValor(memoria, tipo2, quad[2])

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

	if quad[0] == '!='
		tipo1 = getTipo(quad[1])
		tipo2 = getTipo(quad[2])
		op1 = getValor(memoria, tipo1, quad[1])
		op2 = getValor(memoria, tipo2, quad[2])

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

	if quad[0] == '||':
		tipo1 = getTipo(quad[1])
		tipo2 = getTipo(quad[2])
		op1 = getValor(memoria, tipo1, quad[1])
		op2 = getValor(memoria, tipo2, quad[2])
		if op1 == op2 and op1 == False and op2 == False:
			res = False
		else:
			res = True

	if quad[0] == '&&':
		tipo1 = getTipo(quad[1])
		tipo2 = getTipo(quad[2])
		op1 = getValor(memoria, tipo1, quad[1])
		op2 = getValor(memoria, tipo2, quad[2])
		if op1 == op2 and op1 == True:
			res = True
		else:
			res = False

'''
Lee el archivo obejota. EJEMPLO (+,a,b,t1) -> +,a,b,t1
line : string del archivo obejota
python replace syntax -> string.replace('old substring', 'new substring')
python split syntax -> string.split('separator')
'''
for line in obejota:
	line = line.replace('(','')
	line = line.replace(')','')
	quad = tuple(line.split(','))
	auxQuad = (1,1,1,1)
	try:
		auxQuad[0] = int(float(quad[0]))
	except:
		pass
	try:
		auxQuad[1] = int(float(quad[1]))
	except:
		pass
	try: 
		auxQuad[2] = int(float(quad[2]))
	except:
		pass
	try:
		auxQuad[3] = int(float(quad[3]))
	except:
		pass
	quad = (quad[0], quad[1], quad[2], quad[3])
	quadList.append(quad)

ejecucion() #llamada a funcion para ejecutar cuadruplo por cuadruplo generado despues de lectura de obejota
