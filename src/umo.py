import math
import numpy as np


class UMO:
    '''Unconstrained Multivariable Optimization'''

    def __init__(self, fun:callable, x:list=[.0, .0], jac:callable=None, eps:float=1e-2):
        self.fun = fun
        self.x = np.array(x)
        self.jac = jac
        self.eps = eps
        self.result = {'x':x, 'fun':fun(x)}
    
    def solve(self, method:str):
        match method:
            case _: raise Exception('! Неправильне введення методу оптимізації !')
        
