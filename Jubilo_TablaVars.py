#Héctor David Salazar Schz, A01207471.
#Melanie Vielma Saldana, A00818905.
#Diseno de compiladores Ago-Dic 2019. ITESM.
#Jubilo - Objeto que es una Tabla de variables
#21/10/2019

class Jubilo_TablaVars:

    def __init__(self):
        '''
        Tabla del objeto tabla de variables
        diccionario = {nombre: nombre, tipo, renglones, columnas}
        nombre : nombre de la variable a guardar
        tipo : tipo de la variable a guardar
        renglones : Numero de renglones si es variable dimensionada
        columnas : Numero de columnas si es variable dimensionada
        memPos : Posicion de memoria donde reside la variable
        '''
        self.diccionario = {} #Inicializa la tabla de variables

    '''
    Funcion para saber si existe un nombre de variable en el diccionario.
    '''
    def exist_var(self, nombre):
        return nombre in self.diccionario.keys()

    '''
    Funcion para agregar variable al diccionario.
    Regresa true si pudo crear la variable o false si no pudo crearla.
    '''
    def add_var(self, nombre, tipo, renglones, columnas, memPos):
        #Si el nombre de la variable en esta funcion ya esta definida
        #desplegar error
        if self.exist_var(nombre):
            print("Error: Variable ", str(nombre), " ya definida.\n")
            return False
            #TODO: Maybe ocupa un return
        else:
            self.diccionario[nombre] = {
                'nombre' : nombre,
                'tipo' : tipo,
                'renglones' : renglones,
                'columnas' : columnas,
                'memPos' : memPos
            }
            return True

    '''
    Funcion para actualizar renglones y columnas de una variable previamente creada
    '''
    def update_varDimensions(self, nombre, renglones, columnas):
        #Si ya existe la variable actualizar su numero de renglones y columnas
        if self.exist_var(nombre):
            if columnas < 0: #Se quiere actualizar renglones
                self.diccionario[nombre]['renglones'] = renglones
            else:
                self.diccionario[nombre]['columnas'] = columnas
        #Si no existe desplegar error
        else:
            print("Error. Imposible actualizar dimensiones de una variale no existente: ", nombre)
        print("Variable: ", nombre, "Renglones actualizados: ", self.diccionario[nombre]['renglones'], "Columnas actualizadas: ", self.diccionario[nombre]['columnas'])

    '''
    Funcion que busca y regresa una variable y sus datos, del diccionario.
    '''
    def search_var(self, nombre):
        if self.exist_var(nombre):
            return self.diccionario[nombre]
        else:
            return None

    '''
    Funcion que busca y regresa el tipo de una variable, del diccionario.
    '''
    def search_varType(self, nombre):
        if self.exist_var(nombre):
            return self.diccionario[nombre]['tipo']
        else:
            return None

    '''
    Funcion que busca y regresa la posicion de memoria de una variable
    '''
    def search_memPos(self, nombre):
        if self.exist_var(nombre):
            return self.diccionario[nombre]['memPos']
        else:
            return None
