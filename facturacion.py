from tkinter import Tk, Frame, Label, Entry, Button, Text, ttk, StringVar, DoubleVar, messagebox, Scrollbar, END, INSERT
import numpy as np


productList = ["Mango", "Papaya", "Melon"]

class Facturar():
    def __init__(self, root):
        self.root =root

        self.subFrame1 = Frame(self.root)
        self.subFrame2 = Frame(self.root)
        self.facFrame = Frame(self.root)
        self.subFrame3 = Frame(self.root)
        # ------------Variables de control-------------
        self.quantity = DoubleVar(value=0)
        self.product = StringVar()
        self.price = DoubleVar(value=0)
        self.subTotal = DoubleVar(value=0)
        self.total = DoubleVar(value=0)
        self.prevBalance = DoubleVar(value=0)
        self.payment = DoubleVar(value=0)
        self.finBalance = DoubleVar(value=0)
        self.facArray=[]

        self.rowCount = 0

        # -----------------subFrame1------------------
        self.dateLabel = Label(self.subFrame1, text="Fecha:", font=(14))
        self.dataEntry = Entry(self.subFrame1, justify="center")

        self.facNumbLabel = Label(self.subFrame1, text="N°:", font=(14))
        self.facNumbEntry = Entry(self.subFrame1, justify="center")

        self.nameLabel = Label(self.subFrame1, text="Nombre:", font=(14))
        self.nameEntry = Entry(self.subFrame1, justify="center")
        # -----------------subFrame2-------------------
        Label(self.subFrame2, text="Cantidad", font=(14),
              bg="gray").grid(row=0, column=0, padx=15, pady=10)
        Label(self.subFrame2, text="Producto", font=(14),
              bg="gray").grid(row=0, column=1, padx=15, pady=10)
        Label(self.subFrame2, text="Precio.U", font=(14),
              bg="gray").grid(row=0, column=2, padx=15, pady=10)
        Label(self.subFrame2, text="Subtotal", font=(14),
              bg="gray").grid(row=0, column=3, padx=15, pady=10)

        self.quantityEntry = Entry(
            self.subFrame2, justify="center", textvariable=self.quantity)
        self.productEntry = ttk.Combobox(
            self.subFrame2, justify="center", values=productList, textvariable=self.product)
        self.priceEntry = Entry(
            self.subFrame2, justify="center", textvariable=self.price)
        self.subTotalEntry = Entry(
            self.subFrame2, justify="center", state="disabled", textvariable=self.subTotal)

        self.quantity.trace('w', self.calSubTotal)
        self.price.trace('w', self.calSubTotal)

        self.addButton = Button(self.subFrame2, text="+", command=self.addFac)
        self.lessButton = Button(self.subFrame2, text="-",command=self.lessFac)

        # -----------------facFrame---------------------
        self.facText = Text(self.facFrame, height=10)
        self.Scrollfac = Scrollbar(self.facFrame, command=self.facText.yview)
        self.facText.config(yscrollcommand = self.Scrollfac.set)
        
        # -----------------subFrame3---------------------
        self.cancelButton = Button(self.subFrame3, text="Cancelar",
                                   command=self.cancelFac)
        self.saveButton = Button(self.subFrame3, text ="Guardar", 
                                 command=lambda:0)
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
        self.prevBalance.set(12000)

        # --------------Window structure-------------------
        self.root.title("Factura")
        self.root.geometry("900x700")
        #self.ScrollRoot.grid(column=1, sticky="nsew", fill ="y")
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

        self.quantityEntry.grid(row=1, column=0, padx=5, pady=5)
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

    def addFac(self):
        line = [float(self.quantity.get()), self.product.get(), 
                float(self.price.get()), float(self.subTotal.get())]

        text = str(line[0]) + "\t" + line[1] + "\t" + str(line[2]) + \
               "\t" + str(line[3])+"\n"

        self.facArray.append(line)
        self.facText.insert(END, text)
        self.sumarFac()
        self.rowCount += 1

    def lessFac(self):   
        row = str(self.rowCount) +".0" 
        self.facText.delete(row, INSERT)
        
        if self.rowCount > 0:
            self.rowCount -= 1
            self.facArray = self.facArray[:self.rowCount]
            self.sumarFac()
        else:
            messagebox.showwarning(message="No hay nada que borrar", 
                                   title="Cuidado")

    def sumarFac(self):
        array = np.array(self.facArray, dtype=object)
        self.total.set(np.sum(array[:,3]))

    def calSubTotal(self, *args):
        ErrorDate = False
        
        try:
            self.subTotal.set(self.quantity.get() * self.price.get())
        except:
            ErrorDate = True

        if ErrorDate:
            pass
    def updateBalance(self, *args):
        ErrorDate = False
        try:    
            self.finBalance.set(self.prevBalance.get() + \
                                self.total.get() - self.payment.get())
        except:
            ErrorDate = True

        if ErrorDate:
            pass

    def cancelFac(self):
        self.root.destroy()


def main():
    root = Tk()
    Facturar(root)
    root.mainloop()

if __name__ == '__main__':
    main()
