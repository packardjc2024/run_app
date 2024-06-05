"""
This module serves as the connection between the running app and the MySQL
database. The login info is requested by the app in the login module and then
sent to the class. The database parameter is defaulted to none in case it is
the user's first time logging in. After that the database name and table name
are retrieved from the configuration file.
"""

import mysql.connector
from pathlib import Path
from constants import *
import datetime


class Database:
    def __init__(self, user, password, database=None, table=None):
        """
        Establishes the database connection while initializing the class so
        that all other methods are ready to be called.
        """
        self.user = user
        self.password = password
        self.database = database
        self.table = table
        self.config_path = Path.joinpath(Path.cwd(), 'config.ini')

        self.connection = mysql.connector.connect(
            host='localhost',
            user=self.user,
            password=self.password,
            database=self.database
        )

    def get_database_and_table_from_config(self):
        config = read_config_file(self.config_path)
        self.database = config.get('mysql_info', 'database')
        self.table = config.get('mysql_info', 'table')

    def execute_query(self, statement: str) -> list[tuple]:
        """
        Takes a sql statement as a string and executes it in the database and
        returns a list of tuples.
        """
        cursor = self.connection.cursor()
        cursor.execute(statement)
        result = cursor.fetchall()
        self.connection.commit()
        cursor.close()
        return result

    def get_column_names(self) -> list[str]:
        """
        Returns a list of the column names in the table.
        """
        statement = f"DESC {self.table};"
        result = self.execute_query(statement)
        formatted_result = [res[0] for res in result]
        return formatted_result

    def add_to_database(self, run_dict):
        """
        Takes a dictionary of a new run and formats the insert statement
        to send to the database. All values are converted to a string and
        placed in quotation marks to account for date and time datatypes in
        MySQL
        """
        columns = f"({', '.join(list(run_dict.keys()))})"
        values = f"('{"', '".join([str(value) for value in run_dict.values()])}')"
        insert_statement = f"""INSERT INTO {self.table} {columns} VALUES {values};"""
        self.execute_query(insert_statement)

    def update(self, run_dict, original_date):
        """
        Updates the row in the table based on the date of the run.
        """
        condition = f"date = '{original_date}'"
        values_list = [f"{key} = '{value}' " for key, value in run_dict.items()]
        values = ', '.join(values_list)
        update_statement = f"UPDATE {self.table} SET {values} WHERE {condition};"
        self.execute_query(update_statement)

    def delete(self, date):
        """
        Deletes the row in the table based on the date.
        """
        delete_statement = f"DELETE FROM {self.table} WHERE date = '{date}';"
        self.execute_query(delete_statement)

    def create_database(self):
        self.execute_query(f'CREATE DATABASE {self.database};')

    def create_table(self):
        strings_list = [f"{column} {datatype}" for column, datatype in MYSQL_DATATYPES]
        statement = f"CREATE TABLE {self.table} ({', '.join(strings_list)});"
        self.execute_query(statement)

