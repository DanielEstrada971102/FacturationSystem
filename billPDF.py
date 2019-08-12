from reportlab.pdfgen import canvas
from reportlab.lib.colors import CMYKColor

class PDFBill(object):
    """docstring for PDFBill"""
    def __init__(self, facName, size):

        self.papersize = self.milimetersToPoints(*size) #148, 210
        self.border = self.milimetersToPoints(5, 10)
        self.logo = "Logo.jpg"
        self.canvas = canvas.Canvas(facName, self.papersize)

        self.header(self.border[0], self.papersize[1])
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
        width = self.papersize[0]- 4 * self.border[0]
        height =  width / 2.8
        self.canvas.drawImage(self.logo, x + self.border[0], y - height - self.border[1] , width = width , height = height)

    def footer(self, message):
        self.canvas.setFont("Courier-Bold", 15)
        self.canvas.setFillColorRGB(0.929, .49, 0.192)
        self.canvas.drawString(2.5 * self.border[0], self.border[1], message)

    def end(self):
        self.canvas.showPage()
        self.canvas.save()

def main():
    fact = PDFBill("prueba.pdf", (148, 210))
    fact.insertText(100,100, ["prueba","prueba"])
    fact.end()


if __name__ == '__main__':
    main()