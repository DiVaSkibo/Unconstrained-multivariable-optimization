import pandas as pd
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

    METHODS = {'Найшвидшого спуску':'Steepest Descent',
               'Спряжених градієнтів':'Conjugate Gradient',
               'Ньютона':'Newton',
               'Квазі-Ньютона (BFGS)':'Quasi-Newton'}

    def __init__(self, fun:callable, x:tuple=(.0, .0), grad:callable=None, hesse:callable=None, eps:float=1e-3, maxiter:int=1000):
        self.fun = fun
        self.x = x
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
        '''
        self.result = None
        self.table = None
        match method:
            case 'Steepest Descent':
                self.result, self.table = self._steepestDescent()
            case 'Conjugate Gradient':
                self.result, self.table = self._conjugateGradient()
            case 'Newton':
                self.result, self.table = self._newton()
            case 'Quasi-Newton':
                self.result, self.table = self._bfgs()
            case _:
                raise Exception('! Неправильне введення методу оптимізації !')
    
    def displayResult(self):
        print('Result:')
        for key in self.result:
            if key == 'method': print(f' Method: {self.result[key]}')
            else: print(f'  {key}\t   =\t {self.result[key]}')
        print()
    def tableResult(self):
        rtable = [f'{round(self.result['fun'], 4)}']
        for key in ('x', 'grad', 'hesse', 'alpha', 'gnorm', 'iter'):
            if key in self.result:
                value = self.result[key]
                if type(value) == float: value = round(value, 4)
                elif type(value) == list:
                    if type(value[0]) == float: value = [round(v, 4) for v in value]
                    elif type(value[0]) == list: value = [[round(w, 4) for w in v] for v in value]
                rtable.append(f'{value}')
        space = int(3 * len(' '.join(rtable)) / len(rtable))
        return (' '*space).join(rtable)
    
    def _steepestDescent(self):
        '''Метод найшвидшого спуску'''
        x = np.asarray(self.x, dtype=float)
        alpha = .0
        dx = -self.grad(x)
        table = []
        for _ in range(self.MAXITER):
            table.append({'method':'Steepest Descent', 'x':x.tolist(), 'fun':float(self.fun(x)), 'grad':dx.tolist(), 'alpha':float(alpha)})
            if LA.norm(self.grad(x)) < self.EPS: break
            alpha = self._armijo_line_search(x, dx)
            x += alpha * dx
            dx = -self.grad(x)
        return table[-1], pd.DataFrame(table)
    def _conjugateGradient(self):
        '''Метод спряжених градієнтів'''
        x = np.asarray(self.x, dtype=float)
        alpha = .0
        dx = -self.grad(x)
        gnorm = LA.norm(self.grad(x))
        table = []
        for _ in range(self.MAXITER):
            table.append({'method':'Conjugate Gradient', 'x':x.tolist(), 'fun':float(self.fun(x)), 'grad':dx.tolist(), 'alpha':float(alpha), 'gnorm':float(gnorm)})
            if gnorm < self.EPS: break
            alpha = self._armijo_line_search(x, dx)
            x += alpha * dx
            grad_new = LA.norm(self.grad(x))
            beta = (grad_new ** 2) / (gnorm * gnorm)
            dx = dx * beta - self.grad(x)
            gnorm = grad_new
        return table[-1], pd.DataFrame(table)
    def _newton(self):
        '''Метод Ньютона'''
        x = np.asarray(self.x, dtype=float)
        dx = self.grad(x)
        deltax = -LA.inv(self.hesse(x)) @ dx
        gnorm = LA.norm(dx)
        table = []
        for _ in range(self.MAXITER):
            table.append({'method':'Newton', 'x':x.tolist(), 'fun':float(self.fun(x)), 'grad':dx.tolist(), 'hesse':self.hesse(x).tolist(), 'gnorm':float(gnorm)})
            if gnorm < self.EPS: break
            x += deltax
            dx = self.grad(x)
            deltax = -LA.inv(self.hesse(x)) @ dx
            gnorm = LA.norm(self.grad(x))
        return table[-1], pd.DataFrame(table)
    def _bfgs(self):
        '''Метод Бройдена-Флетчера-Гольдфарба-Шанно'''
        x = np.asarray(self.x, dtype=float)
        H = np.eye(len(x))
        dx = self.grad(x)
        gnorm = LA.norm(dx)
        table = []
        for _ in range(self.MAXITER):
            table.append({'method':'Quasi-Newton', 'x':x.tolist(), 'fun':float(self.fun(x)), 'grad':dx.tolist(), 'hesse':self.hesse(x).tolist(), 'gnorm':float(gnorm)})
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
        return table[-1], pd.DataFrame(table)
    # def _hookejeeves(self):
    #     '''Метод Хука-Дживса'''
    #     x = self.x.copy()
    # def _neldermead(self):
    #     '''Метод Нелдера-Міда'''
    #     x = self.x.copy()
    #     # xs = np.array([x0, np.add(x0, [delta, 0.0]), np.add(x0, [0.0, delta])])
    #     # fx = np.array([fun(x) for x in xs])
    #     # xs = xs[np.argsort(fx)]
    #     # fx = fx[np.argsort(fx)]
    #     # iter = 0
    #     # while np.max(np.abs(xs - xs.mean(axis=0))) > eps:
    #     #     best, good, worst = xs
    #     #     mid = np.add(xs[0], xs[1]) / 2.
    #     #     r = mid + alpha * (mid - worst)
    #     #     fr = fun(r)
    #     #     if fx[0] <= fr < fx[1]:
    #     #         xs[2] = r
    #     #     elif fr < fx[0]:
    #     #         e = mid + gamma * (r - mid)
    #     #         if fun(e) < fr:
    #     #             xs[2] = e
    #     #         else:
    #     #             xs[2] = r
    #     #     else:
    #     #         if fr < fx[2]:
    #     #             c = mid + beta * (r - mid)
    #     #         else:
    #     #             c = mid + beta * (worst - mid)
    #     #         if fun(c) < fx[2]:
    #     #             xs[2] = c
    #     #         else:
    #     #             best = xs[0]
    #     #             xs = best + beta * (xs - best)
    #     #     fx = np.array([fun(x) for x in xs])
    #     #     xs = xs[np.argsort(fx)]
    #     #     fx = fx[np.argsort(fx)]
    #     #     iter += 1
    #     # return xs[0], iter

    
    def _armijo_line_search(self, x, dx, alpha:float=1., beta:float=0.5, const:float=1e-4):
        '''Лінійний пошук зі зменшенням кроку за правилом Арміхо'''
        f_x = self.fun(x)
        grad_x = self.grad(x)
        while self.fun(x + alpha * dx) > f_x + const * alpha * np.dot(grad_x, dx):
            alpha *= beta
        return alpha

