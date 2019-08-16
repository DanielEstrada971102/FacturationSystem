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

    def save(self, nameFile):

        factura = [self.renderProduct(productName) for productName in self.products]

        file = PDF_receipt(nameFile, (148, 130 + len(factura)* 5))
        
        positionName = file.border[X] * 3, file.papersize[Y] - file.logoHeight - 50
        positionNumb = file.papersize[X] - (10 * file.border[X]), positionName[Y]
        positiondate = file.border[X]*3, positionName[Y] - 15
        positionFirstLine = positiondate[X], positiondate[Y] - 10, file.papersize[X] - 3 * file.border[X], positiondate[Y] - 10 
        positionSecondLine = positiondate[X], positionFirstLine[Y] - (len(factura) + 1 ) * 15, \
                             file.papersize[X] - 3 * file.border[X], positionFirstLine[Y] - (len(factura) + 1 ) * 15 

        
        file.canvas.drawString(positionName[X], positionName[Y], "Nombre: %s"%(self.customer))
        file.canvas.drawString(positionNumb[X], positionNumb[Y], "Fac N°: %s"%str(self.facNumber))
        file.canvas.drawString(positiondate[X], positiondate[Y], "Fecha: %s   "%(self.date.strftime("%d/%m/%Y/ %H:%M")))
        file.canvas.line(*positionFirstLine)

        balance = [ "Total:                             %.2f"%(self.total),
                    "Saldo Anterior:                    %.2f"%(self.prevBalance),
                    "Abono:                             %.2f"%(self.payment), 
                    "Saldo Final:                       %.2f"%(self.finBalance)]

        file.insertText(file.border[X] * 3, positionFirstLine[Y] - 15, factura)
        file.canvas.line(*positionSecondLine)
        file.insertText(file.border[X] * 3, positionSecondLine[Y] - 15, balance)
        file.end()

def main():
    pass

if __name__ == '__main__':
    main()