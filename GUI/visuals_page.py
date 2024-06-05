"""
This module serves as the visuals page. The top will have a box for the user to
choose what visuals they would like to see and the bottom will have an embedded
canvas that will be used to display the matplotlib figure.
"""


from tkinter import *
from constants import *
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)


class RunVisuals:
    def __init__(self, root):
        self.root = root
        self.table = self.root.connection.table

    def create_choices_frame(self):
        """
        Creates the top frame that will hold the choices for the user.
        """
        self.visuals_frame = Frame(self.root.top_frame, borderwidth=1,
                                   relief='sunken')
        self.visuals_frame.grid(row=0, column=0, padx=10, pady=10)

        label = Label(self.visuals_frame, text="Scatter Plot", borderwidth=2,
                      relief='raised')
        label.grid(row=0, columnspan=2, sticky='NEWS')

        # Create the combobox for selecting the x-axis values
        columns = [column[:-1] for column in list(DISPLAY_NAMES_DICT.values())]
        x_label = Label(self.visuals_frame, text='X Axis:')
        x_label.grid(row=1, column=0, sticky='E')
        self.x_axis = ttk.Combobox(self.visuals_frame, values=columns)
        self.x_axis.current(0)
        self.x_axis.grid(row=1, column=1)

        # Create the combobox for the y-axis values
        y_label = Label(self.visuals_frame, text='Y Axis:')
        y_label.grid(row=2, column=0, sticky='E')
        self.y_axis = ttk.Combobox(self.visuals_frame, values=columns)
        self.y_axis.current(2)
        self.y_axis.grid(row=2, column=1)

        # Create the combobox for the date range value
        range_label = Label(self.visuals_frame, text='Range:')
        range_label.grid(row=3, column=0, sticky='E')
        self.range = ttk.Combobox(self.visuals_frame,
                                  values=['ALL', '30 Days', '60 Days', '90 Days'])
        self.range.current(0)
        self.range.grid(row=3, column=1)

        # Create a button that collects the info and creates teh visual
        self.visuals_button = Button(self.visuals_frame, text='Plot',
                                     command=self.plot)
        self.visuals_button.grid(row=4, columnspan=2)

    def create_plot_frame(self):
        # Create the bottom frame that will house the visual
        self.visuals_display = Frame(self.root.bottom_frame)
        self.visuals_display.grid(row=0, column=0, padx=10,
                                  pady=10)

    def plot(self):
        # Destroy and recreate plot frame in case existing visual
        self.visuals_display.destroy()
        self.create_plot_frame()

        # Get the values from the combo boxes
        x = self.x_axis.get().strip().lower().replace(' ', '_')
        y = self.y_axis.get().strip().lower().replace(' ', '_')
        date_range = self.range.get()
        if date_range == 'ALL':
            where = ''
        else:
            limit = int(date_range[:2])
            date = datetime.date.today() - datetime.timedelta(limit)
            where = f"date > '{date}' AND "

        # Format the results of the query into lists for the x and y-axis
        select_statement = f"""SELECT {x}, {y} FROM {self.table} WHERE {where}
         {x} is not null and {y} is not null;"""
        result = self.root.connection.execute_query(select_statement)
        x_results = [x[0] for x in result]
        y_results = [y[1] for y in result]

        # Create to embedded figure that will hold the plot
        figure = Figure(figsize=(10, 4), dpi=100)
        ax = figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(figure=figure,
                                        master=self.visuals_display)
        self.canvas.get_tk_widget().grid(row=0, column=0)

        # Create and draw the plot on the canvas
        ax.scatter(x_results, y_results)
        ax.set_xlabel(self.x_axis.get())
        ax.set_ylabel(self.y_axis.get())
        toolbar = NavigationToolbar2Tk(self.canvas, self.visuals_display,
                                       pack_toolbar=False)
        toolbar.update()
        toolbar.grid()
        self.canvas.draw()

    def initialize(self):
        self.root.table.destroy()
        self.create_choices_frame()
        self.create_plot_frame()
        self.current_frame = self.visuals_frame
        self.root.visuals_display = self.visuals_display
