import pandas as pd
from customtkinter import *
from PIL import Image


class Tableview(CTkScrollableFrame):
    def __init__(self, master, signal:callable=None, width = 600, height = 600, corner_radius = None, border_width = None, bg_color = 'transparent', fg_color = None, border_color = None, background_corner_colors = None, overwrite_preferred_drawing_method = None, **kwargs):
        super().__init__(master, width, height, corner_radius, border_width, bg_color, fg_color, border_color, background_corner_colors, overwrite_preferred_drawing_method, **kwargs)
        self.signal = signal
        self.table = None
        self.Iter = IntVar(value=0)
    
    def clear(self):
        self.table = None
        self.Iter.set(0)
        for child in self.winfo_children():
            child.destroy()
    
    def iteration(self) -> dict:
        return self.table.iloc[self.Iter.get()].to_dict()

    def panda(self, table:pd.DataFrame):
        def on_next():
            self.Iter.set((self.Iter.get() + 1) % len(self.table.values))
        def on_radio_changed():
            if self.signal:
                self.signal(self.iteration())
            else:
                self.iteration()
        self.clear()
        self.table = table    
        next_png = Image.open('icons/next.png')
        icon = CTkImage(dark_image=next_png, light_image=next_png, size=(15, 15))
        btn = CTkButton(master=self, command=on_next, image=icon, text='', width=15, height=15)
        btn.grid(padx=1.6, sticky=W)
        btn.image = icon
        for j, key in zip(range(len(self.table.keys())), self.table.keys()):
            if key == 'method': continue
            match key:
                case 'x' | 'grad': width = 130
                case 'fun' | 'gnorm': width = 75
                case 'hesse': width = 130
                case 'alpha': width = 55
            entk = CTkEntry(master=self, width=width, fg_color='#2A2A4A')
            entk.grid(row=0, column=j)
            entk.insert(0, f'{key}')
            entk.configure(state=DISABLED)
        for i, row in self.table.iterrows():
            CTkRadioButton(master=self, value=i, variable=self.Iter, command=on_radio_changed, text=f'{i}', width=20, height=20, radiobutton_width=15, radiobutton_height=15).grid(row=i+1, column=0, padx=10)
            for j, value in zip(range(len(row)), row):
                if type(value) is str: continue
                match self.table.keys()[j]:
                    case 'x' | 'grad':
                        width = 130
                        val = '\t'.join([f'{v:.3f}' for v in value])
                    case 'fun' | 'gnorm':
                        width = 75
                        val = f'{value:.3f}'
                    case 'hesse':
                        width = 130
                        val = [v for vv in value for v in vv]
                        val = '\t'.join([f'{v:.3f}' for v in val])
                        val = f'{'\t'.join([f'{v:.3f}' for v in value[0]])}\n{'\t'.join([f'{v:.3f}' for v in value[1]])}'
                        txbxv = CTkTextbox(master=self, width=width, height=50)
                        txbxv.grid(row=i+1, column=j)
                        txbxv.insert('1.0', val)
                        txbxv.configure(state=DISABLED)
                        continue
                    case 'alpha':
                        width = 55
                        val = f'{value:.3f}'
                entv = CTkEntry(master=self, width=width)
                entv.grid(row=i+1, column=j)
                entv.insert(0, val)
                entv.configure(state=DISABLED)
