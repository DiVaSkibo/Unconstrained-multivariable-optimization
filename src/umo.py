import numpy as np
from numpy import linalg as LA


class UMO:
    '''
    **Unconstrained Multivariable Optimization** - *Багатовимірна Безумовна Оптимізація*
    
    *Використання:*

        1. umo = UMO(fun: callable, x: tuple | list = (.0,.0), grad: callable = None, hesse: callable = None, eps: float = 1e-3, maxiter: int = 1000)
        2. umo.solve(method: str)
        3. umo.displayResult() | result = umo.result
    '''

    def __init__(self, fun:callable, x:tuple=(.0, .0), grad:callable=None, hesse:callable=None, eps:float=1e-3, maxiter:int=1000):
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
            Метод квазі-Ньютона (BFGS)  ->  "Quasi-Newton"
            дживса , елдера-міда
        '''
        self.result = None
        match method:
            case 'Steepest Descent':
                self.result = self._steepestDescent()
            case 'Conjugate Gradient':
                self.result = self._conjugateGradient()
            case 'Newton':
                self.result = self._newton()
            case 'Quasi-Newton':
                self.result = self._bfgs()
            case _:
                raise Exception('! Неправильне введення методу оптимізації !')
    
    def displayResult(self):
        print('Result:')
        for key in self.result:
            if key == 'method': print(f' Method: {self.result[key]}')
            else: print(f'  {key}\t   =\t {self.result[key]}')
        print()
    
    def _steepestDescent(self) -> dict:
        '''Метод найшвидшого спуску'''
        x = self.x.copy()
        alpha = .0
        i = 0
        for i in range(self.MAXITER):
            if LA.norm(self.grad(x)) < self.EPS: break
            dx = -self.grad(x)
            alpha = self._armijo_line_search(x, dx)
            x += alpha * dx
        return {'method':'Steepest Descent', 'x':x.tolist(), 'fun':float(self.fun(x)), 'grad':dx.tolist(), 'alpha':float(alpha), 'iter':i}
    def _conjugateGradient(self) -> dict:
        '''Метод спряжених градієнтів'''
        x = self.x.copy()
        alpha = .0
        dx = -self.grad(x)
        gnorm = LA.norm(self.grad(x))
        i = 0
        for i in range(self.MAXITER):
            if gnorm < self.EPS: break
            alpha = self._armijo_line_search(x, dx)
            x += alpha * dx
            grad_new = LA.norm(self.grad(x))
            beta = (grad_new ** 2) / (gnorm * gnorm)
            dx = dx * beta - self.grad(x)
            gnorm = grad_new
        return {'method':'Conjugate Gradient', 'x':x.tolist(), 'fun':float(self.fun(x)), 'grad':dx.tolist(), 'alpha':float(alpha), 'gnorm':float(gnorm), 'iter':i}
    def _newton(self) -> dict:
        '''Метод Ньютона'''
        x = self.x.copy()
        dx = self.grad(x)
        deltax = -LA.inv(self.hesse(x)) @ dx
        gnorm = LA.norm(dx)
        i = 0
        for i in range(self.MAXITER):
            if gnorm < self.EPS: break
            x += deltax
            dx = self.grad(x)
            deltax = -LA.inv(self.hesse(x)) @ dx
            gnorm = LA.norm(self.grad(x))
        return {'method':'Newton', 'x':x.tolist(), 'fun':float(self.fun(x)), 'grad':dx.tolist(), 'hesse':self.hesse(x).tolist(), 'gnorm':float(gnorm), 'iter':i}
    def _bfgs(self) -> dict:
        '''Метод Бройдена-Флетчера-Гольдфарба-Шанно'''
        x = self.x.copy()
        H = np.eye(len(x))
        dx = self.grad(x)
        gnorm = LA.norm(dx)
        i = 0
        for i in range(self.MAXITER):
            if gnorm < self.EPS: break
            direction = -H @ dx
            alpha = self._armijo_line_search(x, direction)
            x_new = x + alpha * direction
            dx_new = self.grad(x_new)
            d = x_new - x
            g = dx_new - dx
            denom = g @ d
            if abs(denom) < 1e-12: break
            rho = 1. / denom
            I = np.eye(len(x))
            H = (I - rho * np.outer(d, g)) @ H @ (I - rho * np.outer(g, d)) + rho * np.outer(d, d)
            x = x_new
            dx = dx_new
            gnorm = LA.norm(dx)
        return {'method':'Quasi-Newton', 'x':x.tolist(), 'fun':float(self.fun(x)), 'grad':dx.tolist(), 'hesse':self.hesse(x).tolist(), 'gnorm':float(gnorm), 'iter':i}
    
    def _armijo_line_search(self, x, dx, alpha:float=1., beta:float=0.5, const:float=1e-4):
        '''Лінійний пошук зі зменшенням кроку за правилом Арміхо'''
        f_x = self.fun(x)
        grad_x = self.grad(x)
        while self.fun(x + alpha * dx) > f_x + const * alpha * np.dot(grad_x, dx):
            alpha *= beta
        return alpha

