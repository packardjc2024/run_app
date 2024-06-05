"""
This page is used to get the desired database and table name from the user
when setting up the app. That information is then written to the config
file to be accessed later.
"""

from GUI.temp_window import TempWindow
from tkinter import *
from GUI.login_window import LoginPage
from constants import read_config_file


class ConfigureMySQL:
    def __init__(self, config_path):
        self.config_path = config_path
        self.config = read_config_file(self.config_path)

    def create_window(self):
        self.window = TempWindow()
        self.window.create_main_frame()

    def mysql_frame(self):
        """
        Creates the entries to get the users input.
        """
        title = Label(self.window.frame,
                      text='Choose your database and table names',
                      borderwidth=2, relief='raised')
        database_label = Label(self.window.frame, text='Database:')
        self.database_entry = Entry(self.window.frame)
        table_label = Label(self.window.frame, text='Table:')
        self.table_entry = Entry(self.window.frame)
        button = Button(self.window.frame, text='Submit',
                        command=self.get_mysql_info)

        title.grid(row=0, columnspan=2, sticky='NEWS')
        database_label.grid(row=1, column=0)
        self.database_entry.grid(row=1, column=1)
        table_label.grid(row=2, column=0)
        self.table_entry.grid(row=2, column=1)
        button.grid(row=3, columnspan=2)

    def get_mysql_info(self):
        """
        Gets the users input from the GUI.
        """
        self.database = self.database_entry.get().strip().lower()
        self.table = self.table_entry.get().strip().lower()
        self.write_mysql_to_config()

    def write_mysql_to_config(self):
        """
        Writes the database and table names to the config file. 
        """
        self.config.set('mysql_info', 'database', self.database)
        self.config.set('mysql_info', 'table', self.table)
        self.config.set('set_up', 'is_configured', '1')
        with open(self.config_path, 'w') as config_file:
            self.config.write(config_file)
        self.window.destroy()
        self.login()

    def login(self):
        """
        Takes the user to the login page to log in to MySQL so that
        the database can be created.
        """
        login = LoginPage(self.config_path, is_configured=False)
        login.initialize()

    def initialize(self):
        self.create_window()
        self.mysql_frame()
        self.window.mainloop()
