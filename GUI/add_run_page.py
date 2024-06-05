"""
This module has the class for the page that will add new runs to the database.
When runs are added to the database the time datatypes will be added to the
database as total minutes, but displayed in the table on screen as a string.
"""


from tkinter import *
from tkcalendar import Calendar
from GUI.custom_widgets import PaceEntry, TimeEntry, DurationEntry
from tkinter import messagebox
from constants import *


class AddRunPage:
    def __init__(self, root):
        self.root = root
        self.entries_dict = {}

    def create_frame(self):
        """
        Creates the main frame that serves as the add new run page for the app.
        """
        self.frame = Frame(self.root.top_frame, borderwidth=2, relief='sunken')
        self.frame.grid(row=0, column=0, padx=10, pady=10, sticky='NEWS')
        self.frame.rowconfigure(0, weight=0)
        for i in range(5):
            self.frame.columnconfigure(i, weight=1)
        for i in range(1, 8):
            self.frame.rowconfigure(i, weight=1)

    def fill_frame(self):
        """
        Adds the entries for all the columns in the database to add a new run.
        """
        # Create a label for the Frame
        self.frame_label = Label(self.frame, text="Enter A New Run",
                                 borderwidth=2, relief='raised')
        self.frame_label.grid(row=0, columnspan=5, sticky='NEWS', padx=0)

        # Grid date widget separately due to its size
        date_frame = Frame(self.frame)
        date_frame.grid(column=0, rowspan=6, row=1, padx=5)
        date_label = Label(date_frame, text='Date:')
        date_label.grid(column=0, row=0, sticky='EW', padx=5, pady=0)
        self.date_entry = Calendar(date_frame, selectmode='day',
                              year=CURRENT_DATE.year,
                              month=CURRENT_DATE.month,
                              day=CURRENT_DATE.day)
        self.date_entry.grid(row=1, column=0)
        self.entries_dict['date'] = self.date_entry

        # Create an entry for each of the remaining columns
        row = 1
        column = 1
        for key, value in DISPLAY_NAMES_DICT.items():
            if key != 'date':
                label = Label(self.frame, text=value)
                label.grid(column=column, row=row, sticky='E', padx=5, pady=0)
                column += 1
                if key in TIMES:
                    entry = TimeEntry(self.frame)
                elif key in MINUTES:
                    entry = DurationEntry(self.frame)
                elif key == 'pace':
                    entry = PaceEntry(self.frame)
                else:
                    entry = Entry(self.frame)
                entry.grid(column=column, row=row, padx=5)
                self.entries_dict[key] = entry
                if row < 6:
                    row += 1
                    column -= 1
                else:
                    row = 1
                    column += 1

        # Create a button to get and check all the values in the entries
        self.submit = Button(self.frame, text='Submit',
                             command=self.get_values)
        self.submit.grid(row=7, columnspan=5)

    def get_values(self, edit=False, original_date=None):
        """
        This function is called when the user clicks the
        submit button. It will get all the values from the entries, then save
        them to a dictionary, and then send that dictionary to the check_values
        function. If the values come from the edit page the edit parameter will
        be changed to True and will be passed on.
        """
        new_run = {}
        for key, entry in self.entries_dict.items():
            if key == 'date':  # Has a different method than regular entries
                value = entry.get_date()
            else:
                value = entry.get()
            new_run[key] = value
        self.check_values(new_run, edit, original_date)

    def check_values(self, run_dict: dict, edit, original_date):
        """
        Takes the dictionary of user input from the entries and first checks
        that no value is 0. Then it tries to convert the string to the proper
        datatype based on the lists established in the setup module.
        If there is an error a messagebox appears alerting the user to the entry
        and then clearing that entry and setting the focus on it.
        """
        for key, value in run_dict.items():
            # Force user to enter something other than 0
            if not value or value == 0:
                message = f"{key.upper()} cannot be '0' or left blank."
                messagebox.showwarning(message=message)
                self.entries_dict[key].delete(0, END)
                self.entries_dict[key].focus_set()
                break
            else:  # Attempt to convert value to proper datatype
                try:
                    if key in (INTEGERS, MINUTES):
                        run_dict[key] = int(value)
                    elif key in FLOATS:
                        run_dict[key] = float(value)
                    elif key in DATES:
                        run_dict[key] = datetime.datetime.strptime(value, '%m/%d/%y')
                except ValueError:
                    messagebox.showwarning(message=f"Invalid {key.upper()}")
                    self.entries_dict[key].delete(0, END)
                    self.entries_dict[key].focus_set()
                    break
        else:  # If no errors are found verify data and submit
            # Format the data for the messagebox verification
            message = "Are you sure you want to submit the run?\n"
            formatted_values = format_times(list(run_dict.values()))
            keys = list(run_dict.keys())
            keys = [key.replace('_', ' ').capitalize() for key in keys]
            message_dict = {keys[i]: value for i, value in enumerate(formatted_values)}
            message_dict['Date'] = str(message_dict['Date'])[:10]
            for key, value in message_dict.items():
                message += f"\t\t{key}: {value}\n"

            submit = messagebox.askyesno(message=message)
            if submit:
                self.send_to_database(run_dict, edit, original_date)
            else:
                self.entries_dict['duration'].focus_set()

    def send_to_database(self, run_dict, edit, original_date):
        """
        Sends the new run to the database, then reloads the table with the
        new run included. Also resets the entries for a new run.
        If edit it calls the update database method instead of add.
        """
        # Add the new run to the database
        if edit:
            self.root.connection.update(run_dict, original_date)
        else:
            self.root.connection.add_to_database(run_dict)

        # Reset the table to include the new run
        self.root.table.fill_table()

        # Clear the entries to enter a new run
        for entry in self.entries_dict:
            if entry != 'date':
                self.entries_dict[entry].delete(0, END)

    def initialize(self):
        self.create_frame()
        self.fill_frame()
        self.root.current_frame = self.frame
