import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }
MONTHS=['january', 'february', 'march', 'april', 'may', 'june']
CITIES=['chicago','new york','washington']
DAYS=['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday']
def get_city():
    """
    Function that returns the city from list of cities
    Returns:
    (Str) city- of users choise
    """

    test=True
    while test:
        if test:
            city=input(" Please input which city of the following cities your'e interested in :  \n Chicago, New York or Washington ?\n").lower()
        for c in CITIES:
            if c==city:
                test=False
    return city

def validate(lst,exp):
    '''
    Checks if string is in list
    Returns:
    (Boolean) True/False
    '''
    if exp in lst:
        return True
    else:
        return False

def loop_raw_data(df):
    '''
    Prints 5 rows of raw data then asks user if she wants to see 5 more
    '''
    print('-'*60)
    c=0
    answer_1 =input("Would you like to see raw data ? ,\nPress YES! ").lower()
    if answer_1=='yes':
        for index,row in df.iterrows():
            print(row)
            if c ==5:
                answer =input("Do 5 more rows,Press No to end").lower()
                if answer!='no':
                    c=0
                    print('='*60)
                    continue
                else:
                    break
            c+=1
            print('-'*60)
    else:
        return



def get_filters():

    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    #call to city function
    city=get_city()

    while True:
            user_input=input("Input the duration for the filter: \n Month , Day, Both or none \n").lower()
            if user_input=='month':
                month = input(" Wich month ? \n January,February,March,April,May,June \n").lower()
                if validate(MONTHS,month):
                    return city,month,'all'
                else:
                    continue
            elif user_input=='day':
                try:
                    day=int(input(" Wich day of the week ? \n  Please type your response as an integer (e.g., 1=Sunday)"))
                    if day >= 0 and day < 8:
                        return city,'all', DAYS[day-1]
                    else:
                        print(' Please supply a number between 1-7 for the day of the week, number given was : {} '.format(day))
                except ValueError:
                    print("Please supply a integer between 1-7 , for day of week (e.g., 1=Sunday")
                    continue
            elif user_input=='both':
                raw_both=input("First enter Month followed by day as a Integer (e.g., 1=Sunday) sepearated by a \",\" \n")
                try:
                    month,day_str=raw_both.split(',')
                    day=int(day_str)
                    day-=1
                except:
                    print("Wrong input! ")
                    continue
                if validate(MONTHS,month.lower()) and (day >=0 and day < 8):
                    return city,month,(DAYS[day])
                else:
                    print("Unknown month, or day")
                    continue
            elif user_input=='none':
                return city,'all','all'
            else:
                print('Unknown command, please try again!')
                continue


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
    try:
# load data file into a dataframe
        tst=CITY_DATA[city]
        df = pd.read_csv(tst)
 #dof = pd.read_csv('newyork.csv')
    except FileExistsError:
        print("File not found")
    except:
        print('Unknown fault, wehn trying to load csv-file')
# convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

 # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.strftime('%A')

# filter by month if applicable
    if month != 'all':
# use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

 # filter by month to create the new dataframe
        df = df[df['month'] == month]

# filter by day of week if applicable
    if day != 'all':
 # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df



def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print('################### TIME STATISTICS #####################\n')
    print('\n Calculating The Most Frequent Times of Travel........\n')
    start_time = time.time()
    i_day_of_month=df['Start Time'].dt.month.mode()[0]

# display the most common month
    print('The most common month is :{}'.format(MONTHS[i_day_of_month-1]))
# display the most common day of week
    i_day_of_month=df['day_of_week'].mode()[0]
    print('The most common month is :{}'.format(i_day_of_month))
# display the most common start hour
    i_start_hour=df['Start Time'].dt.hour.mode()[0]
    print('The most common starthour is : {} a clock '.format(i_start_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*55)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print('################# STATION STATISTICS ###################\n')
    print('\nCalculating The Most Popular Stations and Trip........\n')
    start_time = time.time()

# display most commonly used start station
    s_pop_srt_stn=df['Start Station'].mode()
    print('Most common used start station is : {} '.format(s_pop_srt_stn[0]))

# display most commonly used end station

    s_pop_stp_stn=df['End Station'].mode()
    print('Most common used end station is : {} '.format(s_pop_stp_stn[0]))
# display most frequent combination of start station and end station trip

    print('Most popular combination of start and stop station is : {} , with {} number of occurances '.format(df[['Start Station','End Station']].value_counts().index[0],df[['Start Station','End Station']].value_counts()[0]))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*55)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    print('################# DURATION STATISTICS ###################\n')
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    sum_trv_tme=df['Trip Duration'].sum()
    print('Total traveltime is {} seconds or {} hours '.format(sum_trv_tme,round(sum_trv_tme/360,1)))


    # display mean travel time
    mean_trv_time=df['Trip Duration'].mean()
    print('Mean traveltime is {} seconds or {} minutes '.format( mean_trv_time,round(mean_trv_time/60,2)))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*55)


def user_stats(df):
    """Displays statistics on bikeshare users."""
    print('################### USER STATISTICS #####################\n')
    print('\nCalculating User Stats...\n')
    start_time = time.time()
# Display counts of user types
    num_of_usr=df['User Type'].value_counts(dropna=True)
    print('Number of users by category :')

    for i in range(0,len(num_of_usr),1):
       print('User type : {}  : {} '.format(num_of_usr.index[i],num_of_usr[i]))

# Display counts of gender
    if 'Gender' in df:
#check if there is a Gender column
        g_counts=df['Gender'].value_counts(dropna=True)
        print('Number of Males : {} \n Number of Females: {} '.format(g_counts['Male'],g_counts['Female']))
    else:
        print('Gender data is not in this dataframe')

# Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        #check if Birthyear is in dataframe
        e_date=df['Birth Year'].min()
        str_edt=str(e_date)[0:-2]
        print('Oldest user born in year : {} '.format(str_edt))

# Most recent
        r_date=df['Birth Year'].max()
        str_rdt=str(r_date)[0:-2]
        print('Youngest user born in year : {} '.format(str_rdt))

#Most common date of birth:
        c_d_birth=df['Birth Year'].mode()[0]
        str_cdt=str(c_d_birth)[0:-2]
        print('Most common date of birth : {} '.format(str_cdt))
    else:
        print('Birth year data is not in dataframe')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
            print('-'*60)
            print('Hello! Let\'s explore some US bikeshare data!')
            print('-'*60)

            city, month,day =get_filters()
            df = load_data(city, month, day)
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)
            loop_raw_data(df)
            restart = input('\nWould you like to restart? Enter yes or no.\n')
            if restart.lower() != 'yes':
                break


if __name__ == "__main__":
	main()
