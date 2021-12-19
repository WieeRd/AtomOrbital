import time
import orjson
import numpy as np
from typing import Callable, List

# probability density function
PDF = Callable[[float, float, float], float]


def cube(x: float, y: float, z: float) -> float:
    # 3x3x3 cube-shaped PDF for testing
    return x < 3 and y < 3 and z < 3


def calc_numpy(func: PDF, size: float, resol: int) -> np.ndarray:
    data = np.zeros((resol, resol, resol), dtype=np.float32)

    init = -size / 2
    sections = resol - 1

    # delta = size / sections
    # using delta might be inaccurate
    # ex) delta*sections != size

    # i, j, k : voxel pos (int)
    # x, y, z : actual pos (float)
    for k in range(resol):
        z = init + size * k / sections
        for j in range(resol):
            y = init + size * j / sections
            for i in range(resol):
                x = init + size * i / sections

                data[k][j][i] = func(x, y, z)

    return data


def calc_list(func: PDF, size: float, resol: int) -> List[List[List[float]]]:
    data = [[[0.0 for _ in range(resol)] for _ in range(resol)] for _ in range(resol)]

    init = -size / 2
    sections = resol - 1

    # delta = size / sections
    # using delta might be inaccurate
    # ex) delta*sections != size

    # i, j, k : voxel pos (int)
    # x, y, z : actual pos (float)
    for k in range(resol):
        z = init + size * k / sections
        for j in range(resol):
            y = init + size * j / sections
            for i in range(resol):
                x = init + size * i / sections

                data[k][j][i] = func(x, y, z)

    return data


t0 = time.time()
data = calc_numpy(cube, 10, 128)
t1 = time.time()
print(f"Calculating took {(t1 - t0)*1000:.2f}ms")

t0 = time.time()
json = orjson.dumps(data, option=orjson.OPT_SERIALIZE_NUMPY)
t1 = time.time()
print(f"Dumping took {(t1 - t0)*1000:.2f}ms")

with open("cube.json", "wb") as f:
    f.write(json)

t0 = time.time()
with open("cube.json", "rb") as f:
    data = orjson.loads(f.read())
t1 = time.time()
print(f"Reading took {(t1 - t0)*1000:.2f}ms")

t0 = time.time()
data = np.array(data, dtype=np.float32)
t1 = time.time()
print(f"Converting took {(t1 - t0)*1000:.2f}ms")
