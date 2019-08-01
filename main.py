from tkinter import *
from facturacion import *


def newButton(contendor, texto, fila, columna):
    Button(contendor, text=texto, command=lambda: Facturar(contendor)).grid(
        row=fila, column=columna, padx=20, pady=10)


def main():
    principalWindow = Tk()

    principalWindow.title("Programa principal")
    principalWindow.geometry("500x800")

    Label(principalWindow, text="Sistema de Facturación",
          font=(18)).grid(row=0, column=0, padx=20, pady=15)
    newButton(principalWindow, "Prueba", 1, 0)

    principalWindow.mainloop()


if __name__ == '__main__':
    main()
