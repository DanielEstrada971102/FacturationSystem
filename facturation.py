from factura import *
from tkinter import *
from tkinter import ttk
from glob import glob
from tkinter import messagebox
from datetime import datetime
from numpy import array
from csv import reader


productList =[]

with open("Base_de_datos/Productos/Productos.csv", 'r') as f:
    file = reader(f)
    for row in file:
        productList.append(row) 

productList = array(productList)

customerList =[]

with open("Base_de_datos/Clientes/Clientes.csv", 'r') as f:
    file = reader(f)
    for row in file:
        customerList.append(row) 

customerList = array(customerList)


class Facturar(object):

    def __init__(self, master):

        self.DATE = datetime.now() 
        self.root = master
        self.factura = Bill()

        self.subFrame1 = Frame(self.root)
        self.subFrame2 = Frame(self.root)
        self.facFrame = Frame(self.root)
        self.subFrame3 = Frame(self.root)
        # ------------Variables de control-------------
        self.date = StringVar(value=self.DATE.strftime("%d/%m/%Y"))
        self.Numb = StringVar(value=str(len(glob("Base_de_datos/facturas/*.fact"))))
        self.customerName = StringVar()

        self.amount = DoubleVar()
        self.product = StringVar()
        self.price = IntVar()
        self.subTotal = DoubleVar()

        self.total = DoubleVar(value=0)
        self.prevBalance = DoubleVar(value=0)
        self.payment = DoubleVar(value=0)
        self.finBalance = DoubleVar(value=0)

        # -----------------subFrame1------------------
        self.dateLabel = Label(self.subFrame1, text="Fecha:", font=(14))
        self.dataEntry = Entry(self.subFrame1, justify="center", textvariable=self.date)

        self.facNumbLabel = Label(self.subFrame1, text="N°:", font=(14))
        self.facNumbEntry = Entry(self.subFrame1, justify="center", textvariable=self.Numb, state="disable")

        self.nameLabel = Label(self.subFrame1, text="Nombre:", font=(14))
        self.nameEntry = ttk.Combobox(
            self.subFrame1, justify="center", values=customerList[1:,0], textvariable=self.customerName)

        # -----------------subFrame2-------------------
        Label(self.subFrame2, text="Cantidad", font=(14),
              bg="gray").grid(row=0, column=0, padx=15, pady=10)
        Label(self.subFrame2, text="Producto", font=(14),
              bg="gray").grid(row=0, column=1, padx=15, pady=10)
        Label(self.subFrame2, text="Precio.U", font=(14),
              bg="gray").grid(row=0, column=2, padx=15, pady=10)
        Label(self.subFrame2, text="Subtotal", font=(14),
              bg="gray").grid(row=0, column=3, padx=15, pady=10)

        self.amountEntry = Entry(
            self.subFrame2, justify="center", textvariable=self.amount)
        self.productEntry = ttk.Combobox(
            self.subFrame2, justify="center", values=productList[1:,0], textvariable=self.product)
        self.priceEntry = Entry(
            self.subFrame2, justify="center", textvariable=self.price)
        self.subTotalEntry = Entry(
            self.subFrame2, justify="center", state="disabled", textvariable=self.subTotal)

        self.amount.trace('w', self.calSubTotal)
        self.price.trace('w', self.calSubTotal)

        self.addButton = Button(self.subFrame2, text="+", command=self.add)
        self.lessButton = Button(self.subFrame2, text="-",command=self.delete)

        # -----------------facFrame---------------------
        self.facText = Text(self.facFrame, height=10)
        self.Scrollfac = Scrollbar(self.facFrame, command=self.facText.yview)
        self.facText.config(yscrollcommand = self.Scrollfac.set)

        # -----------------subFrame3---------------------
        self.cancelButton = Button(self.subFrame3, text="Cancelar",
                                   command= lambda: self.root.destroy())
        self.saveButton = Button(self.subFrame3, text ="Guardar", 
                                 command=self.save)
        self.printButton = Button(self.subFrame3, text ="Imprimir",
                                  command=lambda:0)
        self.saveAndPrintButton = Button(self.subFrame3, 
                                         text ="Imprimir y Guardar",    
                                         command=lambda:0)

        Label(self.subFrame3, text="TOTAL: ", font=(24), 
              bg="gray").grid(row=0, column=1, padx=10)
        Label(self.subFrame3, text="Saldo.Ant: ", font=(24), 
              bg="gray").grid(row=1, column=1, padx=10)
        Label(self.subFrame3, text="Abono: ", font=(24), 
              bg="gray").grid(row=2, column=1, padx=10)
        Label(self.subFrame3, text="Saldo.Fin: ", font=(24), 
              bg="gray").grid(row=3, column=1, padx=10)

        self.totalEntry = Entry(self.subFrame3, state="disabled", 
                                justify="center", textvariable=self.total)
        self.prevBalanceEntry = Entry(self.subFrame3, state="disabled", 
                                      justify="center", 
                                      textvariable=self.prevBalance)
        self.paymentEntry = Entry(self.subFrame3, justify="center", 
                                  textvariable=self.payment)
        self.finBalanceEntry = Entry(self.subFrame3, state="disabled", 
                                     justify="center", 
                                     textvariable=self.finBalance)

        self.total.trace('w', self.updateBalance)
        self.payment.trace('w', self.updateBalance)
        # --------------Window structure-------------------
        self.root.title("Factura")
        self.root.geometry("900x700")

        self.subFrame1.grid(row=0, column=0, padx=20, pady=10)
        self.subFrame2.grid(row=1, column=0, padx=20, pady=10)
        self.facFrame.grid(row=2, column=0, padx=20, pady=10)
        self.subFrame3.grid(row=3, column=0, padx=20, pady=10)

        self.dateLabel.grid(row=0, column=0, padx=10, pady=5)
        self.dataEntry.grid(row=0, column=1, padx=10, pady=5)
        self.nameLabel.grid(row=1, column=0, padx=10, pady=5)
        self.nameEntry.grid(row=1, column=1, padx=10, pady=5)	
        self.facNumbLabel.grid(row=0, column=2, padx=10, pady=5)
        self.facNumbEntry.grid(row=0, column=3, padx=10, pady=5)

        self.amountEntry.grid(row=1, column=0, padx=5, pady=5)
        self.productEntry.grid(row=1, column=1, padx=5, pady=5)
        self.priceEntry.grid(row=1, column=2, padx=5, pady=5)
        self.subTotalEntry.grid(row=1, column=3, padx=5, pady=5)

        self.facText.grid(row=0, column=0)
        self.Scrollfac.grid(row=0, column=1, sticky="nsew")

        self.addButton.grid(row=1, column=4, padx=5, pady=5)
        self.lessButton.grid(row=1, column=5, padx=5, pady=5)

        self.cancelButton.grid(row=0, column=0, padx=15, pady=10)
        self.saveButton.grid(row=1, column=0, padx=15, pady=10)
        self.printButton.grid(row=2, column=0, padx=15, pady=10)
        self.saveAndPrintButton.grid(row=3, column=0, padx=15, pady=10)
        self.totalEntry.grid(row=0, column=2)
        self.prevBalanceEntry.grid(row=1, column=2)
        self.paymentEntry.grid(row=2, column=2)
        self.finBalanceEntry.grid(row=3, column=2)


    def calSubTotal(self, *args):
	    ErrorDate = False
	    
	    try:
	        self.subTotal.set(self.amount.get() * self.price.get())
	    except:
	        ErrorDate = True

	    if ErrorDate:
	        pass

    def updateText(self):
        self.facText.delete('0.0', END)

        for product in self.factura.products:
            self.facText.insert(END, self.factura.renderProduct(product))

    def add(self):
        product = self.product.get()

        self.factura.addField(self.amount.get(), product, self.price.get())

        self.updateText()

        self.total.set(self.factura.getTotal())

        print(self.factura.products)

    def delete(self):
        product = self.product.get()
        self.factura.deleteField(product)
        print(self.factura.products)

        self.updateText()


    def updateBalance(self, *args):
        ErrorDate = False

        try:    
            self.finBalance.set(self.prevBalance.get() + \
                                self.total.get() - self.payment.get())
        except:
            ErrorDate = True

        if ErrorDate:
            pass

    def save(self):
        facName = "Base_de_datos/facturas/" + self.customerName.get() +\
                  "_" + self.DATE.strftime("%d_%m_%Y_%H:%M") +".fact"
        
        self.factura.save(facName)
        answer = messagebox.askyesno(message="La factura fue guardada con exito, desea salir ?", title= "save successful")
        
        if answer:
            self.root.destroy()


def main():
    root = Tk()
    window = Facturar(root)
    root.mainloop()

if __name__ == '__main__':
    main()	

    