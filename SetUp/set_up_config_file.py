"""
This file is used to reset the configuration file. It can be used manually
to reset the app if there are issues. It is also called from the login
page if the database name already exists to reset the set-up process.
"""

import configparser
from pathlib import Path


def clear_configuration_file(config_path):
    # config object
    config = configparser.ConfigParser()

    # Set up section
    config['set_up'] = {'is_configured': '0'}

    # MySQL section
    config['mysql_info'] = {'database': '0', 'table': '0'}

    # Directory info section
    config['directory_info'] = {'downloads_directory': '0',
                                'program_directory': '0',
                                'cleaning_data_directory': '0',
                                'zip_file': '0',
                                'unzipped_folder': '0',
                                'unzipped_file': '0',
                                'old_xml_file': '0',
                                'cleaned_data': '0'}

    # Write the file
    with open(config_path, 'w') as config_file:
        config.write(config_file)


if __name__ == '__main__':
    config_path = Path.joinpath(Path.cwd().parent, 'config.ini')
    clear_configuration_file(config_path)
