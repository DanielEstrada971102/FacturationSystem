from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

X = 0
Y = 1

class PDF_receipt(object):

    def __init__(self, facName, size):

        self.papersize = self.milimetersToPoints(*size) #A4 (148, 210)
        self.border = self.milimetersToPoints(5, 10)
        self.logo = ImageReader("Logo.jpg")

        size = self.logo.getSize()
        factor =  size[Y] / size[X]
        self.logoWidth = self.papersize[X] - 4 * self.border[X] 
        self.logoHeight = self.logoWidth * factor
     
        self.canvas = canvas.Canvas(facName, self.papersize)
        self.header(self.border[X], self.papersize[Y])
        self.footer('¡Gracias por su compra, Vuelva pronto!') 
        self.canvas.setFont("Courier", 12)
        self.canvas.setFillColor("black")

    def milimetersToPoints(self, width, height):
        width = (0.0393701 * width) / (1 / 72)
        height = 0.0393701 * height / (1 / 72)

        return width, height

    def insertText(self, x, y, texto):
        text = self.canvas.beginText(x, y)

        for row in texto:
            text.textLine(row)

        self.canvas.drawText(text)

    def header(self, x, y):
        spaceTocenter = (self.papersize[X] - 2 * self.border[X] - self.logoWidth ) / 2
        self.canvas.drawImage(self.logo, x + spaceTocenter, y - self.logoHeight - self.border[Y],\
                              width = self.logoWidth , height = self.logoHeight)

    def footer(self, message):
        self.canvas.setFont("Courier-Bold", 15)
        self.canvas.setFillColorRGB(0.929, .49, 0.192)
        self.canvas.drawString(2.5 * self.border[X], self.border[Y], message)

    def end(self):
        self.canvas.showPage()
        self.canvas.save()

def main():
    fact = PDFBill("prueba.pdf", (148, 210))
    fact.insertText(100,100, ["prueba","prueba"])
    fact.end()


if __name__ == '__main__':
    main()