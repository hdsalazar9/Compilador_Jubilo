#Héctor David Salazar Schz, A01207471.
#Melanie Vielma Saldana, A00818905.
#Diseno de compiladores Ago-Dic 2019. ITESM.
#Jubilo - Directorio de Funciones
#21/10/2019
import sys
#Importar objeto para guardar las tablas de variables
from Jubilo_TablaVars import *

class Jubilo_DirFunc:
    def __init__(self):
        '''
        Diccionario de directorio de Funciones
        diccionario = {nombre: tipo}
        nombre : nombre de la funcion que se va a guardar
        tipo : tipo de la funcion que se va a guardar
        variable : 
        '''
        self.diccionario = {} #inicializa el diccionario de funciones

    def add_function(self, nombre, tipo):
        if (nombre in self.diccionario.keys()):
            print("Error: Funcion ", str(nombre), " ya definida.\n")
            #TODO: Maybe ocupa un return.
        else:
            self.diccionario[nombre] = {

            }




    def addFunc(self, nombre, tipo, quadCount):
        """ Adjunta la funcion especificada al Directorio de Funciones
            Args:
             nombre : Nombre de la funcion a aniadir.
             tipo   : Tipo de dato que le pertenece a la funcion.
             quadCount : Cantidad de cuádruplos generados hasta el momento.
        """
        if (nombre in DirFunc.instance.val):
            print('Function {} previously defined.'.format(nombre))
            sys.exit()
        else:
            DirFunc.instance.val[nombre] = (tipo, {}, 0, quadCount)
