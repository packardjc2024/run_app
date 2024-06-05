"""
This module contains variables and functions that will be shared between all
pages of the app. The majority of the variables and functions are related to
categorizing and formatting the datatypes.
"""

import configparser
import datetime
import re


# Get the current date
CURRENT_DATE = datetime.datetime.now().date()

# The column names in the order they appear in the CSV and MySQL
COLUMN_NAMES = ['date', 'start_time', 'distance', 'duration', 'pace',
                'calories', 'vo2_max', 'avg_hr', 'max_hr', 'min_hr',
                'elevation', 'temperature', 'humidity']

# Format the display names to use as the entry and table labels
DISPLAY_NAMES_DICT = {}
for column in COLUMN_NAMES:
    display_name = f"{column.replace('_', ' ').capitalize()}:"
    DISPLAY_NAMES_DICT[column] = display_name

# Create lists of different datatypes for the columns to use in checking values
INTEGERS = ['calories', 'avg_hr', 'max_hr', 'temperature', 'humidity',
            'min_hr', 'elevation']
FLOATS = ['distance', 'vo2_max', 'pace']
DATES = ['date']
TIMES = ['start_time']
MINUTES = ['duration', ]

# Get the times' datatypes indexes for use in the format_times function
DURATION_INDICES = {}
for column in COLUMN_NAMES:
    if column in MINUTES or column in TIMES or column == 'pace':
        DURATION_INDICES[column] = COLUMN_NAMES.index(column)

MYSQL_DATATYPES = [('run_id', 'SMALLINT UNSIGNED PRIMARY KEY AUTO_INCREMENT'),
                   ('date', 'DATE'),
                   ('start_time', 'TIME'), ('distance', 'DECIMAL (4, 2)'),
                   ('duration', 'DECIMAL(5, 2)'),
                   ('pace', 'DECIMAL(4, 2)'), ('calories', 'SMALLINT UNSIGNED'),
                   ('vo2_max', 'DECIMAL(4, 2)'), ('avg_hr', 'TINYINT UNSIGNED'),
                   ('max_hr', 'TINYINT UNSIGNED'), ('min_hr', 'TINYINT UNSIGNED'),
                   ('elevation', 'SMALLINT UNSIGNED'),
                   ('temperature', 'TINYINT UNSIGNED'),
                   ('humidity', 'TINYINT UNSIGNED')]


def read_config_file(config_path):
    config = configparser.ConfigParser()
    config.read(config_path)
    return config


def format_times(run: list) -> list:
    """
    This function takes the time in total minutes and converts it to a more
    user readable string for use in the app. All times in the database/app are
    saved as a decimal(4, 2)/float of total minutes.
    """
    for time_column, index in DURATION_INDICES.items():
        if run[index] != 'NULL' and run[index]:
            if time_column == 'duration':
                display_time = datetime.timedelta(minutes=float(run[index]))
                run[index] = re.search(r'(\d*:\d\d:\d\d)', str(display_time)).group(1)
            elif time_column == 'pace':
                display_time = datetime.timedelta(minutes=float(run[index]))
                run[index] = re.search(r'\d*:(\d\d:\d\d)', str(display_time)).group(1)
            elif time_column == 'start_time':
                datetime_object = datetime.datetime.strptime(str(run[index]),
                                                             '%H:%M:%S')
                run[index] = datetime_object.strftime('%I:%M %p')
    return run


