#!/usr/bin/env python3
import time
import numpy as np
from PIL import Image
from math import exp, sqrt

RESOL = 1024
SIZE = 0.1

X1 = -1.5
X2 = +1.5


def value(y: float, z: float) -> float:
    yyzz = y * y + z * z
    return (
        z * z * exp(-2 * sqrt(yyzz)) * (
            X2 - X1
            - (X2 ** 3 - X1 ** 3) / (3 * sqrt(yyzz))
            + (X2 ** 5 - X1 ** 5) * ((2 / yyzz) + (1 / (yyzz) ** (3 / 2))) / 20
        )
    )

def limit(val: int) -> int:
    """
    = min(max(val, 0), 255)
    """
    tmp = 255 if val>255 else val
    return 0 if tmp<0 else tmp

def grey2RGB(val):  # WieeRd ver
    if val < 1*0xFF:
        return 0, 0, val
    if val < 2*0xFF:
        return 0, val%0xFF, 0xFF
    if val < 3*0xFF:
        return 0, 0xFF, 0xFF-val%0xFF
    if val < 4*0xFF:
        return val%0xFF, 0xFF, 0
    if val < 5*0xFF:
        return 0xFF, 0xFF-val%0xFF, 0
    else:
        return 0xFF, 0, 0

# def grey2RGB(val):  # i have no idea
#     if val < 1*0xFF:
#         return 0, 0, val
#     if val < 2*0xFF:
#         return 0, val%0xFF, 0xFF
#     if val < 3*0xFF:
#         return val%0xFF, 0xFF, 0xFF
#     else:
#         return 0xFF, 0xFF, 0xFF

# def grey2RGB(val):  # kim chan hyeok ver
#     """
#     WTF is this
#     """
#     if val < 2*0xFF:
#         r = min(2*0xFF - val, 255)
#         b = 255
#         g = 2*0xFF - val - r
#     elif val < 5*0xFF:
#         r = max(val - 4*0xFF, 0)
#         b = max(0,min(4*0xFF - val, 255))
#         g = val - 4*0xFF + 255 + b - r
#     elif val < 7*0xFF:
#         r = min(7*0xFF-val, 0xFF)
#         b = 0
#         g = (7*0xFF - val) - r
#     else:
#         r = 0
#         b = 0
#         g = 0
#     return r, g, b

def showRGB():
    data = np.full((100, 1500, 3), 0, dtype=np.uint8)
    for val in range(1500):
        for y in range(100):
            data[y][val] = grey2RGB(val)
    img = Image.fromarray(data, "RGB")
    img.show()

# values = []
data = np.full((RESOL, RESOL, 3), 0, dtype=np.uint8)
t0 = time.time()

for h in range(RESOL):  # height
    for w in range(RESOL):  # width
        z = -SIZE * (2 * h / RESOL - 1)
        y = +SIZE * (2 * w / RESOL - 1)
        if z == 0 and y == 0:
            continue

        val = value(y, z)*12
        r, g, b = grey2RGB(val)
        data[h][w] = r, g, b

t1 = time.time()
print(f"{(t1 - t0)*1000}ms")

# print(min(values))
# print(max(values))

image = Image.fromarray(data, "RGB")
# image.save("p_orbital.png")
image.show()
