"""
This module houses the class for the displayed runs for the app. It is housed
on the bottom frame of the main window and is seen unless on the visuals page.
"""

from tkinter import *
from tkinter import ttk
from constants import *

class RunsTable(Frame):
    """
    The display_frame will hold a treeview widget that will populate
    the old runs from the database and then add the new runs that
    the users enters in.
    """
    def __init__(self, root, bottom_frame, connection=None):
        super().__init__(bottom_frame)
        self.root = root
        self.connection = connection
        self.table = self.connection.table

        # Configure the frame
        self.grid(row=0, column=0, sticky='NEWS', padx=10, pady=10)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=0)  # For # of results
        self.rowconfigure(1, weight=1)  # For the table
        self.rowconfigure(2, weight=0)  # for the toolbar

    def create_table(self):
        """
        Creates the treeview table that will display the runs from the database.
        """
        # Create a label that shows how many results were found
        self.results_label = Label(self, text="0 Results Found")
        self.results_label.grid(row=0, sticky='NEWS')

        # Create the table widget using treeview
        self.run_table = ttk.Treeview(self, show='headings', selectmode='browse')
        self.run_table['columns'] = COLUMN_NAMES
        self.run_table.grid(row=1, column=0, sticky='NEWS')

        # Label the columns and set the width of each column
        index = 0
        for column_name in self.run_table['columns']:
            self.run_table.heading(index, text=DISPLAY_NAMES_DICT[column_name])
            self.run_table.column(column=column_name, width=87, anchor='center')
            index += 1

    def fill_table(self, search_statement=None):
        """
        Upon opening the app the table will automatically get all the
        past runs from the database to display. This method will also be called
        to repopulate the table once a new run has been added.
        """
        # Clears the table if there is any data already in it
        for row in self.run_table.get_children():
            self.run_table.delete(row)

        # Get the runs from the database
        if search_statement:  # Comes from the search page
            select_statement = search_statement
        else:
            select_statement = f"""SELECT * FROM {self.table} ORDER BY date DESC;"""
        query_result = self.connection.execute_query(select_statement)

        # Convert result tuples to lists and remove the run id column
        previous_runs = [list(result)[1:] for result in query_result]

        # Format pace, duration, and start time for viewing
        formatted_runs = [format_times(run) for run in previous_runs]

        # Clear the table
        for item in self.run_table.get_children():
            self.run_table.delete(item)

        # Reconfigures the display frame label with the lenth of the results
        number_results = len(formatted_runs)
        self.results_label.configure(text=f"{number_results} Results Found")

        # Add the runs to the table
        for run in formatted_runs[::-1]:
            self.run_table.insert("", 0, text="",
                                  values=run)

    def initialize(self):
        self.create_table()
        self.fill_table()