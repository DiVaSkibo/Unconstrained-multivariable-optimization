import pandas as pd
from customtkinter import *
from PIL import Image


class Tableview(CTkFrame):
    def __init__(self, master, signal:callable=None, width = 200, height = 200, corner_radius = None, border_width = None, bg_color = "transparent", fg_color = None, border_color = None, background_corner_colors = None, overwrite_preferred_drawing_method = None, **kwargs):
        super().__init__(master, width, height, corner_radius, border_width, bg_color, fg_color, border_color, background_corner_colors, overwrite_preferred_drawing_method, **kwargs)
        self.signal = signal
        self.table = None
        self.Iter = IntVar(value=0)
    
    def clear(self):
        for child in self.winfo_children():
            child.destroy()
    
    def iteration(self) -> dict:
        return self.table.iloc[self.Iter.get()].to_dict()

    def panda(self, table:pd.DataFrame):
        def on_next():
            self.Iter.set((self.Iter.get() + 1) % len(self.table.values))
        def on_radio_changed():
            self.signal(self.iteration())
        self.clear()
        self.table = table    
        next_png = Image.open('icons/next.png')
        icon = CTkImage(dark_image=next_png, light_image=next_png, size=(15, 15))
        btn = CTkButton(master=self, command=on_next, image=icon, text='', width=15, height=15)
        btn.grid(padx=1.6, sticky=W)
        btn.image = icon
        for j, key in zip(range(len(self.table)), self.table.keys()):
            CTkEntry(master=self, textvariable=StringVar(self, value=key), state=DISABLED, fg_color='#2A2A4A').grid(row=0, column=j+1)
        for i, row in self.table.iterrows():
            CTkRadioButton(master=self, value=i, variable=self.Iter, command=on_radio_changed, text=f'{i}', width=20, height=20, radiobutton_width=15, radiobutton_height=15).grid(row=i+1, column=0, padx=10)
            for j, value in zip(range(len(row)), row):
                CTkEntry(master=self, textvariable=StringVar(self, value=value), state=DISABLED).grid(row=i+1, column=j+1)
