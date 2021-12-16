import sympy
from sympy.physics import hydrogen
from typing import Any, Callable


name = "spdf"
orientation = [
    {
        0: "",
    },
    {
        0: "_z",
        +1: "_x",
        -1: "_y",
    },
    {
        0: "_z2",
        +1: "_xz",
        -1: "_yz",
        +2: "_xy",
        -2: "_x2−y2",
    },
    {
        0: "_z3",
        +1: "_xz2",
        -1: "_yz2",
        +2: "_xyz",
        -2: "_z(x2−y2)",
        +3: "_x(x2−3y2)",
        -3: "_y(3x2−y2)",
    },
]


def orbital_name(n: int, l: int, m: int) -> str:
    """
    Generate orbital's name based on quantum numbers.

    Parameters
    ----------
    n, l, m : `int`
        Quantom numbers of the orbital

    Returns
    -------
    `str`
        The orbital's name. e.g. `orbital_name`(2,1,1) -> '2p_x'

    Raises
    ------
    ValueError
        When invalid quantum numbers are given
    NotImplementedError
        Currently only supported upto f orbital
    """
    if n < 1:
        raise ValueError("'n' must be positive integer")
    if not (n > l):
        raise ValueError("'n' must be greater than 'l'")
    if not (abs(m) <= l):
        raise ValueError("|'m'| must be less or equal to 'l'")
    if not (len(orientation) > l):
        raise NotImplementedError("Currently only supported upto f orbital")
    return f"{n}{name[l]}{orientation[l][m]}"


# TODO: test performance
# opt 1. transform first & pass to spherical
# opt 2. use transformed Psi(x, y, z)
# opt 3. numpy array operation

# TODO: what about imaginary parts of Psi?


def get_wavefunc(
    n: int,
    l: int,
    m: int,
    *,
    Z: int = 1,
    abs_sqrd: bool = False,
    orthogonal: bool = False,
    **options,
) -> Callable[[Any, Any, Any], Any]:
    """
    Generate wave function of atomic orbital

    Parameters
    ----------
    n, l, m : `int`
        Quantom numbers of the orbital
    Z : `int`
        Atomic number. Default is set to 1 (Hydrogen)
    abs_sqrd : `bool`
        If `True`, absolute square of wave function (probability density) is used
    orthogonal : `bool`
        If `True`, returned function will take (x, y, z) instead of (r, theta, phi)
    **options : `dict`
        These kwargs will be passed to `sympy.lambdify()`

    Returns
    -------
    Callable[[`float`, `float`, `float`], `float`]
        Function that calculates Psi(r, theta, phi)

    Notes
    -----
    Generated wave functions only returns real part
    """
    r = sympy.Symbol("r", real=True, positive=True)
    theta = sympy.Symbol("theta", real=True)
    phi = sympy.Symbol("phi", real=True)

    # XXX: hydrogen.Psi_nlm() uses order [r, phi, theta] (why??)
    expr = hydrogen.Psi_nlm(n, l, m, r, phi, theta, Z)
    if abs_sqrd:
        expr = expr * sympy.conjugate(expr)  # probability density
    else:
        expr = sympy.re(expr)  # only take the real part
    assert isinstance(expr, sympy.Expr)

    if not orthogonal:
        return sympy.lambdify([r, theta, phi], expr, **options)

    x = sympy.Symbol("x", real=True)
    y = sympy.Symbol("y", real=True)
    z = sympy.Symbol("z", real=True)

    expr = expr.subs(
        [
            (r, x * x + y * y + z * z),
            (theta, sympy.acos(z / y)),
            (phi, sympy.atan(y / x)),
        ]
    )

    return sympy.lambdify([x, y, z], expr, **options)


class Psi_nlm:
    def __init__(self, n: int, l: int, m: int, *, Z: int = 1, prec: int = 6):
        self.n = n
        self.l = l
        self.m = m

        self.Z = Z
        self.prec = prec

        self.r = sympy.Symbol("r", real=True, positive=True)
        self.theta = sympy.Symbol("theta", real=True)
        self.phi = sympy.Symbol("phi", real=True)

        # XXX: Psi_nlm uses order (r, phi, theta) for some reason
        self.expr = hydrogen.Psi_nlm(n, l, m, self.r, self.phi, self.theta, Z)

    def __repr__(self) -> str:
        n, l, m = self.n, self.l, self.m
        return f"{self.__class__.__name__}({n}, {l}, {m}, Z={self.Z}, prec={self.prec})"

    def __str__(self) -> str:
        n, l, m = self.n, self.l, self.m
        return f"{self.__class__.__name__}({orbital_name(n, l, m)})"

    def spherical(self, r, theta, phi):
        subs = {self.r: r, self.theta: theta, self.phi: phi}
        return self.expr.evalf(self.prec, subs=subs)

    def orthogonal(self, x, y, z):
        r = sympy.sqrt(x * x + y * y + z * z)
        theta = sympy.acos(z / y)
        phi = sympy.atan(y / x)
        subs = {self.r: r, self.theta: theta, self.phi: phi}
        return self.expr.evalf(self.prec, subs=subs)


class PDF_nlm(Psi_nlm):
    def __init__(self, n: int, l: int, m: int, Z: int = 1, prec: int = 6):
        super().__init__(n, l, m, Z=Z, prec=prec)
        self.expr = self.expr * sympy.conjugate(self.expr)
