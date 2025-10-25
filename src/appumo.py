import math
import numpy as np
from customtkinter import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image

from src.ui import *
from src.umo import UMO


class Appumo(CTk):
    '''
    **GUI - Багатовимірна Безумовна Оптимізація**

    *Використання:*
    
        1. appumo = Appumo(ui: UI = UI())
        2. ...
        3. appumo.recover() # після налаштування/редагування
        4. appumo.mainloop()
    '''
    def __init__(self, ui:UI=UI()):
        '''
        **GUI - Багатовимірна Безумовна Оптимізація**

        *Використання:*
        
            1. appumo = Appumo(ui: UI = UI())
            2. ...
            3. appumo.recover() # після налаштування/редагування
            4. appumo.mainloop()
        '''
        super().__init__()
        self.ui = ui
        self.title('Багатовимірна безумовна оптимізація')
        #self.geometry('1000x525+25+150')
        self.minsize(1000, 525)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        set_default_color_theme('style.json')
        self.switchTheme(self.ui.theme, False)
        self.configure(fg_color=self.ui.BG())
        self.build()
    
    def build(self):
        '''Будування додатку'''
        self._buildTitle()
        self._buildMain()
    def recover(self):
        '''Відновлення додатку'''
        self.configure(fg_color=self.ui.BG())
        self.frm_plot.destroy()
        self._buildPlot()
    
    def _buildTitle(self):
        '''Будування Титульної форми'''
        theme_png = Image.open('icons/theme.png')
        recover_png = Image.open('icons/recover.png')

        self.frm_title = CTkFrame(master=self)
        self.frm_title.grid(row=0, column=0, sticky=EW, padx=40, pady=30)
        
        CTkLabel(master=self.frm_title, text='БАГАТОВИМІРНА БЕЗУМОВНА ОПТИМІЗАЦІЯ', justify=CENTER, font=self.ui.FONT_TITLE()).pack(side=LEFT, fill=X, expand=True)
        # іконка відновлення
        icon = CTkImage(dark_image=recover_png, light_image=recover_png, size=(30, 30))
        btn = CTkButton(master=self.frm_title, command=self.recover, image=icon, text='', width=30, height=30)
        btn.pack(side=RIGHT)
        btn.image = icon
        # іконка теми
        icon = CTkImage(dark_image=theme_png, light_image=theme_png, size=(30, 30))
        btn = CTkButton(master=self.frm_title, command=self.switchTheme, image=icon, text='', width=30, height=30)
        btn.pack(side=RIGHT)
        btn.image = icon
    def _buildMain(self):
        '''Будування Головної форми'''
        self.frm_main = CTkFrame(master=self)
        self.frm_main.grid(row=1, column=0, sticky=NSEW, padx=25, pady=25)
        self.frm_main.rowconfigure(0, weight=1)
        self.frm_main.columnconfigure(1, weight=1)
        
        self._buildInput()
        self._buildPlot()
        self._buildTable()

    def _buildInput(self):
        '''Будування форми для Введення'''
        self.Fun = StringVar(value='5*x[0]**2 + 2*x[1]**2 + 4*x[0]*x[1] + 4*sqrt(5)*(x[0] + x[1]) - 14')
        self.X = [DoubleVar(value=.0), DoubleVar(value=.0)]
        self.Grad = [StringVar(value='10*x[0] + 4*x[1] + 4*sqrt(5)'), StringVar(value='4*x[0] + 4*x[1] + 4*sqrt(5)')]
        self.Hesse = [[StringVar(value='10'), StringVar(value='4')], [StringVar(value='4'), StringVar(value='4')]]
        self.Eps = DoubleVar(value=1e-3)
        
        self.frm_input = CTkFrame(master=self.frm_main)
        self.frm_input.grid(row=0, column=0, sticky=NW)
        
        # заголовок
        CTkLabel(master=self.frm_input, text='ВВЕДЕННЯ', font=self.ui.FONT_HEADER()).grid(row=0, column=0, columnspan=3, sticky=EW, pady=20)
        # функція
        CTkLabel(master=self.frm_input, text='Функція:', anchor=W).grid(row=1, column=0, columnspan=2, sticky=EW)
        CTkEntry(master=self.frm_input, textvariable=self.Fun).grid(row=2, column=0, columnspan=3, sticky=EW)
        # початкова точка
        CTkLabel(master=self.frm_input, text='Початкова точка:', anchor=E).grid(row=3, column=0, sticky=EW, pady=17)
        CTkEntry(master=self.frm_input, textvariable=self.X[0], width=36).grid(row=3, column=1)
        CTkEntry(master=self.frm_input, textvariable=self.X[1], width=36).grid(row=3, column=2, sticky=W)
        # градієнт
        CTkLabel(master=self.frm_input, text='Градієнт:', anchor=E).grid(row=4, column=0, rowspan=2, sticky=EW, pady=20)
        CTkEntry(master=self.frm_input, textvariable=self.Grad[0]).grid(row=4, column=1, columnspan=2, sticky=EW)
        CTkEntry(master=self.frm_input, textvariable=self.Grad[1]).grid(row=5, column=1, columnspan=2, sticky=EW)
        # гессе
        CTkLabel(master=self.frm_input, text='Гессе:', anchor=E).grid(row=7, column=0, rowspan=2, sticky=EW, pady=20)
        CTkEntry(master=self.frm_input, textvariable=self.Hesse[0][0], width=63).grid(row=7, column=1)
        CTkEntry(master=self.frm_input, textvariable=self.Hesse[0][1], width=63).grid(row=7, column=2)
        CTkEntry(master=self.frm_input, textvariable=self.Hesse[1][0], width=63).grid(row=8, column=1)
        CTkEntry(master=self.frm_input, textvariable=self.Hesse[1][1], width=63).grid(row=8, column=2)
        # точність
        CTkLabel(master=self.frm_input, text='Точність:', anchor=E).grid(row=10, column=0, sticky=EW, pady=17)
        CTkEntry(master=self.frm_input, textvariable=self.Eps, width=81).grid(row=10, column=1)
    def _buildTable(self):
        '''Будування форми для Таблиці'''
        self.frm_table = CTkFrame(master=self.frm_main)
        self.frm_table.grid(row=0, column=2, sticky=NE, padx=20)
        CTkLabel(master=self.frm_table, text='ТАБЛИЦЯ', font=self.ui.FONT_HEADER()).grid(row=0, column=0)
        
        CTkLabel(master=self.frm_table, text='ну скоро буде...').grid(row=1, column=0)
    def _buildPlot(self):
        '''Будування форми для Графіку'''
        self.frm_plot = CTkFrame(master=self.frm_main)
        self.frm_plot.grid(row=0, column=1, sticky=NSEW)
        
        fig = Figure(figsize=(5, 5), dpi=100, constrained_layout=True, facecolor=self.ui.BG())
        plot = fig.add_subplot(111, projection='3d', facecolor=self.ui.BG())
        
        namespace = {'sqrt':math.sqrt}
        exec('def _FUNC(x) -> float: return ' + self.Fun.get(), namespace)
        _FUNC = namespace['_FUNC']

        x = np.arange(-7.5, 7.5, .01)
        y = np.arange(-7.5, 7.5, .01)
        x, y = np.meshgrid(x, y)
        zlims = (-25, 25)
        z = np.array([_FUNC([xi, yi]) for (xi, yi) in zip(x, y)])
        z = np.where((z < zlims[0]) | (z > zlims[1]), np.nan, z)
        plot.set_zlim(zlims)
        
        plot.plot_surface(x, y, z, cmap='viridis', linewidth=0, antialiased=False)
        #plot.plot_wireframe(x, y, z, color=self.ui.GRAPH(), linewidth=0.6)
        plot.tick_params(colors=self.ui.FG())
        plot.xaxis.pane.set_facecolor(self.ui.BG())
        plot.yaxis.pane.set_facecolor(self.ui.BG())
        plot.zaxis.pane.set_facecolor(self.ui.BG())
        plot.grid(color=self.ui.FG())
        
        canvas = FigureCanvasTkAgg(fig, master=self.frm_plot)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.configure(bg=self.ui.BG(), highlightthickness=0)
        canvas_widget.pack(fill=BOTH, expand=True)
        canvas.draw()
    
    def switchTheme(self, theme:Theme=None, is_recover=True):
        '''Перемикання теми (Темна <-> Світла)'''
        set_appearance_mode(self.ui.switch(theme).value)
        if is_recover: self.recover()

