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


from sympy.physics import hydrogen
from sympy import Symbol, integrate, conjugate, pi, oo, sin, sqrt, simplify

r = Symbol("r", real=True, positive=True)
theta = Symbol("theta", real=True)
phi = Symbol("phi", real=True)

wf = hydrogen.Psi_nlm(2, 1, 1, r, phi, theta)
print(f"Psi(2,1,1) = {wf}")
abs_sqrd = wf * conjugate(wf)
print(f"PDF(2,1,1) = {abs_sqrd}")

jacobi = r * r * sin(theta)
i = integrate(abs_sqrd*jacobi, (r, 0, oo), (phi, 0, 2*pi), (theta, 0, pi))
print(f"Integral PDF(2,1,1) = {i}")

print()

wf2 = hydrogen.Psi_nlm(2, 1, -1, r, theta, phi)
print(f"Psi(2,1,-1) = {wf2}")

sp_x = (wf + wf2) / sqrt(2)
sp_x = simplify(sp_x)
print(f"Psi(2p_x) = {sp_x}\n")

abs_sqrd2 = simplify(sp_x * conjugate(sp_x))
print(f"PDF(2p_x) = {abs_sqrd2}\n")

i = integrate(abs_sqrd2*jacobi, (r, 0, oo), (phi, 0, 2*pi), (theta, 0, pi))
print(f"Integral PDF(2p_x) = {i}")
