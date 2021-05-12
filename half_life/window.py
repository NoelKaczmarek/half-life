from tkinter import ttk
import tkinter as tk

LARGE_FONT= ('Helvetica', 20)


class Window(tk.Tk):
    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)

        self.conf = {'base_path': '.'}
        self.save = 'config.json'
        
        # State
        self.ready = False
        self.running = False

        self.running_nodes = tk.IntVar()
        self.paused_nodes = tk.IntVar()

        # img = tk.Image('photo', file='icon.png')
        # self.tk.call('wm','iconphoto', self._w, img)

        self.width = 600
        self.height = 400
        self.geometry('%ix%i+%i+%i' % (self.width, self.height, self.winfo_screenwidth() / 2 - self.width / 2,
                                        self.winfo_screenheight() / 2 - self.height / 2))
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

        self.show_frame(StartPage)

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

        version = ttk.Label(win, text='Version 1.0.0')
        version.grid()

        credit = ttk.Label(win, text='© 2021 Noel Kaczmarek')
        credit.grid()

        b = ttk.Button(win, text='Okay', command=win.destroy)
        b.grid(row=1, column=0)


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

        self.columnconfigure(0, pad=2, weight=1)
        self.columnconfigure(1, pad=2)
        self.columnconfigure(2, pad=2)
        self.columnconfigure(3, pad=2, weight=1)
        self.columnconfigure(4, pad=2)

        self.rowconfigure(0, pad=2)
        self.rowconfigure(1, pad=2)
        self.rowconfigure(2, pad=2)
        self.rowconfigure(3, pad=2)
        self.rowconfigure(4, pad=2)
        self.rowconfigure(5, pad=2)
        self.rowconfigure(6, pad=2)
        self.rowconfigure(7, pad=2)
        self.rowconfigure(8, pad=2, weight=1)

        self.status = tk.StringVar()
        self.status.set('Not Connected')

        label = ttk.Label(self, text='Dashboard', font=LARGE_FONT)
        label.grid(row=0, column=0, sticky=tk.W)

        url_label = ttk.Label(self, text='Server URL:')
        url_label.grid(row=1, column=0, sticky=tk.W)
        self.url_value = ttk.Label(self)
        self.url_value.grid(row=1, column=4, sticky=tk.E)

        id_label = ttk.Label(self, text='ID:')
        id_label.grid(row=2, column=0, sticky=tk.W)
        self.id_val = ttk.Label(self)
        self.id_val.grid(row=2, column=4, sticky=tk.E)

        max_nodes_label = ttk.Label(self, text='Max. Nodes:')
        max_nodes_label.grid(row=3, column=0, sticky=tk.W)
        self.max_nodes_val = ttk.Label(self)
        self.max_nodes_val.grid(row=3, column=4, sticky=tk.E)

        running_nodes_label = ttk.Label(self, text='Running Nodes:')
        running_nodes_label.grid(row=4, column=0, sticky=tk.W)
        running_nodes = ttk.Label(self, textvariable=self.app.running_nodes)
        running_nodes.grid(row=4, column=4, sticky=tk.E)

        paused_nodes_label = ttk.Label(self, text='Paused Nodes:')
        paused_nodes_label.grid(row=5, column=0, sticky=tk.W)
        paused_nodes = ttk.Label(self, textvariable=self.app.paused_nodes)
        paused_nodes.grid(row=5, column=4, sticky=tk.E)

        status_label = ttk.Label(self, text='Status:')
        status_label.grid(row=6, column=0, sticky=tk.W)
        status_val = ttk.Label(self, textvariable=self.status)
        status_val.grid(row=6, column=4, sticky=tk.E)

        self.progress = ttk.Progressbar(self, mode='determinate')

        home_btn = ttk.Button(self, text='Back to Home',
                            command=lambda: controller.show_frame(StartPage))
        home_btn.grid(row=8, column=0, sticky=tk.S + tk.W)

        self.configure_btn = ttk.Button(self, text='Configure',
                            command=lambda: controller.show_frame(ConfigView))
        self.configure_btn.grid(row=8, column=2, sticky=tk.S + tk.E)
