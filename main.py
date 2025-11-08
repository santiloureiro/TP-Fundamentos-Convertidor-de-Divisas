# Cosas a agregar: Registro o log de usuarios y feedback, interfaz grafica, programa para visualizar el feedback y uso de los usuarios 
from InquirerPy import inquirer
import requests
import csv
from tabulate import tabulate
from pathlib import Path

# * FUNCIONES PARA LISTA DE USUARIOS

# Crea el archivo CSV de usuarios
def inicializarListaUsuarios(infoUsuario,archivo):
    ENCABEZADOSCSV = [['Nombre', 'Moneda', 'CantidadArs', 'CantidadConvertida','Fecha'], infoUsuario]
    with open(archivo, 'w', newline='') as archivoUsuarios:
        escritorCsv = csv.writer(archivoUsuarios)
        escritorCsv.writerows(ENCABEZADOSCSV)

# Añade info al archivo CSV de usuarios
def añadirUsuario(infoUsuario, archivo):
    with open(archivo, 'a', newline='') as archivoUsuarios:
        escritorCsv = csv.writer(archivoUsuarios,lineterminator="\n")
        escritorCsv.writerow(infoUsuario)

# * FUNCIONES PARA EL COTIZADOR

# Arma los menues de seleccion
def elegirOperacion(titulo,items):
    return inquirer.select(message = titulo, choices = items).execute()

# Peticion a url 
def conseguirValoresDesdeAPI(url):
    solicitudDatos = requests.get(url)
    return solicitudDatos.json()

def obtenerListaDeCSV(archivo):
    listaObtenida = []
    with open(archivo, 'r', newline='') as archivoUsuarios:
        lectorCsv = csv.reader(archivoUsuarios)
        for fila in lectorCsv:
            listaObtenida.append(fila)
    return(listaObtenida)

def conseguirMayorCotizacion(listaDeUsuarios):
    mayorUsuario = listaDeUsuarios[0]
    for usuario in listaDeUsuarios:
        if(int(usuario[2]) > int(mayorUsuario[2])):
            mayorUsuario = usuario
    return(mayorUsuario)

def obtenerListaSinTitulos(lista):
    listaLimpia = []
    for i in range(len(lista) - 1):
        i = i + 1
        listaLimpia.append(lista[i])
    return(listaLimpia)

# Modifica la url base para pedir diferentes informacion a la api
def armarUrl(url, moneda):
    urlModificada = url
    if moneda == "Pesos Chilenos":
        urlModificada = urlModificada + "cotizaciones/clp"
    elif moneda == "Real Brasilero":
        urlModificada = urlModificada + "cotizaciones/brl"
    elif moneda == "Dolar":
        urlModificada = urlModificada + "dolares/oficial"
    elif moneda == "Peso Uruguayo":
        urlModificada = urlModificada + "cotizaciones/uyu"
    elif moneda == "Euro":
        urlModificada = urlModificada + "cotizaciones/eur"
    return urlModificada

URLBASE = 'https://dolarapi.com/v1/'

LISTAUSUARIOS = Path('usuarios.csv')

# Lista de monedas elegibles
MONEDAS = ["Pesos Chilenos", "Real Brasilero", "Dolar", "Peso Uruguayo", "Euro"]

operacion = elegirOperacion("Elegir operacion: ", ["Convertir", "Analisis de usuarios"])

if operacion == "Convertir" :
    nombreUsuario = input("Ingresa tu nombre: ")

    cantidadAConvertir = int(input("Ingresar cantidad de ARS$: "))

    while cantidadAConvertir < 0 : 
        cantidadAConvertir = int(input("Ingresar una cantidad valida de ARS$: "))


    userInput = elegirOperacion("Elegir moneda para la cotizacion: ",MONEDAS)

    urlPeticion = armarUrl(URLBASE, userInput)

    print("Cargando valores...")
    datosFormateados = conseguirValoresDesdeAPI(urlPeticion)
    valoresCompra = round(cantidadAConvertir / datosFormateados["compra"], 2)
    valoresVenta = round(cantidadAConvertir / datosFormateados["venta"], 2)
    datosUsuario = [nombreUsuario, datosFormateados["moneda"],cantidadAConvertir,valoresVenta,datosFormateados["fechaActualizacion"]]
    print("---------------------Tabla de valores---------------------")
    print("Moneda:",datosFormateados["moneda"])
    print("Nombre: ",datosFormateados["nombre"])
    print("Compra: ",round(datosFormateados["compra"],2))
    print("Venta: ",round(datosFormateados["venta"],2))
    print("Ultima actualizacion: " ,datosFormateados["fechaActualizacion"])
    print()
    print("Cantidad ingresada: ","ARS$", cantidadAConvertir)
    print("Con esa cantidad se pueden comprar: ", datosFormateados["moneda"], valoresVenta)

    # Checkea si el archivo de usuarios no existe y crea el archivo
    if not LISTAUSUARIOS.exists():   
        inicializarListaUsuarios(datosUsuario, LISTAUSUARIOS)
    # Añade a la lista si el archivo existe
    else:
        añadirUsuario(datosUsuario, LISTAUSUARIOS)
else:
    if not LISTAUSUARIOS.exists():
        print("No hay ningun usuario registrado!")
    else:
        # Arma el menu de operaciones de analisis de informacion de usuarios
        analisisElegido = elegirOperacion("Que informacion queres ver?", ["Mayor Conversion", "Lista de usuarios"])
        listaDeUsuarios = obtenerListaDeCSV(LISTAUSUARIOS)
        
        # Se separan los titulos del csv de la informacion de usuarios
        titulos = listaDeUsuarios[0]
        datosDeUsuarios = obtenerListaSinTitulos(listaDeUsuarios)

        # Se retorna la informacion dependiendo de la operacion elegida
        if analisisElegido == "Mayor Conversion":
            mayorCotizacion = conseguirMayorCotizacion(datosDeUsuarios)
            print("El usuario que mas convirtio fue:", mayorCotizacion[0], end=", ")
            print("opero en:", mayorCotizacion[1], end=", ")
            print("para convertir $ARS",mayorCotizacion[2], end=" y ")
            print("el resultado de la conversion fue $",mayorCotizacion[1], mayorCotizacion[3])
        if analisisElegido == "Lista de usuarios":
            print(tabulate(datosDeUsuarios, headers=titulos, tablefmt="grid"))



