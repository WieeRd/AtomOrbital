import sympy
from sympy.physics import hydrogen


name = "spdf"
orientation = [
    {
        0: "",
    },
    {
        0: "z",
        +1: "x",
        -1: "y",
    },
    {
        0: "z2",
        +1: "xz",
        -1: "yz",
        +2: "xy",
        -2: "x2−y2",
    },
    {
        0: "z3",
        +1: "xz2",
        -1: "yz2",
        +2: "xyz",
        -2: "z(x2−y2)",
        +3: "x(x2−3y2)",
        -3: "y(3x2−y2)",
    },
]


def orbital_name(n: int, l: int, m: int) -> str:
    """
    Generate orbital name based on quantum numbers
    ex) (2,1,1) -> 2p_x
    """
    return f"{n}{name[l]}_{orientation[l][m]}"


class WaveFunc:
    def __init__(self, n: int, l: int, m: int, *, Z: int = 1, prec: int = 6):
        self.n = n
        self.l = l
        self.m = m

        self.Z = Z
        self.prec = prec

        self.r = sympy.Symbol("r", real=True, positive=True)
        self.theta = sympy.Symbol("theta", real=True)
        self.phi = sympy.Symbol("phi", real=True)

        sympy.lambdify  # TODO: this & numpy would make the code a lot faster
        self.expr = hydrogen.Psi_nlm(n, l, m, self.r, self.theta, self.phi, Z)

    def __repr__(self) -> str:
        n, l, m = self.n, self.l, self.m
        return f"{self.__class__.__name__}({n}, {l}, {m}, Z={self.Z}, prec={self.prec})"

    def __str__(self) -> str:
        n, l, m = self.n, self.l, self.m
        return f"Psi({orbital_name(n, l, m)})"

    def spherical(self, r, theta, phi):
        subs = {self.r: r, self.theta: theta, self.phi: phi}
        return self.expr.evalf(self.prec, subs=subs)

    def orthogonal(self, x, y, z):
        r = sympy.sqrt(x * x + y * y + z * z)
        theta = sympy.acos(z / y)
        phi = sympy.atan(y / x)
        subs = {self.r: r, self.theta: theta, self.phi: phi}
        return self.expr.evalf(self.prec, subs=subs)


class Orbital(WaveFunc):
    def __init__(self, n: int, l: int, m: int, Z: int = 1, prec: int = 6):
        super().__init__(n, l, m, Z=Z, prec=prec)
        self.expr = self.expr * sympy.conjugate(self.expr)

    def __str__(self) -> str:
        n, l, m = self.n, self.l, self.m
        return f"PDF({orbital_name(n, l, m)})"
