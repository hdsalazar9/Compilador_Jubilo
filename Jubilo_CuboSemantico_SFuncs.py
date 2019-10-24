#Héctor David Salazar Schz, A01207471.
#Melanie Vielma Saldana, A00818905.
#Diseno de compiladores Ago-Dic 2019. ITESM.
#Jubilo - CUBO SEMANTICO (Semantica de funciones especiales)
#15/10/2019

class Jubilo_CuboSemantico_SFuncs:
    def __init__(self):
        '''
        Este diccionario establece todas las combinaciones posibles entre
        las funciones especiales y sus posibles operandos de parametro para todos
        los tipos de datos manejados por Jubilo (int, float, bool, char) en la forma ->

        (special_funcion, operando1, operando2) : tipo de operando resultado
        '''
        self.diccionario = {
            ( 'arrange' , 'int' , 'int' ) :'int',
            ( 'zeros' , 'int' , '' ) :'int',
            ( 'ones' , 'int' , '' ) : 'int',
            ( 'sum' , 'int' , '' ) : 'int',
            ( 'sum' , 'float' , '' ) : 'float',
            ( 'fact' , 'int' , '' ) : 'int',

            ( 'mean' , 'int' , '' ) : 'float',
            ( 'mean' , 'float' , '' ) : 'float',
            ( 'median' , 'int' , '' ) : 'float',
            ( 'median' , 'float' , '' ) : 'float',
            ( 'mode' , 'int' , '' ) : 'int',
            ( 'mode' , 'float' , '' ) : 'float',
            ( 'stdev' , 'int' , '' ) : 'float',
            ( 'stdev' , 'float' , '' ) : 'float',
            ( 'var' , 'int' , '' ) : 'float',
            ( 'var' , 'float' , '' ) : 'float',

            ( 'covariance' , 'int' , 'int' ) : 'float',
            ( 'covariance' , 'int' , 'float' ) : 'float',
            ( 'covariance' , 'float' , 'float') : 'float',
            ( 'covariance' , 'float' , 'int') : 'float',

            ( 'var' , 'float' , '' ) : 'float',
            ( 'var' , 'int' , '' ) : 'float',

            ( 'correlation' , 'int' , 'int' ) : 'float',
            ( 'correlation' , 'int' , 'float' ) : 'float',
            ( 'correlation' , 'float' , 'float') : 'float',
            ( 'correlation' , 'float' , 'int') : 'float',

            ( 'sort' , 'int' , '' ) : 'int',
            ( 'sort' , 'float' , '' ) : 'float',
            ( 'sort' , 'char' , '' ) : 'char',

            ( 'transpose' , 'int' , '' ) : 'int',
            ( 'transpose' , 'float', '') : 'float',

            ( 'readcsv' , 'string' , 'int' ) : 'int',
            ( 'readcsv' , 'string' , 'float' ) : 'float',
            ( 'readcsv' , 'string' , 'string' ) : 'string',
            ( 'readcsv' , 'string' , 'char' ) : 'char',

            ( 'exportcsv' , 'string' , 'int' ) : 'bool',
            ( 'exportcsv' , 'string' , 'float' ) : 'bool',
            ( 'exportcsv' , 'string' , 'string' ) : 'bool',
            ( 'exportcsv' , 'string' , 'char' ) : 'bool',

            ( 'plothist' , 'int', '' ) : 'histogram',
            ( 'plothist' , 'float', '') : 'histogram',

            ( 'plotline' , 'int' , 'int' ) : 'line',
            ( 'plotline' , 'int' , 'float' ) : 'line',
            ( 'plotline' , 'float' , 'float' ) : 'line',
            ( 'plotline' , 'float' , 'int' ) : 'line',

            #Se puede regresar vacio? Pregunta para mi yo del futuro. v
            #Tas bien guapo we. Para Hector del futuro cuando este triste
            ('exchange', 'int', 'int'): '',
            ('exchange', 'string', 'string'): '',
            ('exchange', 'float', 'float'): '',
            ('exchange', 'char', 'char'): '',

            ( 'lineareg' , 'int' , 'int' ) : 'float',
            ( 'lineareg' , 'int' , 'float' ) : 'float',
            ( 'lineareg' , 'float' , 'float' ) : 'float',
            ( 'lineareg' , 'float' , 'int' ) : 'float',


            #Para las funciones de random se considera que se validara que
            #ambos rangos vengan y se manden como enteros, antes de mandar a
            #validar si son tipos de datos validos. Es decir revisar que ambos
            #limites sean o enteros o flotantes.
            #Al igual para el numero de renglones y columnas en las matrices:
            #se validara que ambos vengan enteros antes de validar que el tipo
            #de dato se puede ingresar en la funcion especial.

            ( 'randint' , 'int' , 'int' ) : 'int', #1er int son limites, 2do int es cant de randoms
            ( 'randint' , 'int' , '' ) : 'int',
            ( 'randfloat' , 'float' , 'int' ) : 'float', #1er float son limites, 2do int es cant de randoms
            ( 'randfloat' , 'float' , '' ) : 'float',
            ( 'randintmat' , 'int' , 'int' ) : 'int', #1er int son limites, 2do int es cant de rows/columns
            ( 'randfloatmat' , 'float' , 'int' ) : 'float' #1er float son limites, 2do int es cant de rows/columns
        }

        '''
        Funcion de obtencion de tipo de valor resultado de la funcion especial
        con los tipos de valor pasados como parametro
        '''
        def get_tipo(self, spfunc, operando1, operando2):
            try:
                resultado = self.diccionario[spfunc, operando1, operando1]
            except:
                resultado = 'error'
            return resultado
