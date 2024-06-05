"""
This module is the start-up for the run app. It starts by checking the
configuration module in the program directory. If the app is not configured,
it runs through the processes in the SetUp folder. Otherwise, it prompts the
returning user to log in via the login page.
"""

from constants import *
from pathlib import Path
from SetUp.configure_mysql import ConfigureMySQL
from SetUp.configure_directories import ConfigureDirectories
from GUI.login_window import LoginPage


def main():
    # Get the current working directory and config file path
    program_directory = Path.cwd()
    config_path = Path.joinpath(program_directory, 'config.ini')

    # Read the config file
    config = read_config_file(config_path)

    # Check if the app is configured
    is_configured = config.getboolean('set_up', 'is_configured')
    if is_configured:
        login = LoginPage(config_path)
        login.initialize()
    else:
        directories_configuration = ConfigureDirectories(program_directory)
        directories_configuration.initialize()
        mysql_configuration = ConfigureMySQL(config_path)
        mysql_configuration.initialize()


main()
