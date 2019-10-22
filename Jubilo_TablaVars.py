#Héctor David Salazar Schz, A01207471.
#Melanie Vielma Saldana, A00818905.
#Diseno de compiladores Ago-Dic 2019. ITESM.
#Jubilo - Objeto que es una Tabla de variables
#21/10/2019

class Jubilo_TablaVars:

    def __init__(self):
        '''
        Tabla del objeto tabla de variables
        tabla = {nombre: tipo}
        nombre : nombre de la variable a guardar
        tipo : tipo de la variable a guardar
        renglones : Numero de renglones si es variable dimensionada
        columnas : Numero de columnas si es variable dimensionada
         ~ TODO: Esto ocupa mas cosas, creo
        '''
        self.diccionario = {} #Inicializa la tabla de variables

    '''
    Funcion para agregar variable al diccionario.
    ~ TODO: documentacion
    '''
    def add_var(self, nombre, tipo, renglones, columnas):
        #Si el nombre de la variable en este scope ya esta definida
        #desplegar error
        if (nombre in self.diccionario.keys()):
            print("Error: Variable ", str(nombre), " ya definida.\n")
            #TODO: Maybe ocupa un return
        else:
            self.diccionario[nombre] = {
                'nombre' : nombre,
                'tipo' : tipo,
                'renglones' : renglones,
                'columnas' : columnas
            }

    '''
    Funcion para saber si existe un nombre de variable en el diccionario.
    ~ TODO:
    '''
    def exist_var(self, nombre):
        return nombre in self.diccionario.keys()

    '''
    Funcion que busca y regresa una variable y sus datos, del diccionario.
    ~ TODO:
    '''
    def search_var(self, nombre):
        if self.exist_var(nombre):
            return self.diccionario[nombre]
        else:
            return None
