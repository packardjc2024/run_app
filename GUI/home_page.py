"""
This module houses the class that serves as the home/welcome page of the app.
This is the page that will appear when the app is initialized after logging in.
It queries the database and displays run summary information.
"""

from tkinter import *
from constants import *
import platform


class HomePage:
    def __init__(self, root):
        self.root = root
        self.table = self.root.connection.table

    def create_frame(self):
        """
        Creates the main frame and the summary frame that will hold the
        displayed information.
        """
        self.frame = Frame(self.root.top_frame, borderwidth=2)
        self.frame.grid(row=0, column=0, padx=10, pady=10)

        # Greeting
        text = "Welcome To Your Personal Run Tracking APP"
        welcome_label = Label(self.frame, text=text)
        welcome_label.grid(row=0, column=0, pady=10, padx=10)

        self.summary_frame = Frame(self.frame, borderwidth=2,
                                   relief='sunken')
        self.summary_frame.grid(row=1, column=0)
        label = Label(self.summary_frame, text='Your Running Summary',
                      borderwidth=2, relief='raised')
        label.grid(row=0, column=0, sticky='NEWS')

    def summaries(self):
        """
        Queries the database and displays the information about the users run
        history.
        """
        # Display the longest run time
        long_statement = f"SELECT MAX(duration) FROM {self.table};"
        long_query = self.root.connection.execute_query(long_statement)[0][0]
        display_time = datetime.timedelta(minutes=float(long_query))
        display_time = str(display_time)[:7]
        if platform.system() == 'Darwin':
            longest = Label(self.summary_frame, text=f"Longest Run (Time):\t\t{display_time}")
        elif platform.system() == 'Windows':
            longest = Label(self.summary_frame, text=f"Longest Run (Time):\t{display_time}")
        longest.grid(row=1, column=0, sticky='W')

        # Display the longest run distance
        distance_statement = f"SELECT MAX(distance) FROM {self.table};"
        distance_query = self.root.connection.execute_query(distance_statement)[0][0]
        distance = Label(self.summary_frame,
                         text=f"Longest Run (Distance):\t{distance_query} Miles")
        distance.grid(row=2, column=0, sticky='W')

        # Display the quickest mile pace
        pace_statement = f"SELECT MIN(pace) FROM {self.table};"
        pace_query = self.root.connection.execute_query(pace_statement)[0][0]
        pace_display = datetime.timedelta(minutes=float(pace_query))
        pace_display = str(pace_display)[2:7]
        pace = Label(self.summary_frame, text=f"Quickest Pace:\t\t{pace_display}")
        pace.grid(row=3, column=0, sticky='W')

        # Display the number of runs this month
        runs = self.root.connection.execute_query(f"""SELECT COUNT(run_id) FROM {self.table}
                WHERE date BETWEEN '{CURRENT_DATE.year}-{CURRENT_DATE.month}-01'
                AND '{CURRENT_DATE.year}-{CURRENT_DATE.month}-31';""")[0][0]
        runs_label = Label(self.summary_frame, text=f"Runs this month:\t\t{runs}")
        runs_label.grid(row=4, column=0, sticky='W')

    def check_for_runs(self):
        """
        Checks if there are any runs. If the table is empty, displays a different
        instead of calling the summaries method.
        """
        if self.root.connection.execute_query(f"""SELECT * FROM {self.table};"""):
            self.summaries()
        else:
            text = ("""Empty table. Enter a new run or import runs into the database\n
                  to get started""")
            label = Label(self.summary_frame, text=text)
            label.grid(row=1, column=0)

    def initialize(self):
        self.create_frame()
        self.check_for_runs()
        self.root.current_frame = self.frame
