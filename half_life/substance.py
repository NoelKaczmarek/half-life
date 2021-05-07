class Substance(object):
    def __init__(self, mean_lifetime: float, initial_mass: float):
        self._mean_lifetime = mean_lifetime
        self._initial_mass = initial_mass

    @property
    def mean_lifetime(self) -> float:
        return self._mean_lifetime

    @property
    def initial_mass(self) -> float:
        return self._initial_mass


all = [
    'Substance'
]
