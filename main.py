from logica import *
def menu():
    global ciudades
    fin = True
    while fin:
        print("\n1.  Cargar Archivo    \n2. Ingresar datos \n3. Salir \n")
        opc = input("Ingrese el número de la opción: ")
        if opc == "1":   
            print("Ingrese la ruta del archivo.")                      
            ruta = input()
            ciudades = Logica(ruta)
            ciudades.readXML()
        elif opc == "2":
            print()
            ciudades.Lista_Mapas.ver_mapas()
            print("")
            ciudades.Lista_Drones.ver_drones()

            print("Ingrese el nombre de la ciudad: ",end=" ")
            name = input()
            print("Ingrese nombre de robot: ",end="")
            nombre_robot = input()
            print("Ingrese tipo de misión",end=" ")
            tipo= input()
            print("Ingrese el numero de la fila de entrada: ",end=" ")
            fila_entrada = input()
            print("Ingrese el numero de la columna de entrada: ",end="")
            columna_entrada = input()
            print("Ingrese el numero de la fila destino",end=" ")
            fila_destino= input()
            print("Ingrese el numero de la columna destino",end=" ")
            colmuna_destino= input()
            ciudades.seleccion(tipo,name,nombre_robot,int(fila_entrada),int(columna_entrada),int(fila_destino),int(colmuna_destino))
        elif opc == "3":
            print("pa juera")
            fin = False
            
        else:
            print("\n \nNúmero inválido, vuelva a intentar. \n")

menu()