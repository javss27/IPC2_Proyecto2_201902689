from typing import List
from xml.dom import minidom
from TDAS import *
from clases import *
import os
class Logica:
    def __init__(self,ruta):
        self.mydoc = minidom.parse(ruta)
        self.terreno = self.mydoc.getElementsByTagName('listaCiudades')
        self.Lista_Mapas = Lista()
        self.Lista_Drones = Lista()
        self.arriba = 1
        self.abajo = 1
        self.derecha = 1
        self.izquierda = 1
        
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
        #    print(cont,end=" ")
            cont += 1
       # print()
        return lista
    
    def seleccion(self,tipo_mision,ciudad,robot,fila_entrada,columna_entrada,fila_destino,columna_destino):
        if tipo_mision == "ChapinRescue":
            if self.Lista_Mapas.buscar(ciudad,"civil") and self.Lista_Drones.buscar_tipo_robot(robot,tipo_mision) :
                print("aber el rescate")
                mapa = self.Lista_Mapas.getMapa(ciudad)
                # mapa.ver_cabeceras()
                if mapa.buscar_entrada(fila_entrada,columna_entrada) and mapa.buscar_salida(fila_destino,columna_destino,"civil"):
                    print("ya esta en la entrada pos fila: ",fila_entrada,"columa",columna_entrada)
                    mapa.setRecorrido(fila_entrada,columna_entrada,"P",0,fila_entrada,columna_entrada)
                    self.Camino(mapa,fila_entrada,columna_entrada,fila_destino,columna_destino)
                    mapa.ver_cabeceras()
                    self.busca_enlace(mapa)
                    mapa.ver_recorrido()
                else:
                    print("coordenadas errores o no es una entrada")
            else:
                print("Mision imposible, unidades civiles no existe o robot no cumple")
        else:
            if self.Lista_Mapas.buscar(ciudad,"recurso") and self.Lista_Drones.buscar_tipo_robot(robot,tipo_mision) :
                print("aber los recursos")
                mapa = self.Lista_Mapas.getMapa(ciudad)
                robot = self.Lista_Drones.getRobot(robot)
                if mapa.buscar_entrada(fila_entrada,columna_entrada) and mapa.buscar_salida(fila_destino,columna_destino,"recurso"):
                    print("ya esta en la entrada",fila_entrada,"columa",columna_entrada)
                    #mapa.setRecorrido(fila_entrada,columna_entrada,"P",0,fila_entrada,columna_entrada)
                    #mapa.ver_cabeceras()
                    print(robot.nombre)
                else:
                    print("coordenadas errores o no es una entrada")
            else:
                print("Mision imposible, unidades de recursos no existe o robot no cumple")
    
    def Camino(self,mapa,fila_entrada,columna_entrada,fila_destino,columna_destino):
        llegada = True
        while llegada:
            enter = input()
            mapa.ver_cabeceras()
            if fila_entrada==fila_destino and columna_entrada==columna_destino:
                print("llego")
                llegada = False
            else:
                for x in range(4):
                    print("aber el for")
                    self.Enlace(mapa,fila_entrada,columna_entrada)
                
                x = self.busca_enlace(mapa)
                try:
                    fila_entrada = x[0]
                    columna_entrada = x[1]
                except:
                    print("Al parecer no hay camino")
                    llegada = False

    def Enlace(self,mapa,fila,columna):
        fila_arriba = fila-1
        fila_abajo = fila+1
        colum_derecha = columna +1
        colum_izq = columna-1
        if(mapa.getEstado(fila_arriba,columna)=="transitable" or mapa.getEstado(fila_arriba,columna)=="civil") and mapa.getRecorrido(fila_arriba,columna)=="L":
            print("arriba")
            mapa.setRecorrido(fila_arriba,columna,"E",mapa.getDistancia(fila,columna),fila,columna)

        elif (mapa.getEstado(fila_abajo,columna)=="transitable" or mapa.getEstado(fila_abajo,columna)=="civil") and mapa.getRecorrido(fila_abajo,columna)=="L":    
            print("abajo")
            mapa.setRecorrido(fila_abajo,columna,"E",mapa.getDistancia(fila,columna),fila,columna)

        elif (mapa.getEstado(fila,colum_derecha)=="transitable" or mapa.getEstado(fila,colum_derecha)=="civil") and mapa.getRecorrido(fila,colum_derecha)=="L":    
            print("derecha",mapa.getDistancia(fila,columna))
            mapa.setRecorrido(fila,colum_derecha,"E",mapa.getDistancia(fila,columna),fila,columna)

        elif (mapa.getEstado(fila,colum_izq)=="transitable" or mapa.getEstado(fila,colum_izq)=="civil") and mapa.getRecorrido(fila,colum_izq)=="L":    
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
            print(temp.obj.num)
            temp2 = temp.obj.lista.cabeza
            while temp2 != None:
                if temp2.obj.recorrido == "E":
                    print(temp2.obj.recorrido,temp2.obj.pre_fila,temp2.obj.pre_columna)
                    print(temp.obj.num,temp2.obj.num)
                    #self.Camino(mapa,int(temp.obj.num),int(temp2.obj.num),1,5)
                    temp2.obj.recorrido = "P"
                    return int(temp.obj.num),int(temp2.obj.num)
                temp2 = temp2.siguiente
            temp = temp.siguiente
    
    def camino2(self,mapa,fila_entrada,columna_entrada,fila_destino,columna_destino):
        llegada = True
        while llegada:
            input()
            mapa.ver_cabeceras()
            if fila_entrada==fila_destino and columna_entrada==columna_destino:
                print("llego")
                llegada = False
            else:
                for x in range(4):
                    print("aber el for")
                    self.Enlace2(mapa,fila_entrada,columna_entrada)
                
                x = self.busca_enlace(mapa)
                try:
                    fila_entrada = x[0]
                    columna_entrada = x[1]
                except:
                    print("Al parecer no hay camino")
                    llegada = False
    
    def Enlace2(self,mapa,lista_militar,lista_robot,fila,columna):
        fila_arriba = fila-1
        fila_abajo = fila+1
        colum_derecha = columna +1
        colum_izq = columna-1
        if(mapa.getEstado(fila_arriba,columna)=="transitable" or mapa.getEstado(fila_arriba,columna)=="civil") and mapa.getRecorrido(fila_arriba,columna)=="L":
            print("arriba")
            #hay que ver si existe unidad militar
            #si existe hay que buscar al robot y ver como va en capacidad para validar si seguir o no
            #si no existe hay que siguir normal
            mapa.setRecorrido(fila_arriba,columna,"E",mapa.getDistancia(fila,columna),fila,columna)

        elif (mapa.getEstado(fila_abajo,columna)=="transitable" or mapa.getEstado(fila_abajo,columna)=="civil") and mapa.getRecorrido(fila_abajo,columna)=="L":    
            print("abajo")
            mapa.setRecorrido(fila_abajo,columna,"E",mapa.getDistancia(fila,columna),fila,columna)

        elif (mapa.getEstado(fila,colum_derecha)=="transitable" or mapa.getEstado(fila,colum_derecha)=="civil") and mapa.getRecorrido(fila,colum_derecha)=="L":    
            print("derecha",mapa.getDistancia(fila,columna))
            mapa.setRecorrido(fila,colum_derecha,"E",mapa.getDistancia(fila,columna),fila,columna)

        elif (mapa.getEstado(fila,colum_izq)=="transitable" or mapa.getEstado(fila,colum_izq)=="civil") and mapa.getRecorrido(fila,colum_izq)=="L":    
            print("izquierda")
            mapa.setRecorrido(fila,colum_izq,"E",mapa.getDistancia(fila,columna),fila,columna)
        else:
            print("Sin movimiento")#,mapa.getEstado(fila_arriba,columna),mapa.getEstado(fila_arriba,columna),mapa.getRecorrido(fila_arriba,columna))
            """print("Sin movimiento",mapa.getEstado(fila_abajo,columna),mapa.getEstado(fila_abajo,columna),mapa.getRecorrido(fila_abajo,columna))
            print("Sin movimiento",mapa.getEstado(fila,colum_derecha),mapa.getEstado(fila,colum_derecha),mapa.getRecorrido(fila,colum_derecha))
            print("Sin movimiento",mapa.getEstado(fila,colum_izq),mapa.getEstado(fila,colum_izq),mapa.getRecorrido(fila,colum_izq))"""

    
        
p = Logica('C:/Users/otrop/Desktop/Entrada0.xml')
p.readXML()
p.seleccion("ChapinFighter","CiudadGuate2","Robocop",3,1,1,1)
#p.Lista_Mapas.ver_mapas()
#p.Lista_Drones.ver_drones()
