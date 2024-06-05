"""
This file builds all the necessary file paths using the program directory and
the downloads folder so that the program knows where to look for the export
zip and where to save the export xml and cleaned data csv files.
"""

from constants import read_config_file
from pathlib import Path


class ConfigureDirectories:
    def __init__(self, program_directory):
        """
        The program directory and config file path are passed from the main
        module and the rest of the paths are built using those.
        """
        self.program_directory = program_directory
        self.config_path = Path.joinpath(self.program_directory,
                                         'config.ini')
        self.config = read_config_file(self.config_path)

    def format_file_paths(self):
        """
        The file paths are written to a dictionary that will be used
        to update the configuration file.
        """
        self.filepaths = {
            'program_directory': self.program_directory,
            'downloads_directory': Path.joinpath(Path.home(),
                                                 'Downloads'),
            'cleaning_data_directory': Path.joinpath(self.program_directory,
                                                     'CleaningData')
        }
        self.filepaths.update({
            'zip_file': Path.joinpath(self.filepaths['downloads_directory'],
                                      'export.zip'),
            'unzipped_folder': Path.joinpath(self.filepaths['downloads_directory'],
                                             'apple_health_export'),
            'old_xml_file': Path.joinpath(self.filepaths['cleaning_data_directory'],
                                          'export.xml'),
            'cleaned_data': Path.joinpath(self.filepaths['cleaning_data_directory'],
                                          'cleaned_data.csv'),
        })
        self.filepaths.update({
            'unzipped_file': Path.joinpath(self.filepaths['unzipped_folder'],
                                           'export.xml')
        })

    def write_file_paths_to_config(self):
        for key, value in self.filepaths.items():
            self.config.set('directory_info', key, str(value))

        with open(self.config_path, 'w') as config_file:
            self.config.write(config_file)

    def initialize(self):
        self.format_file_paths()
        self.write_file_paths_to_config()

