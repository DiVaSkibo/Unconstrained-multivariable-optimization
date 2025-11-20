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
    FG = lambda self: '#ffffff' if self.theme == Theme.Dark else '#000000'
    BG = lambda self: '#131326' if self.theme == Theme.Dark else '#e5e5cc'
    BG_ACCENT = lambda self: '#2A2A4A' if self.theme == Theme.Dark else '#B5B59A'
    DOT = lambda self: 'lightyellow' if self.theme == Theme.Dark else 'navy'
    DOT_ACCENT = lambda self: 'yellow' if self.theme == Theme.Dark else 'royalblue'
    LINE = lambda self: 'aquamarine' if self.theme == Theme.Dark else 'teal'
    LINE_ACCENT = lambda self: 'orangered' if self.theme == Theme.Dark else 'limegreen'
    FONT_FAMILY = 'Georgia'
    FONT_TITLE = lambda self: (self.FONT_FAMILY, 28, 'bold')
    FONT_HEADER = lambda self: (self.FONT_FAMILY, 18, 'bold')
    CMAPS = ('turbo', 'gnuplot2', 'hot', 'Spectral', 'bone')

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
