import math

from .substance import Substance


class HalfLifeCalculator(object):
    def __init__(self):
        pass

    @staticmethod
    def calc_remaining(substance: Substance, t: float) -> float:
        return substance.initial_mass * math.exp(-t / substance.mean_lifetime)

    @staticmethod
    def calc_all(substance: Substance, t: float, step_size: float = 1) -> list:
        values = []
        steps = round(t / step_size)
        current_t = 0

        for _ in range(steps):
            values.append(substance.initial_mass * (2 ** (-(current_t / substance.mean_lifetime))))
            current_t += step_size

        return values
