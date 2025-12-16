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
    
    def __init__(self, fun:callable, x:tuple=(.0, .0), grad:callable=None, hesse:callable=None, eps:float=1e-3, maxiter:int=100):
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
    def _neldermead(self, delta=1.):
        '''Метод Нелдера-Міда'''
        x = np.asarray(self.x, dtype=float)
        simplex = [x]
        fsimplex = [self.fun(x)]
        for i in range(len(x)):
            y = x.copy()
            y[i] += delta
            simplex.append(y)
            fsimplex.append(self.fun(y))
        simplex = np.array(simplex, dtype=float)
        fsimplex = np.array(fsimplex, dtype=float)
        table = []
        for _ in range(self.MAXITER):
            sidxs = np.argsort(fsimplex)
            simplex = simplex[sidxs]
            fsimplex = fsimplex[sidxs]
            p = simplex[:-1].mean(axis=0)
            if abs(fsimplex[0] - self.fun(p)) < self.EPS: break
            xk = simplex[-1] + 2. * (p - simplex[-1])
            fxk = self.fun(xk)
            if fxk < fsimplex[0]:
                theta = 2.
            elif fsimplex[-1] <= fxk <= fsimplex[-2]:
                theta = .5
            elif fxk >= self.fun(p):
                theta = -.5
            else:
                theta = 1.
            xk = simplex[-1] + (1 + theta) * (p - simplex[-1])
            table.append({'method':'Нелдера-Міда', 'x':xk.tolist(), 'fun':float(fsimplex[0].tolist()), 'simplex':[s.tolist() for s in simplex], 'fsimplex':[float(fs) for fs in fsimplex]})
            simplex[-1] = xk
            fsimplex[-1] = self.fun(xk)
        return table[-1], pd.DataFrame(table)
    def _steepestDescent(self):
        '''Метод найшвидшого спуску'''
        x = np.asarray(self.x, dtype=float)
        alpha = .0
        dx = -self.grad(x)
        table = []
        for _ in range(self.MAXITER):
            table.append({'method':'Найшвидшого спуску', 'x':x.tolist(), 'fun':float(self.fun(x)), 'grad':dx.tolist(), 'alpha':float(alpha), 'gnorm':float(LA.norm(-dx))})
            if LA.norm(-dx) < self.EPS: break
            alpha = self._line_search(x, dx)
            x += alpha * dx
            dx = -self.grad(x)
        return table[-1], pd.DataFrame(table)
    def _conjugateGradient(self):
        '''Метод спряжених градієнтів'''
        x = np.asarray(self.x, dtype=float)
        alpha = .0
        dx = -self.grad(x)
        gnorm = LA.norm(-dx)
        table = []
        for _ in range(self.MAXITER):
            table.append({'method':'Спряжених градієнтів', 'x':x.tolist(), 'fun':float(self.fun(x)), 'grad':dx.tolist(), 'alpha':float(alpha), 'gnorm':float(gnorm)})
            if gnorm < self.EPS: break
            alpha = self._line_search(x, dx)
            x += alpha * dx
            gnormk = LA.norm(self.grad(x))
            beta = gnormk ** 2 / gnorm ** 2
            dx = beta * dx - self.grad(x)
            gnorm = gnormk
        return table[-1], pd.DataFrame(table)
    def _bfgs(self):
        '''Метод Бройдена-Флетчера-Гольдфарба-Шанно'''
        x = np.asarray(self.x, dtype=float)
        H = np.eye(len(x))
        dx = self.grad(x)
        gnorm = LA.norm(dx)
        table = []
        for _ in range(self.MAXITER):
            table.append({'method':'Квазі-Ньютона (BFGS)', 'x':x.tolist(), 'fun':float(self.fun(x)), 'grad':dx.tolist(), 'hesse':H.tolist(), 'gnorm':float(gnorm)})
            if gnorm < self.EPS: break
            direction = -H @ dx
            alpha = self._line_search(x, direction)
            xk = x + alpha * direction
            dxk = self.grad(xk)
            d = xk - x
            g = dxk - dx
            denom = g @ d
            if abs(denom) < 1e-12: break
            rho = 1. / denom
            I = np.eye(len(x))
            H = (I - rho * np.outer(d, g)) @ H @ (I - rho * np.outer(g, d)) + rho * np.outer(d, d)
            x = xk.copy()
            dx = dxk
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
            gnorm = LA.norm(dx)
        return table[-1], pd.DataFrame(table)
    
    def _line_search(self, x, dx, a0:float=.0, h:float=.002) -> float:
        '''Лінійний пошук зі зменшенням кроку за квадратичною інтерполяцією'''
        def phi(y) -> float:
            return self.fun(x + y * dx)
        
        if phi(a0) < phi(a0 + h):
            h = -h
        while phi(a0) > phi(a0 + h):
            a0 += h
            h *= 2
        alpha, beta, gamma = .0, .0, .0
        if phi(a0) > phi(a0 + h / 2):
            alpha = a0
            beta = a0 + h / 2
            gamma = a0 + h
        else:
            alpha = a0 - h / 2
            beta = a0
            gamma = a0 + h / 2
        falpha = phi(alpha)
        fbeta = phi(beta)
        fgamma = phi(gamma)
        delta = .0
        fdelta = .0
        for _ in range(self.MAXITER):
            if abs(beta - delta) < self.EPS: break
            Delta = (alpha - beta) * (beta - gamma) * (gamma - alpha)
            a = (falpha * (gamma - beta) + fbeta * (alpha - gamma) + fgamma * (beta - alpha)) / Delta
            b = (falpha * (beta * beta - gamma * gamma) + fbeta * (gamma * gamma - alpha * alpha) + fgamma * (alpha * alpha - beta * beta)) / Delta
            delta = -b / a / 2
            fdelta = phi(delta)
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
