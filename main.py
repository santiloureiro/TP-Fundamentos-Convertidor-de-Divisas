# Cosas a agregar: Registro o log de usuarios y feedback, interfaz grafica, programa para visualizar el feedback y uso de los usuarios 
from InquirerPy import inquirer
import requests
import csv
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

# Arma el menu de seleccion de monedas
def elegirMoneda(items):
    return inquirer.select(message = "Elegir moneda para la cotizacion: ", choices = items).execute()

# Peticion a url 
def conseguirValoresDesdeAPI(url):
    solicitudDatos = requests.get(url)
    return solicitudDatos.json()

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
nombreUsuario = input("Ingresa tu nombre: ")
cantidadAConvertir = int(input("Ingresar cantidad de ARS$: "))

userInput = elegirMoneda(MONEDAS)

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