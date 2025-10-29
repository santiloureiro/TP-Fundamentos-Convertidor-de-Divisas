# Cosas a agregar: Registro o log de usuarios y feedback, interfaz grafica, programa para visualizar el feedback y uso de los usuarios 

from InquirerPy import inquirer
import requests

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

# Lista de monedas elegibles
MONEDAS = ["Pesos Chilenos", "Real Brasilero", "Dolar", "Peso Uruguayo", "Euro"]

cantidadAConvertir = int(input("Ingresar cantidad de ARS$: "))

userInput = elegirMoneda(MONEDAS)

urlPeticion = armarUrl(URLBASE, userInput)

print("Cargando valores...")
datosFormateados = conseguirValoresDesdeAPI(urlPeticion)

valoresCompra = round(cantidadAConvertir / datosFormateados["compra"], 2)
valoresVenta = round(cantidadAConvertir / datosFormateados["venta"], 2)

print("---------------------Tabla de valores---------------------")
print("Moneda:",datosFormateados["moneda"])
print("Nombre: ",datosFormateados["nombre"])
print("Compra: ",round(datosFormateados["compra"],2))
print("Venta: ",round(datosFormateados["venta"],2))
print("Ultima actualizacion: " ,datosFormateados["fechaActualizacion"])
print()
print("Cantidad ingresada: ","ARS$", cantidadAConvertir)
print("Con esa cantidad se pueden comprar: ", datosFormateados["moneda"], valoresVenta)
