#!/usr/bin/env python3
import time
import numpy as np
from PIL import Image
from math import exp, sqrt, sin, cos

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


# values = []
data = np.full((RESOL, RESOL), 0, dtype=np.uint8)

t0 = time.time()
for h in range(RESOL):  # height
    for w in range(RESOL):  # width
        z = -SIZE * (2 * h / RESOL - 1)
        y = +SIZE * (2 * w / RESOL - 1)
        if z == 0 and y == 0:
            continue
        val = value(y, z)*2
        # values.append(val)
        data[h][w] = val if val<255 else 255
t1 = time.time()
print(f"{(t1 - t0)*1000}ms")

# print(min(values))
# print(max(values))

image = Image.fromarray(data)
# image.save("p_orbital.png")
image.show()
