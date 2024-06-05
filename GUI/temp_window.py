"""
This module creates a smaller window that is used for logging in and for
getting the database and table name from the user. It will be destroyed
before opening the large main program window.
"""

from tkinter import *


class TempWindow(Tk):
    def __init__(self, window_width=400, window_height=400):
        super().__init__()
        self.window_width = window_width
        self.window_height = window_height

        # Set up the window geometry
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        y = screen_height // 2 - self.window_height // 2
        x = screen_width // 2 - self.window_width // 2
        self.geometry(f"{self.window_width}x{self.window_height}+{x}+{y}")

        # Set up the window configuration
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

    def create_main_frame(self):
        self.frame = Frame(self, borderwidth=2, relief='sunken')
        self.frame.grid(row=0, column=0)
        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=1)
