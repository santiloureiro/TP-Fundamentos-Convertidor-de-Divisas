from InquirerPy import inquirer
import requests
import sys

BASE = "https://dolarapi.com/v1/cotizaciones"

# Mapeo opción visible -> código esperado por la API
CHOICES = {
    "Pesos Chilenos": "clp",
    "Real Brasilero": "brl",
    "Dólar": "usd",
    "Peso Uruguayo": "uyu",
    "Euro": "eur",
}

def pedir_moneda():
    return inquirer.select(
        message="Moneda a cotizar contra ARS:",
        choices=list(CHOICES.keys())
    ).execute()

def pedir_direccion():
    return inquirer.select(
        message="Dirección de conversión:",
        choices=["ARS -> Moneda", "Moneda -> ARS"]
    ).execute()

def pedir_monto():
    return inquirer.number(
        message="Monto a convertir:",
        float_allowed=True,
        min_allowed=0
    ).execute()

def obtener_cotizacion(codigo):
    url = f"{BASE}/{codigo}"
    try:
        r = requests.get(url, timeout=8)
        r.raise_for_status()
        data = r.json()
        return data
    except requests.RequestException as e:
        print(f"Error consultando la API: {e}")
        sys.exit(1)
    except ValueError:
        print("Respuesta de API no es JSON válido.")
        sys.exit(1)

def extraer_tasas(data):
    # Intentamos los nombres más comunes
    compra = data.get("compra") or data.get("bid") or data.get("buy") or data.get("valor") or data.get("value")
    venta  = data.get("venta")  or data.get("ask") or data.get("sell") or compra
    try:
        compra = float(compra)
        venta = float(venta)
    except (TypeError, ValueError):
        print("Estructura de respuesta inesperada, contenido recibido:")
        print(data)
        sys.exit(1)
    return compra, venta

def main():
    moneda = pedir_moneda()          # p.ej. "Euro"
    direccion = pedir_direccion()    # "ARS -> Moneda" | "Moneda -> ARS"
    monto = float(pedir_monto())

    codigo = CHOICES[moneda]         # p.ej. "eur"
    data = obtener_cotizacion(codigo)
    compra, venta = extraer_tasas(data)

    # Por convención:
    # - venta: lo que te cuesta comprar la moneda (ARS por 1 unidad extranjera)
    # - compra: lo que te pagan si vendés esa moneda (ARS por 1 unidad extranjera)
    if direccion == "ARS -> Moneda":
        # quiero X ARS en EUR/CLP/BRL/etc. => divido por "venta"
        resultado = monto / venta
    else:
        # quiero X EUR/CLP/BRL/etc. en ARS => multiplico por "compra"
        resultado = monto * compra

    simbolo = data.get("moneda", codigo).upper()
    nombre = data.get("nombre", moneda)

    print("\n--- Cotización ---")
    print(f"Moneda: {nombre} ({simbolo})")
    print(f"Compra: {compra:.4f} ARS/{simbolo}")
    print(f"Venta : {venta:.4f} ARS/{simbolo}")

    if direccion == "ARS -> Moneda":
        print(f"\n{monto:.2f} ARS = {resultado:.4f} {simbolo}")
    else:
        print(f"\n{monto:.4f} {simbolo} = {resultado:.2f} ARS")

if __name__ == "__main__":
    main()