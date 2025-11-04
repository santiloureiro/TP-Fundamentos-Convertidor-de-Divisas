import csv
from pathlib import Path
        
def conseguirListaUsuarios(archivo):
    lista = []
    with open(archivo, 'r', newline='') as archivoUsuarios:
        lectorCsv = csv.reader(archivoUsuarios)
        for row in lectorCsv:
            lista.append(row)
    return(lista)

def leerUsuarios(listaUsuarios):
    for i in range(1,len(listaUsuarios)):
        print(listaUsuarios[i])
            
ARCHIVO = Path("usuarios.csv")
            
listaDeUsuarios = conseguirListaUsuarios(ARCHIVO)

print(listaDeUsuarios)

leerUsuarios(listaDeUsuarios)