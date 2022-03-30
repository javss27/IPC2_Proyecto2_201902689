
def menu():
    fin = True
    while fin:
        print("\n1.  Cargar Archivo    \n2.  Ingresar datos \n3.  Escribir archivo de salida  \n4.  Generar grafica \n5.  Salir \n")
        opc = input("Ingrese el número de la opcioón: ")
        if opc == "1":   
            print("Ingrese la ruta del archivo.")                      
        elif opc == "2":
            print("Ingrese el nombre de la ciudad")
            name = input()
        elif opc == "3":  
            print("Generando xml")
        elif opc == "4":   
             print("Generar graficas")
        elif opc == "5":
            print("pa juera")
            fin = False
            
        else:
            print("\n \nNúmero inválido, vuelva a intentar. \n")

menu()