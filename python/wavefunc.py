from typing import Tuple
import sympy
from sympy.physics import hydrogen


def orbital_name(n: int, l: int, m: int) -> str:
    """
    Generate orbital name based on quantum numbers
    """
    return str(n) + "spdf"[l]  # TODO: direction


def transform(x: float, y: float, z: float) -> Tuple[float, float, float]:
    ...


def Psi_nlm(n_: int, l_: int, m_: int, Z_: int = 1):

    # sympify arguments
    n, l, m, Z = map(sympy.sympify, [n_, l_, m_, Z_])

    r = sympy.Symbol("r", real=True, positive=True)
    theta = sympy.Symbol("theta", real=True)
    phi = sympy.Symbol("phi", real=True)

    # check if values for n,l,m make physically sense
    if n.is_integer and n < 1:
        raise ValueError("'n' must be positive integer")
    if l.is_integer and not (n > l):
        raise ValueError("'n' must be greater than 'l'")
    if m.is_integer and not (abs(m) <= l):
        raise ValueError("|'m'| must be less or equal 'l'")

    # return the hydrogen wave function
    return hydrogen.R_nl(n, l, r, Z) * hydrogen.Ynm(l, m, theta, phi)


class HydrogenWave:
    def __init__(self, n: int, l: int, m: int):
        ...

    def __call__(self, x: float, y: float, z: float) -> float:
        ...


class HydrogenPDF(HydrogenWave):
    ...
