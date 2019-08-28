from tkinter import *
from csv import DictReader

def loadFile(fileName, headers):
    with open(fileName) as f:
        reader = DictReader(f)
        reader = {row[headers[0]]: row[headers[1]] for row in reader}

    return reader

customerList = loadFile("Base_de_datos/Clientes/Clientes.csv",["Nombre", "Saldo"])

class Clientes(object):
    
    def __init__(self, master, button):

        self.root = master
        self.subFrame1 = Frame(self.root)
        self.subFrame2 = Frame(self.root)
        
        if(button == "state"):

            self.name = StringVar()
            self.label1 = Label(self.subFrame1, text="Ingrese el nombre del cliente para conocer su estado de cuenta:")

            self.entry1 = ttk.Combobox(self.subFrame1, textvariable=self.name, justify = "center", values=list(customerList.keys()))
            #self.name.trace('w', self.updateText)
            self.searchButton = Button(self.subFrame1, text='Buscar', command = self.updateText)
   
            self.textBox = Text(self.subFrame2, height=5)
            self.Scroll = Scrollbar(self.textBox, command=self.textBox.yview)
            self.textBox.config(yscrollcommand = self.Scroll.set)
            self.fillText()

            self.subFrame1.grid(row=0, column=0, padx=20, pady=10)
            self.subFrame2.grid(row=1, column=0, padx=20, pady=10)
            self.label1.grid(row=0, column=0, padx=10, pady=5)
            self.entry1.grid(row=1, column=0, padx=10, pady=5)
            self.searchButton.grid(row=1, column=1, padx=10, pady=5)
            self.textBox.grid(row=0, column=0)
            #self.Scroll.grid(row=0, column=1, sticky="nsew")

        self.root.title("Clientes")
        

    def updateText(self, *args):
        name = self.name.get()

        if (name == ""):
            self.fillText()
        else:
            self.textBox.delete('0.0', END)
            self.textBox.insert(END, "%s      %s \n"%(name + (20 - len(name)) * " " , customerList[name]))

    def fillText(self):
        for name, state in customerList.items():
            self.textBox.insert(END, "%s      %s \n"%(name + (20 - len(name)) * " " , state))

