/* All of the MySQL statements needed to create the database and table,
and then import the old run data csv into the table. The table can also
 be created using a for loop from the csv file as is done in the app. */

# Create the database
CREATE DATABASE run_app;

# Select the database
USE run_app;

# Create the table
CREATE TABLE run_data
(run_id SMALLINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
date DATE,
start_time TIME,
distance DECIMAL(4, 2), 
duration DECIMAL(4, 2), 
pace DECIMAL(4, 2), 
calories SMALLINT, 
vo2_max DECIMAL(4, 2), 
avg_hr TINYINT UNSIGNED,
max_hr TINYINT UNSIGNED,
min_hr TINYINT UNSIGNED,
elevation SMALLINT UNSIGNED,
temperature TINYINT, 
humidity TINYINT);

# Change local infile in order to import CSV
SET GLOBAL LOCAL_INFILE=1;

# Load the old run data csv into the table
LOAD DATA LOCAL INFILE '***MAIN PROJECT DIRECTORY***/CleaningData/cleaned_data.csv'
INTO TABLE run_data
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(date, start_time, distance, duration, pace, calories,
vo2_max, avg_hr, max_hr, min_hr, elevation, temperature,
humidity);

# Reset the local infile for security
SET GLOBAL LOCAL_INFILE=0;


