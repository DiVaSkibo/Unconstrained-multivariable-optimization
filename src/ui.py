from enum import Enum


class Theme(Enum): Dark, Light = 'dark', 'light'

class UI:
    '''
    **Налаштування інтерфейсу користувача**

    *Використання:*
        
        1. ui = UI(theme: str | Theme = Theme.Dark)
        2. ui.switch(theme: Theme = None)  # для перемикання теми
    
    Константи:
    
        FG - foreground
        BG - background
        GRAPH - graph color
        FONT_FAMILY - шрифт
        FONT_TITLE - шрифт головного тексту
        FONT_HEADER - шрифт заголовку
    '''
    theme = Theme.Dark
    FG = lambda self: '#ffffff' if self.theme == Theme.Dark else '#000000'
    BG = lambda self: '#131326' if self.theme == Theme.Dark else "#e5e5cc"
    GRAPH = lambda self: "#00ff99" if self.theme == Theme.Dark else "#5b00da"
    FONT_FAMILY = 'Georgia'
    FONT_TITLE = lambda self: (self.FONT_FAMILY, 28, 'bold')
    FONT_HEADER = lambda self: (self.FONT_FAMILY, 18, 'bold')

    def __init__(self, theme:Theme=Theme.Dark):
        self.theme = theme
    
    def switch(self, theme:Theme=None) -> Theme:
        '''Перемикання теми (Темна <-> Світла)'''
        if theme: self.theme = theme
        else:
            if self.theme == Theme.Dark: self.theme = Theme.Light
            else: self.theme = Theme.Dark
        return self.theme
    
