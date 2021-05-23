from half_life import RESOURCE_PATH
from half_life.substance import Substance
from half_life.calculator import HalfLifeCalculator
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib

from tkinter import filedialog as fd
from tkinter import ttk
import tkinter as tk
import random
import os

LARGE_FONT= ('Helvetica', 20)


class Window(tk.Tk):
    def __init__(self, on_value_change, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.on_value_change = on_value_change
        self.frames = {}

        self.configure_gui()
        self.create_widgets()

        self.show_frame(StartPage)
        self.focus_force()

    def configure_gui(self):
        self.title('Half-Life Simulation')
        # img = tk.Image('photo', file=os.path.join(RESOURCE_PATH, 'icon.png'))
        # self.tk.call('wm','iconphoto', self._w, img)
        self.protocol('WM_DELETE_WINDOW', self.on_close)
        self.iconbitmap(os.path.join(RESOURCE_PATH, 'icon.ico'))
        # background_color = '#0099FF'
        # self.configure(bg=background_color)

        self.width = 640
        self.height = 480
        # self.geometry('%ix%i+%i+%i' % (self.width, self.height, self.winfo_screenwidth() / 2 - self.width / 2,
        #                                self.winfo_screenheight() / 2 - self.height / 2))
        # self.resizable(False, False)
        # ttk.Style().configure('TButton', padding=(0, 5, 0, 5), font='Helvetica')

    def create_widgets(self):
        container = ttk.Frame(self)

        container.pack(side='top', fill='both', padx=10, pady=10, expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        for F in (StartPage, SimulationView, GraphView,):
            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky='nsew')

        self.create_menubar()

    def create_menubar(self):
        menubar = tk.Menu(self)

        filemenu = tk.Menu(menubar, tearoff=0)

        filemenu.add_command(label='Export', command=self.get_frame(GraphView).export)        
        filemenu.add_separator()

        filemenu.add_command(label='Quit', command=self.quit)
        menubar.add_cascade(label='File', menu=filemenu)

        navmenu = tk.Menu(menubar, tearoff=0)

        commands = {}

        for frame in self.frames:
            def frame_command(frame):
                def show_frame():
                    self.show_frame(frame)
                return show_frame

            commands[frame] = frame_command(frame)

        for frame in self.frames:
            navmenu.add_command(label=frame.name, command=commands[frame])
        
        menubar.add_cascade(label='Navigation', menu=navmenu)

        helpmenu = tk.Menu(menubar, tearoff=0)
        helpmenu.add_command(label='About', command=self.about)
        menubar.add_cascade(label='Help', menu=helpmenu)

        self.config(menu=menubar)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def get_frame(self, cont):
        return self.frames[cont]

    def about(self):
        win = tk.Toplevel()
        win.wm_title('About')
        win.resizable(0, 0)
        win.attributes('-toolwindow', True)

        win.columnconfigure(0, pad=2)

        win.rowconfigure(0, pad=2)
        win.rowconfigure(1, pad=2)
        win.rowconfigure(2, pad=2)

        version = ttk.Label(win, text='Version 1.0.0')
        version.grid(row=0, column=0)

        credit = ttk.Label(win, text='© 2021 Noel Kaczmarek')
        credit.grid(row=1, column=0)

        b = ttk.Button(win, text='OK', command=win.destroy)
        b.grid(row=2, column=0)

        win.focus_force()

    def on_close(self):
        self.quit()


class StartPage(tk.Frame):
    name = 'Home'

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.grid_columnconfigure(0, weight=1)

        label = ttk.Label(self, text='Start Page', font=LARGE_FONT)
        label.grid(row=0, pady=10, padx=10, sticky=tk.E + tk.W)

        s = ttk.Style()
        s.configure('my.TButton', font=('Helvetica', 13))

        graph_btn = ttk.Button(self, text='Graph',
                            command=lambda: controller.show_frame(GraphView), style='my.TButton')
        graph_btn.grid(row=1, ipadx=50, ipady=20, sticky=tk.E + tk.W)

        simulation_btn = ttk.Button(self, text='Simulation',
                            command=lambda: controller.show_frame(SimulationView), style='my.TButton')
        simulation_btn.grid(row=2, ipadx=50, ipady=20, sticky=tk.E + tk.W)


class SimulationView(tk.Frame):
    name = 'Simulation'

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.app = controller
        
        self.running = False

        self.decayed_points = []
        self.points = []

        self.mean_lifetime = tk.IntVar()
        self.mean_lifetime.set(20)

        self.decayed = 0
        self.time_elapsed = tk.IntVar()
        self.substance = Substance(self.mean_lifetime.get(), 100)

        self.total_points = tk.IntVar()
        self.points_left = tk.DoubleVar()
        self.points_decayed = tk.DoubleVar()

        self.configure_gui()
        self.create_widgets()

    def configure_gui(self):
        self.line_distance = 20
        self.point_size = 10

    def create_widgets(self):
        label = ttk.Label(self, text='Simulation', font=LARGE_FONT)
        label.pack(fill=tk.X)

        self.canvas = tk.Canvas(self)
        self.canvas.pack(expand=tk.YES, fill=tk.BOTH, pady=2)
        # self.canvas.bind('<B1-Motion>', self.paint)

        self.create_labels()

    def create_labels(self):
        bottom_frame = ttk.Frame(self)
        bottom_frame.pack(side=tk.BOTTOM, fill=tk.BOTH)

        bottom_frame.columnconfigure(0, pad=20)
        bottom_frame.columnconfigure(1, pad=2)
        bottom_frame.columnconfigure(2, pad=2, weight=1)

        bottom_frame.rowconfigure(0, pad=2)
        bottom_frame.rowconfigure(1, pad=2)
        bottom_frame.rowconfigure(2, pad=2)
        bottom_frame.rowconfigure(3, pad=2)
        bottom_frame.rowconfigure(4, pad=2)

        total_points_label = ttk.Label(bottom_frame, text='Total Points:')
        total_points_label.grid(row=0, column=0, sticky=tk.W)

        total_points_value = ttk.Label(bottom_frame, textvariable=self.total_points)
        total_points_value.grid(row=0, column=1, sticky=tk.E + tk.W)

        points_left_label = ttk.Label(bottom_frame, text='Points Left:')
        points_left_label.grid(row=1, column=0, sticky=tk.W)

        points_left_value = ttk.Label(bottom_frame, textvariable=self.points_left)
        points_left_value.grid(row=1, column=1, sticky=tk.E + tk.W)

        points_decayed_label = ttk.Label(bottom_frame, text='Points Decayed:')
        points_decayed_label.grid(row=2, column=0, sticky=tk.W)

        points_decayed_value = ttk.Label(bottom_frame, textvariable=self.points_decayed)
        points_decayed_value.grid(row=2, column=1, sticky=tk.E + tk.W)

        time_elapsed_label = ttk.Label(bottom_frame, text='Time Elapsed:')
        time_elapsed_label.grid(row=3, column=0, sticky=tk.W)

        time_elapsed_value = ttk.Label(bottom_frame, textvariable=self.time_elapsed)
        time_elapsed_value.grid(row=3, column=1, sticky=tk.E + tk.W)

        mean_lifetime_label = ttk.Label(bottom_frame, text='Mean Lifetime:')
        mean_lifetime_label.grid(row=4, column=0, sticky=tk.W)

        self.mean_lifetime_slider = ttk.Scale(bottom_frame,
            from_=0,
            to=100,
            orient='horizontal',
            variable=self.mean_lifetime)
        self.mean_lifetime_slider.grid(row=4, column=2, sticky=tk.E)

        mean_lifetime_value = ttk.Label(bottom_frame, textvariable=self.mean_lifetime)
        mean_lifetime_value.grid(row=4, column=1, sticky=tk.E + tk.W)

        self.start_btn = ttk.Button(bottom_frame, text='Start', command=self.start)
        self.start_btn.grid(row=0, column=2, sticky=tk.E, ipadx=15)

        self.pause_btn = ttk.Button(bottom_frame, text='Pause', state=tk.DISABLED, command=self.pause)
        self.pause_btn.grid(row=1, column=2, sticky=tk.E, ipadx=15)

    def draw_checkerboard(self, line_distance):
        self.canvas.update()
        width, height = self.canvas.winfo_width(), self.canvas.winfo_height()

        for x in range(line_distance, width, line_distance):
            self.canvas.create_line(x, 0, x, height, fill='#476042')

        for y in range(line_distance, height, line_distance):
            self.canvas.create_line(0, y, width, y, fill='#476042')

    def paint(self, event):
        python_green = '#476042'
        x1, y1 = (event.x - 1), (event.y - 1)
        x2, y2 = (event.x + 1), (event.y + 1)
        self.canvas.create_oval(x1, y1, x2, y2, fill=python_green)

    def draw_point(self, x, y):
        python_green = '#0099FF'
        one_axis_size = self.point_size / 2
        x1, y1 = (x - one_axis_size), (y - one_axis_size)
        x2, y2 = (x + one_axis_size), (y + one_axis_size)
        return self.canvas.create_oval(x1, y1, x2, y2, fill=python_green)

    def draw_points(self):
        width, height = self.canvas.winfo_width(), self.canvas.winfo_height()
        points_per_row = round(width / self.line_distance)
        points_per_column = round(height / self.line_distance)
        self.decayed_points = []
        self.points = []

        for i in range(points_per_column):
            for j in range(points_per_row):
                self.points.append(self.draw_point(j * self.line_distance + self.point_size, i * self.line_distance + self.point_size))
        
    def start(self):
        if self.running:
            self.running = False
            self.start_btn.configure(text='Start')
            self.pause_btn.configure(state=tk.DISABLED, text='Pause')
            self.mean_lifetime_slider.configure(state=tk.NORMAL)
            self.canvas.delete('all')
        else:
            self.running = True
            self.start_btn.configure(text='Reset')
            self.pause_btn.configure(state=tk.NORMAL)
            self.mean_lifetime_slider.configure(state=tk.DISABLED)
        
        self.draw_checkerboard(self.line_distance)
        self.draw_points()

        self.substance = Substance(self.mean_lifetime.get(), 100)
        self.total_points.set(len(self.points))
        self.time_elapsed.set(0)
        self.decayed = 0

        self.loop()

    def pause(self):
        if self.running:
            self.running = False
            self.pause_btn.configure(text='Resume')
        else:
            self.running = True
            self.pause_btn.configure(text='Pause')
            self.loop()

    def loop(self):
        if not self.running:
            return
        
        decayed_last = self.decayed
        percent_left = HalfLifeCalculator.calc_step(self.substance, self.time_elapsed.get())
        percent_decayed = 100 - percent_left
        self.points_left.set(percent_left / 100 * self.total_points.get())
        self.points_decayed.set(self.total_points.get() - self.points_left.get())
        self.decayed = self.points_decayed.get()
        points_to_decay = self.decayed - decayed_last
        # print('Left (%):', percent_left, 'Decayed (%):', percent_decayed, 'To decay (Points):', points_to_decay)

        for _ in range(round(points_to_decay)):
            point = random.choice(self.points)
            self.points.remove(point)
            self.decayed_points.append(point)
            self.canvas.itemconfig(point, fill='orange')

        self.update()

        if len(self.points) == 0:
            self.running = False

        self.time_elapsed.set(self.time_elapsed.get() + 1)
        self.canvas.after(1000, self.loop)

        
class GraphView(tk.Frame):
    name = 'Graph'

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.app = controller

        self.configure_gui()
        self.create_widgets()

    def configure_gui(self):
        self.columnconfigure(0, pad=2)
        self.columnconfigure(1, pad=2, weight=1)
        self.columnconfigure(2, pad=2)

        self.rowconfigure(0, pad=2)
        self.rowconfigure(1, pad=2)
        self.rowconfigure(2, pad=2)
        self.rowconfigure(3, pad=2)
        self.rowconfigure(4, pad=0, weight=1)

    def create_widgets(self):
        label = ttk.Label(self, text='Dashboard', font=LARGE_FONT)
        label.grid(row=0, column=0, sticky=tk.W)

        url_label = ttk.Label(self, text='Time Window:')
        url_label.grid(row=1, column=0, sticky=tk.W)

        self.time_window = tk.DoubleVar()
        self.time_window.set(100)
        time_window_value = ttk.Label(
            self,
            textvariable=self.time_window
        )
        time_window_value.grid(row=1, column=1)
        time_window_slider = ttk.Scale(
            self,
            from_=1,
            to=100,
            orient='horizontal',
            variable=self.time_window,
            command=self.on_value_change
        )
        time_window_slider.grid(row=1, column=2)

        id_label = ttk.Label(self, text='Initial Mass:')
        id_label.grid(row=2, column=0, sticky=tk.W)

        self.initial_mass = tk.DoubleVar()
        self.initial_mass.set(100)
        initial_mass_value = ttk.Label(
            self,
            textvariable=self.initial_mass
        )
        initial_mass_value.grid(row=2, column=1)
        initial_mass_slider = ttk.Scale(
            self,
            from_=1,
            to=100,
            orient='horizontal',
            variable=self.initial_mass,
            command=self.on_value_change
        )
        initial_mass_slider.grid(row=2, column=2)

        status_label = ttk.Label(self, text='Half-Life:')
        status_label.grid(row=3, column=0, sticky=tk.W)

        self.half_life = tk.DoubleVar()
        self.half_life.set(20)
        half_life_value = ttk.Label(
            self,
            textvariable=self.half_life
        )
        half_life_value.grid(row=3, column=1)
        half_life_slider = ttk.Scale(
            self,
            from_=1,
            to=100,
            orient='horizontal',
            variable=self.half_life,
            command=self.on_value_change
        )
        half_life_slider.grid(row=3, column=2)

        self.create_plot()
        
    def create_plot(self):
        matplotlib.use('TkAgg')
        self.fig = plt.figure(1)
        plt.xlabel('Time in Seconds')
        plt.ylabel('Nuclei left in %')
        canvas = FigureCanvasTkAgg(self.fig, master=self)
        plot_widget = canvas.get_tk_widget()
        plot_widget.grid(row=4, columnspan=3, sticky=tk.N + tk.S + tk.E + tk.W, pady=(5, 0))

    def on_value_change(self, event=None):
        self.app.on_value_change()

    def export(self):
        filename = fd.asksaveasfilename(
            title='Save file',
            initialdir='.',
            filetypes=[('PNG files', '*.png'),],
            defaultextension='.png')
        
        if filename:
            plt.savefig(filename, 
                dpi = 100)

    def update_graph(self, vals):
        """Example function triggered by Tkinter GUI to change matplotlib graphs."""
        plt.clf()
        plt.xlabel('Time in Seconds')
        plt.ylabel('Nuclei left in %')
        plt.plot(vals)
        self.fig.canvas.draw()


all = [
    'Window'
]
