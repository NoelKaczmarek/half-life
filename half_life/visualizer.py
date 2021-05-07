import matplotlib.pyplot as plt


class Visualizer(object):
    @staticmethod
    def show_graph(values, xlabel='Time in Seconds', ylabel='Nucleus left'):
        plt.plot(values)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.show()
