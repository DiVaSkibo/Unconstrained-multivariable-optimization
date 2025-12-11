import math
import numpy as np
import pandas as pd
import inspect
from customtkinter import *
from PIL import Image

from src.ui import *
from src.umo import UMO
from src.widgets.table import Tableview
from src.widgets.plot import Plotview


class Appumo(CTk):
    '''
    **GUI - Багатовимірна Безумовна Оптимізація**

    *Використання:*
    
      1. appumo = Appumo(umo: UMO, ui: UI = UI())
      -. ...
      -. appumo.switchTheme(theme: Theme = None)
      -. appumo.switchColormap()
      -. appumo.recover()
      -. ...
      2. appumo.solve() | appumo.solveIgnored() # для solve бажано використовувати try except
      3. appumo.mainloop()
    '''
    def __init__(self, umo:UMO, ui:UI=UI()):
        '''
        **GUI - Багатовимірна Безумовна Оптимізація**

        *Використання:*
        
          1. appumo = Appumo(umo: UMO, ui: UI = UI())
          -. ...
          -. appumo.switchTheme(theme: Theme = None)
          -. appumo.switchColormap()
          -. appumo.recover()
          -. ...
          2. appumo.solve() | appumo.solveIgnored() # для solve бажано використовувати try except
          3. appumo.mainloop()
        '''
        super().__init__()
        self.umo = umo
        self.ui = ui
        self.tableveiw = None
        self.plotview = None
        self.title('Багатовимірна безумовна оптимізація')
        self.minsize(1000, 625)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        set_default_color_theme('style.json')
        self.configure(fg_color=self.ui.BG())
        self.build()
        self.switchTheme(theme=self.ui.theme, is_init=True)
        self.after(0, lambda:self.state('zoomed'))
    
    def build(self):
        '''Будування додатку'''
        self._buildTitle()
        self._buildMain()
    def recover(self):
        '''Відновлення додатку'''
        self.umo.fun = callexec('Function', self.Fun)
        x, y, z = self._axes()
        self.plotview.plot(x, y, z)
        self.plotview.recover()
        self.tableveiw.recover()
    
    def _buildTitle(self):
        '''Будування Титульної форми'''
        solve_png = Image.open('icons/solve.png')
        recover_png = Image.open('icons/recover.png')
        excel_png = Image.open('icons/excel.png')
        theme_png = Image.open('icons/theme.png')
        colormap_png = Image.open('icons/colormap.png')

        self.frm_title = CTkFrame(master=self)
        self.frm_title.grid(row=0, column=0, sticky=EW, padx=40, pady=30)
        
          # іконка розв'язку
        icon = CTkImage(dark_image=solve_png, light_image=solve_png, size=(22, 22))
        btn = CTkButton(master=self.frm_title, command=self.solveIgnored, image=icon, text='', width=30, height=30)
        btn.pack(side=LEFT)
        btn.image = icon
          # іконка відновлення
        icon = CTkImage(dark_image=recover_png, light_image=recover_png, size=(30, 30))
        btn = CTkButton(master=self.frm_title, command=self.recover, image=icon, text='', width=30, height=30)
        btn.pack(side=LEFT)
        btn.image = icon
          # іконка ексель файлу
        icon = CTkImage(dark_image=excel_png, light_image=excel_png, size=(30, 30))
        btn = CTkButton(master=self.frm_title, command=self.xlsx, image=icon, text='', width=30, height=30)
        btn.pack(side=LEFT)
        btn.image = icon
          # заголовок
        CTkLabel(master=self.frm_title, text='БАГАТОВИМІРНА БЕЗУМОВНА ОПТИМІЗАЦІЯ', justify=CENTER, font=self.ui.FONT_TITLE()).pack(side=LEFT, fill=X, expand=True)
          # іконка теми
        icon = CTkImage(dark_image=theme_png, light_image=theme_png, size=(30, 30))
        btn = CTkButton(master=self.frm_title, command=self.switchTheme, image=icon, text='', width=30, height=30)
        btn.pack(side=RIGHT)
        btn.image = icon
          # іконка кольорової-мапи
        icon = CTkImage(dark_image=colormap_png, light_image=colormap_png, size=(20, 20))
        btn = CTkButton(master=self.frm_title, command=self.switchColormap, image=icon, text='', width=30, height=30)
        btn.pack(side=RIGHT)
        btn.image = icon
    def _buildMain(self):
        '''Будування Головної форми'''
        self.frm_main = CTkFrame(master=self)
        self.frm_main.grid(row=1, column=0, sticky=NSEW, padx=25, pady=15)
        self.frm_main.rowconfigure(0, weight=1)
        self.frm_main.columnconfigure(1, weight=1)

          # створення змінних для програми
        funstr = inspect.getsource(self.umo.fun)
        funstr = funstr[funstr.find('return ') + 7:]
        funstr = funstr.replace('math.', '').replace(' * ', '*').replace(' ** ', '**')
        if self.umo.grad:
            gradstr = inspect.getsource(self.umo.grad)
            gradstr = gradstr[gradstr.find('np.array') + 10:-3]
            gradstr = gradstr.replace('math.', '').replace(' * ', '*').replace(' ** ', '**')
            gradstr = gradstr.split(', ')
        else: gradstr = ['', '']
        if self.umo.hesse:
            hessestr = inspect.getsource(self.umo.hesse)
            hessestr = hessestr[hessestr.find('np.array') + 11:-4]
            hessestr = hessestr.replace('math.', '').replace(' * ', '*').replace(' ** ', '**').replace('[', '').replace(']', '')
            hessestr = hessestr.split(', ')
        else: hessestr = ['', '', '', '']

        self.Method = StringVar(value=None)
        self.Fun = StringVar(value=funstr)
        self.X = [DoubleVar(value=self.umo.x[0]), DoubleVar(value=self.umo.x[1])]
        self.Grad = [StringVar(value=gradstr[0]), StringVar(value=gradstr[1])]
        self.Hesse = [[StringVar(value=hessestr[0]), StringVar(value=hessestr[1])], [StringVar(value=hessestr[2]), StringVar(value=hessestr[3])]]
        self.Eps = DoubleVar(value=self.umo.EPS)
        
        self.Offset = (DoubleVar(value=.0), DoubleVar(value=.0), DoubleVar(value=.0))
        self.Scale = DoubleVar(value=5.)
        
          # будування підформ
        self._buildInput()
        self._buildPlot()
        self._buildTable()
    
    def _buildInput(self):
        '''Будування форми для Введення'''
        self.frm_input = CTkFrame(master=self.frm_main)
        self.frm_input.grid(row=0, column=0, sticky=NW)
        self.frm_input.rowconfigure((3, 9), minsize=10)
        
          # заголовок
        CTkLabel(master=self.frm_input, text='ВВЕДЕННЯ', font=self.ui.FONT_HEADER()).grid(row=0, column=0, columnspan=3, sticky=EW, pady=10)
          # метод
        CTkLabel(master=self.frm_input, text='Метод:', anchor=W).grid(row=1, column=0, columnspan=2, sticky=EW)
        CTkOptionMenu(master=self.frm_input, values=UMO.METHODS, variable=self.Method).grid(row=2, column=0, columnspan=3, sticky=EW)
          # функція
        CTkLabel(master=self.frm_input, text='Функція:', anchor=W).grid(row=4, column=0, columnspan=2, sticky=EW)
        CTkEntry(master=self.frm_input, textvariable=self.Fun).grid(row=5, column=0, columnspan=3, sticky=EW)
          # початкова точка
        CTkLabel(master=self.frm_input, text='Початкова точка:', anchor=E).grid(row=6, column=0, sticky=EW, pady=30)
        CTkEntry(master=self.frm_input, textvariable=self.X[0], width=36).grid(row=6, column=1)
        CTkEntry(master=self.frm_input, textvariable=self.X[1], width=36).grid(row=6, column=2, sticky=W)
          # градієнт
        CTkLabel(master=self.frm_input, text='Градієнт:', anchor=E).grid(row=7, column=0, rowspan=2, sticky=EW, padx=20, pady=20)
        CTkEntry(master=self.frm_input, textvariable=self.Grad[0]).grid(row=7, column=1, columnspan=2, sticky=EW)
        CTkEntry(master=self.frm_input, textvariable=self.Grad[1]).grid(row=8, column=1, columnspan=2, sticky=EW)
          # гессе
        CTkLabel(master=self.frm_input, text='Гессе:', anchor=E).grid(row=10, column=0, rowspan=2, sticky=EW, padx=10, pady=20)
        CTkEntry(master=self.frm_input, textvariable=self.Hesse[0][0], width=63).grid(row=10, column=1)
        CTkEntry(master=self.frm_input, textvariable=self.Hesse[0][1], width=63).grid(row=10, column=2)
        CTkEntry(master=self.frm_input, textvariable=self.Hesse[1][0], width=63).grid(row=11, column=1)
        CTkEntry(master=self.frm_input, textvariable=self.Hesse[1][1], width=63).grid(row=11, column=2)
          # точність
        CTkLabel(master=self.frm_input, text='Точність:', anchor=E).grid(row=12, column=0, sticky=EW, padx=20, pady=30)
        CTkEntry(master=self.frm_input, textvariable=self.Eps, width=81).grid(row=12, column=1)
    def _buildTable(self):
        '''Будування форми для Таблиці'''
        def on_iter_changed(it):
            self.plotview.route(path=list(self.umo.table.T.to_dict().values()), curloc=it, is_init=False)
            self.plotview.draw()
        
        self.frm_table = CTkFrame(master=self.frm_main)
        self.frm_table.grid(row=0, column=2, sticky=NW)
        self.frm_table.rowconfigure(1, weight=1)
        
          # заголовок
        CTkLabel(master=self.frm_table, text='ТАБЛИЦЯ', font=self.ui.FONT_HEADER()).grid(row=0, column=0, sticky=EW, pady=10)
          # таблиця
        self.tableveiw = Tableview(master=self.frm_table, ui=self.ui, signal=on_iter_changed, bg_color='red')
        self.tableveiw.grid(row=1, column=0, sticky=NSEW)
    def _buildPlot(self, tab:str=None):
        '''Будування форми для Графіку'''
        def on_plot_resize(_):
            x, y, z = self._axes()
            self.plotview.plot(x, y, z)
        
        self.frm_plot = CTkFrame(master=self.frm_main)
        self.frm_plot.grid(row=0, column=1, sticky=NSEW)
        self.frm_plot.rowconfigure(0, weight=1)
        self.frm_plot.columnconfigure(0, weight=1)
        self.frm_plot.rowconfigure(3, minsize=10)
        
          # дані
        x, y, z = self._axes()
          # фабула з вкладками
        self.plotview = Plotview(master=self.frm_plot, ui=self.ui, x=x, y=y, z=z, tabset=tab)
        self.plotview.grid(row=0, column=0, sticky=NSEW)
          # слайдери
        CTkSlider(self.frm_plot, command=on_plot_resize, from_=-20., to=20., number_of_steps=40, variable=self.Offset[0], orientation=HORIZONTAL, height=10).grid(row=1, column=0, pady=4)
        CTkSlider(self.frm_plot, command=on_plot_resize, from_=-20., to=20., number_of_steps=40, variable=self.Offset[1], orientation=VERTICAL, width=10).grid(row=0, column=1, padx=4)
        CTkSlider(self.frm_plot, command=on_plot_resize, from_=-40., to=40., number_of_steps=80, variable=self.Offset[2], orientation=VERTICAL, width=10).grid(row=0, column=2, padx=4)
        CTkSlider(self.frm_plot, command=on_plot_resize, from_=10., to=.5, number_of_steps=20, variable=self.Scale, orientation=HORIZONTAL, height=10).grid(row=2, column=0, pady=4)
    
    def solve(self, method:str=None):
        '''Розрахунок задачі'''
        if not method: method = self.Method.get()
        if method not in UMO.METHODS: raise Exception(f'? Appumo.solve: unknown method "{method}"')
        else: self.Method.set(method)

          # підготовка даних
        try:
            self.umo.x = tuple(x.get() for x in self.X)
            self.umo.fun = callexec('Function', self.Fun)
            self.umo.grad = callexec('Gradient', self.Grad)
            self.umo.hesse = callexec('Hesse', self.Hesse)
            try: self.umo.EPS = self.Eps.get()
            except Exception: raise Exception('[Epsilon]')
        except Exception as exc:
            raise Exception(f'? Appumo.solve: incorrect input in {exc}')
          # розв'язок
        try: self.umo.solve(method)
        except Exception: raise Exception('! Appumo.solve: umo.solve error')
          # виведення результату
        x, y, z = self._axes()
        self.umo.displayResult()
        self.tableveiw.panda(self.umo.table)
        self.plotview.plot(x, y, z)
        self.plotview.route(path=list(self.umo.table.T.to_dict().values()))
        self.plotview.draw()
    def solveIgnored(self):
        '''Безпечний розрахунок задачі'''
        try: self.solve()
        except Exception as exc: print(exc)
    
    def xlsx(self, path:str=None):
        if not path: path = f'UMO - {self.Method.get()}'
        writer = pd.ExcelWriter(f'{path}.xlsx')
        self.umo.table.to_excel(writer, sheet_name=self.Method.get())
        writer._save()
    
    def _axes(self) -> tuple:
        '''Значення X, Y, Z'''
        offset = (self.Offset[0].get(), self.Offset[1].get(), self.Offset[2].get())
        scale = self.Scale.get()
        xmin, xmax = offset[0] - scale, offset[0] + scale
        ymin, ymax = offset[1] - scale, offset[1] + scale
        zmin, zmax = offset[2] - 5 * scale, offset[2] + 5 * scale
        x = np.arange(xmin, xmax, abs(xmax - xmin) / 100)
        y = np.arange(ymin, ymax, abs(xmax - xmin) / 100)
        x, y = np.meshgrid(x, y)
        z = np.array([self.umo.fun([xi, yi]) for (xi, yi) in zip(x, y)])
        z = np.where((z < zmin) | (z > zmax), np.nan, z)
        return x, y, z
    
    def switchTheme(self, theme:Theme=None, is_init:bool=False):
        '''Перемикання теми (Темна <-> Світла)'''
        set_appearance_mode(self.ui.switch(theme).value)
        self.configure(fg_color=self.ui.BG())
        if not is_init: self.plotview.recover()
        self.tableveiw.recover()
    def switchColormap(self):
        '''Перемикання кольорової-мапи'''
        self.ui.cwitch()
        self.plotview.cmap()
        self.plotview.draw()

def callexec(what:str, line:str|list) -> callable:
    namespace = {'sqrt':math.sqrt, 'np':np}
    match what:
        case 'Function':
            call = line.get()
            if not call: raise Exception('[Function]')
            ckey = '_FUNC'
            call = 'def ' + ckey + '(x) -> float: return ' + call
        case 'Gradient':
            call = (line[0].get(), line[1].get())
            if not call[0] or not call[1]: raise Exception('[Gradient]')
            ckey = '_GRAD'
            call = 'def ' + ckey + '(x) -> np.ndarray: return np.array([' + call[0] + ', ' + call[1] + '])'
        case 'Hesse':
            call = (line[0][0].get(), line[0][1].get(), line[1][0].get(), line[1][1].get())
            if not call[0] or not call[1] or not call[2] or not call[3]: raise Exception('[Hesse]')
            ckey = '_HESSE'
            call = 'def ' + ckey + '(x) -> np.ndarray: return np.array([[' + call[0] + ', ' + call[1] + '], [' + call[2] + ', ' + call[3] + ']])'
        case _:
            raise Exception('[?]')
    exec(call, namespace)
    return namespace[ckey]
