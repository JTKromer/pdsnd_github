import time
import pandas as pd
import numpy as np
import calendar as cal

CITY_DATA = { 'Chicago': 'chicago.csv',
              'New York City': 'new_york_city.csv',
              'Washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    #referenced support pages https://knowledge.udacity.com/questions/839526 and https://knowledge.udacity.com/questions/721492 and https://knowledge.udacity.com/questions/244964
    city = input("Please choose one city to review: Chicago, New York City or Washington: ").title()
    while city not in  ['Chicago', 'New York City', 'Washington']:
        print("That city is not found.")
        city = input("Please choose one city to review: Chicago, New York City or Washington: ").title()
        #city input accepted, we continue!
    
    # TO DO: get user input for month (all, january, february, ... , june)
    month = input("Please choose one month to study, or 'all': January, February, March, April, May, June or All: ").title()
    while month not in ['January', 'February', 'March', 'April', 'May', 'June', 'All']:
        print("That month is not found.")
        month = input("Please choose one month to study, or 'all': January, February, March, April, May, June or All: ").title()
    
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)        
    day = input("Please provide choose day to study, or 'all': Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or All: ").title()
    while day not in ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'All']:
        print("That day is not found.")
        day = input("Please provide choose day to study, or 'all': Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or All: ").title()   
            
    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    # load data file into a dataframe for the input city
    df = pd.read_csv(CITY_DATA[city])
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    # filter by month if applicable
    if month != 'All':
        # use the index of the months list to get the corresponding int
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        month = months.index(month) + 1 
        #index +1 because the index would otherwise start at 0
    
        # filter by month to create the new dataframe
        df = df[df['month'] == month]
    # filter by day of week if applicable
    if day != 'All':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day]

    return df
    print(df)

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    com_month = df['month'].mode()[0]
    print("The most common month of use is: ", cal.month_name[com_month])
    #convert int month to the full month name with calendar 'cal'. Referenced https://pynative.com/python-get-month-name-from-number/

    # TO DO: display the most common day of week
    com_day = df['day_of_week'].mode()[0]
    print("The most common day of use is: ", com_day)

    # TO DO: display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    com_hour = df['hour'].mode()[0]
    print("The most common hour of use is: ", com_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
    
def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    com_start_sta = df['Start Station'].mode()[0]
    print("The most common start station of use is: ", com_start_sta)

    # TO DO: display most commonly used end station
    com_end_sta = df['End Station'].mode()[0]
    print("The most common end station of use is: ", com_end_sta)

    # TO DO: display most frequent combination of start station and end station trip
    com_combo_sta = df.groupby(['Start Station', 'End Station']).size().idxmax()
    #referenced to get combo count max syntax https://stackoverflow.com/questions/53037698/how-can-i-find-the-most-frequent-two-column-combination-in-a-dataframe-in-python
    #groupby start and end station columns to quasi-concatenate then size and idmax to quantify station combos and return result with highest count
    print("The most common combination of start and end stations used is: ", com_combo_sta)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_time = df['Trip Duration'].sum()
    print("The total travel time is: ", total_time / 3600, " hours.")
    #divide seconds sum by 3600 to present nicer output for reader, in hours

    # TO DO: display mean travel time
    mean_time = df['Trip Duration'].mean()
    print("The average travel time is: ", mean_time / 60, " minutes.")
    #divide seconds sum by 60 to present nicer output for reader, in minutes

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df.groupby(['User Type'])['User Type'].count()
    print("User breakdown: \n", user_types)
    print("\n")

    # TO DO: Display counts of gender
    user_gender = df.groupby(['Gender'])['Gender'].count()
    print("User gender breakdown: \n", user_gender)
    print("\n")   
    
    # TO DO: Display earliest, most recent, and most common year of birth
    min_bday = int(df['Birth Year'].min())
    max_bday = int(df['Birth Year'].max())
    mode_bday = int(df['Birth Year'].mode())
    #int added to clean up view for end user, removing 0.0 format
    print("The earliest user birth year is: ", min_bday)
    print("The latest user birth year is: ", max_bday)
    print("The most common user birth year is: ", mode_bday)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    """Prompts end user if they would like to see 5 rows of raw data, then addtional rows"""
    #referenced https://knowledge.udacity.com/questions/110782
    reply = input("\nWould you like to see a few lines of the raw data? Type 'yes' or 'no': ").lower()
    row_ns = 0
    if reply == 'yes':
        while True:
            print(df.iloc[row_ns:row_ns+5])
            row_ns += 5
            reply2 = input("\nWould you like to see additional lines of the raw data? Type 'yes' or 'no': LINE 184").lower()
            if reply2 == 'no':
                    break
            if reply2 not in ['yes', 'no']:
                print("\nThat entry is not recognized.")
                reply2 = input("\nWould you like to see additional lines of the raw data? Type 'yes' or 'no': LINE 188").lower()
                if reply2 == 'no':
                    break
            if reply2 == 'yes':
                print(df.iloc[row_ns:row_ns+5])
                row_ns += 5
                reply2 = input("\nWould you like to see additional lines of the raw data? Type 'yes' or 'no': LINE 195").lower()
                if reply2 == 'no':
                    break
    
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()