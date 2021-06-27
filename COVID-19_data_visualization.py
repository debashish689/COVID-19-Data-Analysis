"""
COVID-19 Data Analysis:

This program presents a comparative visual analysis of COVID-19 cases in several countries around the world in the
timespan, starting on January 22. 2020 and going up until May 12. 2021.

1. At first the program reads the filenames in the 'COUNTRY_DIRECTORY' and makes a list-type variable, 'countries',
  containing all the filenames(.txt). and another list-type variable, 'normalized_countries' is created containing
  uppercase version of the above filenames.

2. Now for each filename in 'countries', the original file in the 'COUNTRY_DIRECTORY' is read and for each file a
  list-type variable, 'list_of_cumulative_cases' containing number of cumulative cases for each day is created. And from
  'list_of_cumulative_cases', another list, 'list_of_daily_cases' containing number of individual daily cases for each
  day is created.

  And each 'list_of_daily_cases' is stored against corresponding country_name (obtained by omitting '.TXT' from each filename)
  in the dictionary-type variable, 'countries_daily_data_dict' defined by 'country_name -> list_of_daily_cases' pair.

3. Now the user is instructed to enter country_names of his/her choice from the list of keys in the
  'countries_daily_data_dict'. the user can enter the country_name in both upper and lower case. The entered valid
  country_names (i.e. country_names for which data are available) are stored in a list, 'countries_to_compare'.

  The analysis can be performed in two ways:
  mode 1: For doing analysis for last few days from the 'data ending date'.
  mode 2: For doing analysis between any two dates within the range from 'data starting date' upto 'data ending date'.
          The mode of analysis is determined by the user.

4. Now for each country in 'countries_to_compare', the corresponding section (in the range specified by the user)
  of list of values from the 'countries_daily_data_dict' is obtained and stored in  corresponding list,
  'list_of_data_to_compare' for that country.

5. The values in each 'list_of_data_to_compare' for each country in 'countries_to_compare' are converted to fractions of
  the largest value and each set of fractions for each country is stored in corresponding list, 'daily_fractions' and
  each 'daily_fractions' is stored under corresponding country_name in dictionary, 'countries_data_fractions', defined by
  country_name -> 'daily_fractions'.

6. Now for each country / 'daily_fractions' pair in the 'countries_data_fractions', an image containing a series of
  coloured data stripes (representing number of daily cases on each day relative to the highest daily cases for that
  country) is created using 'daily_fractions' and for each country, its image is stored in the 'visualizations_dict'
  dictionary.

7. At last all the images stored in 'visualizations_dict' are accessed one by one by each country_name and image for
  each country is shown on screen and saved in the home_directory one after another.
"""

import os
from simpleimage import SimpleImage

# Constants Declaration:

COUNTRY_DIRECTORY = "countries/"   # All the data files (.txt), one for each country, are stored in this directory.
GREEN = 127                        # The constant value of 'green' in the 'RGB' colour scheme of images.
BLUE = 127                         # The constant value of 'blue' in the 'RGB' colour scheme of images.
REFERENCE_DATE = "00.00.0000"  # This constant is used as reference for calculation of number of days between two dates.
DATA_START_DATE = "22.01.2020"     # This is the starting date from which data are available.
DATA_END_DATE = "12.05.2021"       # This is the ending date upto which data are available.
STRIPE_WIDTH = 50                  # This is the width of each individual data-stripe for each day.


def main():
    countries = os.listdir(COUNTRY_DIRECTORY)#All the filenames in the COUNTRY_DIRECTORY are stored in list, 'countries'
    normalized_countries = normalize(countries)
    countries_data_fractions = {}
    countries_daily_data_dict = {}
    visualizations_dict = {}
    for item in countries:
        """
        Each file in the 'COUNTRY_DIRECTORY' is accessed by each filename in 'countries' and the file is read and 
        list_of_cumulative_values for each file (specified by each filename) is created.
        list_of_daily_values for each file (specified by each filename) is created for the corresponding 
        list_of_cumulative_values.
        And each corresponding list_of_daily_values is stored against each country (in uppercase) in the dictionary,
        'countries_daily_data_dict'.     
        """
        list_of_cumulative_cases = list_cumulative_cases(COUNTRY_DIRECTORY+item)
        list_of_daily_cases = list_daily_cases(list_of_cumulative_cases)
        item = item.strip("txt")
        item = item.upper()
        countries_daily_data_dict[item[:-1]] = list_of_daily_cases
    print("")
    print("Comparative Visual Analysis of COVID-19 cases in several Countries in the timespan,\nstarting on " + DATA_START_DATE + " and going up until " + DATA_END_DATE + " : ")
    print("")
    countries_to_compare = get_countries(normalized_countries)
    if countries_to_compare:
        print("")
        mode = accept_mode()
        if mode:
            if mode == 1:
                """
                The user is instructed to enter a number of days of his/her choice and it is checked whether
                the user-entry is a valid number within the date range of data available.
                """
                print("")
                entire_data_span = (calculate_days_span(REFERENCE_DATE, DATA_END_DATE) - calculate_days_span(REFERENCE_DATE, DATA_START_DATE)) + 1
                N_days_to_compare = input("Last how many days from " + DATA_END_DATE + " do you want to compare for?\nEnter a number between 1 and " + str(entire_data_span) + " (both inclusive)." + " (Or press 'Enter' to exit): ")
                while N_days_to_compare and (not N_days_to_compare.isdigit()):
                    print("Invalid range.")
                    N_days_to_compare = input(
                        "Last how many days from " + DATA_END_DATE + " do you want to compare for?\nEnter a number between 1 and " + str(entire_data_span) + " (both inclusive)." + " (Or press 'Enter' to exit): ")
                    if N_days_to_compare == "":
                        exit(0)
                if N_days_to_compare and N_days_to_compare != "0":
                    N = int(N_days_to_compare)
                    while N > entire_data_span:
                        """
                        This loop checks and ensures that the 'number of days' entered by the user is
                        lesser than the total number of days between 'DATA_START_DATE' and 'DATA_END_DATE'
                        ('DATE_END_DATE' included).
                        """
                        print("Your range of days exceeds the date range of data.")
                        N_days_to_compare = input(
                            "Last how many days from " + DATA_END_DATE + " do you want to compare for?\nEnter a number between 1 and " + str(entire_data_span) + " (both inclusive)." + " (Or press 'Enter' to exit): ")
                        while N_days_to_compare and (not N_days_to_compare.isdigit()):
                            print("Invalid range.")
                            N_days_to_compare = input(
                                "Last how many days from " + DATA_END_DATE + " do you want to compare for?\nEnter a number between 1 and " + str(entire_data_span) + " (both inclusive)." + " (Or press 'Enter' to exit): ")
                            if N_days_to_compare == "":
                                exit(0)
                        if N_days_to_compare and N_days_to_compare != "0":
                            N = int(N_days_to_compare)
                        else:
                            exit(0)

                    P = 0
                else:
                    exit(0)

            elif mode == 2:
                """
                The user is instructed to enter the start date, the entered date is checked for validity and range and 
                if the date is not valid and not within specified range, the user is instructed to enter another start
                date until the entered start date is valid and within range.
                
                Then the user is instructed to enter the end date and the entered date is checked for validity and range
                in the above manner.
                
                Once valid and within-range start date and end date are received, the two dates are given as inputs to 
                the function, 'check_order_of_dates_and_guide(start_date, end_date)' to check if the end date is a later
                date than the start date. 
                """
                print("")
                start_date = input("Enter your start date in 'DD.MM.YYYY' format (Or press 'Enter' to exit): ")

                if start_date:
                    start_date = check_validity_and_range_of_date("start", start_date)
                    end_date = input("Enter your end date in 'DD.MM.YYYY' format (Or press 'Enter' to exit): ")
                else:
                    exit(0)
                if end_date:
                    end_date = check_validity_and_range_of_date("end", end_date)
                    date_tuple = check_order_of_dates_and_guide(start_date, end_date)
                    start_date = date_tuple[0]
                    end_date = date_tuple[-1]
                    print("")
                    print("Your start date is: " + start_date)
                    print("Your end date is: " + end_date)
                    """
                    The number of days from start_date upto and including end_date is calculated as follows:
                    At first the number of days from REFERENCE_DATE (00.00.0000) upto and including start_date 
                    is calculated.
                    Then the number of days from REFERENCE_DATE upto and including end_date is calculated.
                    The earlier number of days is subtracted from this number of days to obtain the number of days 
                    from start_date upto and including end_date.
                    The above method has been applied for calculating the number of days from any date upto and 
                    including any later (than the former) date.
                    """
                    span1 = calculate_days_span(REFERENCE_DATE, start_date) - calculate_days_span(REFERENCE_DATE, DATA_START_DATE)
                    span2 = (calculate_days_span(REFERENCE_DATE, end_date) - calculate_days_span(REFERENCE_DATE, start_date)) + 1
                    span3 = calculate_days_span(REFERENCE_DATE, DATA_END_DATE) - calculate_days_span(REFERENCE_DATE, end_date)
                    N = span2 + span3
                    P = span3
                else:
                    exit(0)
            else:
                exit(0)
        else:
            exit(0)

        for country in countries_to_compare:
            """
             The data required for comparison is sliced and acquired (depending on the 'mode' and value or dates 
             provided by the user) from the 'countries_daily_data_dict' and fractions (representative of relative 
             value of each data value in comparison to the largest available data value in the list) are calculated 
             and a new list 'daily_fractions' is created for each country to compare and the each 'daily_fractions' 
             is stored in a new dictionary, 'countries_data_fractions' against each corresponding country.
             
             Then each "country -> 'daily_fractions'" pair is accessed from 'countries_data_fractions' and the 
             fractions are plotted in an image, 'visualization' for each country.
             
             And each "country -> 'visualization'" pair is stored in another dictionary, 'visualizations_dict'. 
            """
            list_of_data = countries_daily_data_dict.get(country)
            list_of_data_to_compare = list_of_data[(len(list_of_data) - N) : (len(list_of_data) - P)]
            daily_fractions = compute_daily_fractions(list_of_data_to_compare)
            countries_data_fractions[country] = daily_fractions
            visualization = plot_analysis(country, countries_data_fractions[country], (N - P))
            visualizations_dict[country] = visualization
        print("")
        print("")
        print("Fetching Countries' Visualizations: ")
        serial = 0
        for country in visualizations_dict.keys():
            """
            For each country to compare, the corresponding image is accessed from 'visualizations_dict' and shown
            on the screen. The created images are also saved in the home directory of the program.
            """
            serial += 1
            print(str(serial) + "." + country)
            output = country + ".png"
            visualizations_dict[country].show()
            visualizations_dict[country].pil_image.save(output)



def accept_mode():
    """
    This function accepts the string for mode of analysis from the user and check if the entered mode is valid or not.

    If the entered mode is not valid, then the user is instructed to enter another valid string until the entered string
    is found to be valid.

    the valid string is converted to an int.

    the int-type variable, 'mode_index' is returned.
    """
    mode_index = 0
    choice_of_mode = input("How do you want to analyze? Enter '1' for analysis of last few days, \nor '2' for analysis between two dates of your choice. (Or press 'Enter' to exit): ")
    if choice_of_mode:
        while ((not choice_of_mode.isdigit()) or (choice_of_mode != "1" and choice_of_mode != "2")):
            print("Wrong entry.")
            choice_of_mode = input(
                "How do you want to analyze? Enter '1' for analysis of last few days, \nor '2' for analysis between two dates of your choice. (Or press 'Enter' to exit): ")
            if choice_of_mode == "":
                break
        if choice_of_mode:
            choice_of_mode = int(choice_of_mode)
            mode_index = choice_of_mode

    return mode_index



def check_validity_and_range_of_date(boundary_type, date):
    """
    This function checks the validity and range of a date entered by the user
    and if the date is not valid or not within range, the user is instructed to
    reenter another valid and within-range date until it is found to be valid and within range.

    It takes as input: string variable, 'boundary_type' (to specify start date or end date), another string variable,
                       'date'.
    It gives as output a valid and within-range date.
    """
    date = check_date_validity(boundary_type, date)  # First, the validity of the date is checked.
    if date:
        date = check_date_range(boundary_type, date)  # Once the date is valid, it is checked if the date is within range.
    else:
        exit(0)
    return date


def check_date_validity(boundary_type, date):
    """
    Given the 'boundary_type' ( having value "start" for start date and "end" for end date) and 'date' as inputs,
    this function checks the validity (in terms of structure and feasibility) of the date.

    If the date is not valid, then the user is instructed to reenter a valid date (start date or end date specified
    by the value of 'boundary_type') until the entered date becomes valid.

    At last, the valid date is returned.

    """

    while not date[:2].isdigit() or not date[3:5].isdigit() or not date[-4:].isdigit() or len(date) != 10:
        """
        This loop checks if the entered date is structurally valid (i.e. the date is in DD.MM.YYYY format and each 
        date-field is a collection of digits.
        """
        print("The Dates must be between " + DATA_START_DATE + " and " + DATA_END_DATE + " and in 'DD.MM.YYYY' format" + ".")

        date = input("Enter your " + boundary_type + " date in 'DD.MM.YYYY' format (Or press 'Enter' to exit): ")
        if date == "":
            exit(0)
    check = is_leap_year(int(date[-4:]))
    while (((int(date[3:5]) == 1 or int(date[3:5]) == 3 or int(date[3:5]) == 5 or int(date[3:5]) == 7 or
             int(date[3:5]) == 8 or int(date[3:5]) == 10 or int(date[3:5]) == 12) and int(date[:2]) > 31) or
           ((int(date[3:5]) == 4 or int(date[3:5]) == 6 or int(date[3:5]) == 9 or int(date[3:5]) == 11) and int(date[:2]) > 30) or
           (check and int(date[3:5]) == 2 and int(date[:2]) > 29) or
           ((not check) and int(date[3:5]) == 2 and int(date[:2]) > 28) or int(date[3:5]) > 12 or int(date[3:5]) < 1):
        """
        This loop checks if the entered date is practically possible i.e. the date is a real date.
        """
        print("Invalid date.")
        date = input("Enter your " + boundary_type + " date in 'DD.MM.YYYY' format (Or press 'Enter' to exit): ")
        if date == "":
            exit(0)
        while not date[:2].isdigit() or not date[3:5].isdigit() or not date[-4:].isdigit() or len(date) != 10:
            """
            This loop checks if the entered date is structurally valid (i.e. the date is in DD.MM.YYYY format and each 
            date-field is a collection of digits.
            """
            print(
                "The dates must be between " + DATA_START_DATE + " and " + DATA_END_DATE + " and in 'DD.MM.YYYY' format" + ".")

            date = input("Enter your " + boundary_type + " date in 'DD.MM.YYYY' format (Or press 'Enter' to exit): ")
            if date == "":
                exit(0)
    return date


def check_date_range(boundary_type, date):
    """
    Once a valid date is entered by the user, the date (specified by the string variable, 'date') and the type of the
    date ("start" or "end", specified by the string variable, 'boundary_type') is given to this function as input.

    This function checks if the date is within the specified range (bound by 'DATA_START_DATE' and 'DATA_END_DATE')
    according to the value of 'boundary_type' and if the date is found to be not within the range, then the user is
    instructed to enter a new date until the entered date is found to be within the range.

    With each entry, the validity of the date is also checked, and done accordingly.

    The valid and within-range date is returned as output.
    """
    if boundary_type == "start":
        while ((int(date[-4:]) < int(DATA_START_DATE[-4:])) or (int(date[-4:]) > int(DATA_END_DATE[-4:])) or (
            ((int(date[-4:]) == int(DATA_START_DATE[-4:])) and (int(date[3:5]) == int(DATA_START_DATE[3:5])) and
            (int(date[0:2]) < int(DATA_START_DATE[0:2])))) or (((int(date[-4:]) == int(DATA_END_DATE[-4:])) and
            (int(date[3:5]) == int(DATA_END_DATE[3:5])) and (int(date[0:2])) >= int(DATA_END_DATE[0:2])))) or (
                ((int(date[-4:]) == int(DATA_END_DATE[-4:])) and (int(date[3:5]) > int(DATA_END_DATE[3:5])))):
            """
            This loop checks the range of the start date.
            """
            print("The Dates must be between " + DATA_START_DATE + " and " + DATA_END_DATE + " (both inclusive), \nThe end date can never be " + DATA_START_DATE + " and the start date can never be " + DATA_END_DATE + ".")
            date = input("Enter your " + boundary_type + " date in 'DD.MM.YYYY' format (Or press 'Enter' to exit): ")
            if date:
                date = check_date_validity(boundary_type, date)
            else:
                exit(0)
    elif boundary_type == "end":
        while (int(date[-4:]) < int(DATA_START_DATE[-4:]))  or (int(date[-4:]) > int(DATA_END_DATE[-4:]))  or \
                (((int(date[-4:]) == int(DATA_START_DATE[-4:])) and (int(date[3:5]) == int(DATA_START_DATE[3:5])) and
                (int(date[0:2]) <= int(DATA_START_DATE[0:2])))) or (((int(date[-4:]) == int(DATA_END_DATE[-4:])) and
                (int(date[3:5]) == int(DATA_END_DATE[3:5])) and (int(date[0:2])) > int(DATA_END_DATE[0:2]))) or (
                ((int(date[-4:]) == int(DATA_END_DATE[-4:])) and (int(date[3:5]) > int(DATA_END_DATE[3:5])))):
            """
            This loop checks the range of the end date.
            """
            print("The Dates must be between " + DATA_START_DATE + " and " + DATA_END_DATE + " (both inclusive), \nThe end date can never be " + DATA_START_DATE + " and the start date can never be " + DATA_END_DATE + ".")
            date = input("Enter your " + boundary_type + " date in 'DD.MM.YYYY' format (Or press 'Enter' to exit): ")
            if date:
                date = check_date_validity(boundary_type, date)
            else:
                exit(0)
    return date


def check_order_of_dates_and_guide(start_date, end_date):
    """
    Two valid date-strings, start date and end date, specified by 'start_date' and 'end_date' respectively, are given
    to this function as inputs.

    This function checks the order of the dates (i.e. if the date sprcified by 'end_date' is a later date than the date
    specified by 'start_date').

    With each entry, the validity and range of the date is also checked, and done accordingly.

    If the order is not correct, then the user is instructed to enter two dates in correct order, until the dates are in
    correct order.

    The in-order tuple, '(start_date, end_date)' is returned.
    """
    while (int(start_date[-4:]) > int(end_date[-4:])) or ((int(start_date[-4:]) == int(end_date[-4:])) and (
            int(start_date[3:5]) > int(end_date[3:5]))) or ((
            int(start_date[-4:]) == int(end_date[-4:]) and (int(start_date[3:5]) == int(end_date[3:5])) and (
            int(start_date[0:2]) >= int(end_date[0:2])))):
        if int(start_date[-4:]) > int(end_date[-4:]):
            print("The 'YYYY' of end-date must be of higher value than 'YYYY' of start-date.")
        elif ((int(start_date[-4:]) == int(end_date[-4:])) and (int(start_date[3:5]) > int(end_date[3:5]))):
            print("The 'MM' of end-date must be of higher value than 'MM' of start-date if both 'YYYY' values are same.")
        else:
            print("The 'DD' of end-date must be of higher value than 'DD' of start-date if both 'MM' values and both 'YYYY' values are same.")
        start_date = input("Enter your start date in 'DD.MM.YYYY' format (Or press 'Enter' to exit): ")
        if start_date:
            start_date = check_validity_and_range_of_date("start", start_date)
            end_date = input("Enter your end date in 'DD.MM.YYYY' format (Or press 'Enter' to exit): ")
            if end_date:
                end_date = check_validity_and_range_of_date("end", end_date)
            else:
                exit(0)

        else:
            exit(0)

    return (start_date, end_date)




def is_leap_year(given_year):
    """
    Checks if a given year denoted by 'given_year' is leap-year or not.
    Returns True if 'given_year' is leap-year.
    Returns False otherwise.
    """
    if given_year % 100 == 0:
        if given_year % 400 == 0:
            return True
        else:
            return False
    else:
        if given_year % 4 == 0:
            return True
        else:
            return False



def calculate_days_span(start_date, end_date):
    """
    This function calculates the number of days between two dates starting from the start-date upto and
    including the end-date:

    Inputs: String variable 'start_date' (representing the start-date in 'DD.MM.YYYY' format)
            string variable 'end_date' (representing the end-date in 'DD.MM.YYYY' format)
    Output: int variable 'days_span' (representing the number of days upto and including the end-date from the start-date)
    """
    N_leap = 0   # Stores the number of leap-year full years (initialized to contain 0).
    N_non_leap = 0 # Stores the number of non leap-year full years (initialized to contain 0).
    start_date_list = start_date.split(".")
    end_date_list = end_date.split(".")
    start_year = int(start_date_list[-1])
    start_month = int(start_date_list[1])
    start_day = int(start_date_list[0])
    end_year = int(end_date_list[-1])
    end_month = int(end_date_list[1])
    end_day = int(end_date_list[0])
    end_year -= 1
    while end_year != start_year:
        """
        This loop counts the number of leap-year and non leap-year full years between the end-date and the start-date.
        It decreases the 'end_year' variable (representing the year of end-date) by 1 at each step until it becomes 
        equal to 'start_year' variable (representing the year of start-date) and checks if it is leap-year or not at 
        each step and increases 'N_leap' or N_non_leap' by 1 according to the value of boolean variable 'check'.
        """
        check = is_leap_year(end_year)
        if check:
            N_leap += 1
        else:
            N_non_leap += 1
        end_year -= 1
    # The number of days in full years between start-date and end-date is calculated.
    full_year_days = (N_leap * 366) + (N_non_leap * 365)
    # Finally the number of days in the end-year upto the end-date is calculated.
    current_year_days = calculate_days_in_current_year(end_date_list)
    days_span = full_year_days + current_year_days
    return days_span



def calculate_days_in_current_year(current_date_list):
    """
    Given a list type variable, 'current_date_list', this function calculates and returns the number of days
    (represented by 'days_in_current_year' variable of type int) upto and including the current date from the beginning
    date of the current year.
    """
    days_in_current_year = 0
    current_year = int(current_date_list[-1])
    current_month = int(current_date_list[1])
    current_day = int(current_date_list[0])
    """
    A list variable 'month_days_list' containing number of days in every month (denoted by numbers from 1(for January),
    gradually increasing by 1 upto 12(for December)) as values is defined.
    """
    month_days_list = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    # At first the 'current_year' is checked if it is a leap-year or not.
    check = is_leap_year(current_year)
    if check:
        """
        If the current year is a leap-year, then the corresponding value for February in the 'month_days_list' 
        is set as 29 as February in a leap-year has 29 days.
        """
        month_days_list[1] = 29
    while current_month > 1:
        """
        If the 'current_month' variable (representing the current month_number) is greater than 1, then 'current_month'
        is reduced by 1 (to account for all the full months upto the current date from the beginning of the current year)
        indefinitely until the value of 'current_month' becomes 1. And for each value of 'current_month' the number of 
        days in that month is fetched from 'month_days_list' (It is indexed by [current_month - 1]) and 
        added to the variable 'days_in_current_year'.
        """
        current_month -= 1
        days_in_current_year += month_days_list[current_month - 1]
    """
    Finally, the number of days in the current month, upto the current date from the beginning of the current month
    denoted by variable, 'current_day' is added to 'days_in_current_year'.
    """
    days_in_current_year += current_day
    return days_in_current_year



def normalize(countries_list):
    """
    Given the list, 'countries_list', containing the filenames, the function
    returns a normalized list with uppercase version of all the filenames in it.

    """
    normalized_list = []
    for item in countries_list:
        normalized_list.append(item.upper())
    return normalized_list
        

def compute_daily_fractions(daily_cases_list):
    """
    Given a list of integers(representative of a list of daily cases),'daily_cases_list', this function finds the
    largest value and represents each value as a fraction of the largest value and populates the list, 'fractions'
    with the fractional values.

    The resulting list, 'fractions' is returned.
    """
    largest_number = find_largest_number(daily_cases_list)
    fractions = []
    if largest_number == 0:
        for i in range(len(daily_cases_list)):
            fractions.append(largest_number)
    else:
        for value in daily_cases_list:
            fraction = value/largest_number
            fractions.append(fraction)

    return fractions


def find_largest_number(numbers_list):
    """
    Given a list of integers as input, this function sorts the list elements in ascending
    order and returns the largest number in the list. 

    """
    sorted_numbers_list = sorted(numbers_list) # The list 'numbers_list' is sorted in ascending order. 
    largest = sorted_numbers_list[-1]  # The last number is the largest number in list 'sorted_numbers_list
    return largest


def get_countries(normalized_countries_list):
    """
    This function takes a normalized list of filenames(in which all the filenames are in uppercase) as input.

    It accepts a series of country_names of user's choice from the user one by one and checks if the uppercase
    version of each country_name appears in any of the filenames in the input list 'normalized_countries_list.

    If the result of the above check is true, then the country_name in its uppercase version is appended in
    the output list 'selected_countries'.
    Else, the user is directed to enter another country_name.

    The two steps immediately above are repeated for each entry by the user until the user enters an empty string("").

    At last the list 'selected_countries', containing the entered country_names, is returned.

    If the uppercase version of user-entry is 'ALL', then the empty list 'selected_countries' is populated with
    all the country_names in the filenames in the input list and returned.
    """
    selected_countries = []
    print("Getting countries to compare: ")
    while True:
        country = input("Enter a country: ")
        while country.upper() != "ALL" and country != "" and (country.upper() + ".TXT") not in normalized_countries_list:
            print("Invalid entry")
            country = input("Enter a country: ")
        if country.upper() == "ALL":
            selected_countries = get_all_countries(normalized_countries_list)
            break
        if country == "":
            break
        selected_countries.append(country.upper())
    return selected_countries



def get_all_countries(countries_list):
    """
    This function takes a list of filenames containing country_names as input and extracts
    country_name from each filename in the input list, 'countries_list' and appends each country_name
    in the output list, 'all_countries'.

    The resulting list, 'all_countries' is returned.
    """
    all_countries = []
    for item in countries_list:
        item = item.rstrip("TXT")
        
        all_countries.append(item[:-1])

    return all_countries 


def plot_analysis(country, country_data, N_data_values):
    """
    Given a country_name, its list of data and number of data values in that list, this function returns a coloured
    image representative of that country's data:

    This function takes 3 inputs:a country_name('country'), list of fractional data_values for that country_name
    ('country_data') and number of values('N_data_values') in 'country_data'.

    It creates a blank image containing 'N_data_values' number of data-stripes.

    It colours each data-stripe selectively red based on corresponding fractional value (i.e. the higher the fraction,
    the more red the corresponding data-stripe is) in country_data.
    Green and blue values are same for each pixel.

    It returns a coloured image, 'img' for each set of inputs.  

    """
    img = SimpleImage.blank((N_data_values * STRIPE_WIDTH), (N_data_values * 2))
    width = img.width
    height = img.height
    for i in range (len(country_data)):
        for x in range(STRIPE_WIDTH):
            for y in range(height):
                pixel = img.get_pixel(((STRIPE_WIDTH * i) + x), y)
                pixel.red = country_data[i] * 255
                pixel.green = GREEN
                pixel.blue = BLUE
                img.set_pixel(((STRIPE_WIDTH * i) + x), y, pixel)
    return img


def list_cumulative_cases(filename):
    """
    Given filename of a file (specifying a country), containing daily cumulative cases, this function reads the file
    and makes and returns a list of cumulative cases for that filename.
    """
    lst = []
    with open(filename) as f:
        for line in f:
            lst.append(line.strip())
    for i in range(len(lst)):
        lst[i] = int(lst[i])
    return lst


def list_daily_cases(list_of_cumulative_cases):
    """
    Given a list of cumulative cases, this function makes and returns a list of
    daily cases.
    """
    daily_list = [0]

    for i in range(1, len(list_of_cumulative_cases)):
        N_daily_case = list_of_cumulative_cases[i] - list_of_cumulative_cases[i - 1]
        daily_list.append(N_daily_case)
    
    return daily_list


if __name__=="__main__":
    main()
