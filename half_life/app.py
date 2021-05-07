from .window import Window


class Application(object):
    def __init__(self):
        self.window = Window()

    
    def run(self):
        self.window.mainloop()
