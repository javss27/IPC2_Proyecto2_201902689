from turtle import distance
from clases import*
class Nodo:
    def __init__(self, siguiente = None, obj = None):
        self.obj = obj
        self.siguiente = siguiente

class Lista:
    def __init__(self):
        self.cabeza = None

    def add(self, obj):
        nuevo = Nodo(None, obj)
        if self.cabeza == None:
            self.cabeza = nuevo
            
        else: 
            temp = self.cabeza           
            while temp.siguiente != None:              
                temp = temp.siguiente
            temp.siguiente = nuevo  


    def ver_cabeceras(self):    
        #print("aber")  
        if self.cabeza == None:
            print("ta vacio")
        else:        
            temp = self.cabeza
            while temp != None:
                print(temp.obj.num,"\t",end="")
                self.ver2(temp.obj.lista.cabeza)
                temp = temp.siguiente

    def ver2(self, temporal): 
        if temporal == None:
            print("ta vacio")
        else:        
            temp = temporal
            while temp != None:
                print(temp.obj.recorrido, end=" ")
                #print(temp.obj.estado, "\t", end=" ")
                temp = temp.siguiente
        print()

    def ver_recorrido(self):
        temp = self.cabeza
        while temp != None:
            print(temp.obj.num,"\t",end="")
            temp2 = temp.obj.lista.cabeza
            while temp2 != None:
                print(temp2.obj.pre_fila,temp2.obj.pre_columna, end="   ")
                #print(temp.obj.estado, "\t", end=" ")
                temp2 = temp2.siguiente
            print()
            temp = temp.siguiente


    def ver_caminoRegreso(self):
        if self.cabeza == None:
            print("sin camino")
        else:
            temp = self.cabeza
            while temp != None:
                print(temp.obj.num,"\t",end="")
                temp2 = temp.obj.lista.cabeza
                while temp2 != None:
                    #print(temp2.obj.pre_fila,temp2.obj.pre_columna, end="   ")
                    print(temp2.obj.camino, "  ", end=" ")
                    temp2 = temp2.siguiente
                print()
                temp = temp.siguiente

    def buscar(self,nombre,unidad):
        if self.cabeza == None:
            print("ta vacio")
            return False
        else:        
            temp = self.cabeza
            while temp != None:
                #print(temp.obj.nombre)
                if (temp.obj.nombre == nombre) and self.buscar_unidad(temp.obj.lista.cabeza,unidad):
                    #print("ciudad: ",nombre,unidad)
                    return True
                temp = temp.siguiente
        print("ciudad ",nombre,"no encontrada")
        return False 

    def buscar_unidad(self,temporal,unidad):
        if temporal== None:
            print("ta vacio")
            return False
        else:        
            temp = temporal
            while temp != None:
                #print(temp.obj.num,"\t",end="")
                if self.buscar_unidad2(temp.obj.lista.cabeza,unidad):
                    return True
                temp = temp.siguiente
        return False

    def buscar_unidad2(self, temporal,unidad): 
        if temporal == None:
            print("ta vacio")
            return False
        else:        
            temp = temporal
            while temp != None:
                #print(temp.obj.num, end=" ")
                if temp.obj.estado == unidad:
                    #print("aber el estado",unidad)
                    return True
                temp = temp.siguiente
        return False

    def buscar_entrada(self,fila,columna):
        #print("aber buscar_entrada")  
        if self.cabeza == None:
            print("ta vacio")
            return False
        else:        
            temp = self.cabeza
            while temp != None:
                #print(temp.obj.num,"\t",end="")
                if (int(temp.obj.num) == fila) and self.buscar_entrada2(temp.obj.lista.cabeza,columna):
                    return True
                temp = temp.siguiente
        return False

    def buscar_entrada2(self,temporal,columna):
        #print("aber buscar_entrada2")
        if temporal == None:
            print("ta vacio")
            return False
        else:        
            temp = temporal
            while temp != None:
                #print(temp.obj.num, end=" ")
                if (int(temp.obj.num) == columna) and (temp.obj.estado == "entrada"):
                    #print("aber si entro")
                    return True
                temp = temp.siguiente
        return False


    def ver_militar(self):    
        print("Lista de unidades militares")  
        if self.cabeza == None:
            print("ta vacio")
        else:        
            temp = self.cabeza
            while temp != None:
                print("fila:",temp.obj.fila ,"columa:",temp.obj.columna,temp.obj.capacidad)
                temp = temp.siguiente

    def buscar_salida(self,fila,columna,unidad):
        #print("aber buscar_salida")  
        if self.cabeza == None:
            print("ta vacio")
            return False
        else:        
            temp = self.cabeza
            while temp != None:
                #print(temp.obj.num,"\t",end="")
                if (int(temp.obj.num) == fila) and self.buscar_salida2(temp.obj.lista.cabeza,columna,unidad):
                    return True
                temp = temp.siguiente
        return False

    def buscar_salida2(self,temporal,columna,unidad):
        #print("aber buscar_salida2")
        if temporal == None:
            print("ta vacio")
            return False
        else:        
            temp = temporal
            while temp != None:
                #print(temp.obj.num, end=" ")
                if unidad == "civil":
                    if (int(temp.obj.num) == columna) and (temp.obj.estado == "civil"):
                        #print("aber si entro civil")
                        return True
                else:
                    if (int(temp.obj.num) == columna) and (temp.obj.estado == "recurso"):
                        #print("aber si entro recurso")
                        return True
                temp = temp.siguiente
        return False
    def ver_drones(self):
        if self.cabeza == None:
                print("ta vacio")
        else:        
            temp = self.cabeza
            while temp != None:
                print(temp.obj.nombre )
                temp = temp.siguiente

    def buscar_tipo_robot(self,nombre,tipo):
        if self.cabeza == None:
            print("ta vacio")
            return False
        else:        
            temp = self.cabeza
            while temp != None:
                if temp.obj.tipo == tipo and temp.obj.nombre == nombre :
                    #print(temp.obj.nombre,temp.obj.tipo )
                    return True
                temp = temp.siguiente
        print(nombre,"no encontrado o no es del tipo correcto")
        return False
    
    def ver_mapas(self):
        if self.cabeza == None:
            print("ta vacio")
        else:        
            temp = self.cabeza
            while temp != None:
                print(temp.obj.nombre)
                temp = temp.siguiente

    def getMapa(self,ciudad):
        if self.cabeza == None:
            print("ta vacio")
        else:        
            temp = self.cabeza
            while temp != None:
                if temp.obj.nombre == ciudad:
                    #print(temp.obj.nombre)
                    return temp.obj.lista
                temp = temp.siguiente

    def getLista_Militar(self,ciudad):
        if self.cabeza == None:
            print("ta vacio")
        else:        
            temp = self.cabeza
            while temp != None:
                if temp.obj.nombre == ciudad:
                    #print(temp.obj.nombre)
                    return temp.obj.lista2
                temp = temp.siguiente

    def getRobot(self,robot):
        if self.cabeza == None:
            print("ta vacio")
        else:        
            temp = self.cabeza
            while temp != None:
                if temp.obj.nombre == robot:
                    print(temp.obj.nombre)
                    return temp.obj
                temp = temp.siguiente

    def getEspacio(self,fila,columna):
        if self.cabeza == None:
            print("ta vacio")
        else:        
            temp = self.cabeza
            while temp != None:
                if int(temp.obj.num) == fila:
                    
                    return self.getEspacio2(temp.obj.lista.cabeza,columna)
                temp = temp.siguiente
        return False
    def getEspacio2(self,temporal,columna):
        if temporal == None:
            print("vacio")
            return False
        else:
            temp = temporal
            while temp != None:
                if int(temp.obj.num) == columna:
                    print("aber el tru")
                    return True
                temp = temp.siguiente
        print("aber el false")
        return False


    def setRecorrido(self,fila,columna,recorrido,distancia,f2,c2):        
        temp = self.cabeza
        while temp != None:
            if int(temp.obj.num) == fila:
                self.setRecorrido2(temp.obj.lista.cabeza,columna,recorrido,distancia,f2,c2)
            temp = temp.siguiente
    def setRecorrido2(self,temporal,columna,recorrido,distancia,f2,c2):
        temp = temporal
        while temp != None:
            if int(temp.obj.num) == columna:
                temp.obj.recorrido = recorrido
                temp.obj.distancia_acumulada += distancia
                temp.obj.pre_fila = f2
                temp.obj.pre_columna = c2
                #print(temp.obj.distancia_acumulada)
            temp = temp.siguiente


    def setEnlace(self,fila,columna):        
        temp = self.cabeza
        while temp != None:
            if int(temp.obj.num) == fila:
                self.setEnlace2(temp.obj.lista.cabeza,columna)
            temp = temp.siguiente
    def setEnlace2(self,temporal,columna):
        temp = temporal
        while temp != None:
            if int(temp.obj.num) == columna:
                temp.obj.recorrido = "E"
            temp = temp.siguiente
       

    def getEstado(self,fila,columna):
        temp = self.cabeza
        while temp != None:
            if int(temp.obj.num) == fila:
                estado = self.getEstado2(temp.obj.lista.cabeza,columna)
                return estado
            temp = temp.siguiente
        return "diferente"
    def getEstado2(self,temporal,columna):
        temp = temporal
        while temp != None:
            if int(temp.obj.num) == columna:
                #print(temp.obj.estado)
                return temp.obj.estado
            temp = temp.siguiente
        return "diferente"
    

    def getRecorrido(self,fila,columna):
        temp = self.cabeza
        while temp != None:
            if int(temp.obj.num) == fila:
                return self.getRecorrido2(temp.obj.lista.cabeza,columna)
            temp = temp.siguiente
        return "diferente"    
    def getRecorrido2(self,temporal,columna):
        temp = temporal
        while temp != None:
            if int(temp.obj.num) == columna:
                #print(temp.obj.estado)
                return temp.obj.recorrido
            temp = temp.siguiente
        return "diferente"


    def getDistancia(self,fila,columna):
        temp = self.cabeza
        while temp != None:
            if int(temp.obj.num) == fila:
                return self.getDistancia2(temp.obj.lista.cabeza,columna)
            temp = temp.siguiente
    def getDistancia2(self,temporal,columna):
        temp = temporal
        while temp != None:
            if int(temp.obj.num) == columna:
                return temp.obj.distancia_acumulada
            temp = temp.siguiente

  
    def getMilitar(self,fila,columna):
        if  self.cabeza == None:
            print("vacio")
            return False
        else:
            temp = self.cabeza
            while temp != None:
                if int(temp.obj.fila) == fila and int(temp.obj.columna)== columna:
                    return True
                temp = temp.siguiente
        return False

    def getCapacidad(self,fila,columna):
        if  self.cabeza == None:
                print("vacio")
                return False
        else:
            temp = self.cabeza
            while temp != None:
                if int(temp.obj.fila) == fila and int(temp.obj.columna)== columna:
                    return int(temp.obj.capacidad)
                temp = temp.siguiente
        return False

    def getCamino(self,fila,columna):
        #print("fila")
        if self.cabeza == None:
            print("vacio")
        else:
            temp = self.cabeza
            while temp != None:
                #print("fila")
                if int(temp.obj.num) == fila:
                    temp2 = temp.obj.lista.cabeza
                    while temp2 != None:
                        #print("columna")
                        if int(temp2.obj.num)==columna:
                            temp2.obj.camino = "V"
                            print("Estado Camino")
                            return int(temp2.obj.pre_fila), int(temp2.obj.pre_columna)
                        temp2 = temp2.siguiente
                temp = temp.siguiente

    def borrar(self, nodo):
        if nodo == self.cabeza:
            self.cabeza = nodo.siguiente

        else:
            temp = self.cabeza
            anterior = temp
            while temp != None:
                if nodo == temp:
                    anterior.siguiente = nodo.siguiente
                anterior = temp
                temp = temp.siguiente
