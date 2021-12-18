import numpy as np
from PIL import Image

from wavefunc import get_wavefunc, to_spherical, PDF_nlm

resol = 255
sections = resol - 1
size = 15

# func = get_wavefunc(2,1,1, abs_sqrd=True, modules="math")
import sympy
from sympy.physics import hydrogen

r = sympy.Symbol("r", real=True, positive=True)
theta = sympy.Symbol("theta", real=True)
phi = sympy.Symbol("phi", real=True)

# p1 = hydrogen.Psi_nlm(2, 1, 1, r, phi, theta)
# p2 = hydrogen.Psi_nlm(2, 1, -1, r, phi, theta)
# expr = p1
# expr = (p1 + p2) / sympy.sqrt(2)
# expr = expr * sympy.conjugate(expr)
# expr = sympy.re(expr)
# func = sympy.lambdify([r, theta, phi], expr, cse=True, modules="numpy")

func = get_wavefunc(2,1,0, abs_sqrd=True)
data = np.zeros((resol, resol), dtype=np.uint8)

# def func(r, theta, phi):
#     if 0.5 > r:
#         return phi
#     else:
#         return 0

# pdf = PDF_nlm(2,1,1, prec=6)
# func = pdf.spherical

init = size / 2
sections = resol - 1

for h in range(resol):
    y = init - size * h / sections
    for w in range(resol):
        x = -init + size * w / sections

        r, theta, phi = to_spherical(x, 0, y)
        # val = func(r, theta, phi)
        # print(val)
        val = int(func(r, theta, phi)*100000)
        data[h][w] = val if 255 > val else 255

img = Image.fromarray(data)
img.show()
