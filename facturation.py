from factura import *
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime
from csv import DictReader
#from os import startfile

#----------------cargando Base de datos---------------------

def uploadFile(fileName, headers):
    with open(fileName) as f:
        reader = DictReader(f)
        reader = {row[headers[0]]: row[headers[1]] for row in reader}

    return reader

productList = uploadFile("Base_de_datos/Productos/Productos.csv", ["Product", "Default Price"])
customerList = uploadFile("Base_de_datos/Clientes/Clientes.csv",["Nombre", "Saldo"])

#-----------------------------------------------------------

class Facturar(object):

    def __init__(self, master):

        self.root = master
        self.factura = Bill(date = datetime.now())

        self.subFrame1 = Frame(self.root)
        self.subFrame2 = Frame(self.root)
        self.facFrame = Frame(self.root)
        self.subFrame3 = Frame(self.root)

        # ------------Variables de control-------------

        self.date = StringVar(value=self.factura.get_dateToFrame())
        self.Numb = IntVar(value= self.factura.facNumber)
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
            self.subFrame1, justify="center", values=list(customerList.keys()), textvariable=self.customerName)

        self.customerName.trace('w', self.getPrevBalance)

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
            self.subFrame2, justify="center", values=list(productList.keys()), textvariable=self.product)
        self.priceEntry = Entry(
            self.subFrame2, justify="center", textvariable=self.price)
        self.subTotalEntry = Entry(
            self.subFrame2, justify="center", state="disabled", textvariable=self.subTotal)

        self.amount.trace('w', self.calSubTotal)
        self.price.trace('w', self.calSubTotal)
        self.product.trace('w', lambda *args: self.price.set(productList[self.product.get()]))

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
                                  command= self.Print)
        self.saveAndPrintButton = Button(self.subFrame3, 
                                         text ="Imprimir y Guardar",    
                                         command= self.printAndSave)

        Label(self.subFrame3, text="TOTAL: ", font=(24), 
              bg="gray").grid(row=0, column=1, padx=10)
        Label(self.subFrame3, text="Saldo.Ant: ", font=(24), 
              bg="gray").grid(row=1, column=1, padx=10)
        Label(self.subFrame3, text="Pago: ", font=(24), 
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
        self.total.set(self.factura.get_total())

    def delete(self):
        product = self.product.get()

        self.factura.deleteField(product)
        self.updateText()
        self.total.set(self.factura.get_total())

    def updateBalance(self, FIN = False, *args):
        ErrorDate = False
        
        try:
            self.factura.payment = self.payment.get()
            self.factura.set_finBalance()    
            self.finBalance.set(self.factura.finBalance)

        except:
            ErrorDate = True

        if ErrorDate:
            pass

        if FIN:
            customerList[self.factura.customer] = self.factura.finBalance
            with open("Base_de_datos/Clientes/Clientes.csv", 'w') as f:
                f.write("%s,%s\n"%("Nombre", "Saldo"))
                for customer, Balance in customerList.items():
                    f.write("%s,%s\n"%(customer, Balance))

    def getPrevBalance(self, *args):
        self.factura.customer = self.customerName.get()
        ErrorDate = False

        try:    
            self.factura.prevBalance = float(customerList[self.factura.customer])
            self.prevBalance.set(self.factura.prevBalance)
            self.updateBalance()

        except: 
            ErrorDate = True

        if ErrorDate:
            pass

    def save(self):
        self.factura.save(self.factura.get_facName())
        self.updateBalance(FIN = True)
        self.addToRegister()

        answer = messagebox.askyesno(message="La factura fue guardada con exito, desea salir ?", title= "save successful")

        if answer:
            self.root.destroy()

    def Print(self):
        pass #startfile(self.facName, "print")

    def printAndSave(self):
        self.Print()
        self.save()

    def addToRegister(self):
        text = "%s,%d,%d,%d\n"%(self.factura.get_dateToFrame(), 
                                self.factura.payment, 
                                self.factura.total -\
                                self.factura.payment,
                                self.factura.total)

        with open("Base_de_datos/facturas/Registro.csv", "a") as f:
            f.write(text)

class Balance(object):
    """docstring for DailyBalance"""
    def __init__(self, master):
        self.root = master

    # --------------Window structure-------------------
        self.root.title("Balance")
        self.root.geometry("500x800")
        

def main():
    root = Tk()
    window = Facturar(root)
    root.mainloop()

if __name__ == '__main__':
    main()	

    