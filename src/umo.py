import math
import numpy as np


class UMO:
    '''
    **Unconstrained Multivariable Optimization** - *Багатовимірна Безумовна Оптимізація*
    '''

    def __init__(self, fun:callable, x:list=[.0, .0], grad:callable=None, eps:float=1e-2, maxiter=1000):
        self.fun = fun
        self.x = np.array(x)
        self.grad = grad
        self.eps = eps
        self.MAXITER = maxiter
        self.result = {'x':x, 'fun':fun(x)}
    
    def solve(self, method:str):
        '''
        *Оптимізація функції за методом:*
        
            Метод найшвидшого спуску -> "Steepest Descent"
        '''
        match method:
            case 'Steepest Descent':
                self.result = self._steepestDescent()
            case _:
                raise Exception('! Неправильне введення методу оптимізації !')
    
    def _steepestDescent(self) -> dict:
        '''Метод найшвидшого спуску'''
        x = self.x
        eps = self.eps
        alpha = 0
        for _ in range(self.MAXITER):
            if np.linalg.norm(self.grad(x)) < eps: break
            dx = -self.grad(x)
            alpha = self._armijo_line_search(x, dx)
            x += alpha * dx
        return {'x':x.tolist(), 'fun':self.fun(x).tolist(), 'dx':dx.tolist(), 'alpha':float(alpha)}
    
    
    def _armijo_line_search(self, x:list, dx:list, alpha:float=1., beta:float=0.5, const:float=1e-4):
        '''Лінійний пошук зі зменшенням кроку за правилом Арміхо'''
        f_x = self.fun(x)
        grad_x = self.grad(x)
        while self.fun(x + alpha * dx) > f_x + const * alpha * np.dot(grad_x, dx):
            alpha *= beta
        return alpha

