import math


class Substance(object):
    def __init__(self, half_life: float, initial_mass: float):
        self._mean_lifetime = None
        self._half_life = half_life
        self._initial_mass = initial_mass
        self._decay_constant = math.log(2) / self._half_life

    @property
    def half_life(self) -> float:
        print(self._half_life)
        return self._half_life

    @property
    def mean_lifetime(self) -> float:
        return self._mean_lifetime

    @property
    def initial_mass(self) -> float:
        return self._initial_mass

    @property
    def decay_constant(self) -> float:
        return self._decay_constant


all = [
    'Substance'
]
