from tkinter import *
from time import sleep

def funtion():
    root.withdraw()
    sleep(3)
    root.deiconify()
 

root = Tk()
frame = Frame(root)

message = Label(frame, text="HOLA ESTO ES PRUEBA")
button = Button(frame, text="Ensayar", command=funtion)

root.geometry("500x500")
message.grid(row=0, column = 0)
button.grid(row=1, column =0)
frame.pack()

root.mainloop()