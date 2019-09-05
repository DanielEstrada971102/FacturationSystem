from tkinter import *
from csv import DictReader
from tkinter import messagebox
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from pandas import read_csv
from datetime import datetime

def loadFile(fileName, headers):
    with open(fileName) as f:
        reader = DictReader(f)
        reader = {row[headers[0]]: float(row[headers[1]]) for row in reader}

    return reader

class customerMenu(object):
    def __init__(self, master):      
        self.root = master
        self.subFrame1 = Frame(self.root)

        self.stateButton = Button(self.subFrame1, text= "Estado de Cuenta", command=self.state)
        self.buyRegisterButton = Button(self.subFrame1, text= "Registro de movimientos", command=self.register)
        self.addCustomerButton = Button(self.subFrame1, text= "Añadir nuevo cliente", command=self.add)
        self.deleteCustomerButton = Button(self.subFrame1, text= "Eliminar cliente", command=self.delete)

        self.root.title("Clientes")
        self.subFrame1.grid(row=0, column=0, padx=20, pady=10)
        self.stateButton.grid(row=0, column=0, padx=15, pady=10)
        self.buyRegisterButton.grid(row=1, column=0, padx=15, pady=10)
        self.addCustomerButton.grid(row=2, column=0, padx=15, pady=10)
        self.deleteCustomerButton.grid(row=3, column=0, padx=15, pady=10)

    def state(self):
        root = Toplevel(self.root)
        custWindow =  Clientes(root, "state")
        
    def register(self):
        root = Toplevel(self.root)
        regWindow =  movimientos(root)

    def add(self):
        root = Toplevel(self.root)
        add_Window = addWindow(root)

    def delete(self):
        pass

    def on_cancel(self):
        self.master.destroy() 


class Clientes(object):
    
    def __init__(self, master, button):
        self.root = master
        self.subFrame1 = Frame(self.root)
        self.subFrame2 = Frame(self.root)
        self.subFrame3 = Frame(self.root)
        
        self.date = datetime.now()
        self.customerList = loadFile("Base_de_datos/Clientes/Clientes.csv",["Nombre", "Saldo"])

        if(button == "state"):

            self.name = StringVar()

            self.label1 = Label(self.subFrame1, text="Ingrese el nombre del cliente para conocer su estado de cuenta:")

            self.entry1 = ttk.Combobox(self.subFrame1, textvariable=self.name, justify = "center", values=list(self.customerList.keys()))
            self.name.trace('w', self.updateText)
            self.payButton = Button(self.subFrame2, text='Actualizar estado', command = self.updateBalnce)
            self.goBackButton = Button(self.subFrame2, text='Atras', command = self.goBack)
   
            self.textBox = Text(self.subFrame3, height=5)
            self.Scroll = Scrollbar(self.textBox, command=self.textBox.yview)
            self.textBox.config(yscrollcommand = self.Scroll.set, state="disable")
            self.fillText()

            self.subFrame1.grid(row=0, column=0, padx=20, pady=10)
            self.subFrame2.grid(row=1, column=0, padx=20, pady=10)
            self.subFrame3.grid(row=2, column=0, padx=20, pady=10)
            self.label1.grid(row=0, column=0, padx=10, pady=5)
            self.entry1.grid(row=1, column=0, padx=10, pady=5)
            self.payButton.grid(row=0, column=0, padx=10, pady=5)
            self.goBackButton.grid(row=0, column=1, padx=10, pady=5)
            self.textBox.grid(row=0, column=0)
            #self.Scroll.grid(row=0, column=1, sticky="nsew")

        self.root.title("Clientes")
        

    def updateText(self, *args):
        self.textBox.config(state="normal")
        name = self.name.get()
        try:
            if (name == ""):
                self.fillText()
            else:
                self.textBox.delete('0.0', END)
                self.textBox.insert(END, "%s      %s \n"%(name + (20 - len(name)) * " " , self.customerList[name]))
        except:
            self.fillText()

        self.textBox.config(state="disable")

    def updateBalnce(self):
        root = Toplevel(self.root)
        frame = Frame(root)
        frame1 = Frame(frame)
        frame2 = Frame(frame)
        frame3 = Frame(frame)

        self.name1 = StringVar()
        self.pay = IntVar(0)

        label = Label(frame1, text="Ingrese el nombre del cliente y elija continuar para abonar a su saldo: ")
        label1 = Label(frame2, text="Nombre")
        label2 = Label(frame2, text="Cantidad ($)")
        entry1 = ttk.Combobox(frame2, textvariable = self.name1, justify = "center", values=list(self.customerList.keys()))
        entry2 = Entry(frame2, textvariable = self.pay, justify = "center")
        buttonadd = Button(frame3, text="Sumar", command = self.add)
        buttonPay = Button(frame3, text="Abonar", command = self.payment)        
        buttonCancel = Button(frame3, text="Regresar", command = lambda: root.destroy())

        label.grid(row = 0, column = 0, padx=10, pady=5)
        label1.grid(row = 0, column = 0, padx=5, pady=5)
        label2.grid(row = 0, column = 1, padx=5, pady=5)
        entry1.grid(row = 1, column = 0, padx=5, pady=5)
        entry2.grid(row = 1, column = 1, padx=5, pady=5)
        buttonadd.grid(row = 0, column = 0, padx=10, pady=5)
        buttonPay.grid(row = 0, column = 1, padx=10, pady=5)
        buttonCancel.grid(row = 0, column = 2, padx=10, pady=5)
        frame1.grid(row = 0, column = 0)
        frame2.grid(row = 1, column = 0)
        frame3.grid(row = 2, column = 0)
        frame.pack()

    def add(self):
        name = self.name1.get()
        pay = self.pay.get()
        self.customerList[name] += pay
        messagebox.showinfo(message= "Se ha añadido $%d a la cuanta pendiente de %s"%(pay, name))
        self.updateRegister()
        self.name1.set("")
        self.pay.set(0)

    def payment(self):
        name = self.name1.get()
        pay = self.pay.get()
        self.customerList[name] -= pay
        messagebox.showinfo(message= "Se han descontado $%d a la cuanta pendiente de %s"%(pay, name))
        self.updateRegister()
        self.name1.set("")   
        self.pay.set(0)

    def fillText(self):
        self.textBox.config(state="normal")
        for name, state in self.customerList.items():
            self.textBox.insert(END, "%s      %s \n"%(name + (20 - len(name)) * " " , state))
        self.textBox.config(state="disable")

    def updateRegister(self):
        customerEstateRegister = "%s,%s,%s, %d, %d \n"%(self.date.strftime("%d/%m/%Y"),self.date.strftime("%H:%M"), 
                                                 self.name1.get(), 0, self.customerList[self.name1.get()])
        with open("Base_de_datos/Clientes/Registro_de_Estado.csv", "a") as f:
            f.write(customerEstateRegister)
 
    def goBack(self):
        answer = messagebox.askyesno(message="¿Desea guardar los cambios en el registro?")
        if answer:
            with open("Base_de_datos/Clientes/Clientes.csv", 'w') as f:
                f.write("%s,%s\n"%("Nombre", "Saldo"))
                for customer, Balance in self.customerList.items():
                    f.write("%s, %s\n"%(customer, Balance))
        
        self.root.destroy()

class movimientos(object):
    """docstring for movimientos"""
    def __init__(self, master):
        self.root = master

        self.frame1 = Frame(self.root)
        self.frame2 = Frame(self.root)
        self.frame3 = Frame(self.root)

        self.customerList = loadFile("Base_de_datos/Clientes/Clientes.csv",["Nombre", "Saldo"]) 
        self.customerMovements = read_csv("Base_de_datos/Clientes/Registro_de_Estado.csv")
        self.name = StringVar()
        self.time = StringVar()
        self.dates = 0
        self.y1 = 0
        self.y2 = 0

        self.label1 = Label(self.frame1, text="Seleccione el cliente para consultar sus movimientos ")
        self.label2 = Label(self.frame2, text="Nombre")
        self.label3 = Label(self.frame2, text="intervalo de tiempo")
        self.entry1 = ttk.Combobox(self.frame2, textvariable = self.time, justify = "center", values=["semanal", "mensual", "anual"])
        self.entry2 = ttk.Combobox(self.frame2, textvariable = self.name, justify = "center", values=list(self.customerList.keys()))

        self.name.trace('w', self.defDates)
        
        self.fig = Figure(figsize=(7, 6))
        self.ax0 = self.fig.add_axes((.08, .1, .89 , .85))
   
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame3)
        self.frame1.grid(row = 0, column = 0, padx=20, pady=10)
        self.frame2.grid(row = 1, column = 0, padx=5, pady=5)
        self.frame3.grid(row = 2, column = 0, padx=5, pady=5)
        self.label1.grid(row = 0, column = 0, padx=5, pady=5)
        self.label2.grid(row = 0, column = 0, padx=5, pady=5)
        self.label3.grid(row = 0, column = 2, padx=5, pady=5)
        self.entry1.grid(row = 0, column = 3, padx=5, pady=5)
        self.entry2.grid(row = 0, column = 1, padx=5, pady=5)
        self.canvas.get_tk_widget().grid(row = 0, column = 0, padx=20, pady=10)
        self.canvas.get_tk_widget().config(borderwidth=5, relief="groove")


    def defDates(self, *args):

        name = self.name.get()
        x = self.customerMovements["Cliente"] == name 
        self.dates = list(self.customerMovements[x]["Fecha"])
        self.y1 = list(self.customerMovements[x]["Compra"])
        self.y2 = list(self.customerMovements[x]["Saldo"])
        print(len(self.y1))

        self.makeGraph() 
        

    def makeGraph(self, *args):
        self.ax0.plot(self.dates, self.y1, "or")
        self.ax0.plot(self.dates, self.y2, "ok")
        self.ax0.set_xlabel( 'Y' )
        self.ax0.set_ylabel( 'X' )
        self.ax0.grid(True, axis='y', linestyle = '--')
        self.canvas.show()

class addWindow(object):
    """docstring for addWindow"""
    def __init__(self, master):
        self.root = master

        self.frame1 = Frame(self.root)
        self.frame2 = Frame(self.root)
        self.frame3 = Frame(self.root)

        self.name = StringVar()
        self.balance = IntVar(0)

        self.label1 = Label(self.frame1, text="Ingrese el nombre del cliente y su estado de cuenta. ")
        self.label2 = Label(self.frame2, text="Nombre ")
        self.label3 = Label(self.frame2, text="Saldo ")
        self.entry1 = Entry(self.frame2, textvariable= self.name, justify="center")
        self.entry2 = Entry(self.frame2, textvariable= self.balance, justify="center")
        self.addButton = Button(self.frame3, text="Añadir", command = self.add)

        self.frame1.grid(row=0, column=0, padx=10, pady=10)
        self.frame2.grid(row=1, column=0, padx=10, pady=10)
        self.frame3.grid(row=2, column=0, padx=10, pady=10)
        self.label1.grid(row=0, column=0, padx=15, pady=10)
        self.label2.grid(row=0, column=0, padx=5, pady=10)
        self.label3.grid(row=0, column=2, padx=5, pady=10)
        self.entry1.grid(row=0, column=1, padx=5, pady=10)
        self.entry2.grid(row=0, column=3, padx=5, pady=10)
        self.addButton.grid(row=0, column=0, padx=15, pady=10)

        
    def add(self):
        answer = messagebox.askyesno(message="¿Desea añadir %s a la base de datos de clientes?"%(self.name.get()))
        if answer:
            with open("Base_de_datos/Clientes/Clientes.csv", 'a') as f:
                f.write("%s,%s\n"%(self.name.get(), str(self.balance.get())))
            self.root.destroy()
        else:
            pass


def main():
    root = Tk()
    window = customerMenu(root)

    root.mainloop()


if __name__ == '__main__':
    main()