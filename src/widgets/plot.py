from customtkinter import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.collections import PathCollection
from matplotlib.lines import Line2D

from src.ui import *


class Plotview(CTkTabview):
  TABS = ('Плоский', 'Об\'ємний', 'Заповнений')
  
  def __init__(self, master, ui:UI, x, y, z, zlims, tabset:str=None, width = 300, height = 250, corner_radius = None, border_width = None, bg_color = "transparent", fg_color = None, border_color = None, segmented_button_fg_color = None, segmented_button_selected_color = None, segmented_button_selected_hover_color = None, segmented_button_unselected_color = None, segmented_button_unselected_hover_color = None, text_color = None, text_color_disabled = None, command = None, anchor = "center", state = "normal", **kwargs):
    super().__init__(master, width, height, corner_radius, border_width, bg_color, fg_color, border_color, segmented_button_fg_color, segmented_button_selected_color, segmented_button_selected_hover_color, segmented_button_unselected_color, segmented_button_unselected_hover_color, text_color, text_color_disabled, command, anchor, state, **kwargs)
    self.ui = ui
    
    self.Figures = {}
    self.Plots = {}
    self.dots = []
    self.lines = []
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
      self._plotTab(tab, x, y, z, zlims)
    self.set(tabset if tabset else self.TABS[0])
  
  def clear(self):
    self.dots.clear()
    self.lines.clear()
    for tab in self.TABS:
      for marker in [p for p in self.Plots[tab].collections if type(p) in (PathCollection, Line2D)]:
        marker.remove()

  def dot(self, x, z, color:str=None, is_accent=False):
    if not color:
      color = self.ui.DOT_ACCENT() if is_accent else self.ui.DOT()
    dot = {'x':x, 'z':z}
    isame = next(( i for i, d in enumerate(self.dots) if all(d[key] == dot[key] for key in dot)), -1)
    if isame == -1:
      dot['color'] = color
      self.dots.append(dot)
    else:
      self.dots[isame]['color'] = color
    for tab in self.TABS:
      match tab:
        case 'Плоский':
          self.Plots[tab].scatter(x[0], x[1], color=color, s=25, zorder=10)
        case 'Об\'ємний':
          self.Plots[tab].scatter(x[0], x[1], z, color=color, s=25, depthshade=False)
        case 'Заповнений':
          self.Plots[tab].scatter(x[0], x[1], color=color, s=25, zorder=10)
      self.Canvases[tab].draw()
  def line(self, x0, z0, x1, z1, color:str=None, is_accent=False):
    if not color:
      color = self.ui.LINE_ACCENT() if is_accent else self.ui.LINE()
    self.lines.append({'x0':x0, 'z0':z0, 'x1':x1, 'z1':z1, 'color':color})
    for tab in self.TABS:
      match tab:
        case 'Плоский':
          self.Plots[tab].plot([x0[0], x1[0]], [x0[1], x1[1]], color=color, linewidth=2, zorder=10)[0]
          self.Plots[tab].scatter(x0[0], x0[1], color=self.ui.DOT(), s=25, zorder=10)
          self.Plots[tab].scatter(x1[0], x1[1], color=self.ui.DOT(), s=25, zorder=10)
        case 'Об\'ємний':
          self.Plots[tab].plot([x0[0], x1[0]], [x0[1], x1[1]], [z0, z1], color=color, linewidth=2)[0]
          self.Plots[tab].scatter(x0[0], x0[1], z0, color=self.ui.DOT(), s=25, zorder=10)
          self.Plots[tab].scatter(x1[0], x1[1], z1, color=self.ui.DOT(), s=25, zorder=10)
        case 'Заповнений':
          self.Plots[tab].plot([x0[0], x1[0]], [x0[1], x1[1]], color=color, linewidth=2, zorder=10)[0]
          self.Plots[tab].scatter(x0[0], x0[1], color=self.ui.DOT(), s=25, zorder=10)
          self.Plots[tab].scatter(x1[0], x1[1], color=self.ui.DOT(), s=25, zorder=10)
      self.Canvases[tab].draw()
  
  def _plotTab(self, tab:str, x, y, z, zlims):
    '''Побудова графіку відповідно до вкладки'''
      # фігура
    self.Figures[tab] = Figure(figsize=(5, 5), dpi=100, constrained_layout=True, facecolor=self.ui.BG())
      # фабула, параметризація фабули
    match tab:
      case 'Плоский':
        self.Plots[tab] = self.Figures[tab].add_subplot(111, facecolor=self.ui.BG())
        self.Plots[tab].contour(x, y, z, levels=10, cmap=self.ui.cmap())
      case 'Об\'ємний':
        self.Plots[tab] = self.Figures[tab].add_subplot(111, projection='3d', facecolor=self.ui.BG())
        self.Plots[tab].set_zlim(zlims)
        self.Plots[tab].plot_surface(x, y, z, linewidth=0, cmap=self.ui.cmap(), alpha=.75, shade=False, axlim_clip=True)
        self.Plots[tab].xaxis.pane.set_facecolor(self.ui.BG())
        self.Plots[tab].yaxis.pane.set_facecolor(self.ui.BG())
        self.Plots[tab].zaxis.pane.set_facecolor(self.ui.BG())
      case 'Заповнений':
        self.Plots[tab] = self.Figures[tab].add_subplot(111, facecolor=self.ui.BG())
        self.Plots[tab].contourf(x, y, z, levels=10, cmap=self.ui.cmap(), alpha=.75)
    self.Plots[tab].tick_params(colors=self.ui.FG())
    self.Plots[tab].grid(color=self.ui.FG())
      # полотно
    self.Canvases[tab] = FigureCanvasTkAgg(self.Figures[tab], master=self.tab(tab))
    self.CanvasWidgets[tab] = self.Canvases[tab].get_tk_widget()
    self.CanvasWidgets[tab].configure(bg=self.ui.BG(), highlightthickness=0)
    self.CanvasWidgets[tab].pack(fill=BOTH, expand=True)
  
  def resize(self, x, y, z, zlims):
    for tab in self.TABS:
      self.Plots[tab].clear()
      match tab:
        case 'Плоский':
          self.Plots[tab].contour(x, y, z, levels=10, cmap=self.ui.cmap())
        case 'Об\'ємний':
          self.Plots[tab].set_zlim(zlims)
          self.Plots[tab].plot_surface(x, y, z, linewidth=0, cmap=self.ui.cmap(), shade=False)
          self.Plots[tab].xaxis.pane.set_facecolor(self.ui.BG())
          self.Plots[tab].yaxis.pane.set_facecolor(self.ui.BG())
          self.Plots[tab].zaxis.pane.set_facecolor(self.ui.BG())
        case 'Заповнений':
          self.Plots[tab].contourf(x, y, z, levels=10, cmap=self.ui.cmap())
      self.Plots[tab].tick_params(colors=self.ui.FG())
      self.Plots[tab].grid(color=self.ui.FG())
        # полотно
      self.Canvases[tab] = FigureCanvasTkAgg(self.Figures[tab], master=self.tab(tab))
      self.Canvases[tab].draw()
      self.CanvasWidgets[tab].destroy()
      self.CanvasWidgets[tab] = self.Canvases[tab].get_tk_widget()
      self.CanvasWidgets[tab].pack(fill=BOTH, expand=True)
    #for dot in self.dots: self.dot(dot['x'], dot['z'], dot['color'])
    #for line in self.lines: self.line(line['x0'], line['z0'], line['x1'], line['z1'], line['color'])
