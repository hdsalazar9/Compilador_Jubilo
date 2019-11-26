#Hector David Salazar Schz, A01207471.
#Melanie Vielma Saldana, A00818905.
#Diseno de compiladores Ago-Dic 2019. ITESM.
#Jubilo
import sys

#Objeto de memoria que guardara los indices de cada instancia de memoria
#Cada funcion genera una instancia de memoria
#Globals cuenta como la primera instancia de memoria
class MemoriaVirtual:
    def __init__(self, nombreFunc):
        '''
        Diccionario de las direcciones de memoria para la funcion actual
        diccionario = {'int': {}, 'float' : {}, 'bool' : {}}
        '''
        self.diccionario = { 'int' : {}, 'float' : {}, 'bool' : {}}
        self.nombre = nombreFunc

    '''
    Funcion para rellenar un espacio de memoria(memory) con el valor (value)
    en el diccionario de tipo (type) en la funcion actual
    '''
    def fillMemory(self, memory, type, value):
        self.diccionario[type][memory] = value
    '''
    Funcion para retornar el valor de un espacio de memoria(memory) de una
    variable de tipo (type)
    '''
    def getValueFromMemory(self, memory, type):
        try:
            toReturn = self.diccionario[type][memory]
            return toReturn
        except:
            print("Error. Ese espacio de memoria no existe en la funcion:{}.".format(self.nombre))
            raise #Elevar el error para que lo pueda checar en Maq Virt

    '''
    Desplegar el diccionario y su contenido
    '''
    def print():
        print("Memoria virtual de {}: \n".format(self.nombre))
        print(self.diccionario)
