from InquirerPy import inquirer
import requests

# Arma el menu de seleccion de monedas
def elegirMoneda(items):
    return inquirer.select(message = "Ingresar moneda a cotizar: ", choices = items).execute()

# Peticion de valores a dolarapi.com
def conseguirInformacion(url):
    return requests.get(url).json()

# Modifica la url base para pedir diferentes valores a la api
def armarUrl(url, moneda):
    urlModificada = url
    if moneda == "Pesos Chilenos":
        urlModificada = urlModificada + "/" + "cotizaciones/clp"
    elif moneda == "Real Brasilero":
        urlModificada = urlModificada + "/" + "cotizaciones/brl"
    elif moneda == "Dolar":
        urlModificada = urlModificada + "/" + "dolares/oficial"
    elif moneda == "Peso Uruguayo":
        urlModificada = urlModificada + "/" + "cotizaciones/uyu"
    elif moneda == "Euro":
        urlModificada = urlModificada + "/" + "cotizaciones/eur"
    return urlModificada

BASEURL = 'https://dolarapi.com/v1'

# Constante de monedas elegibles
MONEDAS = ["Pesos Chilenos", "Real Brasilero", "Dolar", "Peso Uruguayo", "Euro"]

userInput = elegirMoneda(MONEDAS)

urlPeticion = armarUrl(BASEURL, userInput)

response = requests.get(urlPeticion).json()

print("Moneda ",response["moneda"])
print("Casa ",response["casa"])
print("Nombre ",response["nombre"])
print("Compra " ,response["compra"])
print("Venta ", response["venta"])
print("Ultima actualizacion: " ,response["fechaActualizacion"])