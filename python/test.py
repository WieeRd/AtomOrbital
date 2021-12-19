import time
import numpy
import orjson


def list_vs_array():
    resol = 128

    lst = [[[3.14 for _ in range(resol)] for _ in range(resol)] for _ in range(resol)]
    arr = numpy.full((resol, resol, resol), 3.14, dtype=numpy.float32)

    t0 = time.time()
    l = orjson.dumps(lst)
    t1 = time.time()
    dt = (t1 - t0) * 1000
    print(f"Dumping list took: {dt}ms")

    t0 = time.time()
    a = orjson.dumps(arr, option=orjson.OPT_SERIALIZE_NUMPY)
    t1 = time.time()
    dt = (t1 - t0) * 1000
    print(f"Dumping ndarray took: {dt}ms")

    return l, a


import sympy
from sympy.physics import hydrogen

# it's 'real' not 'is_real'
r = sympy.Symbol("r", real=True, positive=True)
theta = sympy.Symbol("theta", real=True)
phi = sympy.Symbol("phi", real=True)

# WHO THE FUCK DECIDED THIS FUCTION'S PARAMETER ORDER
p0 = hydrogen.Psi_nlm(2, 1, 0, r, phi, theta)
p1 = hydrogen.Psi_nlm(2, 1, 1, r, phi, theta)
p2 = hydrogen.Psi_nlm(2, 1, -1, r, phi, theta)


def integrate(wf):
    abs_sqrd = wf * sympy.conjugate(wf)
    jacobi = r * r * sympy.sin(theta)
    return sympy.integrate(
        abs_sqrd * jacobi,
        (r, 0, sympy.oo),
        (phi, 0, 2 * sympy.pi),
        (theta, 0, sympy.pi),
    )
