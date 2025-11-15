import math
import numpy as np
import pandas as pd
from customtkinter import *

from src.umo import UMO
from src.ui import *
from src.appumo import Appumo
from src.widgets.table import Tableview


def fun(x) -> float:
    return 5. * x[0]**2 + 2. * x[1]**2 + 4. * x[0] * x[1] + 4. * math.sqrt(5.) * (x[0] + x[1]) - 14.
def grad(x) -> np.ndarray:
    return np.array([10. * x[0] + 4. * x[1] + 4. * math.sqrt(5.), 4. * x[0] + 4. * x[1] + 4. * math.sqrt(5.)])
def hesse(x) -> np.ndarray:
    return np.array([[10., 4.], [4., 4.]])


# БАГАТОВИМІРНА БЕЗУМОВНА ОПТИМІЗАЦІЯ

if __name__ == "__main__":
    print('\n|| UNCONSTRAINED MULTIVARIABLE OPTIMIZATION ||\n')
    
    panda = pd.DataFrame({
            'Aa':[11, 22, 33, 44, 55, 66],
            'Bb':[11, 22, 33, 44, 55, 66],
            'Cc':[111, 222, 333, 444, 555, 666],
            'Dd':[1111, 2222, 3333, 4444, 5555, 6666],
            'Ee':[11111, 22222, 33333, 44444, 55555, 66666]})
    
    root = CTk()
    set_default_color_theme('style.json')
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)
    
    def out(iteration:dict): print(iteration)
    tableview = Tableview(master=root, signal=out)
    tableview.grid(sticky=NSEW)
    tableview.panda(panda)
    
    root.mainloop()
    
    # appumo = Appumo(UMO(fun=fun, x=(.0, .0), grad=grad, hesse=hesse))
    # appumo.mainloop()
