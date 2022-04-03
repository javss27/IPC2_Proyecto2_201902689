class Drone:
    def __init__(self,nombre, tipo,capacidad):
        self.nombre = nombre
        self.tipo = tipo
        self.capacidad = capacidad
        
class Mapa:
    def __init__(self, nombre, filas,colum, lista,lista2):
        self.nombre = nombre
        self.filas = filas
        self.colum = colum
        self. lista = lista
        self. lista2 = lista2

class Cabecera:
    def __init__(self,num,lista):
        self.num = num
        self.lista = lista

class Espacio:
    def __init__(self,num,estado):
        self.num = num
        self.estado = estado
        self.recorrido = "L"#puede sder P, E o L
        self.distancia_acumulada = 1
        self.pre_fila = 0
        self.pre_columna = 0
        self.camino = "F"

class Unidad_Militar:
    def __init__(self,fila,columna,capacidad):
        self.fila=fila
        self.columna = columna
        self.capacidad = capacidad
