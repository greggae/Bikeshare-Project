import time
import pandas as pd
import numpy as np

CITY_DATA = { 'Chicago': 'chicago.csv',
              'New York City': 'new_york_city.csv',
              'Washington': 'washington.csv' }

month_list = {'All':0, 'January':1, 'February':2, 'March':3, 'April':4, 'May':5, 'June':6, 'None':7}
day_list = {'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'All'}
month = 0
day = 0
data_filter = 0
filter_options = {'Month', 'Day', 'All'} 
    
def get_filters():
 
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # CITY INPUT
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input("Please enter one of the following cities to see their data: Chicago, New York City, or Washington: ")

    while True:
        if city in CITY_DATA:
            break
        else:
            city = input("That's not one of the cities we have data on.  Please enter Chicago, New York City or Washington, in that format: ")

    # MONTH INPUT
    # get user input for month (all, january, february, ... , june)
    data_filter = input("You can filter the data to look at data by Month, Day, or no filter at All.  Please enter Month, Day or All to see the data for all months and days: ")

    while True:
        if data_filter in filter_options:
            break
        else:
            print("That is not one of the ways to filter the data.  Please enter Month to filter by month, Day to filter by day, or All to see all of the data, in that format: " + "\n")
            data_filter = input()
    
    if data_filter == 'All':
        month = 'All'
        day = 'All'
    elif data_filter == 'Month':
        day = 'All'
        month = input("Please enter January, February, March, April, May, June, or All for all months: ")
        while True:
            if month in month_list:
                break
            else:
                print("That's not one of the months we have data on. Please enter January, February, March, April, May, June, or All, in that format: " + "\n")
                month = input()
    else: # input is 'Day'
        month = 'All'
        print("Please enter the day you are interested in: Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or all days in the time period: " + "\n")
        day = input()
        while True:
            if day in day_list:
                break
            else:
                print("That's not one of the days we have data on.  Please enter Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or All, in that format: " + "\n")
                day = input()

    print('-'*40)
    print(city, month, day, data_filter)
    return city, month, day, data_filter


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

    # load csv data
    df = pd.read_csv(CITY_DATA[city])
    print ("CSV LOADED")
        
    df['Start Time'] = pd.to_datetime(df['Start Time'], format='%Y-%m-%d %H:%M:%S')
    print ("START TIME CONVERTED TO DATETIME")

    # column extraction
    df['month'] = df['Start Time'].dt.month
    df['day'] = df['Start Time'].dt.day


    if data_filter == 'Month':
        df_filtered = df[df.month == month]
        return df_filtered
    elif data_filter == 'Day':
        df_filtered = df[df.day == day]
        return df_filtered
    else:
        return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    df['month'] = df['Start Time'].dt.strftime('%B') #get month names immediately
    common_month = df['month'].mode()[0]
    print("The most common month is: {}".format(common_month))

    # display the most common day of week
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    common_day = df['day_of_week'].mode()[0]
    print("The most common day is: {}".format(common_day))

    # display the most common start hour
    df['hour_of_day'] = df['Start Time'].dt.hour
    common_hour = df['hour_of_day'].mode()[0]
    print("The most common start hour is: {}".format(common_hour))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    #most_common_start_station = df.groupby('Start Station').agg(count).max
    most_common_start_station = df['Start Station'].mode()[0]
    print("The most commonly used start station is: {}".format(most_common_start_station))


    # display most commonly used end station
    #most_common_end_station = df.groupby('End Station').agg(count).max
    most_common_end_station = df['End Station'].mode()[0]
    print("The most commonly used end station is: {}".format(most_common_end_station))



    # display most frequent combination of start station and end station trip
    #most_common_trip = df.groupby('Start Station', 'End Station').agg(count).max
    most_common_trip = df.groupby(['Start Station'], ['End Station']).mode()[0]
    print("The most commonly used combination of start and end station is: {} and {}".format(most_common_trip))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df.groupby('Trip Duration').sum
    print("The total travel time is: {}".format(total_travel_time))


    # display mean travel time
    avg_travel_time = df.groupby('Trip Duration').mean
    print("The average travel time is: {}".format(avg_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    #user_count = df.groupby('User Type').agg(count)
    user_count = df.groupby(['User Type']).value_counts()
    print(user_count)


    # Display counts of gender
    #gender_count = df.groupby('Gender').agg(count)
    gender_count = df.groupby(['Gender']).value_counts()
    if gender_count != ():
        print(gender_count)
    else:
        print("There is no gender data available for this city.")


    # Display earliest, most recent, and most common year of birth
    #if birth_year != ():
    if df['Birth Year'] != ():
       earliest_birth = df['Birth Year'].min
       print("The oldest person who used the service was born in: {}".format(earliest_birth))
    
       latest_birth = df['Birth Year'].max
       print("The youngest person who used the service was born in: {}".format(latest_birth))

       #common_year = df['Birth Year'].agg(count)
       common_year = df['Birth Year'].mean(int)
       print("The most common year of birth fof a person using this service was: {}".format(common_year))

    else:
        print("There is no birth data available for this city.")
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


#def main():
#    while True:
#
#        city, month, day = get_filters()
#        print ("GOT USER INPUTS")
#        
#        df = load_data(city, month, day)
#        print ("DATA LOADED")

#        time_stats(df)
#        print ("TIME_STATS DONE")

#        exit()
        
#        station_stats(df)
#        trip_duration_stats(df)
#        user_stats(df)

#        restart = ('\nWould you like to restart? Enter yes or no.\n')
#        if restart.lower() != 'yes':
#            break


#if __name__ == "__main__":
#	main()
    
def main():
    while True:
        city, month, day, data_filter = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
    