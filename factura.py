from glob import glob

class Bill(object):
    def __init__(self, date):
        self.products = dict()
        self.date = date
        self.customer = ""
        self.facNumber = len(glob("Base_de_datos/facturas/*.fact")) + 1 
        self.total = 0
        self.prevBalance = 0
        self.payment = 0
        self.finBalance = 0

    def addField(self, amount, productName, price): 
        self.products[productName] = amount, price, amount * price

    def deleteField(self, productName):
        self.products.pop(productName)

    def get_total(self):
        self.total = 0
        for _, (_, _, subtotal) in self.products.items():
            self.total += subtotal

        print(self.total)

        return self.total

    def set_finBalance(self):
        self.finBalance = self.prevBalance + self.total - self.payment

    def get_dateToFrame(self):
        return self.date.strftime("%d/%m/%Y")

    def get_facName(self):
        neme = "Base_de_datos/facturas/" + self.customer + "_" +\
               self.date.strftime("%d_%m_%Y_%H:%M") + ".fact"
        return name

    def renderProduct(self, product):
        amount, price, subtotal = self.products[product]

        text = '%.2f\t%s\t%d\t%.2f\n' % (amount, product, price, subtotal)

        return text

    def save(self, file):

        header = \
        "*********************************************\n" + \
        "*             MAXIFRUVER LUPE               *\n" + \
        "*                                           *\n" + \
        "*********************************************\n" + \
        " Nombre: %s               Fac N°: %s \n"%(self.customer, str(self.facNumber)) + \
        " Fecha: %s   \n"%(self.date.strftime("%d/%m/%Y/ %H:%M")) + \
        "=============================================\n"

        footer = \
         "  Total:           %.2f\n"%(self.total) + \
         "  Saldo Anterior:  %.2f\n"%(self.prevBalance) + \
         "  Abono:           %.2f\n"%(self.payment) + \
         "  Saldo Final:     %.2f\n"%(self.finBalance) + \
         "=============================================\n" + \
         "         Gracias por su compra              \n"        

        with open(file, 'w') as f:
            f.write(header)
            for productName in self.products:
                file.write(self.renderProduct(productName))
            f.write(footer)
