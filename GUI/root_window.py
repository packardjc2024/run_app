"""
Creates a child class of the main Tk window that will be used to hold
all the frames and the mainloop. The current frame will be tracked in
order for the app to know whether to destroy both the top and bottom
frames or just the top frame when switching between pages.
"""

from tkinter import *
import tkinter.ttk as ttk
from GUI.runs_table import RunsTable
from GUI.edit_run_page import EditRunPage
from GUI.add_run_page import AddRunPage
from GUI.home_page import HomePage
from GUI.search_page import SearchRunsPage
from GUI.visuals_page import RunVisuals


class Window(Tk):
    def __init__(self, connection, window_width=1200, window_height=750):
        super().__init__()
        self.connection = connection
        self.current_frame = Frame()
        self.title('Personal Run Tracking APP')
        self.visuals_display = None
        self.edit_buttons_frame = None

        # Set style to clam to deal with macOS style oddities
        style = ttk.Style()
        style.theme_use('clam')

        # Setting up the page geometry
        self.window_width = window_width
        self.window_height = window_height
        screen_width = self.winfo_screenwidth()
        x = screen_width // 2 - self.window_width // 2
        self.geometry(f"{self.window_width}x{self.window_height}+{x}+0")

        # Setting up the window grid layout
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=0)
        self.rowconfigure(2, weight=1)

    def create_main_frames(self):
        """
        Creates a top frame, bottom frame, and toolbar frame.
        """
        # Set up the top frame
        self.top_frame = Frame(self)
        self.top_frame.grid(row=1, column=0, sticky='NEWS')
        self.top_frame.columnconfigure(0, weight=1)
        self.top_frame.rowconfigure(0, weight=1)

        # Set up the bottom frame
        self.bottom_frame = Frame(self)
        self.bottom_frame.grid(row=2, column=0, sticky='NEWS')
        self.bottom_frame.columnconfigure(0, weight=1)
        self.bottom_frame.rowconfigure(0, weight=1)
        self.bottom_frame.rowconfigure(1, weight=0)

        # Set up the toolbar frame
        self.tool_frame = Frame(self, borderwidth=2, relief='raised')
        self.tool_frame.grid(row=0, column=0, sticky='NEWS',
                             padx=0, pady=(0, 10))

        pages = {'Home': HomePage(self), 'Enter Run': AddRunPage(self),
                 'Edit': EditRunPage(self), 'Search': SearchRunsPage(self),
                 'Visuals': RunVisuals(self), 'Quit': quit}
        column = 0
        for key, value in pages.items():
            if key == 'Quit':
                command = value
            else:
                command = lambda x=value: self.change_page(x)
            button = Button(self.tool_frame, text=key, command=command)
            button.grid(row=0, column=column)
            column += 1

    def change_page(self, page):
        """
        When changing from the visuals page to another page it will destroy
        both the top and bottom frames. If the current page is the edit page,
        it will delete the buttons frame. Switching between all other frames
        it will only destroy the top frame.
        """
        if self.visuals_display:
            self.visuals_display.destroy()
            self.table = RunsTable(self, self.bottom_frame, self.connection)
            self.table.initialize()
            self.visuals_display = None
        elif self.edit_buttons_frame:
            self.edit_buttons_frame.destroy()
            self.edit_buttons_frame = None

        self.current_frame.destroy()
        page.initialize()

    def initialize(self):
        """
        Starts the window with the home page on the top frame and the table
        filled with the runs from the database in the bottom frame.
        """
        current_page = HomePage(self)
        self.create_main_frames()
        self.table = RunsTable(self, self.bottom_frame, self.connection)
        self.table.initialize()
        current_page.initialize()
