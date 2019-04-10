# -*- coding: utf-8 -*-
"""
Created on Mon Mar 11 13:41:05 2019

@author: lcurby
"""

import time
import pandas as pd
import numpy as np


CITY_DATA = { 'chicago': 'chicago.csv','new york city': 'new_york_city.csv','washington': 'washington.csv' }
cities = ['chicago', 'new york city', 'washington']
months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
       (str) city - name of the city to analyze
       (str) month - name of the month to filter by, or "all" to apply no month filter
       (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    city = ""
    while True:
        city = input('What city you would like to check? Choose Chicago, New York City, Washington:\n').lower()
        if city not in cities:
            print('"{}" is not found.'.format(city))
            continue
        else:
           break

    month = ""

    while True:
        month = input('What month you would like to see your data? January, February, March, April, May, June, or All:\n').lower()
        if month not in months:
            print('"{}" is not found.'.format(month))
            continue
        else:
            break

    day = ""

    while True:
        day = input('What day you would like to see your data? Monday, Tuesday, Wednesday, Thursday, Friday, or All:\n').lower()
        if day not in days:
            print('"{}" is not found.'.format(day))
            continue
        else:
            break

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

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    #df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
       # use the index of the months list to get the corresponding int

       months = ['january', 'february', 'march', 'april', 'may', 'june']
       #month = months.index(month)
       month = months.index(month)
       # filter by month to create the new dataframe
       df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
       # filter by day of week to create the new dataframe
       df = df[df['day_of_week'] == day.title()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month from the Start Time column to create a month column
    df['month'] = df['Start Time'].dt.month

    common_month = df['month'].mode()[0]
    print('Most Common Month: {}'.format(common_month))

    # extract day from the Start Time column to create a day column
    df['day'] = df['Start Time'].dt.day

    popular_day = df['day'].mode()[0]
    print('Most Common Day: {}'.format(popular_day))

    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour

    popular_hour = df['hour'].mode()[0]
    print('Most Common Start Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    common_start_station = df['Start Station'].mode()[0]
    print('Most Common Start Station: {}'.format(common_start_station))
    print('Start Station Counts: {}\n'.format(df['Start Station'].value_counts()[common_start_station]))

    common_end_station = df['End Station'].mode()[0]
    print('Most Common End Station: {}'.format(common_end_station))
    print('End Station Counts: {}\n'.format(df['End Station'].value_counts()[common_end_station]))

    round_trip = df['Start Station'] + '-' + df['End Station']

    frequent_trip = round_trip.mode()[0]
    print('Most Frequent Trip: {}'.format(frequent_trip))
    print('Frequent Trip Counts: {}\n'.format(round_trip.value_counts()[frequent_trip]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    travel_time = df['Trip Duration'].sum()
    print('Total Travel Time: {}\n'.format(travel_time))

    mean_travel = df['Trip Duration'].mean()
    print('Mean Travel Time: {}\n'.format(mean_travel))

        # display max travel time
    max_travel = df['Trip Duration'].max()
    print('Max Travel Time: {}\n'.format(max_travel))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    user_types = df['User Type'].value_counts()
    print(user_types)

        # Try and except error handling for Washington filter
    try:
        gender_types = df['Gender'].value_counts()
        print(gender_types)

    except:
        # print error statement for Gender column
        print('Gender column is not available. \nCannot display statistics.\n')
        # print error statement for Birth Year column
        print('Birth Year column is not available. \nCannot display statistics.\n')
    else:
        # find earliest birth year
        earliest_year = df['Birth Year'].min()
        # find most common birth year
        common_year = df['Birth Year'].mode()[0]
        # find most recent year
        recent_year = df['Birth Year'].max()

        # display earliest birth year
        print("The earliest birth year: "+"{:.0f}".format(earliest_year))
        # display most common birth year
        print("The most common birth year: "+"{:.0f}".format(common_year))
        # display recent birth year
        print("The most recent birth year: "+"{:.0f}".format(recent_year))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def raw_data(df):
    """Display raw data for Bikeshare users."""

    print('\nBikeshare Statistics Data\n')
    start_time = time.time()

    request_raw_data = input('\nWould you like to see 5 rows of data? Enter Yes or No:\n').lower()
    if request_raw_data == 'yes' or 'y':
        print('\nPlease wait while accessing raw data...\n')
            # index number = 0
        i = 0
                # while loop cycles through raw data in csv and displays it
    while True:
        print(df.iloc[i:i + 5])
        i += 5

        print("This took %s seconds." % (time.time() - start_time))

        request_more_data = input('\nWould you like to see additional 5 raw data? Enter Yes or No:\n').lower()
        if request_more_data != 'yes' or 'y':
            break

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

        

def main():

    while True:
        city, month, day = get_filters()
        #get_filters = city, month, day
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
        city = ""
        month = ""
        day = ""
        main()
