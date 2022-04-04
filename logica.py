from typing import List
from xml.dom import minidom

from cv2 import COLORMAP_AUTUMN
from TDAS import *
from clases import *
import os
class Logica:
    def __init__(self,ruta):
        self.mydoc = minidom.parse(ruta)
        self.terreno = self.mydoc.getElementsByTagName('listaCiudades')
        self.Lista_Mapas = Lista()
        self.Lista_Drones = Lista()
        self.paso = True
        
    def readXML(self):
        etiqueta_ciudad = self.terreno[0].getElementsByTagName('ciudad')
        #print(len(etiqueta_ciudad))
        for x in range(len(etiqueta_ciudad)):                  
            etiqueta_nombre =etiqueta_ciudad[x].getElementsByTagName('nombre')
            filas = etiqueta_nombre[0].attributes['filas'].value
            columnas = etiqueta_nombre[0].attributes['columnas'].value
            nombre = etiqueta_nombre[0].firstChild.data
            #print(filas,columnas,nombre)
            """
            * - celda intransitable
              - celda transitable
            E - punto de entrada
            C - unidad civil
            R - unidad de Recurso
            """
            lista_cabecera = Lista()
            etiqueta_fila = etiqueta_ciudad[x].getElementsByTagName('fila')
            for i in range(len(etiqueta_fila)):
                #print(etiqueta_fila[i].attributes['numero'].value + "\t"+etiqueta_fila[i].firstChild.data)
                list = self.split_cadena(etiqueta_fila[i].firstChild.data)
                cabecera = Cabecera(etiqueta_fila[i].attributes['numero'].value,list)             
                lista_cabecera.add(cabecera)
            #lista_cabecera.ver_cabeceras()

            lista_militar = Lista()
            etiqueta_militar = etiqueta_ciudad[x].getElementsByTagName('unidadMilitar')
            #print(len(etiqueta_militar))
            if len(etiqueta_militar) == 0:
                print("Sin unidades militares")
            else:
                for i in range(len(etiqueta_militar)):
                    #print(etiqueta_militar[i].attributes['fila'].value, etiqueta_militar[i].attributes['columna'].value+ "\t"+etiqueta_militar[i].firstChild.data)
                    militar = Unidad_Militar(etiqueta_militar[i].attributes['fila'].value, etiqueta_militar[i].attributes['columna'].value,etiqueta_militar[i].firstChild.data)
                    lista_militar.add(militar)
                #lista_militar.ver_militar()
            ciudad = Mapa(nombre,filas,columnas,lista_cabecera,lista_militar)
            self.Lista_Mapas.add(ciudad)

        robots = self.mydoc.getElementsByTagName('robots')    
        etiqueta_robot = robots[0].getElementsByTagName('robot')
        #print(len(etiqueta_robot))  
        for x in range(len(etiqueta_robot)): 
            etiqueta_nombre =etiqueta_robot[x].getElementsByTagName('nombre')
            tipo = etiqueta_nombre[0].attributes['tipo'].value
            if tipo == "ChapinFighter":
                capacidad = etiqueta_nombre[0].attributes['capacidad'].value
                nombre = etiqueta_nombre[0].firstChild.data
                drone = Drone(nombre,"ChapinFighter",capacidad)
                self.Lista_Drones.add(drone)
               # print(capacidad,nombre)
            else:
                nombre = etiqueta_nombre[0].firstChild.data
                drone = Drone(nombre,"ChapinRescue",0)
                self.Lista_Drones.add(drone)
                #print(nombre)
    
    def split_cadena(self,cadena):
        lista = Lista()
        #print(cadena)
        cont = 1
        for caracter in cadena:
            #print(caracter)
            if caracter == "*":
                espacio = Espacio(cont,"intransitable")
                lista.add(espacio)
            elif caracter == " ":
                espacio = Espacio(cont,"transitable")
                lista.add(espacio)
            elif caracter == "E":
                espacio = Espacio(cont,"entrada")
                lista.add(espacio)
            elif caracter == "C":
                espacio = Espacio(cont,"civil")
                lista.add(espacio)
            elif caracter == "R":
                espacio = Espacio(cont,"recurso")
                lista.add(espacio)
            elif caracter == '"':
                continue
            cont += 1
        return lista
    
    def seleccion(self,tipo_mision,ciudad,robot,fila_entrada,columna_entrada,fila_destino,columna_destino):
        if tipo_mision == "ChapinRescue":
            if self.Lista_Mapas.buscar(ciudad,"civil") and self.Lista_Drones.buscar_tipo_robot(robot,tipo_mision) :
                #print("aber el rescate")
                mapa = self.Lista_Mapas.getMapa(ciudad)
                lista_militar2 = self.Lista_Mapas.getLista_Militar(ciudad)
                # mapa.ver_cabeceras()
                if mapa.buscar_entrada(fila_entrada,columna_entrada) and mapa.buscar_salida(fila_destino,columna_destino,"civil"):
                    print("ya esta en la entrada pos fila: ",fila_entrada,"columa",columna_entrada)
                    mapa.setRecorrido(fila_entrada,columna_entrada,"P",0,fila_entrada,columna_entrada)
                    self.Camino(mapa,lista_militar2,fila_entrada,columna_entrada,fila_destino,columna_destino)
                    mapa.ver_cabeceras()
                    self.busca_enlace(mapa)
                    mapa.ver_recorrido()
                    if self.paso:
                        self.camino_regreso(mapa,fila_entrada,columna_entrada,fila_destino,columna_destino)
                        self.graficar(mapa,lista_militar2)
                    else:
                        print("No se puede graficar")
                else:
                    print("Coordenadas erroroneas o no es una entrada")
            else:
                print("Mision imposible, unidades civiles no existe o robot no cumple")
        else:
            if self.Lista_Mapas.buscar(ciudad,"recurso") and self.Lista_Drones.buscar_tipo_robot(robot,tipo_mision) :
                print("aber los recursos")
                mapa = self.Lista_Mapas.getMapa(ciudad)
                robot = self.Lista_Drones.getRobot(robot)
                lista_militar = self.Lista_Mapas.getLista_Militar(ciudad)
                if mapa.buscar_entrada(fila_entrada,columna_entrada) and mapa.buscar_salida(fila_destino,columna_destino,"recurso"):
                    print("ya esta en la entrada",fila_entrada,"columa",columna_entrada)
                    mapa.setRecorrido(fila_entrada,columna_entrada,"P",0,fila_entrada,columna_entrada)
                    #lista_militar.ver_militar()
                    self.camino2(mapa,lista_militar,robot,fila_entrada,columna_entrada,fila_destino,columna_destino)
                    mapa.ver_recorrido()
                    print(robot.nombre)
                    self.graficar(mapa,lista_militar)
                    
                else:
                    print("Coordenadas erroroneas o no es una entrada")
            else:
                print("Mision imposible, unidades de recursos no existe o robot no cumple")
    
    def camino_regreso(self,mapa,fila1,columna1,fila2,columna2):
        mapa.ver_caminoRegreso()
        input()
        if fila1==fila2 and columna1==columna2:
            print("++++Recorrido de regreso completado+++")
        else:
            x = mapa.getCamino(fila2,columna2)
            try:
                #print(mapa.getCamino(fila2,columna2))
                #print("retornos",x[0],x[1]) 
                self.camino_regreso(mapa,fila1,columna1,x[0],x[1])
            except:
                print("-----------NO SE PUDO COMPLETAR EL CAMINO-------")
                self.paso = False

    def Camino(self,mapa,lista,fila_entrada,columna_entrada,fila_destino,columna_destino):
        llegada = True
        while llegada:
            enter = input()
            mapa.ver_cabeceras()
            if fila_entrada==fila_destino and columna_entrada==columna_destino:
                print("********RUTA ENCOTRADA*********")
                llegada = False
            else:
                for x in range(4):
                    #print("aber el for")
                    self.Enlace(mapa,lista,fila_entrada,columna_entrada)
                
                x = self.busca_enlace(mapa)
                try:
                    fila_entrada = x[0]
                    columna_entrada = x[1]
                except:
                    print("-------NO HAY CAMINO DISPONIBLE-------")
                    self.paso = False
                    llegada = False

    def Enlace(self,mapa,lista,fila,columna):
        fila_arriba = fila-1
        fila_abajo = fila+1
        colum_derecha = columna +1
        colum_izq = columna-1
        if(mapa.getEstado(fila_arriba,columna)=="transitable" or mapa.getEstado(fila_arriba,columna)=="civil") and (mapa.getRecorrido(fila_arriba,columna)=="L") and lista.getMilitar(fila_arriba,columna) != True:
            print("arriba")
            mapa.setRecorrido(fila_arriba,columna,"E",mapa.getDistancia(fila,columna),fila,columna)

        elif (mapa.getEstado(fila_abajo,columna)=="transitable" or mapa.getEstado(fila_abajo,columna)=="civil") and (mapa.getRecorrido(fila_abajo,columna)=="L") and lista.getMilitar(fila_abajo,columna) != True:    
            print("abajo")
            mapa.setRecorrido(fila_abajo,columna,"E",mapa.getDistancia(fila,columna),fila,columna)

        elif (mapa.getEstado(fila,colum_derecha)=="transitable" or mapa.getEstado(fila,colum_derecha)=="civil") and (mapa.getRecorrido(fila,colum_derecha)=="L") and lista.getMilitar(fila,colum_derecha) != True:    
            print("derecha")
            mapa.setRecorrido(fila,colum_derecha,"E",mapa.getDistancia(fila,columna),fila,columna)

        elif (mapa.getEstado(fila,colum_izq)=="transitable" or mapa.getEstado(fila,colum_izq)=="civil") and (mapa.getRecorrido(fila,colum_izq)=="L")and lista.getMilitar(fila,colum_izq) != True:    
            print("izquierda")
            mapa.setRecorrido(fila,colum_izq,"E",mapa.getDistancia(fila,columna),fila,columna)
        else:
            print("Sin movimiento")#,mapa.getEstado(fila_arriba,columna),mapa.getEstado(fila_arriba,columna),mapa.getRecorrido(fila_arriba,columna))
            """print("Sin movimiento",mapa.getEstado(fila_abajo,columna),mapa.getEstado(fila_abajo,columna),mapa.getRecorrido(fila_abajo,columna))
            print("Sin movimiento",mapa.getEstado(fila,colum_derecha),mapa.getEstado(fila,colum_derecha),mapa.getRecorrido(fila,colum_derecha))
            print("Sin movimiento",mapa.getEstado(fila,colum_izq),mapa.getEstado(fila,colum_izq),mapa.getRecorrido(fila,colum_izq))"""
    
    def busca_enlace(self,mapa):
        temp = mapa.cabeza
        while temp != None:
            #print(temp.obj.num)
            temp2 = temp.obj.lista.cabeza
            while temp2 != None:
                if temp2.obj.recorrido == "E":
                    #print(temp2.obj.recorrido,temp2.obj.pre_fila,temp2.obj.pre_columna)
                    #print(temp.obj.num,temp2.obj.num)
                    #self.Camino(mapa,int(temp.obj.num),int(temp2.obj.num),1,5)
                    temp2.obj.recorrido = "P"
                    return int(temp.obj.num),int(temp2.obj.num)
                temp2 = temp2.siguiente
            temp = temp.siguiente
    
    def camino2(self,mapa,lista_militar,robot,fila_entrada,columna_entrada,fila_destino,columna_destino):
        llegada = True
        while llegada:
            entrada = input()
            mapa.ver_cabeceras()
            if fila_entrada==fila_destino and columna_entrada==columna_destino:
                print("llego")
                llegada = False
            else:
                for x in range(4):
                    print("aber el for")
                    self.Enlace2(mapa,lista_militar,robot,fila_entrada,columna_entrada)
                
                x = self.busca_enlace(mapa)
                try:
                    fila_entrada = x[0]
                    columna_entrada = x[1]
                except:
                    print("Al parecer no hay camino")
                    llegada = False
    
    def Enlace2(self,mapa,lista_militar,robot,fila,columna):
        fila_arriba = fila-1
        fila_abajo = fila+1
        colum_derecha = columna +1
        colum_izq = columna-1
        if(mapa.getEstado(fila_arriba,columna)=="transitable" or mapa.getEstado(fila_arriba,columna)=="civil"or mapa.getEstado(fila_arriba,columna)=="recurso") and mapa.getRecorrido(fila_arriba,columna)=="L":
            print("arriba")
            #hay que ver si existe unidad militar
            if lista_militar.getMilitar(fila_arriba,columna) and int(robot.capacidad) >= 0:
                print("si hay unidad militar")
                print("cap unidad",lista_militar.getCapacidad(fila_arriba,columna)," cap robot",robot.capacidad)
                nuevaCapacidad = int(robot.capacidad)-lista_militar.getCapacidad(fila_arriba,columna)
                robot.capacidad = nuevaCapacidad
                print("nueva cap robt:",nuevaCapacidad)
                if nuevaCapacidad >= 0:
                    mapa.setRecorrido(fila_arriba,columna,"E",mapa.getDistancia(fila,columna),fila,columna)
                else:
                    print("El robot:",robot.nombre," no fue derrotado :(")
                
                #si existe hay que buscar al robot y ver como va en capacidad para validar si seguir o no
            else:
                if int(robot.capacidad) < 0:
                    print("El robot ya no puede seguir")
                else:
                    print("no hay unidad militar")
                    #si no existe hay que siguir normal
                    mapa.setRecorrido(fila_arriba,columna,"E",mapa.getDistancia(fila,columna),fila,columna)

        elif (mapa.getEstado(fila_abajo,columna)=="transitable" or mapa.getEstado(fila_abajo,columna)=="civil" or mapa.getEstado(fila_abajo,columna)=="recurso") and mapa.getRecorrido(fila_abajo,columna)=="L":    
            print("abajo")
            #hay que ver si existe unidad militar
            if lista_militar.getMilitar(fila_abajo,columna) and int(robot.capacidad) >= 0:
                print("si hay unidad militar")
                #si existe hay que buscar al robot y ver como va en capacidad para validar si seguir o no
                print("cap unidad",lista_militar.getCapacidad(fila,colum_derecha)," cap robot",robot.capacidad)
                nuevaCapacidad = int(robot.capacidad)-lista_militar.getCapacidad(fila_abajo,columna)
                robot.capacidad = nuevaCapacidad
                print("nueva cap robt:",nuevaCapacidad)
                if nuevaCapacidad >= 0:
                    mapa.setRecorrido(fila_abajo,columna,"E",mapa.getDistancia(fila,columna),fila,columna)
                else:
                    print("El robot:",robot.nombre," no fue derrotado :(")
            else:
                print("no si hay unidad militar")
                #si no existe hay que siguir normal
                if int(robot.capacidad) < 0:
                    print("El robot ya no puede seguir")
                else:
                    print("no hay unidad militar")
                    #si no existe hay que siguir normal
                    mapa.setRecorrido(fila_abajo,columna,"E",mapa.getDistancia(fila,columna),fila,columna)

        elif (mapa.getEstado(fila,colum_derecha)=="transitable" or mapa.getEstado(fila,colum_derecha)=="civil"or mapa.getEstado(fila,colum_derecha)=="recurso") and mapa.getRecorrido(fila,colum_derecha)=="L":    
            print("derecha",mapa.getDistancia(fila,columna))
            #hay que ver si existe unidad militar
            if lista_militar.getMilitar(fila,colum_derecha) and int(robot.capacidad) >= 0:
                print("si hay unidad militar")
                print("cap unidad",lista_militar.getCapacidad(fila,colum_derecha)," cap robot",robot.capacidad)
                nuevaCapacidad = int(robot.capacidad)-lista_militar.getCapacidad(fila,colum_derecha)
                robot.capacidad = nuevaCapacidad
                print("nueva cap robt:",nuevaCapacidad)
                if nuevaCapacidad >= 0:
                    mapa.setRecorrido(fila,colum_derecha,"E",mapa.getDistancia(fila,columna),fila,columna)
                else:
                    print("El robot:",robot.nombre," no fue derrotado :(")
                #si existe hay que buscar al robot y ver como va en capacidad para validar si seguir o no
            else:
                if int(robot.capacidad) < 0:
                    print("El robot ya no puede seguir")
                else:
                    print("no hay unidad militar")
                    #si no existe hay que siguir normal
                
                    #si no existe hay que siguir normal
                    mapa.setRecorrido(fila,colum_derecha,"E",mapa.getDistancia(fila,columna),fila,columna)

        elif (mapa.getEstado(fila,colum_izq)=="transitable" or mapa.getEstado(fila,colum_izq)=="civil" or mapa.getEstado(fila,colum_izq)=="recurso") and mapa.getRecorrido(fila,colum_izq)=="L":    
            print("izquierda")
            #hay que ver si existe unidad militar
            if lista_militar.getMilitar(fila,colum_izq) and int(robot.capacidad) >= 0:
                print("si hay unidad militar")
                #si existe hay que buscar al robot y ver como va en capacidad para validar si seguir o no
                print("cap unidad",lista_militar.getCapacidad(fila,colum_derecha)," cap robot",robot.capacidad)
                nuevaCapacidad = int(robot.capacidad)-lista_militar.getCapacidad(fila,colum_izq)
                robot.capacidad = nuevaCapacidad
                print("nueva cap robt:",nuevaCapacidad)
                if nuevaCapacidad >= 0:
                    mapa.setRecorrido(fila,colum_izq,"E",mapa.getDistancia(fila,columna),fila,columna)
                else:
                    print("El robot:",robot.nombre," no fue derrotado :(")
            else:
        
                if int(robot.capacidad) < 0:
                    print("El robot ya no puede seguir")
                else:
                    print("no hay unidad militar")
                    #si no existe hay que siguir normal
                #si no existe hay que siguir normal
                    mapa.setRecorrido(fila,colum_izq,"E",mapa.getDistancia(fila,columna),fila,columna)
        else:
            print("Sin movimiento")#,mapa.getEstado(fila_arriba,columna),mapa.getEstado(fila_arriba,columna),mapa.getRecorrido(fila_arriba,columna))
            """print("Sin movimiento",mapa.getEstado(fila_abajo,columna),mapa.getEstado(fila_abajo,columna),mapa.getRecorrido(fila_abajo,columna))
            print("Sin movimiento",mapa.getEstado(fila,colum_derecha),mapa.getEstado(fila,colum_derecha),mapa.getRecorrido(fila,colum_derecha))
            print("Sin movimiento",mapa.getEstado(fila,colum_izq),mapa.getEstado(fila,colum_izq),mapa.getRecorrido(fila,colum_izq))"""

    def graficar(self,mapa,militar):
        nombre = "nameXD"
        cadena = "digraph Matriz{ \n"; 
        cadena += "node[shape = box,width=0.95,height=0.95,fillcolor=\"azure2\" color=\"white\" style=\"filled\"];\n"
        cadena += "edge[style = \"bold\"]; \n"
        #cadena+="node[label = "+ nombre +" fillcolor=\" darkolivegreen1\" pos = \"-1,1!\"]principal;\n"

        """ ESTO FUNCIONA PERO NO SE NECESITA
        #grafica cabeceras y(filas)
        temp = mapa.cabeza
        while temp != None:
            print(temp.obj.num)
            cadena+="node[label = "+temp.obj.num+" fillcolor=\" azure1\" pos = \"-1,-"+temp.obj.num+"!\"]y"+temp.obj.num+";\n"
            temp = temp.siguiente
        
        #grafica flechitas
        temp = mapa.cabeza
        while temp.siguiente != None:
            #print("acutal:",temp.obj.num,"siguiente:",aux.obj.num)
            cadena+="y"+temp.obj.num+"->"+"y"+temp.siguiente.obj.num+";\n"
            temp = temp.siguiente
        cadena += "principal->y1\n"
        """

        #nodos internos
        temp = mapa.cabeza
        while temp != None:
            #declarando nodos internos
            temp2 = temp.obj.lista.cabeza
            while temp2 != None:
                if temp2.obj.estado == "intransitable":
                    cadena +="   node[label = "+str(temp2.obj.num)+" fillcolor=\" black\" pos = \""+str(temp2.obj.num)+",-"+str(temp.obj.num)+"!\"]x"+str(temp.obj.num)+"y"+str(temp2.obj.num)+";\n"
                elif temp2.obj.estado == "entrada":
                    cadena +="   node[label = "+str(temp2.obj.num)+" fillcolor=\" forestgreen\" pos = \""+str(temp2.obj.num)+",-"+str(temp.obj.num)+"!\"]x"+str(temp.obj.num)+"y"+str(temp2.obj.num)+";\n"
                elif temp2.obj.estado == "recurso":
                    cadena +="   node[label = "+str(temp2.obj.num)+" fillcolor=\" gray55\" pos = \""+str(temp2.obj.num)+",-"+str(temp.obj.num)+"!\"]x"+str(temp.obj.num)+"y"+str(temp2.obj.num)+";\n"
                elif temp2.obj.estado =="civil":
                    cadena +="   node[label = "+str(temp2.obj.num)+" fillcolor=\" blue2\" pos = \""+str(temp2.obj.num)+",-"+str(temp.obj.num)+"!\"]x"+str(temp.obj.num)+"y"+str(temp2.obj.num)+";\n"
                elif (temp2.obj.estado == "transitable") and militar.getMilitar(int(temp.obj.num),int(temp2.obj.num)):
                    cadena +="   node[label = "+str(temp2.obj.num)+" fillcolor=\" red\" pos = \""+str(temp2.obj.num)+",-"+str(temp.obj.num)+"!\"]x"+str(temp.obj.num)+"y"+str(temp2.obj.num)+";\n"
                else:
                    if (temp2.obj.estado == "transitable") and (temp2.obj.camino == "V"):
                        cadena +="   node[label = "+str(temp2.obj.num)+" fillcolor=\" gold\" pos = \""+str(temp2.obj.num)+",-"+str(temp.obj.num)+"!\"]x"+str(temp.obj.num)+"y"+str(temp2.obj.num)+";\n"
                    else:
                        cadena +="   node[label = "+str(temp2.obj.num)+" fillcolor=\" gray95\" pos = \""+str(temp2.obj.num)+",-"+str(temp.obj.num)+"!\"]x"+str(temp.obj.num)+"y"+str(temp2.obj.num)+";\n"

                temp2 = temp2.siguiente
            """
            #graficar flechas
            temp2 = temp.obj.lista.cabeza
            while temp2.siguiente != None:
                cadena +="   x"+str(temp.obj.num)+"y"+str(temp2.obj.num)+"->x"+str(temp.obj.num)+"y"+str(temp2.siguiente.obj.num)+";\n"
                temp2 = temp2.siguiente
            #cabezas apuntan a notods    
            temp2 = temp.obj.lista.cabeza
            if temp.obj.lista.cabeza != None:
                cadena+="y"+str(temp.obj.num)+"->"+"x"+str(temp.obj.num)+"y"+str(temp2.obj.num)+";\n"
            """
            cadena += "\n"
            temp = temp.siguiente

        cadena+= "\n}"
        print(cadena)
 #hacer un recorrido que comience desde las unidades militares para ver si llega al rescate 
 # si llega retonrar una matriz 
 # si no llega no retornar nada o retornar la matriz en la forma que se quedo
 # para todo esto ir tomando la capacidad del robot   
        
p = Logica('C:/Users/otrop/Desktop/Entrada0.xml')
p.readXML()
p.seleccion("ChapinRescue","CiudadGuate2","Ironman",3,1,1,5)
#p.Lista_Mapas.ver_mapas()
#p.Lista_Drones.ver_drones()
