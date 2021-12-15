import time
import numpy
import orjson

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
