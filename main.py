import math
import numpy as np

from src.umo import UMO


def fun(x) -> float:
    return 5. * x[0] * x[0] + 2. * x[1] * x[1] + 4. * x[0] * x[1] + 4. * math.sqrt(5.) * (x[0] + x[1]) - 14.
def jac(x) -> float:
    return np.array([10. * x[0] + 4. * x[1] + 4. * math.sqrt(5.), 4. * x[0] + 4. * x[1] + 4. * math.sqrt(5.)])


# UNCONSTRAINED MULTIVARIABLE OPTIMIZATION

if __name__ == "__main__":
    print('\n|| UNCONSTRAINED MULTIVARIABLE OPTIMIZATION ||\n')

    model = UMO(fun=fun, x=[.0, .0], jac=jac)
