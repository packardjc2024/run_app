"""
Custom widgets created in order to make dealing with the desired
datatypes and necessary conversions easier. Their methods are named to
match other tk entry widgets in order to make it easier to use for loops
for all entries at once.
"""

import datetime
import tkinter as tk
from tkinter import ttk


class DurationEntry(tk.Frame):
    def __init__(self, parent):
        """
        A custom widget using tk option menus to make an entry for time
        duration.
        """
        super().__init__(master=parent)
        self.entries = {}  # Holds the entries for so they can be got later
        self.values = {}  # Holds the values gotten from the entries

        # Set up the frame
        for i in range(6):
            self.columnconfigure(i, weight=0)
        self.rowconfigure(0, weight=1)

        # Set up the values lists for the combo boxes
        self.hours = [f"0{str(i)}" if i < 10 else str(i) for i in range(13)]
        self.mins_secs = [f"0{str(i)}" if i < 10 else str(i) for i in range(60)]

        # Set up the hour spinbox
        self.hour = ttk.Combobox(self, values=self.hours, width=2,
                                 state='readonly')
        self.hour.current(0)
        self.hour.grid(column=0, row=0)
        self.entries['hour'] = self.hour
        hr_label = tk.Label(self, text="hr")
        hr_label.grid(row=0, column=1, sticky='NEWS')

        # Set up the minute spinbox
        self.minute = ttk.Combobox(self, values=self.mins_secs, width=2,
                                   state='readonly')
        self.minute.current(0)
        self.minute.grid(column=2, row=0)
        self.entries['minute'] = self.minute
        min_label = tk.Label(self, text="min")
        min_label.grid(row=0, column=3, sticky='NEWS')

        # Set up the second spinbox
        self.second = ttk.Combobox(self, values=self.mins_secs, width=2,
                                   state='readonly')
        self.second.current(0)
        self.second.grid(column=4, row=0)
        self.entries['second'] = self.second
        sec_label = tk.Label(self, text="sec")
        sec_label.grid(row=0, column=5, sticky='NEWS')

    def insert(self, string):
        """
        Takes a string, converts it to datetime, then inserts those values
        into the combo boxes. This will be used for the edit page to populate
        the entry with the chosen run.
        """
        dt = datetime.datetime.strptime(string, '%H:%M:%S')
        self.hour.set(dt.hour)
        self.minute.set(dt.minute)
        self.second.set(dt.second)

    def get(self) -> float:
        """
        Gets the hour, minutes, and seconds entered by the user and then
        converts that to a float of the total minutes.
        """
        for key, value in self.entries.items():
            self.values[key] = int(value.get())
        hours = self.values['hour'] * 60
        seconds = round(self.values['second'] / 60, 2)
        minutes = hours + self.values['minute'] + seconds
        return minutes

    def delete(self, start=None, END=None):
        """
        This method was created to make the delete for loop easier since the
        option menu widget on its own does not have a delete method. Therefore,
        the parameters were created to match other widgets and won't be used.
        """
        self.hour.current(0)
        self.minute.current(0)
        self.second.current(0)
                

class TimeEntry(tk.Frame):
    def __init__(self, parent):
        """
        A custom widget using tk option menus to make an entry for time
        that will be converted to a datetime time object.
        """
        super().__init__(master=parent)
        self.entries = {}

        # Set up the frame
        for i in range(4):
            self.columnconfigure(i, weight=0)
        self.rowconfigure(0, weight=1)

        # Set up the values lists for the combo boxes
        self.hours = [f"0{str(i)}" if i < 10 else str(i) for i in range(1, 13)]
        self.mins_secs = [f"0{str(i)}" if i < 10 else str(i) for i in range(60)]

        # Set up the self.hour spinbox
        self.hour = ttk.Combobox(self, values=self.hours, width=2,
                                 state='readonly')
        self.hour.current(0)
        self.hour.grid(column=0, row=0)
        self.entries['hour'] = self.hour
        label1 = tk.Label(self, text=":")
        label1.grid(row=0, column=1)

        # Set up the minute spinbox
        self.minute = ttk.Combobox(self, values=self.mins_secs, width=2,
                                   state='readonly')
        self.minute.current(0)
        self.minute.grid(column=2, row=0)
        self.entries['minute'] = self.minute
        label2 = tk.Label(self, text=":")
        label2.grid(row=0, column=3)

        # Set up the AM/PM box
        self.am_pm = ttk.Combobox(self, values=['AM', 'PM'], width=3,
                                  state='readonly')
        self.am_pm.current(0)
        self.am_pm.grid(column=3, row=0, padx=(10, 0))
        self.entries['am_pm'] = self.am_pm

    def insert(self, string):
        """
        Takes a string, converts it to datetime, then inserts those values
        into the combo boxes. This will be used on the edit page.
        """
        dt = datetime.datetime.strptime(string, '%I:%M %p')
        self.hour.set(dt.hour)
        self.minute.set(dt.minute)
        self.am_pm.set(dt.strftime('%p'))

    def get(self) -> datetime.time:
        """
        Converts the time string entered by the user first to a datetime
        object and then to a time object
        """
        time_list = []
        for key, value in self.entries.items():
            time_list.append(value.get())
        datetime_object = datetime.datetime.strptime(''.join(time_list),
                                                     '%I%M%p')
        time_object = datetime_object.time()
        return time_object

    def delete(self, start=None, END=None):
        """
        This method was created to make the delete for loop easier since the
        option menu widget on its own does not have a delete method. Therefore,
        the parameters were created to match other widgets and won't be used.
        """
        self.hour.current(0)
        self.minute.current(0)
        self.am_pm.current(0)


class PaceEntry(tk.Frame):
    def __init__(self, parent):
        """
        A custom widget using tk option menus to make an entry for time
        duration for a run's mile pace time.
        """
        super().__init__(master=parent)
        self.entries = {}
        self.values = {}

        # Set up the frame
        for i in range(4):
            self.columnconfigure(i, weight=0)
        self.rowconfigure(0, weight=1)

        # Set up the values lists for the combo boxes
        self.mins_secs = [f"0{str(i)}" if i < 10 else str(i) for i in range(60)]

        # Set up the minute spinbox
        self.minute = ttk.Combobox(self, values=self.mins_secs, width=2,
                                   state='readonly')
        self.minute.current(0)
        self.minute.grid(column=2, row=0)
        self.entries['minute'] = self.minute
        min_label = tk.Label(self, text="min")
        min_label.grid(row=0, column=3, sticky='NEWS')

        # Set up the second spinbox
        self.second = ttk.Combobox(self, values=self.mins_secs, width=2,
                                   state='readonly')
        self.second.current(0)
        self.second.grid(column=4, row=0)
        self.entries['second'] = self.second
        sec_label = tk.Label(self, text="sec")
        sec_label.grid(row=0, column=5, sticky='NEWS')

    def insert(self, string):
        """
        Takes a string, converts it to datetime, then inserts those values
        into the combo boxes. This will be used on the edit page.
        """
        dt = datetime.datetime.strptime(string, '%M:%S')
        self.minute.set(dt.minute)
        self.second.set(dt.second)

    def get(self) -> float:
        """
        Gets the hour, minutes, and seconds entered by the user and then
        converts that to a float of the total minutes.
        """
        for key, value in self.entries.items():
            self.values[key] = int(value.get())
        seconds = round(self.values['second'] / 60, 2)
        minutes = self.values['minute'] + seconds
        return minutes

    def delete(self, start=None, END=None):
        """
        This method was created to make the delete for loop easier since the
        option menu widget on its own does not have a delete method. Therefore,
        the parameters were created to match other widgets and won't be used.
        """
        self.minute.current(0)
        self.second.current(0)
