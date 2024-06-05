"""
The program begins by initializing a tkinter window that will only be used for
the login. Once logged in the program attempts to find a new data file,
clean it, and unpack. If no file is found, the app is initialized. The app is
opened in a new window using the root window module.
"""

from constants import *
import mysql.connector
from tkinter import *
from tkinter import messagebox
from GUI.root_window import Window
from database import Database
from pathlib import Path
from SetUp.set_up_config_file import clear_configuration_file
from CleaningData.get_new_xml import GetNewXML
from CleaningData.clean_xml import CleanXML
from CleaningData.add_csv_to_database import AddCSVtoDatabase


class LoginPage(Tk):
    def __init__(self, config_path, is_configured=True):
        super().__init__()
        self.config_path = config_path
        self.is_configured = is_configured
        self.login_attempts = 3
        self.config = read_config_file(self.config_path)

    def configure_window(self):
        # Set up the window geometry
        window_width = 400
        window_height = 400
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        y = screen_height // 2 - window_height // 2
        x = screen_width // 2 - window_width // 2
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # Set up the window configuration
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

    def create_login_frame(self):
        """
        Creates the login frame that will be used if the database
        has already been created.
        """
        self.login_frame = Frame(self, borderwidth=2, relief='sunken')
        self.login_frame.grid()
        self.login_frame.columnconfigure(0, weight=0)
        self.login_frame.columnconfigure(1, weight=0)
        login_label = Label(self.login_frame,
                            text='Login Using Your MySQL Information',
                            borderwidth=2, relief='raised')

        # Username and Password
        username_label = Label(self.login_frame, text='User:')
        self.username_entry = Entry(self.login_frame, show="*")
        password_label = Label(self.login_frame, text='Password:')
        self.password_entry = Entry(self.login_frame, show="*")
        self.password_entry.bind('<Return>', self.login)
        login_label.grid(row=0, columnspan=2, sticky='EW')
        username_label.grid(row=1, column=0)
        self.username_entry.grid(row=1, column=1)
        password_label.grid(row=2, column=0)
        self.password_entry.grid(row=2, column=1)

        # Button
        self.login_button = Button(self.login_frame, text='Login',
                                   command=self.login)
        self.login_button.grid(row=3, columnspan=2)


    def login(self, *args):
        # Get the username and password
        self.user = self.username_entry.get().strip()
        self.password = self.password_entry.get().strip()

        # Login to MySQL
        try:
            self.connection = Database(self.user, self.password)
        except mysql.connector.errors.ProgrammingError:
            if self.login_attempts > 0:
                message = f"""Invalid User or Password
    \nPlease Try Again\n
    {self.login_attempts} Login Attempts Remaining.\n"""
                messagebox.showwarning(message=message)
                self.username_entry.delete(0, END)
                self.password_entry.delete(0, END)
                self.username_entry.focus_set()
                self.login_attempts -= 1
            else:
                message = """Too Many Failed Login Attempts.\n
                Please Try Again Later."""
                messagebox.showwarning(message=message)
                self.destroy()
        else:
            if self.is_configured:
                self.returning_login()
            else:
                self.new_login()

    def reconnect_to_database(self):
        """
        The connection has to be reset using the database name since the
        original login was done with database set to 'None'.
        """
        database = self.config.get('mysql_info', 'database')
        table = self.config.get('mysql_info', 'table')
        self.connection.connection.close()
        try:
            self.connection = Database(self.user, self.password, database, table)
        except:
            messagebox.showwarning(message="""Database doesn't exist. Check MySQL \n
            and your configuration file and try again""")
            exit()

    def returning_login(self):
        self.reconnect_to_database()
        self.check_for_new_xml()
        self.start_app()

    def new_login(self):
        """
        Once logged in the program first checks for an export zip. If none is
        found it then checks for a csv file. If none is found it creates an
        empty table in the database.
        """
        try:
            self.connection.get_database_and_table_from_config()
            self.connection.create_database()
        except mysql.connector.errors.DatabaseError:
            message = """Database already exists. Choose another name\n
            or first delete the old database."""
            messagebox.showwarning(message=message)
            self.destroy()
            clear_configuration_file(self.config_path)
            from main import main
            main()
        else:
            self.reconnect_to_database()
            self.connection.create_table()
            xml = self.check_for_new_xml()
            if xml:
                csv_path = Path(self.config.get('directory_info', 'cleaned_data'))
                if Path.exists(csv_path):
                    add = AddCSVtoDatabase(self.connection, config_path=self.config_path)
                    add.add_to_database()
            self.start_app()

    def check_for_new_xml(self):
        """
        Once successfully logged in the program checks for a new XML file. If
        so it is cleaned, saved as a CSV, and the new runs are added to the
        database.
        """
        check = GetNewXML(config_file=self.config_path)
        check.check_for_file()
        if check.new_file:
            # Clean the new XML Data
            try:
                cleaner = CleanXML(self.config_path)
                cleaner.clean_file()
            except FileNotFoundError:
                message = """There was a problem cleaning the XML file.\n
                Check your Downloads folder and CleaningData directory.\n
                Select 'Yes' to continue or 'No' to close the app."""
                xml_error = messagebox.askyesno(message=message)
                if xml_error == 'No':
                    quit()
            else:
                try:
                    # Upload the new XML data to the database
                    add = AddCSVtoDatabase(self.connection, config_path=self.config_path)
                    add.add_to_database()
                except FileNotFoundError:
                    message = """There was a problem cleaning the CSV file\n
                    or it could not be found.\n
                    Check your CleaningData directory.\n
                    Select 'Yes' to continue or 'No' to close the app."""
                    csv_error = messagebox.askyesno(message=message)
                    if csv_error == 'No':
                        quit()
        else:
            return True


    def start_app(self):
        self.destroy()
        root = Window(self.connection)
        root.initialize()
        root.mainloop()
        root.connection.connection.close()

    def initialize(self):
        self.configure_window()
        self.create_login_frame()
        self.mainloop()
