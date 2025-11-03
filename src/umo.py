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
    
    def _steepestDescent(self) -> dict:
        '''Метод найшвидшого спуску'''
        x = np.asarray(self.x, dtype=float)
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
        x = np.asarray(self.x, dtype=float)
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
        x = np.asarray(self.x, dtype=float)
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
        x = np.asarray(self.x, dtype=float)
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
    # def _hookejeeves(self) -> dict:
    #     '''Метод Хука-Дживса'''
    #     x = self.x.copy()
    # def _neldermead(self) -> dict:
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

