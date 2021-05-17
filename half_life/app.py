from half_life.calculator import HalfLifeCalculator
from half_life.substance import Substance
from .window import DashboardView, Window
import sys


class Application(object):
    def __init__(self):
        self.window = Window(self.on_value_change)

        self.substance: Substance = Substance(0, 0)
        self.time_window = 0
    
    def run(self):
        self.window.mainloop()
        sys.exit()

    def on_value_change(self):
        self.substance = Substance(float(self.window.get_frame(DashboardView).half_life.get()), float(self.window.get_frame(DashboardView).initial_mass.get()))
        self.time_window = self.window.get_frame(DashboardView).time_window.get()

        vals = HalfLifeCalculator.calc_all(self.substance, self.time_window)

        self.window.get_frame(DashboardView).update_graph(vals)
