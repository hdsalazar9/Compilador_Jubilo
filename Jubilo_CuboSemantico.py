#Héctor David Salazar Schz, A01207471.
#Melanie Vielma Saldana, A00818905.
#Diseno de compiladores Ago-Dic 2019. ITESM.
#Jubilo - CUBO SEMANTICO (Semantica basica)
#15/10/2019

class Jubilo_CuboSemantico:
    def __init__(self):
        '''
        Este diccionario establece todas las combinaciones posibles entre
        dos operandos para todos los tipos de datos manejados por Jubilo
        (int, float, bool) en la forma ->

        (operando1, operando2, operador) : tipo de operando resultado
        '''
        self.diccionario = {
            ( 'int' , 'int' , '+' ) :'int',
            ( 'int' , 'int' , '-' ) : 'int',
            ( 'int' , 'int' , '*' ) : 'int',
            ( 'int' , 'int' , '/' ) : 'float',
            ( 'int' , 'int' , '=' ) : 'int',
            ( 'int' , 'int' , '==' ) : 'bool',
            ( 'int' , 'int' , '<' ) : 'bool',
            ( 'int' , 'int' , '>' ) : 'bool',
            ( 'int' , 'int' , '<=' ) : 'bool',
            ( 'int' , 'int' , '>=' ) : 'bool',
            ( 'int' , 'int' , '!=' ) : 'bool',
            ( 'int' , 'int' , '||' ) : 'error',
            ( 'int' , 'int' , '&&' ) : 'error',

            ( 'int' , 'float' , '+' ) : 'float',
            ( 'int' , 'float' , '-' ) : 'float',
            ( 'int' , 'float' , '*' ) : 'float',
            ( 'int' , 'float' , '/' ) : 'float',
            ( 'int' , 'float' , '=' ) : 'int', #Cuando se asigna a una variable int, un flotante se redondea a int
            ( 'int' , 'float' , '==' ) : 'bool',
            ( 'int' , 'float' , '<' ) : 'bool',
            ( 'int' , 'float' , '>' ) : 'bool',
            ( 'int' , 'float' , '<=' ) : 'bool',
            ( 'int' , 'float' , '>=' ) : 'bool',
            ( 'int' , 'float' , '!=' ) : 'bool',
            ( 'int' , 'float' , '||' ) : 'error',
            ( 'int' , 'float' , '&&' ) : 'error',

            ( 'int' , 'bool' , '+' ) : 'error',
            ( 'int' , 'bool' , '-' ) : 'error',
            ( 'int' , 'bool' , '*' ) : 'error',
            ( 'int' , 'bool' , '/' ) : 'error',
            ( 'int' , 'bool' , '=' ) : 'error',
            ( 'int' , 'bool' , '==' ) : 'error',
            ( 'int' , 'bool' , '<' ) : 'error',
            ( 'int' , 'bool' , '>' ) : 'error',
            ( 'int' , 'bool' , '<=' ) : 'error',
            ( 'int' , 'bool' , '>=' ) : 'error',
            ( 'int' , 'bool' , '!=' ) : 'error',
            ( 'int' , 'bool' , '||' ) : 'error',
            ( 'int' , 'bool' , '&&' ) : 'error',

            ( 'float' , 'int' , '+' ) : 'float',
            ( 'float' , 'int' , '-' ) : 'float',
            ( 'float' , 'int' , '*' ) : 'float',
            ( 'float' , 'int' , '/' ) : 'float',
            ( 'float' , 'int' , '=' ) : 'float',
            ( 'float' , 'int' , '==' ) : 'bool',
            ( 'float' , 'int' , '<' ) : 'bool',
            ( 'float' , 'int' , '>' ) : 'bool',
            ( 'float' , 'int' , '<=' ) : 'bool',
            ( 'float' , 'int' , '>=' ) : 'bool',
            ( 'float' , 'int' , '!=' ) : 'bool',
            ( 'float' , 'int' , '||' ) : 'error',
            ( 'float' , 'int' , '&&' ) : 'error',

            ( 'float' , 'float' , '+' ) : 'float',
            ( 'float' , 'float' , '-' ) : 'float',
            ( 'float' , 'float' , '*' ) : 'float',
            ( 'float' , 'float' , '/' ) : 'float',
            ( 'float' , 'float' , '=' ) : 'float',
            ( 'float' , 'float' , '==' ) : 'bool',
            ( 'float' , 'float' , '<' ) : 'bool',
            ( 'float' , 'float' , '>' ) : 'bool',
            ( 'float' , 'float' , '<=' ) : 'bool',
            ( 'float' , 'float' , '>=' ) : 'bool',
            ( 'float' , 'float' , '!=' ) : 'bool',
            ( 'float' , 'float' , '||' ) : 'error',
            ( 'float' , 'float' , '&&' ) : 'error',

            ( 'float' , 'bool' , '+' ) : 'error',
            ( 'float' , 'bool' , '-' ) : 'error',
            ( 'float' , 'bool' , '*' ) : 'error',
            ( 'float' , 'bool' , '/' ) : 'error',
            ( 'float' , 'bool' , '=' ) : 'error',
            ( 'float' , 'bool' , '==' ) : 'error',
            ( 'float' , 'bool' , '<' ) : 'error',
            ( 'float' , 'bool' , '>' ) : 'error',
            ( 'float' , 'bool' , '<=' ) : 'error',
            ( 'float' , 'bool' , '>=' ) : 'error',
            ( 'float' , 'bool' , '!=' ) : 'error',
            ( 'float' , 'bool' , '||' ) : 'error',
            ( 'float' , 'bool' , '&&' ) : 'error',

            ( 'bool' , 'int' , '+' ) : 'error',
            ( 'bool' , 'int' , '-' ) : 'error',
            ( 'bool' , 'int' , '*' ) : 'error',
            ( 'bool' , 'int' , '/' ) : 'error',
            ( 'bool' , 'int' , '=' ) : 'error',
            ( 'bool' , 'int' , '==' ) : 'error',
            ( 'bool' , 'int' , '<' ) : 'error',
            ( 'bool' , 'int' , '>' ) : 'error',
            ( 'bool' , 'int' , '<=' ) : 'error',
            ( 'bool' , 'int' , '>=' ) : 'error',
            ( 'bool' , 'int' , '!=' ) : 'error',
            ( 'bool' , 'int' , '||' ) : 'error',
            ( 'bool' , 'int' , '&&' ) : 'error',

            ( 'bool' , 'float' , '+' ) : 'error',
            ( 'bool' , 'float' , '-' ) : 'error',
            ( 'bool' , 'float' , '*' ) : 'error',
            ( 'bool' , 'float' , '/' ) : 'error',
            ( 'bool' , 'float' , '=' ) : 'error',
            ( 'bool' , 'float' , '==' ) : 'error',
            ( 'bool' , 'float' , '<' ) : 'error',
            ( 'bool' , 'float' , '>' ) : 'error',
            ( 'bool' , 'float' , '<=' ) : 'error',
            ( 'bool' , 'float' , '>=' ) : 'error',
            ( 'bool' , 'float' , '!=' ) : 'error',
            ( 'bool' , 'float' , '||' ) : 'error',
            ( 'bool' , 'float' , '&&' ) : 'error',

            ( 'bool' , 'bool' , '+' ) : 'error',
            ( 'bool' , 'bool' , '-' ) : 'error',
            ( 'bool' , 'bool' , '*' ) : 'error',
            ( 'bool' , 'bool' , '/' ) : 'error',
            ( 'bool' , 'bool' , '=' ) : 'bool',
            ( 'bool' , 'bool' , '==' ) : 'bool',
            ( 'bool' , 'bool' , '<' ) : 'bool',
            ( 'bool' , 'bool' , '>' ) : 'bool',
            ( 'bool' , 'bool' , '<=' ) : 'bool',
            ( 'bool' , 'bool' , '>=' ) : 'bool',
            ( 'bool' , 'bool' , '!=' ) : 'bool',
            ( 'bool' , 'bool' , '||' ) : 'bool',
            ( 'bool' , 'bool' , '&&' ) : 'bool',

            ('read', 'int', '') : 'string',
            ('read', 'float', '') : 'string',
            ('read', 'bool', '') : 'string',
            ('read', 'string', '') : 'error',

            ('print', 'int', '') : 'string',
            ('print', 'float', '') : 'string',
            ('print', 'bool', '') : 'string',
            ('print', 'string', '') : 'string'

        }

    '''
    Funcion de obtencion de tipo de valor resultado de la operacion
    (operator) entre los operandos operando1 y operando2
    '''
    def get_tipo(self, operando1, operando2, operator):
        return self.diccionario[operando1, operando2, operator]
