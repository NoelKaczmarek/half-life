import math

from .substance import Substance


class HalfLifeCalculator(object):
    def __init__(self):
        pass

    @staticmethod
    def calc_remaining(substance: Substance, t: float) -> float:
        return substance.initial_mass * math.exp(-t / substance.mean_lifetime)

    @staticmethod
    def calc_all(substance: Substance, t: float, step_size: float = 0.01) -> list:
        values = []
        steps = round(t / step_size)
        current_t = 0

        for i in range(steps):
            res = HalfLifeCalculator.calc_step(substance, current_t)
            values.append(res / substance.initial_mass * 100 if i > 0 else 100)
            current_t += step_size

        return values

    @staticmethod
    def calc_step(substance: Substance, t: float) -> list:
        return substance.initial_mass * (2 ** (-(t / substance.mean_lifetime)))


all = [
    'HalfLifeCalculator'
]
