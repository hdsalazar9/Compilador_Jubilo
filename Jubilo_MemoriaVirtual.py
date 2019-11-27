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
        diccionario = {'int': {}, 'float' : {}, 'bool' : {}, 'string':{}}
        '''
        self.diccionario = { 'int' : {}, 'float' : {}, 'bool' : {'12000':True,'12001':False}, 'string' : {}}
        self.nombre = nombreFunc

    '''
    Funcion para rellenar un espacio de memoria(memory) con el valor (value)
    en el diccionario de tipo (type) en la funcion actual
    '''
    def fillMemory(self, memory, type, value):
        self.diccionario[str(type)][str(memory)] = value
        #self.printMV()

    '''
    Funcion para retornar el valor de un espacio de memoria(memory) de una
    variable de tipo (type)
    '''
    def getValueFromMemory(self, memory, type):
        try:
            #self.printMV()
            #print("Se quiere hacer get de: ,{}, y ,{}, y valor ,{},".format(type,memory, self.diccionario[str(type)][str(memory)]))
            toReturn = self.diccionario[str(type)][str(memory)]
            #print("Se hizo get de: ,{}, y ,{}, y valor ,{},{}".format(type,memory, toReturn),type(toReturn))
            return toReturn
        except:
            print("Unexpected error:", sys.exc_info()[0])
            print("Error. El espacio de memoria {} no existe en la funcion:{}.".format(memory, self.nombre))
            raise #Elevar el error para que lo pueda checar en Maq Virt

    '''
    Desplegar el diccionario y su contenido
    '''
    def printMV(self):
        print("Memoria virtual de {}: \n".format(self.nombre))
        print(self.diccionario)
