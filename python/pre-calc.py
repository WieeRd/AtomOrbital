import orjson
import numpy as np
import numpy.typing as npt
from typing import Any, Callable

# probability density function
PDF = Callable[[float, float, float], float]

def render(probfunc: PDF, size: float, resolution: int) -> np.ndarray:
    ...
