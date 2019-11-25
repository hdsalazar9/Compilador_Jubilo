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
        los tipos de datos manejados por Jubilo (int, float, bool) en la forma ->

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

            ( 'correlation' , 'int' , 'int' ) : 'float',
            ( 'correlation' , 'int' , 'float' ) : 'float',
            ( 'correlation' , 'float' , 'float') : 'float',
            ( 'correlation' , 'float' , 'int') : 'float',

            ( 'sort' , 'int' , '' ) : 'int',
            ( 'sort' , 'float' , '' ) : 'float',

            ( 'transpose' , 'int' , '' ) : 'int',
            ( 'transpose' , 'float', '') : 'float',

            ( 'exportcsv' , 'string' , 'string' ) : 'bool',

            ( 'plothist' , 'int', 'int' ) : 'histogram',
            ( 'plothist' , 'float', 'float') : 'histogram',

            ( 'plotline' , 'int' , 'int' ) : 'line',
            ( 'plotline' , 'int' , 'float' ) : 'line',
            ( 'plotline' , 'float' , 'float' ) : 'line',
            ( 'plotline' , 'float' , 'int' ) : 'line',

            #Se puede regresar vacio? Pregunta para mi yo del futuro. v
            #Tas bien guapo we. Para Hector del futuro cuando este triste
            ('exchange', 'int', 'int'): 'int',
            ('exchange', 'bool', 'bool'): 'bool',
            ('exchange', 'float', 'float'): 'float',

            ( 'lineareg' , 'int' , 'int' ) : 'float',
            ( 'lineareg' , 'int' , 'float' ) : 'float',
            ( 'lineareg' , 'float' , 'float' ) : 'float',
            ( 'lineareg' , 'float' , 'int' ) : 'float',


            #Para las funciones de random se considera que se validara que
            #ambos rangos vengan y se manden como enteros, antes de mandar a
            #validar si son tipos de datos validos. Es decir revisar que ambos
            #limites sean o enteros o flotantes.

            ( 'randint' , 'int' , 'int' ) : 'int', #1er int son limites, 2do int es cant de randoms
            ( 'randfloat' , 'float' , 'int' ) : 'float' #1er float son limites, 2do int es cant de randoms
        }

    '''
    Funcion de obtencion de tipo de valor resultado de la funcion especial
    con los tipos de valor pasados como parametro
    '''
    def get_tipo(self, spfunc, operando1, operando2):
        try:
            resultado = self.diccionario[spfunc, operando1, operando2]
        except:
            resultado = 'error'
        return resultado
