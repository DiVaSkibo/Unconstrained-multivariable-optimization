import math
import numpy as np

from src.umo import UMO


def fun(x) -> float:
    return 5. * x[0] * x[0] + 2. * x[1] * x[1] + 4. * x[0] * x[1] + 4. * math.sqrt(5.) * (x[0] + x[1]) - 14.
def grad(x) -> np.ndarray:
    return np.array([10. * x[0] + 4. * x[1] + 4. * math.sqrt(5.), 4. * x[0] + 4. * x[1] + 4. * math.sqrt(5.)])
def hesse(x) -> np.ndarray:
    return np.array([[10., 4.], [4., 4.]])


# БАГАТОВИМІРНА БЕЗУМОВНА ОПТИМІЗАЦІЯ

if __name__ == "__main__":
    print('\n|| UNCONSTRAINED MULTIVARIABLE OPTIMIZATION ||\n')

    model = UMO(fun=fun, x=(.0, .0), grad=grad, hesse=hesse)
    model.solve(method='Steepest Descent')
    print(f'result = {model.result}\n')
    model.solve(method='Conjugate Gradient')
    print(f'result = {model.result}\n')
    model.solve(method='Newton')
    print(f'result = {model.result}\n')

