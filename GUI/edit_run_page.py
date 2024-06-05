"""
This module is the class that creates the edit run page for the app.
The edit page is the enter page reconfigured so that when selected
from the table all the info is populated. The class uses the submission
methods from the new run page but pass the edit value as True to make
changes.
"""


from tkinter import *
from GUI.add_run_page import AddRunPage
from tkinter import messagebox
import datetime


class EditRunPage:
    def __init__(self, root):
        self.root = root
        self.original_date = None

    def create_enter_frame(self):
        """
        Creates the add run page.
        """
        self.edit_page = AddRunPage(self.root)
        self.edit_page.initialize()
        self.frame = self.edit_page.frame

    def reconfigure_frame(self):
        """
        Reconfigures the add run page to meet the needs of editing a run. The
        new button calls the get values method from the add run module with
        the value of edit as True.
        """
        self.edit_page.frame_label.configure(text='Edit Run')
        self.edit_page.submit.configure(text='Update',
                                        command=lambda x=True: self.edit_page.get_values(x, self.original_date))

        self.buttons_frame = Frame(self.root.bottom_frame)
        self.buttons_frame.grid(row=1, column=0)
        self.edit_button = Button(self.buttons_frame, text='Edit',
                                  command=self.edit)
        self.delete_button = Button(self.buttons_frame, text='Delete',
                                    command=self.delete)
        self.delete_button.grid(row=0, column=0, pady=(0, 5))
        self.edit_button.grid(row=0, column=1, pady=(0, 5))
        self.root.edit_buttons_frame = self.buttons_frame

    def edit(self):
        """
        Gets the selected run from the table and populates all its info into
        the entries so that the user can make changes.
        """
        # First checks to make sure a run has been selected
        try:
            row = self.root.table.run_table.selection()[0]
        except IndexError:
            messagebox.showwarning(message="Select a run to edit")
        else:
            row = self.root.table.run_table.item(row)['values']
            self.original_date = row[0]

            # clear the entry boxes and insert the values into them
            index = 0
            for key, value in self.edit_page.entries_dict.items():
                if key == 'date':
                    dt = datetime.datetime.strptime(row[0], '%Y-%m-%d')
                    value.selection_set(dt)
                elif key in ('pace', 'start_time', 'duration'):
                    value.insert(row[index])
                else:
                    value.delete(0, END)
                    value.insert(0, row[index])
                index += 1

    def delete(self):
        """
        Deletes the selected run from the database and reloads the table to
        no longer include the deleted run.
        """
        try:  # First make sure that a run has been selected
            row = self.root.table.run_table.selection()[0]
        except IndexError:
            messagebox.showwarning(message="Select a run to delete")
        else:  # Uses a messagebox to make sure the user ment to delete a run
            date = self.root.table.run_table.item(row)['values'][0]
            message = "Are you sure you want to delete this run?"
            delete = messagebox.askyesno(message=message)
            if delete:
                self.root.connection.delete(date)
                self.root.table.fill_table()

    def initialize(self):
        self.create_enter_frame()
        self.reconfigure_frame()
        self.root.current_frame = self.frame
