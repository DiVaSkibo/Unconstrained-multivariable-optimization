import math
import numpy as np
from numpy import linalg as LA


class UMO:
    '''
    **Unconstrained Multivariable Optimization** - *Багатовимірна Безумовна Оптимізація*
    '''

    def __init__(self, fun:callable, x:tuple=(.0, .0), grad:callable=None, eps:float=1e-3, maxiter=1000):
        self.fun = fun
        self.x = np.array(x, dtype=float)
        self.grad = grad
        self.eps = eps
        self.MAXITER = maxiter
        self.result = None
    
    def solve(self, method:str):
        '''
        Оптимізація функції за методом:
        
            Метод найшвидшого спуску -> "Steepest Descent"
            Метод спряжених градієнтів -> "Conjugate Gradient"
        '''
        self.result = None
        match method:
            case 'Steepest Descent':
                self.result = self._steepestDescent()
            case 'Conjugate Gradient':
                self.result = self._conjugateGradient()
            case _:
                raise Exception('! Неправильне введення методу оптимізації !')
    
    def _steepestDescent(self) -> dict:
        '''Метод найшвидшого спуску'''
        x = self.x.copy()
        eps = self.eps
        alpha = .0
        i = 0
        for i in range(self.MAXITER):
            if LA.norm(self.grad(x)) < eps: break
            dx = -self.grad(x)
            alpha = self._armijo_line_search(x, dx)
            x += alpha * dx
        return {'x':x.tolist(), 'fun':self.fun(x), 'dx':dx.tolist(), 'alpha':float(alpha), 'iter':i}
    def _conjugateGradient(self) -> dict:
        '''Метод спряжених градієнтів'''
        x = self.x.copy()
        eps = self.eps
        alpha = .0
        dx = -self.grad(x)
        gradient = LA.norm(self.grad(x))
        i = 0
        for i in range(self.MAXITER):
            if gradient < eps: break
            alpha = self._armijo_line_search(x, dx)
            x += alpha * dx
            gradnew = LA.norm(self.grad(x))
            beta = (gradnew ** 2) / (gradient * gradient)
            dx = dx * beta - self.grad(x)
            gradient = gradnew
        return {'x':x.tolist(), 'fun':self.fun(x), 'dx':dx.tolist(), 'alpha':float(alpha), 'grad':float(gradient), 'iter':i}
    
    
    def _armijo_line_search(self, x, dx, alpha:float=1., beta:float=0.5, const:float=1e-4):
        '''Лінійний пошук зі зменшенням кроку за правилом Арміхо'''
        f_x = self.fun(x)
        grad_x = self.grad(x)
        while self.fun(x + alpha * dx) > f_x + const * alpha * np.dot(grad_x, dx):
            alpha *= beta
        return alpha

