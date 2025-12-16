import pandas as pd
from customtkinter import *
from PIL import Image

from src.ui import *


class Tableview(CTkScrollableFrame):
    '''
    *Віджет відображення таблиць*
    '''
    def __init__(self, master, ui:UI, signal:callable=None, width = 600, height = 600, corner_radius = None, border_width = None, bg_color = 'transparent', fg_color = None, border_color = None, background_corner_colors = None, overwrite_preferred_drawing_method = None, **kwargs):
        '''
        *Віджет відображення таблиць*
        '''
        super().__init__(master, width, height, corner_radius, border_width, bg_color, fg_color, border_color, background_corner_colors, overwrite_preferred_drawing_method, **kwargs)
        self.ui = ui
        self.signal = signal

        self.table = None
        self.Iter = IntVar(value=0)
        self.tabs = []
    
    def clear(self):
        '''Очищення від клітинок'''
        self.table = None
        self.tabs = []
        for child in self.winfo_children():
            child.destroy()
    def recover(self):
        '''Відновлення віджету'''
        for tab in self.tabs:
            tab.configure(fg_color=self.ui.BG_ACCENT(), text_color=self.ui.FG_SHADOW())
    
    def iteration(self) -> dict:
        '''Поточна ітерація'''
        return self.table.iloc[self.Iter.get()].to_dict()

    def panda(self, table:pd.DataFrame):
        '''Побудова таблиці'''
        def on_radio_changed():
            if self.signal: self.signal(self.iteration())
            else: self.iteration()
        def on_next():
            self.Iter.set((self.Iter.get() + 1) % len(self.table.values))
            on_radio_changed()
        
        self.clear()
        self.table = table
        self._parent_canvas.yview_moveto(0.0)
          # іконка наступної ітерації
        next_png = Image.open('icons/next.png')
        icon = CTkImage(dark_image=next_png, light_image=next_png, size=(15, 15))
        btn = CTkButton(master=self, command=on_next, image=icon, text='', width=15, height=15)
        btn.grid(padx=1.6, sticky=W)
        btn.image = icon
        
        self.tabs = []
          # побудова заголовків
        for j, key in zip(range(len(self.table.keys())), self.table.keys()):
            if key == 'method': continue
            match key:
                case 'x':
                    lable = 'Точка'
                    width = 130
                case 'grad':
                    lable = 'Градієнт'
                    width = 130
                case 'fun':
                    lable = 'Функція'
                    width = 75
                case 'simplex':
                    lable = 'Симплекс'
                    width = 135
                case 'fsimplex':
                    lable = 'Функції симплексу'
                    width = 80
                case 'gnorm':
                    lable = 'Нормаль градієнту'
                    width = 75
                case 'hesse':
                    lable = 'Гессе'
                    width = 135
                case 'delta':
                    lable = 'Крок'
                    width = 60
                case 'alpha':
                    lable = 'Альфа'
                    width = 60
            self.tabs.append(CTkEntry(master=self, width=width, fg_color=self.ui.BG_ACCENT(), text_color=self.ui.FG_SHADOW()))
            self.tabs[-1].grid(row=0, column=j)
            self.tabs[-1].insert(0, lable)
            self.tabs[-1].configure(state=DISABLED)
          # побудова клітинок
        for i, row in self.table.iterrows():
            CTkRadioButton(master=self, value=i, variable=self.Iter, command=on_radio_changed, text=f'{i}', width=40, height=20, radiobutton_width=15, radiobutton_height=15).grid(row=i+1, column=0, padx=6, pady=3, sticky=N)
            for j, value in zip(range(len(row)), row):
                if type(value) is str: continue
                match self.table.keys()[j]:
                    case 'x' | 'grad':
                        width = 130
                        val = '\t'.join([f'{v:.3f}' for v in value])
                    case 'fun' | 'gnorm':
                        width = 75
                        val = f'{value:.3f}'
                    case 'simplex':
                        width = 135
                        val = f'{'\n'.join(['\t'.join([f'{v:.3f}' for v in vs]) for vs in value])}'
                        txbxv = CTkTextbox(master=self, width=width, height=67)
                        txbxv.grid(row=i+1, column=j, sticky=N)
                        txbxv.insert('1.0', val)
                        txbxv.configure(state=DISABLED)
                        continue
                    case 'fsimplex':
                        width = 80
                        val = '\n'.join([f'{v:.3f}' for v in value])
                        txbxv = CTkTextbox(master=self, width=width, height=67)
                        txbxv.grid(row=i+1, column=j, sticky=N)
                        txbxv.insert('1.0', val)
                        txbxv.configure(state=DISABLED)
                        continue
                    case 'hesse':
                        width = 135
                        val = [v for vv in value for v in vv]
                        val = '\t'.join([f'{v:.3f}' for v in val])
                        val = f'{'\t'.join([f'{v:.3f}' for v in value[0]])}\n{'\t'.join([f'{v:.3f}' for v in value[1]])}'
                        txbxv = CTkTextbox(master=self, width=width, height=50)
                        txbxv.grid(row=i+1, column=j, sticky=N)
                        txbxv.insert('1.0', val)
                        txbxv.configure(state=DISABLED)
                        continue
                    case 'alpha' | 'delta':
                        width = 60
                        val = f'{value:.3f}'
                entv = CTkEntry(master=self, width=width)
                entv.grid(row=i+1, column=j, sticky=N)
                entv.insert(0, val)
                entv.configure(state=DISABLED)

        self.Iter.set(0)
        on_radio_changed()
