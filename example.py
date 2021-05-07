from half_life.calculator import HalfLifeCalculator
from half_life.substance import Substance


def main():
    francium = Substance(600, 10)
    values = HalfLifeCalculator.calc_all(francium, 3600)
    HalfLifeCalculator.show_graph(values)
	

if __name__ == '__main__':
    main()