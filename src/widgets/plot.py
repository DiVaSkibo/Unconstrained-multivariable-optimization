from customtkinter import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.contour import QuadContourSet
from matplotlib.collections import PathCollection
from mpl_toolkits.mplot3d.art3d import (Poly3DCollection, Path3DCollection)

from src.ui import *


class Plotview(CTkTabview):
    '''
    *Віджет відображення графіків*
    '''
    
    TABS = ('Заповнений', 'Об\'ємний', 'Плоский')

    def __init__(self, master, ui:UI, x, y, z, tabset:str=None, width = 300, height = 250, corner_radius = None, border_width = None, bg_color = "transparent", fg_color = None, border_color = None, segmented_button_fg_color = None, segmented_button_selected_color = None, segmented_button_selected_hover_color = None, segmented_button_unselected_color = None, segmented_button_unselected_hover_color = None, text_color = None, text_color_disabled = None, command = None, anchor = "center", state = "normal", **kwargs):
        '''
        *Віджет відображення графіків*
        '''
        super().__init__(master, width, height, corner_radius, border_width, bg_color, fg_color, border_color, segmented_button_fg_color, segmented_button_selected_color, segmented_button_selected_hover_color, segmented_button_unselected_color, segmented_button_unselected_hover_color, text_color, text_color_disabled, command, anchor, state, **kwargs)
        self.ui = ui
        self.accent = None

        self.Figures = {}
        self.Plots = {}
        self.Canvases = {}
        self.CanvasWidgets = {}

        for tab in self.TABS:
            self.add(tab)
            self.tab(tab).rowconfigure(0, weight=1)
            self.tab(tab).columnconfigure(0, weight=1)
            self.Figures[tab] = None
            self.Plots[tab] = None
            self.Canvases[tab] = None
            self.CanvasWidgets[tab] = None
            self._buildTab(tab, x, y, z)
        self.set(tabset if tabset else self.TABS[0])

    def draw(self):
        '''Малювання полотен'''
        for tab in self.TABS:
            self.Canvases[tab].draw()
    def recover(self):
        '''Відновлення віджету'''
        for tab in self.TABS:
            self.paint(tab)
            self.Canvases[tab].draw()
    def plot(self, x, y, z):
        '''Малювання функції'''
        for tab in self.TABS:
            self.contour(tab, x, y, z)
            self.cmap(tab)
            self.Canvases[tab].draw()
    def clear(self):
        '''Очищення точок, ліній полотен'''
        for tab in self.TABS:
              # точки
            for dot in [p for p in self.Plots[tab].collections if type(p) in (PathCollection, Path3DCollection)]:
                dot.remove()
              # лінії
            for line in self.Plots[tab].lines:
                line.remove()
    
    def dot(self, x, z, color:str=None, is_accent=False):
        '''Малювання точки'''
        if not color: color = self.ui.DOT_ACCENT() if is_accent else self.ui.DOT()
        marker = 'X' if is_accent else '.'
        for tab in self.TABS:
            match tab:
                case 'Плоский' | 'Заповнений':
                    self.Plots[tab].scatter(x[0], x[1], color=color, marker=marker, s=75 if is_accent else 25, zorder=31)
                case 'Об\'ємний':
                    self.Plots[tab].scatter(x[0], x[1], z, color=color, marker=marker, s=75 if is_accent else 25, zorder=31, depthshade=False)
    def line(self, x0, z0, x1, z1, is_accent=False):
        '''Малювання лінії'''
        color = self.ui.LINE_ACCENT() if is_accent else self.ui.LINE()
        linewidth = 3 if is_accent else 2
        zorder = 11 if is_accent else 10
        for tab in self.TABS:
            match tab:
                case 'Плоский' | 'Заповнений':
                    self.Plots[tab].plot([x0[0], x1[0]], [x0[1], x1[1]], c=color, marker='.', ms=10, mfc=self.ui.DOT(), lw=linewidth, zorder=zorder)
                case 'Об\'ємний':
                    self.Plots[tab].plot([x0[0], x1[0]], [x0[1], x1[1]], [z0, z1], c=color, marker='.', ms=10, mfc=self.ui.DOT(), lw=linewidth)
    def route(self, path:dict, curloc=None, is_init=True):
        '''Малювання маршруту'''
        if is_init:
            self.clear()
            self.accent = 0
            self.dot(path[0]['x'], path[0]['fun'], is_accent=True)
              # лінії
            for i in range(len(path) - 1):
                loc0 = path[i]
                loc1 = path[i + 1]
                self.line(loc0['x'], loc0['fun'], loc1['x'], loc1['fun'])
        else:
            self.accent = path.index(curloc) if curloc else 0
            for tab in self.TABS:
                  # точки
                dots = [p for p in self.Plots[tab].collections if type(p) in (PathCollection, Path3DCollection)]
                for dot in dots:
                    dot.remove()
                  # лінії
                lines = self.Plots[tab].lines
                for i, line in zip(range(len(lines)), lines):
                    is_accent = i+1 == self.accent
                    line.set_color(self.ui.LINE_ACCENT() if is_accent else self.ui.LINE())
                    line.set_linewidth(3 if is_accent else 2)
                    line.set_markerfacecolor(self.ui.DOT())
                    if tab in ('Плоский', 'Заповнений'):
                        line.set_zorder(11 if is_accent else 10)
              # акцентова точка
            self.dot(curloc['x'], curloc['fun'], is_accent=True)
    def contour(self, tab:str, x, y, z):
        '''Малювання контору, поверхні'''
        for con in [p for p in self.Plots[tab].collections if type(p) in (QuadContourSet, Poly3DCollection)]:
            con.remove()
        self.Plots[tab].set_xlim((x[0][0], x[-1][-1]))
        self.Plots[tab].set_ylim((y[0][0], y[-1][-1]))
        match tab:
            case 'Плоский':
                self.Plots[tab].contour(x, y, z, levels=15)
            case 'Заповнений':
                self.Plots[tab].contourf(x, y, z, levels=15, alpha=.75)
            case 'Об\'ємний':
                self.Plots[tab].plot_surface(x, y, z, linewidth=0, cmap='viridis', alpha=.75, shade=False, axlim_clip=True)

    def paint(self, tab:str):
        '''Фарбування'''
        self.Figures[tab].set_facecolor(self.ui.BG())

        self.Plots[tab].set_facecolor(self.ui.BG())
        if tab == 'Об\'ємний':
            self.Plots[tab].xaxis.pane.set_facecolor(self.ui.BG())
            self.Plots[tab].yaxis.pane.set_facecolor(self.ui.BG())
            self.Plots[tab].zaxis.pane.set_facecolor(self.ui.BG())
        self.Plots[tab].tick_params(colors=self.ui.FG())
        self.Plots[tab].grid(color=self.ui.FG())
        
          # точки
        for dot in [p for p in self.Plots[tab].collections if type(p) in (PathCollection, Path3DCollection)]:
            dot.set_color(self.ui.DOT_ACCENT() if dot.zorder > 20 else self.ui.DOT())
          # лінії
        lines = self.Plots[tab].lines
        for i, line in zip(range(len(lines)), lines):
            line.set_color(self.ui.LINE_ACCENT() if i+1 == self.accent else self.ui.LINE())
            line.set_markerfacecolor(self.ui.DOT())
        
        self.CanvasWidgets[tab].configure(bg=self.ui.BG(), highlightthickness=0)
    def cmap(self, tab:str=None):
        '''Кольорова-мапа'''
        if tab:
            for con in [p for p in self.Plots[tab].collections if type(p) in (QuadContourSet, Poly3DCollection)]:
                con.set_cmap(self.ui.cmap())
        else:
            for tab in self.TABS:
                for con in [p for p in self.Plots[tab].collections if type(p) in (QuadContourSet, Poly3DCollection)]:
                    con.set_cmap(self.ui.cmap())
    
    def _buildTab(self, tab:str, x, y, z):
        '''Побудова вкладки'''
          # фігура
        self.Figures[tab] = Figure(figsize=(5, 5), dpi=100, constrained_layout=True, facecolor=self.ui.BG())
          # фабула, параметризація фабули
        self.Plots[tab] = self.Figures[tab].add_subplot(111, projection='3d' if tab == 'Об\'ємний' else 'rectilinear', facecolor=self.ui.BG())
        self.contour(tab, x, y, z)
        self.cmap(tab)
          # полотно
        self.Canvases[tab] = FigureCanvasTkAgg(self.Figures[tab], master=self.tab(tab))
        self.Canvases[tab].draw()
        self.CanvasWidgets[tab] = self.Canvases[tab].get_tk_widget()
        self.CanvasWidgets[tab].configure(bg=self.ui.BG(), highlightthickness=0)
        self.CanvasWidgets[tab].pack(fill=BOTH, expand=True)

        self.paint(tab)
