import math
import matplotlib.pyplot as plt


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

        for step in range(steps):
            values.append(substance.initial_mass * (2 ** (-(current_t / substance.mean_lifetime))))
            current_t += step_size

        return values

    @staticmethod
    def show_graph(values):
        plt.plot(values)
        plt.ylabel('Nucleus left')
        plt.xlabel('Time in Seconds')
        plt.show()


def main():
    N0 = float(input('Initial mass of the carbon in kg='))
    t = float(input('Time for radioactive disintegration in sec='))
    T = 1760
    carbon = Substance(T, N0)
    N = HalfLifeCalculator.calc_remaining(carbon, t)
    print('Remaining carbon in kg=', N)


if __name__ == '__main__':
    main()
