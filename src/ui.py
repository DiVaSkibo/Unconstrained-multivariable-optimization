from enum import Enum


class Theme(Enum): Dark, Light = 'dark', 'light'

class UI:
    '''
    **Налаштування інтерфейсу користувача**

    *Використання:*
        
        1. ui = UI(theme: str | Theme = Theme.Dark)
        2. ui.switch(theme: Theme = None)  # для перемикання теми
        3. ui.cwitch()  # для перемикання колорової-мапи
    
    Константи:
    
        FG - foreground
        BG - background
        BG_ACCENT - background для акценту
        DOT - колір точки на графіку
        DOT_ACCENT - колір ключової точки на графіку
        LINE - колір лінії на графіку
        LINE_ACCENT - колір ключової лінії на графіку
        FONT_FAMILY - шрифт
        FONT_TITLE - шрифт головного тексту
        FONT_HEADER - шрифт заголовку
        CMAPS - набір колорових-мап
    '''
    theme = Theme.Dark
    cmapi = 0
    cmap = lambda self: self.CMAPS[self.cmapi]
    FG = lambda self: '#E5E5FF' if self.theme == Theme.Dark else '#000000'
    FG_SHADOW = lambda self: '#606080' if self.theme == Theme.Dark else '#F2F2C2'
    BG = lambda self: '#181829' if self.theme == Theme.Dark else '#E5E5CC'
    BG_ACCENT = lambda self: '#111121' if self.theme == Theme.Dark else '#A6A67C'
    DOT = lambda self: '#5975FF' if self.theme == Theme.Dark else '#FF7559'
    DOT_ACCENT = lambda self: '#FFFF4D' if self.theme == Theme.Dark else '#4DF3FF'
    LINE = lambda self: '#5975FF' if self.theme == Theme.Dark else '#FF7559'
    LINE_ACCENT = lambda self: '#26FF6F' if self.theme == Theme.Dark else '#26FF6F'
    FONT_FAMILY = 'Georgia'
    FONT_TITLE = lambda self: (self.FONT_FAMILY, 28, 'bold')
    FONT_HEADER = lambda self: (self.FONT_FAMILY, 18, 'bold')
    CMAPS = ('Spectral', 'turbo', 'gnuplot2', 'hot', 'bone')

    def __init__(self, theme:Theme=Theme.Dark):
        self.theme = theme
    
    def switch(self, theme:Theme=None) -> Theme:
        '''Перемикання теми (Темна <-> Світла)'''
        if theme: self.theme = theme
        else:
            if self.theme == Theme.Dark: self.theme = Theme.Light
            else: self.theme = Theme.Dark
        return self.theme
    
    def cwitch(self) -> str:
        '''Перемикання колорової-мапи для графіку'''
        self.cmapi = (self.cmapi + 1) % len(self.CMAPS)
        return self.cmap()
