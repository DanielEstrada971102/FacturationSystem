from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import tkinter as Tk
from csv import DictReader
import pandas as pd


x = pd.read_csv("Base_de_datos/Clientes/Clientes.csv")
