from logica import *
from tkinter.filedialog import askopenfilename

def menu():
    global ciudades
    fin = True
    while fin:
        print("\n1.  Cargar Archivo    \n2. Ingresar datos \n3. Salir \n")
        opc = input("Ingrese el número de la opción: ")
        if opc == "1":   
            print("Seleccione un archivo.")                      
            try:
                ruta = askopenfilename()
            except: 
                print("Seleccione un archivo.")

            #archivo = open(ruta, 'r')
            #ruta = archivo.read()
            try:
                ciudades = Logica(ruta)
                ciudades.readXML()
            except:
                print("Error en el ingreso de ruta")
        elif opc == "2":
            print()
            ciudades.Lista_Mapas.ver_mapas()
            print("")
            ciudades.Lista_Drones.ver_drones()

            print("Ingrese el nombre de la ciudad: ",end=" ")
            name = input()
            print("Ingrese nombre de robot: ",end="")
            nombre_robot = input()
            print("Ingrese tipo de Robot",end=" ")
            tipo= input()
            print("Ingrese el numero de la fila de entrada: ",end=" ")
            fila_entrada = input()
            print("Ingrese el numero de la columna de entrada: ",end="")
            columna_entrada = input()
            print("Ingrese el numero de la fila destino",end=" ")
            fila_destino= input()
            print("Ingrese el numero de la columna destino",end=" ")
            colmuna_destino= input()
            try:    
                ciudades.seleccion(tipo,name,nombre_robot,int(fila_entrada),int(columna_entrada),int(fila_destino),int(colmuna_destino))
            except:
                    print("Error en el ingreso de datos")
        
        elif opc == "3":
            print("Saliendo....")
            fin = False
            
        else:
            print("\n \nNúmero inválido, vuelva a intentar. \n")

menu()