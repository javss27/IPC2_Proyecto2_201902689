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
        print("aber")  
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
                print(temp.obj.num, end=" ")
                #print(temp.obj.estado, "\t", end=" ")
                temp = temp.siguiente
        print()
    
    def buscar(self,nombre,unidad):
        if self.cabeza == None:
            print("ta vacio")
            return False
        else:        
            temp = self.cabeza
            while temp != None:
                print(temp.obj.nombre)
                if (temp.obj.nombre == nombre) and self.buscar_unidad(temp.obj.lista.cabeza,unidad):
                    print("ciudad: ",nombre,unidad)
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
                print(temp.obj.num,"\t",end="")
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
                print(temp.obj.num, end=" ")
                if temp.obj.estado == unidad:
                    print("aber el estado",unidad)
                    return True
                temp = temp.siguiente
        return False

    def buscar_entrada(self,fila,columna):
        print("aber buscar_entrada")  
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
        print("aber buscar_entrada2")
        if temporal == None:
            print("ta vacio")
            return False
        else:        
            temp = temporal
            while temp != None:
                #print(temp.obj.num, end=" ")
                if (int(temp.obj.num) == columna) and (temp.obj.estado == "entrada"):
                    print("aber si entro")
                    return True
                temp = temp.siguiente
        return False
    def ver_militar(self):    
        print("aber")  
        if self.cabeza == None:
            print("ta vacio")
        else:        
            temp = self.cabeza
            while temp != None:
                print(temp.obj.fila ,temp.obj.columna,temp.obj.capacidad)
                temp = temp.siguiente

    def buscar_salida(self,fila,columna,unidad):
        print("aber buscar_salida")  
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
        print("aber buscar_salida2")
        if temporal == None:
            print("ta vacio")
            return False
        else:        
            temp = temporal
            while temp != None:
                #print(temp.obj.num, end=" ")
                if unidad == "civil":
                    if (int(temp.obj.num) == columna) and (temp.obj.estado == "civil"):
                        print("aber si entro civil")
                        return True
                else:
                    if (int(temp.obj.num) == columna) and (temp.obj.estado == "recurso"):
                        print("aber si entro recurso")
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
                    print(temp.obj.nombre,temp.obj.tipo )
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
                    print(temp.obj.nombre)
                    return temp.obj.lista
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
