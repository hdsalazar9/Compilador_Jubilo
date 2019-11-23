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
        diccionario = {nombre: nombre, tipo, cantParametros, variables}
        nombre : nombre de la funcion que se va a guardar
        tipo : tipo de la funcion que se va a guardar
        cantParametros : Cantidad de parametros para la funcion definida
        variables : objeto de tipo Jubilo_TablaVars para guardar las variables
        quadCont : Contador actual de cuadruplos
        '''
        #inicializa el diccionario de funciones con globals, funcion auxiliar para las variables globales
        self.diccionario = {'globals': {'nombre' : 'globals', 'tipo' : 'void', 'cantParametros' : 0, 'variables' : Jubilo_TablaVars(), 'quadCont' : 0}}
        print("Funcion creada: globals de tipo void")

    '''
    Funcion para saber si existe una funcion en el diccionario.
    ~ TODO:
    '''
    def exist_function(self, nombre):
        return nombre in self.diccionario.keys()

    '''
    Funcion que busca y regresa una funcion y sus datos, del diccionaro.
    ~ TODO:
    '''
    def search_function(self, nombre):
        if self.exist_function(nombre):
            return self.diccionario[nombre]
        else:
            return None

    '''
    Funcion para agregar una nueva funcion al Diccionario
    ~TODO:
    '''
    def add_function(self, nombre, tipo, cantParametros, quadCont):
        #Revisar que no se haya definido ya una funcion con el mismo nombre
        if self.exist_function(nombre):
            print("Error: Funcion ", str(nombre), " ya definida.\n")
            #TODO: Maybe ocupa un return.
        else:
            #Si no existe, crear la funcion con sus respectivos valores
            self.diccionario[nombre] = {
                'nombre' : nombre,
                'tipo': tipo,
                'cantParametros' : cantParametros,
                'variables' : Jubilo_TablaVars(),
                'quadCont' : quadCont
            }
            print("Funcion creada: ", nombre, " de tipo: ", tipo, " con cantParametros: ", cantParametros)

    '''
    Funcion para actualizar el numero de parametros de una funcion previamente creada
    '''
    def update_functionParams(self, nombre, cantParametros):
        #Si ya existe la funcion actualizar su cantidad  de parametros directamente
        if self.exist_function(nombre):
            self.diccionario[nombre]['cantParametros'] = cantParametros

        #Si no existe desplegar error
        else:
            print("Error: Imposible actualizar parametros de una funcion no existente: ", nombre)

        #print("Funcion creada: ", nombre, " de tipo: ", self.diccionario[nombre]['tipo'], " con cantParametros: ", cantParametros)

    '''
    Funcion que intenta agregar una variable a la funcion nombre
    ~ TODO:
    '''
    def add_varToFunction(self, nombre, nombreVar, tipoVar, renglonesVar, columnasVar):
        '''
        Dentro de mi diccionario de funciones, ir a la funcion nombre
        En su atributo variables e intentar agregar la nueva variable.
        Si regresa verdadero se pudo crear, si regresa falso ya existia esa variable.
        '''
        if self.diccionario[nombre]['variables'].add_var(nombreVar, tipoVar, renglonesVar, columnasVar):
            print("Variable: ", nombreVar, " creada en la funcion: ", nombre)
        else:
            print("Error: No es posible crear variable: ", nombreVar, ", en la funcion: ", nombre)
        print(self.diccionario[nombre]['variables'].diccionario)

    '''
    Funcion que regresa el string del tipo de una variable previamente creada en las funciones
    ~TODO:
    '''
    def search_varType(self, nombre, nombreVar):
        if self.diccionario[nombre]['variables'].exist_var(nombreVar):
            return self.diccionario[nombre]['variables'].search_varType(nombreVar)
        else:
            print("Warning: Variable: ", nombreVar ," no existe en este contexto: ", nombre)
            return None

    '''
    Pone en forma de lista los tipos encontrados en Jubilo_TablaVars
    '''
    def listTypes(self, function):
        return [ self.diccionario[function]['variables'].diccionario[x] ['tipo'] for x in self.diccionario[function]['variables'].diccionario]

    '''
    Funcion que regresa si existe una variable en la tabla de variables de la funcion dada
    '''
    def exist_var(self, nombre, nombreVar):
        if self.diccionario[nombre]['variables'].exist_var(nombreVar):
            return True;
        else:
            return False;
