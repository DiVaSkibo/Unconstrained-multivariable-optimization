import math
import numpy as np
from numpy import linalg as LA


class UMO:
    '''
    **Unconstrained Multivariable Optimization** - *Багатовимірна Безумовна Оптимізація*
    '''

    def __init__(self, fun:callable, x:tuple=(.0, .0), grad:callable=None, hesse:callable=None, eps:float=1e-3, maxiter=1000):
        self.fun = fun
        self.x = np.array(x, dtype=float)
        self.grad = grad
        self.hesse = hesse
        self.EPS = eps
        self.MAXITER = maxiter
        self.result = None
    
    def solve(self, method:str):
        '''
        Оптимізація функції за методом:
        
            Метод найшвидшого спуску    ->  "Steepest Descent"
            Метод спряжених градієнтів  ->  "Conjugate Gradient"
            Метод Ньютона               ->  "Newton"
        '''
        self.result = None
        match method:
            case 'Steepest Descent':
                self.result = self._steepestDescent()
            case 'Conjugate Gradient':
                self.result = self._conjugateGradient()
            case 'Newton':
                self.result = self._newton()
            case _:
                raise Exception('! Неправильне введення методу оптимізації !')
    
    def _steepestDescent(self) -> dict:
        '''Метод найшвидшого спуску'''
        x = self.x.copy()
        EPS = self.EPS
        alpha = .0
        i = 0
        for i in range(self.MAXITER):
            if LA.norm(self.grad(x)) < EPS: break
            dx = -self.grad(x)
            alpha = self._armijo_line_search(x, dx)
            x += alpha * dx
        return {'x':x.tolist(), 'fun':float(self.fun(x)), 'grad':dx.tolist(), 'alpha':float(alpha), 'iter':i}
    def _conjugateGradient(self) -> dict:
        '''Метод спряжених градієнтів'''
        x = self.x.copy()
        EPS = self.EPS
        alpha = .0
        dx = -self.grad(x)
        grad_norm = LA.norm(self.grad(x))
        i = 0
        for i in range(self.MAXITER):
            if grad_norm < EPS: break
            alpha = self._armijo_line_search(x, dx)
            x += alpha * dx
            grad_new = LA.norm(self.grad(x))
            beta = (grad_new ** 2) / (grad_norm * grad_norm)
            dx = dx * beta - self.grad(x)
            grad_norm = grad_new
        return {'x':x.tolist(), 'fun':float(self.fun(x)), 'grad':dx.tolist(), 'alpha':float(alpha), 'grad_norm':float(grad_norm), 'iter':i}
    def _newton(self) -> dict:
        '''Метод Ньютона'''
        x = self.x.copy()
        EPS = self.EPS
        dx = self.grad(x)
        deltax = -LA.inv(self.hesse(x)) @ dx
        grad_norm = LA.norm(dx)
        i = 0
        for i in range(self.MAXITER):
            if grad_norm < EPS: break
            x += deltax
            dx = self.grad(x)
            deltax = -LA.inv(self.hesse(x)) @ dx
            grad_norm = LA.norm(self.grad(x))
        return {'x':x.tolist(), 'fun':float(self.fun(x)), 'grad':self.grad(x).tolist(), 'hesse':self.hesse(x).tolist(), 'grad_norm':float(grad_norm), 'iter':i}

    def _armijo_line_search(self, x, dx, alpha:float=1., beta:float=0.5, const:float=1e-4):
        '''Лінійний пошук зі зменшенням кроку за правилом Арміхо'''
        f_x = self.fun(x)
        grad_x = self.grad(x)
        while self.fun(x + alpha * dx) > f_x + const * alpha * np.dot(grad_x, dx):
            alpha *= beta
        return alpha

