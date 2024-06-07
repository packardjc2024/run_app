# Run APP
This app tracks the user's running history. It uses MySQL to store the information
and creates the base table by getting the information from an Apple Health Export
XML file. The user can then enter runs manually or get new runs from new
Apple Health Export XML files. 

## Requirements
The user must have MySQL installed on their device and will use their MySQL
username and password to login on the login window.

### Non-Built-in Modules Used
matplotlib</br>
pandas</br>
numpy</br>
tkcalendar</br>
mysql-connector-python</br>

### Python Version
3.12

#### Initial Set UP
The first time the user logs in they will be prompted to enter
a database name and a table name.

The database and table will be created without an export file, however,
if there is an export zip file in their downloads folder it will be 
extracted and added to the table. 

The cleaned_data.csv file in the CleaningData directory would not be there the
first time a user set up the app. I included that as an example of what the csv
file would look like after the data was extracted from the export XML file. 

#### Project Directory Layout
Main Directory</br>
&emsp;&emsp;main.py</br>
&emsp;&emsp;config.ini</br>
&emsp;&emsp;database.py</br>
&emsp;&emsp;constants.py</br>
&emsp;&emsp;CleaningData</br>
&emsp;&emsp;&emsp;&emsp;export.xml</br>
&emsp;&emsp;&emsp;&emsp;cleaned_data.csv</br>
&emsp;&emsp;&emsp;&emsp;clean_xml.py</br>
&emsp;&emsp;&emsp;&emsp;add_csv_to_database.py</br>
&emsp;&emsp;&emsp;&emsp;get_new_xml.py</br>
&emsp;&emsp;GUI</br>
&emsp;&emsp;&emsp;&emsp;custom_widgets.py</br>
&emsp;&emsp;&emsp;&emsp;login_window.py</br>
&emsp;&emsp;&emsp;&emsp;root_window.py</br>
&emsp;&emsp;&emsp;&emsp;runs_table.py</br>
&emsp;&emsp;&emsp;&emsp;home_page.py</br>
&emsp;&emsp;&emsp;&emsp;add_run_page.py</br>
&emsp;&emsp;&emsp;&emsp;edit_run_page.py</br>
&emsp;&emsp;&emsp;&emsp;search_page.py</br>
&emsp;&emsp;&emsp;&emsp;visuals_page.py</br>
&emsp;&emsp;&emsp;&emsp;temp_window.py</br>
&emsp;&emsp;SetUp</br>
&emsp;&emsp;&emsp;&emsp;database_creation.sql</br>
&emsp;&emsp;&emsp;&emsp;set_up_config_file.py</br>
&emsp;&emsp;&emsp;&emsp;configure_mysql.py</br>
&emsp;&emsp;&emsp;&emsp;configure_directories.py</br>
        
#### Troubleshooting
If there is a problem logging in the app can be reset by
running the set_up_config_file.py in the SetUp folder.
This will reset the app. It will not drop the database from
MySQL. 

If there is already a database with that name in MySQL, the user
will be prompted to choose another name.

If the user would like to access the export zip file somewhere
other than the user's downloads folder, then after the app has
been initialized for the first time they can manually go into the
configi.ini file and alter the file path.