from InquirerPy import inquirer
import requests     

def elegirMoneda(items):
    return inquirer.select(message = "Ingresar moneda a cotizar: ", choices = items).execute()

def conseguirInformacion(url):
    return requests.get(url).json()

def armarUrl(url,moneda):
    if moneda == "Pesos Chilenos":
        url = url + "/" + "cotizaciones/clp"
    elif moneda == "Real Brasilero":
        url = url + "/" + "cotizaciones/brl"
    elif moneda == "Dolar":
        url = url + "/" + "dolares/v1"
    elif moneda == "Peso Uruguayo":
        url = url + "/" + "cotizaciones/uyu"
    elif moneda == "Euro":
        url = url + "/" + "cotizaciones/eur"


baseUrl = 'https://dolarapi.com/v1'

MONEDAS = ["Pesos Chilenos", "Real Brasilero", "Dolar", "Peso Uruguayo", "Euro"]

userInput = elegirMoneda(MONEDAS)

armarUrl(baseUrl, userInput)

print(baseUrl) 

response = requests.get(baseUrl).json()

print("Moneda ",response["moneda"])
print("Casa ",response["casa"])
print("Nombre ",response["nombre"])
print("Compra " ,response["compra"])
print("Venta ", response["venta"])
print("Ultima actualizacion: " ,response["fechaActualizacion"])