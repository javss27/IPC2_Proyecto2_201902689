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

    def readXML(self):

        etiqueta_ciudad = self.terreno[0].getElementsByTagName('ciudad')
        print(len(etiqueta_ciudad))
        for x in range(len(etiqueta_ciudad)):                  
            etiqueta_nombre =etiqueta_ciudad[x].getElementsByTagName('nombre')
            filas = etiqueta_nombre[0].attributes['filas'].value
            columnas = etiqueta_nombre[0].attributes['columnas'].value
            nombre = etiqueta_nombre[0].firstChild.data
            print(filas,columnas,nombre)
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
            lista_cabecera.ver_cabeceras()

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
                lista_militar.ver_militar()
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
p = Logica('C:/Users/otrop/Desktop/Entrada0.xml')
p.readXML()
p.Lista_Mapas.ver_mapas()
p.Lista_Drones.ver_drones()
