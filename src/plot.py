from customtkinter import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from src.ui import *


class Plotview(CTkTabview):
  def __init__(self, master, ui:UI, x, y, z, zlims, width = 300, height = 250, corner_radius = None, border_width = None, bg_color = "transparent", fg_color = None, border_color = None, segmented_button_fg_color = None, segmented_button_selected_color = None, segmented_button_selected_hover_color = None, segmented_button_unselected_color = None, segmented_button_unselected_hover_color = None, text_color = None, text_color_disabled = None, command = None, anchor = "center", state = "normal", **kwargs):
    super().__init__(master, width, height, corner_radius, border_width, bg_color, fg_color, border_color, segmented_button_fg_color, segmented_button_selected_color, segmented_button_selected_hover_color, segmented_button_unselected_color, segmented_button_unselected_hover_color, text_color, text_color_disabled, command, anchor, state, **kwargs)
    self.ui = ui
    for tabi in range(1, 4):
        self._plotTab(tabi, x, y, z, zlims)
    self.set('tab-1')

  def _plotTab(self, tabi:int, x, y, z, zlims):
    '''Побудова графіку відповідно до вкладки'''
    self.add(f'tab-{tabi}')
    self.tab(f'tab-{tabi}').rowconfigure(0, weight=1)
    self.tab(f'tab-{tabi}').columnconfigure(0, weight=1)
      # фігура
    fig = Figure(figsize=(5, 5), dpi=100, constrained_layout=True, facecolor=self.ui.BG())
      # фабула, параметризація фабули
    match tabi:
        case 1:
            plot = fig.add_subplot(111, projection='3d', facecolor=self.ui.BG())
            plot.set_zlim(zlims)
            plot.plot_surface(x, y, z, cmap=self.ui.cmap(), linewidth=0, shade=False)
            plot.xaxis.pane.set_facecolor(self.ui.BG())
            plot.yaxis.pane.set_facecolor(self.ui.BG())
            plot.zaxis.pane.set_facecolor(self.ui.BG())
        case 2:
            plot = fig.add_subplot(111, facecolor=self.ui.BG())
            plot.contour(x, y, z, cmap=self.ui.cmap())
        case 3:
            plot = fig.add_subplot(111, facecolor=self.ui.BG())
            plot.contourf(x, y, z, cmap=self.ui.cmap())
    plot.tick_params(colors=self.ui.FG())
    plot.grid(color=self.ui.FG())
      # полотно
    canvas = FigureCanvasTkAgg(fig, master=self.tab(f'tab-{tabi}'))
    canvas.draw()
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.configure(bg=self.ui.BG(), highlightthickness=0)
    #canvas_widget.grid(sticky=NSEW)
    canvas_widget.pack(fill=BOTH, expand=True)
