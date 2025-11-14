import pandas as pd
from customtkinter import *


class Tableview(CTkFrame):
    def panda(self, table:pd.DataFrame):
        for child in self.winfo_children():
            child.destroy()
        for i, key in zip(range(len(table)), table.keys()):
            CTkEntry(master=self, textvariable=StringVar(self, value=key), state=DISABLED).grid(row=0, column=i)
        for i, row in table.iterrows():
            for j, value in zip(range(len(row)), row):
                CTkEntry(master=self, textvariable=StringVar(self, value=value), state=DISABLED).grid(row=i+1, column=j)
