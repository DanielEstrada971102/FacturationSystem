from glob import glob
from billPDF import *

class Factura(object):
    def __init__(self, date):
        self.products = dict()
        self.date = date
        self.customer = ""
        self.facNumber = len(glob("Base_de_datos/facturas/*.pdf")) + 1 
        self.total = 0
        self.prevBalance = 0
        self.payment = 0
        self.finBalance = 0

    def addField(self, amount, productName, price):
        productName = productName + (20 - len(productName)) * " " 
        self.products[productName] = amount, price, amount * price

    def deleteField(self, productName):
        self.products.pop(productName)

    def get_total(self):
        self.total = 0
        for _, (_, _, subtotal) in self.products.items():
            self.total += subtotal

        return self.total

    def set_finBalance(self):
        self.finBalance = self.prevBalance + self.total - self.payment

    def get_dateToFrame(self):
        return self.date.strftime("%d/%m/%Y")

    def get_facName(self):
        name = "Base_de_datos/facturas/" + self.customer + "_" +\
               self.date.strftime("%d_%m_%Y_%H:%M") + ".pdf"
        return name

    def renderProduct(self, product):
        amount, price, subtotal = self.products[product]

        text = '%.2f    %s  %d    %.2f' % (amount, product, price, subtotal)

        return text

    def save(self, file):

        factura = []
        file = PDF_receipt(file, (148, 210))
        
        positionName = file.border[0] * 3, 410
        positionNumb = file.papersize[0] - (10 * file.border[0]), 410
        positiondate = file.border[0]*3, 395
        positionFirstLine = positiondate[0], positiondate[1] - 10, file.papersize[0] - 3 * file.border[0], positiondate[1] - 10 
        positionSecondLine = positiondate[0], 140, file.papersize[0] - 3 * file.border[0], 140 

        
        file.canvas.drawString(positionName[0], positionName[1], "Nombre: %s"%(self.customer))
        file.canvas.drawString(positionNumb[0], positionNumb[1], "Fac N°: %s"%str(self.facNumber))
        file.canvas.drawString(positiondate[0], positiondate[1], "Fecha: %s   "%(self.date.strftime("%d/%m/%Y/ %H:%M")))
        file.canvas.line(*positionFirstLine)
        

        for productName in self.products:
            factura.append(self.renderProduct(productName))

        balance = [ "Total:                             %.2f"%(self.total),
                    "Saldo Anterior:                    %.2f"%(self.prevBalance),
                    "Abono:                             %.2f"%(self.payment), 
                    "Saldo Final:                       %.2f"%(self.finBalance)]

        file.insertText(file.border[0] * 3, 370, factura)
        file.canvas.line(*positionSecondLine)
        file.insertText(file.border[0] * 3, 120, balance)
        file.end()