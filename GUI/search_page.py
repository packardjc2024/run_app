"""
This module holds the class that serves as the search page for the app.
The user will be able to select from the fields to request information from
the database.
"""


from tkinter import *
from tkinter import ttk
from tkcalendar import Calendar
from tkinter import messagebox
from GUI.custom_widgets import PaceEntry, TimeEntry, DurationEntry
from constants import *


class SearchRunsPage:
    def __init__(self, root):
        self.root = root
        self.table = self.root.connection.table

    def create_frame(self):
        """
        Creates the frame and sets up the grid configuration.
        """
        self.frame = Frame(self.root.top_frame, borderwidth=2,
                           relief='sunken')
        self.frame.grid(row=0, pady=10)
        self.frame.rowconfigure(0, weight=0)
        self.frame.rowconfigure(1, weight=1)
        self.frame.rowconfigure(2, weight=0)
        self.number_columns = 4
        for column in range(self.number_columns):
            self.frame.columnconfigure(column, weight=0)

    def create_sub_frames(self):
        """
        Creates the sub-frames that will hold the different search options.
        """
        search_label = Label(self.frame, text="Search for a run",
                             relief='raised', borderwidth=2)
        search_label.grid(row=0, columnspan=self.number_columns, sticky='NEWS')

        # Create the 3 subframes that will hold the options
        self.where_frame = Frame(self.frame, borderwidth=2,
                                 relief='sunken')
        self.where_frame.grid(row=1, column=1, sticky='NEWS', padx=5, pady=5)
        self.fill_where_frame()

        self.order_frame = Frame(self.frame, borderwidth=2,
                                 relief='sunken')
        self.order_frame.grid(row=1, column=2, padx=5, pady=5, sticky='NEWS')
        self.fill_order_frame()

        self.limit_frame = Frame(self.frame, borderwidth=2,
                                 relief='sunken')
        self.limit_frame.grid(row=1, column=3, padx=5, pady=5, sticky='NEWS')
        self.fill_limit_frame()

        # Set up the submit button
        submit = Button(self.frame, text='Submit', command=self.query)
        submit.grid(row=2, columnspan=self.number_columns)

    def fill_where_frame(self):
        """
        Creates three entries to be used to make the MySQL comparison statement.
        Three class variables are created to be collected in the button
        function:
        self.column_variable, self.options, self.op_box
        """
        # Set up the grid configuration
        self.where_frame.columnconfigure(0, weight=1)
        self.where_frame.columnconfigure(1, weight=1)

        # Set up the column combobox with a string variable that is traced
        # so that the final row knows what kind of entry to add
        self.column_variable = StringVar(self.where_frame, value='Date')
        self.column_variable.trace('w', self.value_options)

        compare_label = Label(self.where_frame, text="Comparison Column",
                              borderwidth=2, relief='raised')
        compare_label.grid(row=0, columnspan=2, sticky='NEWS')
        options_list = [column[:-1] for column in DISPLAY_NAMES_DICT.values()]
        self.options = ttk.Combobox(self.where_frame, values=options_list,
                                    state='readonly',
                                    textvariable=self.column_variable)
        self.options.grid(row=1, columnspan=2, sticky='NEWS')

        # Choose a comparison operator from a combobox
        operator_label = Label(self.where_frame, text="Comparison",
                               borderwidth=2, relief='raised')
        operator_label.grid(row=2, columnspan=2, sticky='NEWS')
        operators = ["<", "<=", ">", ">=", "==", "!="]
        self.op_box = ttk.Combobox(self.where_frame, values=operators,
                                   state='readyonly')
        self.op_box.current(0)
        self.op_box.grid(row=3, columnspan=2, sticky='NEWS')

        # Create an entry widget based on the value
        value_label = Label(self.where_frame, text="Value",
                            borderwidth=2, relief='raised')
        value_label.grid(row=4, columnspan=2, sticky='NEWS')

        # Create the value entry in a separate frame so that it can be destroyed
        self.value_frame = Frame(self.where_frame)
        self.value_frame.grid(row=5, columnspan=2, sticky='NEWS')
        self.value_frame.columnconfigure(0, weight=1)

        self.value_entry = Calendar(self.value_frame, selectmode='day',
                                    year=CURRENT_DATE.year,
                                    month=CURRENT_DATE.month,
                                    day=CURRENT_DATE.day)
        self.value_entry.grid(row=5, column=0, sticky='NEWS', padx=5, pady=5)

        # Set the column combobox after the value entry box has been populated
        self.options.current(0)

    def fill_order_frame(self):
        """
        Creates two string variables and corresponding radiobuttons to select
        the column to order by and which direction to sort.
        """
        # Set up the frame grid configuration
        self.order_frame.columnconfigure(0, weight=1)
        self.order_frame.columnconfigure(1, weight=1)

        # Radio buttons with each column as an option
        self.order_variable = StringVar(self.order_frame, value=COLUMN_NAMES[0])
        order_label = Label(self.order_frame, text='Order By', relief='raised',
                            borderwidth=2)
        order_label.grid(row=0, columnspan=2, sticky='NEWS')
        row = 1
        column = 0
        for key, value in DISPLAY_NAMES_DICT.items():
            Radiobutton(self.order_frame, value=key,
                        variable=self.order_variable,
                        text=value[:-1]).grid(row=row, column=column, sticky='W')
            if row < 7:
                row += 1
            else:
                row = 1
                column += 1

        # Radio button with asc or desc options
        self.direction_variable = StringVar(self.order_frame, 'DESC')
        direction_row = 8
        direction_label = Label(self.order_frame, text='ASC / DESC',
                                relief='raised', borderwidth=2)
        direction_label.grid(row=direction_row, columnspan=2, sticky='NEWS')

        asc = Radiobutton(self.order_frame, text='Ascending', value='ASC',
                          variable=self.direction_variable)
        asc.grid(row=direction_row + 1, columnspan=2, sticky='W')
        desc = Radiobutton(self.order_frame, value='DESC', text='Descending',
                           variable=self.direction_variable)
        desc.grid(row=direction_row + 2, columnspan=2, sticky='W')

    def fill_limit_frame(self):
        """
        Creates a string variable and corresponding radio buttons for the
        user to select how many results they want to see.
        """
        label = Label(self.limit_frame, text='Maximum Runs to Return',
                      relief='raised', borderwidth=2)
        label.grid(row=0, sticky='NEWS')

        options = ['ALL', 5, 10, 15, 20, 50, 100]
        self.limit = StringVar(self.limit_frame, value=options[0])
        row = 1
        for option in options:
            radio = Radiobutton(self.limit_frame, value=option, text=option,
                                variable=self.limit)
            radio.grid(row=row, sticky='W')
            row += 1

    def query(self):
        """
        Gets all the search frame class variables and combines them into
        a formatted select statement.
        """
        # Get the values from the value entry widget and make sure they are
        # properly formatted. If there is no where value it will be blank
        if self.value_entry:
            comp_column = self.options.get().strip().lower().replace(' ', '_')
            operator = self.op_box.get()
            if comp_column in INTEGERS:
                value = int(float(self.value_entry.get()))
            elif comp_column == 'date':
                value = self.value_entry.get_date()
                dt = datetime.datetime.strptime(value, '%m/%d/%y')
                value = f"'{dt.strftime('%Y-%m-%d')}'"
            elif comp_column in TIMES:
                value = f"'{self.value_entry.get()}'"
            else:
                value = self.value_entry.get()
            where = f"""WHERE {comp_column} {operator} {value}"""
        else:
            where = ''

        # Get the column to order the results by as order
        order = self.order_variable.get()

        # Get the way to order the results as direction
        direction = self.direction_variable.get()

        # Get how many results to return as limit
        if self.limit.get() == 'ALL':
            limit = ''
        else:
            limit = f"LIMIT {int(self.limit.get())}"

        # Format the select statement to search in the database
        select_statement = f"""SELECT * FROM {self.table} {where}
    ORDER BY {order} {direction} {limit};"""
        try:
            self.root.table.fill_table(select_statement)
        except:
            message = f"""Invalid Value for {self.options.get().upper()}\n\n
    Check the VALUE and try again"""
            messagebox.showwarning(message=message)
            self.value_entry.focus_set()

    def value_options(self, *args):
        """
        This function is tied to the value entry string variable and
        populates the correct type of entry for the column selected.
        """
        # Reset the page if the column is changed after starting
        self.value_frame.destroy()

        self.value_frame = Frame(self.where_frame)
        self.value_frame.grid(row=5, columnspan=2, sticky='NEWS')
        self.value_frame.columnconfigure(0, weight=1)

        # Choose the correct entry type for the column
        column = self.column_variable.get().strip().lower().replace(' ', '_')
        if column == 'pace':
            self.value_entry = PaceEntry(self.value_frame)
        elif column in INTEGERS or column in FLOATS:
            self.value_entry = Entry(self.value_frame)
        elif column in DATES:
            self.value_entry = Calendar(self.value_frame, selectmode='day',
                                        year=CURRENT_DATE.year,
                                        month=CURRENT_DATE.month,
                                        day=CURRENT_DATE.day)
        elif column in TIMES:
            self.value_entry = TimeEntry(self.value_frame)
        elif column in MINUTES:
            self.value_entry = DurationEntry(self.value_frame)

        self.value_entry.grid(row=5, column=0, sticky='NEWS', padx=5, pady=5)

    def initialize(self):
        self.create_frame()
        self.create_sub_frames()
        self.fill_where_frame()
        self.fill_limit_frame()
        self.fill_order_frame()
        self.root.current_frame = self.frame
