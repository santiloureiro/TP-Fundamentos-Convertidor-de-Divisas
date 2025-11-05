import csv
from pathlib import Path
import tkinter as tk
        
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

print(listaDeUsuarios[0])

usuarios = leerUsuarios(listaDeUsuarios)

root = tk.Tk()
root.title("Listbox Example")
listaGrafica = tk.Listbox(root, width=200, height=500)
listaGrafica.pack(pady=10,padx=10)

for item in listaDeUsuarios:
    listaGrafica.insert(tk.END,item)
root.mainloop()