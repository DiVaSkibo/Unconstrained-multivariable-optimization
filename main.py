import math
import pandas as pd
import numpy as np

from src.umo import UMO
from src.ui import *
from src.appumo import Appumo


def fun(x) -> float:
    return 5. * x[0]**2 + 2. * x[1]**2 + 4. * x[0] * x[1] + 4. * math.sqrt(5.) * (x[0] + x[1]) - 14.
def grad(x) -> np.ndarray:
    return np.array([10. * x[0] + 4. * x[1] + 4. * math.sqrt(5.), 4. * x[0] + 4. * x[1] + 4. * math.sqrt(5.)])
def hesse(x) -> np.ndarray:
    return np.array([[10., 4.], [4., 4.]])


# БАГАТОВИМІРНА БЕЗУМОВНА ОПТИМІЗАЦІЯ

if __name__ == "__main__":
    print('\n|| UNCONSTRAINED MULTIVARIABLE OPTIMIZATION ||\n')

    umo = UMO(fun=fun, x=(.0, .0), grad=grad, hesse=hesse)
    writer = pd.ExcelWriter('Table.xlsx')
    for meth in umo.METHODS:
        method = umo.METHODS[meth]
        umo.solve(method)
        #umo.displayResult()
        umo.table.to_excel(writer, sheet_name=meth)
    writer._save()
