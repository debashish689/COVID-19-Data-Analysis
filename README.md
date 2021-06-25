# COVID-19-Data-Analysis
This project is about colored data-stripe visualization of daily COVID-19 cases in different countries around the world in the timespan, starting from January 22, 2020 upto May 12, 2021: 

The details of daily cumulative cases (in the above-specified timespan) of a country is stored in a file (country_name.txt) for that country. 
All the files (one for each country), containing number of daily cumulative cases in that country on each day are stored in the 'counties/' directory.

The program presents a comparative visual analysis of COVID-19 cases of the countries (entered by the user) in the selected time period (specified by the user), within the actual data timespan:
     
When the program runs, it accesses the 'countries/' directory of the files, reads all the files and creates a database of daily cases on each day for all the countries individually.
               
Then the program instructs the user to enter his/her choice of one or more or all countries and the time period for which the visualization is required.
               
Now for each country_name entered by the user, the data_list of that country (in the time period specified by the user) is read from the database of the countries and an image (representing number of daily cases on each day) is created.
               
The images contain a series of data stripes (one for each day).

The data stripes are coloured selectively red depending on the number of cases on a day with highest red meaning highest number of cases and the intensity of red gradually decreasing with decreasing number of cases.
               
For each country entered by the user, the visualization of that country is shown on the screen and also saved in the directory of the program.
               
          
