"""
This module will either add new data to the database or create the database
and table if the database does not already exist. It will be called in the
login module depending on whether a configuration file exists. It will then
either load the entire CSV into the database or only the new runs based on
the date.
"""


import csv
from constants import *
from pathlib import Path
import configparser


class AddCSVtoDatabase:
    def __init__(self, connection, config_path):
        self.connection = connection
        self.config_path = config_path

    def read_config_file(self):
        self.config = configparser.ConfigParser()
        self.config.read(self.config_path)
        self.database = self.config.get('mysql_info', 'database')
        self.table = self.config.get('mysql_info', 'table')
        self.csv_file = Path(self.config.get('directory_info', 'cleaned_data'))

    def open_file(self):
        """
        Opens the CSV file in the CleaningData directory and reads it.
        """
        with open(self.csv_file, 'r') as csv_file:
            # Read the file - returns reader object
            csv_reader = csv.reader(csv_file)
            # Save the column names and move on to the first data row
            self.columns = next(csv_reader)
            # Get a list of rows of run data from the csv file
            self.rows = [row for row in csv_reader]

    def insert_rows(self, rows):
        """
        Crafts the insert statement for each row and then inserts that row
        into the database. The values are first put into quotation marks to
        account for the SQL date and time datatypes.
        """
        for row in rows:
            values = [f"'{value}'" if value != 'NULL' else value for value in row]
            statement = f"""INSERT INTO {self.table} ({', '.join(self.columns)}) 
            VALUES ({', '.join(values)});"""
            self.connection.execute_query(statement)

    def add(self):
        """
        First queries the table to get the latest run's date and then adds all
        runs from the CSV file that occurred after that date. If the table is
        it will add all rows.
        """
        select_statement = f"SELECT MAX(date) FROM {self.table};"
        last_date = self.connection.execute_query(select_statement)[0][0]
        if last_date:
            new_rows = []
            for row in self.rows:
                row_datetime = datetime.datetime.strptime(row[0], '%Y-%m-%d').date()
                if row_datetime > last_date:
                    new_rows.append(row)
            self.rows = new_rows
        self.insert_rows(self.rows)

    def add_to_database(self):
        self.read_config_file()
        self.open_file()
        self.add()
