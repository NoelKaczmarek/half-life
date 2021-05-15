from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib

from tkinter import ttk
import tkinter as tk

LARGE_FONT= ('Helvetica', 20)


class Window(tk.Tk):
    def __init__(self, on_value_change, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)
        
        # State
        self.ready = False
        self.running = False

        self.on_value_change = on_value_change

        self.title('Half-Life Simulation')
        img = tk.Image('photo', file='icon.png')
        self.tk.call('wm','iconphoto', self._w, img)

        self.width = 600
        self.height = 400
        # self.geometry('%ix%i+%i+%i' % (self.width, self.height, self.winfo_screenwidth() / 2 - self.width / 2,
        #                                self.winfo_screenheight() / 2 - self.height / 2))
        self.resizable(False, False)
        # ttk.Style().configure('TButton', padding=(0, 5, 0, 5), font='Helvetica')

        container = tk.Frame(self)

        container.pack(side='top', fill='both', padx=10, pady=10, expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, ConfigView, DashboardView):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky='nsew')

        self.show_frame(DashboardView)

        menubar = tk.Menu(self)

        filemenu = tk.Menu(menubar, tearoff=0)

        # Add file menu entries
        
        filemenu.add_separator()

        filemenu.add_command(label='Quit', command=self.quit)
        menubar.add_cascade(label='File', menu=filemenu)

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

        b = ttk.Button(win, text='Okay', command=win.destroy)
        b.grid(row=2, column=0)


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text='Start Page', font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        dashboard_btn = ttk.Button(self, text='Dashboard',
                            command=lambda: controller.show_frame(DashboardView))
        dashboard_btn.pack()

        confgure_btn = ttk.Button(self, text='Configure',
                            command=lambda: controller.show_frame(ConfigView))
        confgure_btn.pack()


class ConfigView(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.app = controller

        self.columnconfigure(0, pad=2)
        self.columnconfigure(1, pad=2, weight=1)
        self.columnconfigure(2, pad=2)
        self.columnconfigure(3, pad=2)

        self.rowconfigure(0, pad=2)
        self.rowconfigure(1, pad=2)
        self.rowconfigure(2, pad=2)
        self.rowconfigure(3, pad=2)
        self.rowconfigure(4, pad=2, weight=1)

        title = ttk.Label(self, text='Config', font=LARGE_FONT)
        title.grid(row=0, column=0, sticky=tk.W)

        url_label = ttk.Label(self, text='Server URL: ')
        url_label.grid(row=1, column=0, sticky=tk.W)
        self.url = ttk.Entry(self)
        self.url.grid(row=1, column=1, sticky=tk.W + tk.E)

        max_nodes_label = ttk.Label(self, text='Max. Nodes: ')
        max_nodes_label.grid(row=2, column=0, sticky=tk.W)
        self.max_nodes = ttk.Entry(self)
        self.max_nodes.grid(row=2, column=1, sticky=tk.W + tk.E)

        base_dir_label = ttk.Label(self, text='Base Directory: ')
        base_dir_label.grid(row=3, column=0, sticky=tk.W)
        self.base_dir = ttk.Entry(self)
        self.base_dir.grid(row=3, column=1, sticky=tk.W + tk.E)

    def update_entries(self):
        self.url.insert(0, self.app.conf['url'])
        self.max_nodes.insert(0, self.app.conf['max_nodes'])
        self.base_dir.insert(0, self.app.conf['base_path'])


class DashboardView(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.app = controller

        self.columnconfigure(0, pad=2)
        self.columnconfigure(1, pad=2, weight=1)
        self.columnconfigure(2, pad=2)

        self.rowconfigure(0, pad=2)
        self.rowconfigure(1, pad=2)
        self.rowconfigure(2, pad=2)
        self.rowconfigure(3, pad=2)
        self.rowconfigure(4, pad=2)

        self.status = tk.StringVar()

        label = ttk.Label(self, text='Dashboard', font=LARGE_FONT)
        label.grid(row=0, column=0, sticky=tk.W)

        url_label = ttk.Label(self, text='Time Window:')
        url_label.grid(row=1, column=0, sticky=tk.W)

        self.time_window = tk.DoubleVar()
        time_window_value = ttk.Label(
            self,
            textvariable=self.time_window
        )
        time_window_value.grid(row=1, column=2)
        time_window_slider = ttk.Scale(
            self,
            from_=0,
            to=100,
            orient='horizontal',
            variable=self.time_window,
            command=self.on_value_change
        )
        time_window_slider.grid(row=1, column=1)

        id_label = ttk.Label(self, text='Initial Mass:')
        id_label.grid(row=2, column=0, sticky=tk.W)

        self.initial_mass = tk.DoubleVar()
        initial_mass_slider = ttk.Scale(
            self,
            from_=0,
            to=100,
            orient='horizontal',
            variable=self.initial_mass,
            command=self.on_value_change
        )
        initial_mass_slider.grid(row=2, column=1)
        initial_mass_value = ttk.Label(
            self,
            textvariable=self.initial_mass
        )
        initial_mass_value.grid(row=2, column=2)

        status_label = ttk.Label(self, text='Half-Life:')
        status_label.grid(row=3, column=0, sticky=tk.W)

        self.half_life = tk.DoubleVar()
        half_life_slider = ttk.Scale(
            self,
            from_=0,
            to=100,
            orient='horizontal',
            variable=self.half_life,
            command=self.on_value_change
        )
        half_life_slider.grid(row=3, column=1)
        half_life_value = ttk.Label(
            self,
            textvariable=self.half_life
        )
        half_life_value.grid(row=3, column=2)

        matplotlib.use('TkAgg')
        self.fig = plt.figure(1)
        canvas = FigureCanvasTkAgg(self.fig, master=self)
        plot_widget = canvas.get_tk_widget()
        plot_widget.grid(row=4, column=1, sticky=tk.S + tk.W)

    def on_value_change(self, event):
        self.app.on_value_change()

    def update_graph(self, vals):
        """Example function triggered by Tkinter GUI to change matplotlib graphs."""
        plt.clf()
        plt.plot(vals)
        self.fig.canvas.draw()


all = [
    'Window',
    'DashboardView'
]
