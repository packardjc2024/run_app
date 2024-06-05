"""
This program opens the Apple Health Data XML file and then extracts the
health and workout data. That data is then converted to a pandas dataframe
to be cleaned and then saved to a CSV file.

XML format:
root element = HealthData,
HealthData attributes (children) that are needed = Record, Workout.
Workout attributes (children) = metadata and workoutStatistcs with
'type' and 'key' keys.
"""

import numpy
import pandas as pd
import xml.etree.ElementTree as Et
from constants import *
import configparser


class CleanXML:
    def __init__(self, config_file):
        self.config_file = config_file
        # The columns that I will have and will use in my MySQL table
        self.table_columns = ['date', 'start_time', 'distance', 'duration', 'pace',
                              'calories', 'vo2_max', 'avg_hr', 'max_hr', 'min_hr',
                              'elevation', 'temperature', 'humidity']
        # Divide the columns into lists by datatype
        self.integers = ['calories', 'max_hr', 'min_hr', 'avg_hr']
        self.decimals = ['duration', 'distance']

    def get_files(self):
        config = configparser.ConfigParser()
        config.read(self.config_file)
        self.xml_file = config.get('directory_info', 'OLD_XML_FILE')
        self.cleaned_data = config.get('directory_info', 'CLEANED_DATA')

    def create_tree(self):
        # Parse the element tree and get the root
        tree = Et.parse(self.xml_file)
        self.root = tree.getroot()

###############################################################################
# Extract the desired data from the workouts elements and their children
###############################################################################

    def get_workout_data(self):
        """
        Get all the desired data from the child attributes of each workout and
        add that data to the main workouts dictionary dataset.
        While going through the loop only get the run type workout
        """
        # Get a list of the workout element objects
        self.workout_elements = [workout for workout in self.root.iter('Workout')]
        self.workouts = []  # List of the workout dictionaries

        for workout in self.workout_elements:
            # Use the workout element attributes as the base dictionary
            workout_dict = workout.attrib
            # Only get data for the run type workouts
            if workout_dict['workoutActivityType'] == 'HKWorkoutActivityTypeRunning':
                # Get all the child attributes
                children = [child.attrib for child in workout]
                for child in children:
                    # Get only the data I want from the metadata and workoutStatistics attributes
                    if 'type' in child.keys():  # This key is only in the metadata attributes
                        if child['type'] == 'HKQuantityTypeIdentifierHeartRate':
                            workout_dict['max_hr'] = child['maximum']
                            workout_dict['min_hr'] = child['minimum']
                            workout_dict['avg_hr'] = child['average']
                        elif child['type'] == 'HKQuantityTypeIdentifierActiveEnergyBurned':
                            workout_dict['calories'] = child['sum']
                        elif child['type'] == 'HKQuantityTypeIdentifierDistanceWalkingRunning':
                            workout_dict['distance'] = child['sum']
                    elif 'key' in child.keys():  # This key is only present in workoutStatistics
                        if child['key'] == 'HKElevationAscended':
                            workout_dict['elevation'] = child['value']
                        elif child['key'] == 'HKWeatherHumidity':
                            workout_dict['humidity'] = child['value']
                        elif child['key'] == 'HKWeatherTemperature':
                            workout_dict['temperature'] = child['value']
                self.workouts.append(workout_dict)

    def get_vo2_max(self):
        """
        Get the vo2_max data from the Record's child element and append the data
        to that workouts dictionary in the main workouts list.
        """
        # Get only the records for vo2 max data
        vo2_type = 'HKQuantityTypeIdentifierVO2Max'
        vo2_records = [record.attrib for record in self.root.iter('Record') if record.attrib['type'] == vo2_type]

        # Get all the vo2 records from a workout's start to end time and add the average
        # to the workout dictionary
        for workout in self.workouts:
            vo2_readings = []
            for record in vo2_records:
                if workout['startDate'] <= record['creationDate'] <= workout['endDate']:
                    vo2_readings.append(float(record['value']))
            if vo2_readings:
                workout.update({'vo2_max': round(numpy.mean(vo2_readings), 2)})
            else:
                workout.update({'vo2_max': 'NULL'})

###############################################################################
# Convert the dictionary to a pandas dataframe and clean up the data
###############################################################################

    def convert_missing_to_null(self):
        """
        Loops through the workout dictionary checking if every key in the table's
        column exists. If not it is added with a value of 'NULL' for MySQL
        """
        for workout in self.workouts:
            for key in self.table_columns:
                if key not in workout.keys():
                    workout[key] = 'NULL'

    def convert_to_dataframe(self):
        """
        Converts the workouts dictionary to a pandas dataframe for further
        cleaning.
        """
        self.df = pd.DataFrame(self.workouts)

    def clean_integers(self):
        """
        Convert columns that will be integers in MySQL.
        """
        for integer in self.integers:
            for value in self.df[integer]:
                if value != 'NULL':
                    self.df.replace(to_replace=value, value=int(float(value)),
                                    inplace=True)

    def clean_floats(self):
        """
        Converts the values that will be decimals in MySQL to floats.
        """
        for two_decimal in self.decimals:
            for value in self.df[two_decimal]:
                if value != 'NULL':
                    self.df.replace(to_replace=value, value=round(float(value), 2),
                                    inplace=True)

    def clean_weather_values(self):
        """
        Cleans up the temperature, humidity, and weather values by converting
        the strings to integers.
        """
        # Clean up the temperature string
        for value in self.df['temperature']:
            if value != 'NULL':
                self.df.replace(to_replace=value, value=value[0:2], inplace=True)

        # Clean up the humidity string
        for value in self.df['humidity']:
            if value != 'NULL':
                self.df.replace(to_replace=value, value=value[0:2], inplace=True)

        # Clean up the elevation data
        for value in self.df['elevation']:
            if value != 'NULL':
                new_value = int(float(str(value)[:4]) / 30.48)
                self.df.replace(to_replace=value, value=new_value, inplace=True)

    def clean_start_time_date(self):
        """
        Changes the single column startDate into two columns 'date' and
        'start_time'.
        """
        start_times, dates = [], []
        for value in self.df['startDate']:
            string_format = '%Y-%m-%d %H:%M:%S -0400'
            dt = datetime.datetime.strptime(value, string_format)
            dates.append(dt.date())
            start_times.append(dt.time())

        self.df['start_time'] = start_times
        self.df['date'] = dates

    def calculate_pace(self):
        """
        Calculates the average mile time using the duration and distance columns
        and then creates a new 'pace' column
        """
        paces = []
        for index, workout in self.df[['duration', 'distance']].iterrows():
            if workout['duration'] == 'NULL' or workout['distance'] == 'NULL':
                paces.append('NULL')
            else:
                paces.append(round(float(workout['duration']) / float(workout['distance']), 2))

        self.df['pace'] = paces

    def drop_columns(self):
        """
        Drops the columns that are no longer necessary and reorders the dataframe
        to match the order of the MySQL table.
        """
        columns_to_drop = ['workoutActivityType', 'durationUnit', 'sourceName',
                           'sourceVersion', 'device', 'creationDate', 'endDate',
                           'startDate']
        self.df.drop(labels=columns_to_drop, axis=1, inplace=True)

        # Reorder the columns to match the MySQL table order
        self.df = self.df[self.table_columns]

    def delete_rows(self):
        """
        Deletes runs that are less than 1 hour long. Can be modified to
        edit out any other data desired at a later point.
        """
        for index, row in self.df.iterrows():
            if int(row['duration']) < 59:
                self.df.drop(index=index, axis=0, inplace=True)

    def save_to_csv(self):
        """
        Saves the pandas dataframe as a CSV file that can be imported into
        MySQL with either an import statement or by reading the CSV and adding
        each run row by row.
        """
        self.df.to_csv(self.cleaned_data, index=False)

    def clean_file(self):
        """
        A single method that calls all the methods in the proper order to
        run the program and output the csv file.
        """
        self.get_files()
        self.create_tree()
        self.get_workout_data()
        self.get_vo2_max()
        self.convert_missing_to_null()
        self.convert_to_dataframe()
        self.clean_integers()
        self.clean_floats()
        self.clean_weather_values()
        self.clean_start_time_date()
        self.calculate_pace()
        self.drop_columns()
        self.delete_rows()
        self.save_to_csv()
