from tkinter import *
from facturation import Facturar



class PrincipalMenu(object):

    def __init__(self, master):
        self.root = master
        self.menuFrame = Frame(self.root)
        self.header = Label(self.menuFrame, text="MAXIFRUVER LUPE")
        self.billButton = Button(self.menuFrame, text="Facturar", 
                                command = self.invoice)
        self.customersButton = Button(self.menuFrame, text="Clientes", 
                                      command= self.customers)	
        self.inventoryButton = Button(self.menuFrame, text="Inventario", 
                                      command= self.inventory)

        self.root.title("MAXIFRUVER LUPE")
        self.menuFrame.grid(row=0, column=0)
        self.header.grid(row=0, column=0, padx=25, pady=20)
        self.header.config(fg="blue", font=(24)) 
        self.billButton.grid(row=1, column=0, padx=25, pady=20)
        self.billButton.config(font=(18))
        self.customersButton.grid(row=2, column=0, padx=25, pady=25)
        self.customersButton.config(font=(18))
        self.inventoryButton.grid(row=3, column=0, padx=25, pady=25)
        self.inventoryButton.config(font=(19))


    def invoice(self): # facturar
        root = Toplevel(self.root)
        bill = Facturar(root)

    def customers(self): # clientes
        pass

    def inventory(self): # inventario
        pass


def main():
    root = Tk()
    menu = PrincipalMenu(root)
    root.mainloop()


if __name__ == '__main__':
    main()
