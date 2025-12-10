import pandas as pd
import numpy as np
from numpy import linalg as LA


class UMO:
    '''
    **Unconstrained Multivariable Optimization** - *Багатовимірна Безумовна Оптимізація*
    
    *Використання:*

        1. umo = UMO(fun: callable, x: tuple | list = (.0,.0), grad: callable = None, hesse: callable = None, eps: float = 1e-3, maxiter: int = 1000)
        2. umo.solve(method: str)
        3. umo.displayResult() | result = umo.result | table = umo.table
    '''

    METHODS = (
        'Хука-Дживса',
        'Нелдера-Міда',
        'Найшвидшого спуску',
        'Спряжених градієнтів',
        'Квазі-Ньютона (BFGS)',
        'Ньютона')

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
        
            метод "Хука-Дживса"
            метод "Нелдера-Міда"
            метод "Найшвидшого спуску"
            метод "Спряжених градієнтів"
            метод "Квазі-Ньютона (BFGS)"
            метод "Ньютона"
        '''
        self.result = None
        self.table = None
        match method:
            case 'Хука-Дживса': self.result, self.table = self._hookejeeves()
            case 'Нелдера-Міда': self.result, self.table = self._neldermead()
            case 'Найшвидшого спуску': self.result, self.table = self._steepestDescent()
            case 'Спряжених градієнтів': self.result, self.table = self._conjugateGradient()
            case 'Квазі-Ньютона (BFGS)': self.result, self.table = self._bfgs()
            case 'Ньютона': self.result, self.table = self._newton()
            case _: raise Exception('! Неправильне введення методу оптимізації !')
    
    def displayResult(self):
        print('Result:')
        for key in self.result:
            if key == 'method': print(f' Method: {self.result[key]}')
            else: print(f'  {key}\t   =\t {self.result[key]}')
        print()
    
    def _hookejeeves(self):
        '''Метод Хука-Дживса'''
        x = np.asarray(self.x, dtype=float)
        y = np.asarray(self.x, dtype=float)
        fx = self.fun(x)
        fy = self.fun(y)
        delta = .5
        alpha = .5
        table = []
        for _ in range(self.MAXITER):
            table.append({'method':'Хука-Дживса', 'x':x.tolist(), 'fun':float(self.fun(x)), 'delta':delta})
            if delta < self.EPS: break
            for j in range(len(x)):
                d = 0
                yj = y.copy()
                yj[j] += delta
                fyj = self.fun(yj)
                if fyj < fy:
                    d = 1
                    fy = fyj
                else:
                    yj[j] -= 2 * delta
                    fyj = self.fun(yj)
                    if fyj < fy:
                        d = -1
                        fy = fyj
                y[j] += delta * d
            if fy < fx:
                xk = y.copy()
                y = xk + (xk - x)
                x = xk.copy()
                fx = fy
            else:
                delta *= alpha
                y = x.copy()
                fy = fx
        return table[-1], pd.DataFrame(table)
    # def _neldermead(self, alpha=2., beta=.1, gamma=2., delta=.08):
    #     '''Метод Нелдера-Міда'''
    #     x = np.asarray(self.x, dtype=float)
    #     xs = np.array([self.x, np.add(self.x, [delta, 0.0]), np.add(self.x, [0.0, delta])])
    #     fx = np.array([self.fun(x) for x in xs])
    #     xs = xs[np.argsort(fx)]
    #     fx = fx[np.argsort(fx)]
    #     table = []
    #     iter = 0
    #     while np.max(np.abs(xs - xs.mean(axis=0))) > self.EPS:
    #         table.append({'method':'Нелдера-Міда', 'x':x.tolist(), 'fun':float(self.fun(x))})
    #         best, good, worst = xs
    #         mid = np.add(xs[0], xs[1]) / 2.
    #         r = mid + alpha * (mid - worst)
    #         fr = self.fun(r)
    #         if fx[0] <= fr < fx[1]:
    #             xs[2] = r
    #         elif fr < fx[0]:
    #             e = mid + gamma * (r - mid)
    #             if self.fun(e) < fr:
    #                 xs[2] = e
    #             else:
    #                 xs[2] = r
    #         else:
    #             if fr < fx[2]:
    #                 c = mid + beta * (r - mid)
    #             else:
    #                 c = mid + beta * (worst - mid)
    #             if self.fun(c) < fx[2]:
    #                 xs[2] = c
    #             else:
    #                 best = xs[0]
    #                 xs = best + beta * (xs - best)
    #         fx = np.array([self.fun(x) for x in xs])
    #         xs = xs[np.argsort(fx)]
    #         fx = fx[np.argsort(fx)]
    #         iter += 1
    #     return table[-1], pd.DataFrame(table)
    def _steepestDescent(self):
        '''Метод найшвидшого спуску'''
        x = np.asarray(self.x, dtype=float)
        alpha = .0
        dx = -self.grad(x)
        table = []
        for _ in range(self.MAXITER):
            table.append({'method':'Найшвидшого спуску', 'x':x.tolist(), 'fun':float(self.fun(x)), 'grad':dx.tolist(), 'alpha':float(alpha)})
            if LA.norm(self.grad(x)) < self.EPS: break
            alpha = self._line_search(x, dx)
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
            table.append({'method':'Спряжених градієнтів', 'x':x.tolist(), 'fun':float(self.fun(x)), 'grad':dx.tolist(), 'alpha':float(alpha), 'gnorm':float(gnorm)})
            if gnorm < self.EPS: break
            alpha = self._line_search(x, dx)
            x += alpha * dx
            gnorm_new = LA.norm(self.grad(x))
            beta = gnorm_new ** 2 / gnorm ** 2
            dx = beta * dx - self.grad(x)
            gnorm = gnorm_new
        return table[-1], pd.DataFrame(table)
    def _bfgs(self):
        '''Метод Бройдена-Флетчера-Гольдфарба-Шанно'''
        x = np.asarray(self.x, dtype=float)
        H = np.eye(len(x))
        dx = self.grad(x)
        gnorm = LA.norm(dx)
        table = []
        for _ in range(self.MAXITER):
            table.append({'method':'Квазі-Ньютона (BFGS)', 'x':x.tolist(), 'fun':float(self.fun(x)), 'grad':dx.tolist(), 'hesse':self.hesse(x).tolist(), 'gnorm':float(gnorm)})
            if gnorm < self.EPS: break
            direction = -H @ dx
            alpha = self._line_search(x, direction)
            x_new = x + alpha * direction
            dx_new = self.grad(x_new)
            d = x_new - x
            g = dx_new - dx
            denom = g @ d
            if abs(denom) < 1e-12: break
            rho = 1. / denom
            I = np.eye(len(x))
            H = (I - rho * np.outer(d, g)) @ H @ (I - rho * np.outer(g, d)) + rho * np.outer(d, d)
            x = x_new.copy()
            dx = dx_new
            gnorm = LA.norm(dx)
        return table[-1], pd.DataFrame(table)
    def _newton(self):
        '''Метод Ньютона'''
        x = np.asarray(self.x, dtype=float)
        dx = self.grad(x)
        deltax = -LA.inv(self.hesse(x)) @ dx
        gnorm = LA.norm(dx)
        table = []
        for _ in range(self.MAXITER):
            table.append({'method':'Ньютона', 'x':x.tolist(), 'fun':float(self.fun(x)), 'grad':dx.tolist(), 'hesse':self.hesse(x).tolist(), 'gnorm':float(gnorm)})
            if gnorm < self.EPS: break
            x += deltax
            dx = self.grad(x)
            deltax = -LA.inv(self.hesse(x)) @ dx
            gnorm = LA.norm(self.grad(x))
        return table[-1], pd.DataFrame(table)

    def _line_search(self, x, dx, a:float=.0, h:float=.002) -> float:
        '''Лінійний пошук зі зменшенням кроку за квадратичною інтерполяцією'''
        if self.fun(x + a * dx) < self.fun(x + (a + h) * dx):
            h = -h
        while self.fun(x + a * dx) > self.fun(x + (a + h) * dx):
            a += h
            h *= 2
        alpha, beta, gamma = 0, 0, 0
        if self.fun(x + a * dx) > self.fun(x + (a + h / 2) * dx):
            alpha = a;
            beta = a + h / 2;
            gamma = a + h;
        else:
            alpha = a - h / 2;
            beta = a;
            gamma = a + h / 2;
        falpha = self.fun(x + alpha * dx)
        fbeta = self.fun(x + beta * dx)
        fgamma = self.fun(x + gamma * dx)
        delta = 0.0
        fdelta = 0.0;
        while abs(beta - delta) > self.EPS:
            Delta = (alpha - beta) * (beta - gamma) * (gamma - alpha)
            a = (falpha * (gamma - beta) + fbeta * (alpha - gamma) + fgamma * (beta - alpha)) / Delta
            b = (falpha * (beta * beta - gamma * gamma) + fbeta * (gamma * gamma - alpha * alpha) + fgamma * (alpha * alpha - beta * beta)) / Delta
            delta = -b / a / 2
            fdelta = self.fun(x + delta * dx)
            if delta < beta:
                if fdelta > fbeta:
                    alpha = delta
                    falpha = fdelta
                else:
                    gamma = beta
                    beta = delta
                    fgamma = fbeta
                    fbeta = fdelta
            else:
                if fdelta > fbeta:
                    gamma = delta
                    fgamma = fdelta
                else:
                    alpha = beta
                    beta = delta
                    falpha = fbeta
                    fbeta = fdelta
        return delta
