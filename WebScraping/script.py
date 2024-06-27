# %%
"""
## Webscraping from Kayak.com
"""

# %%
"""
### Importing libraries and initializing Firefox driver
"""

# %%
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
driver = webdriver.Firefox()
import time

# %%
"""
### Initializing data structures for airports and dates
"""

# %%
airports_dict = {} # this dictionary will have IATA codes as key and city as name
dates_list = [] # this list will have dates to be looked for, for each flight line

# %%
"""
### Getting IATA codes and city for each airport from airports.txt
"""

# %%
def get_airports():
    with open("./airports.txt") as airports:
        for line in airports:
            data = line.split(':')
            airports_dict[data[0]] = data[1].strip()
    airports_list = list(airports_dict.keys())
    return airports_list

# %%
"""
### Getting dates list to be looked for from dates.txt
"""

# %%
def get_dates():
    dates_list = []
    with open("dates.txt") as dates:
        for line in dates:
            dates_list.append(line.strip())
        return dates_list

# %%
"""
### Initializing scraping variables
"""

# %%
base = 'https://www.kayak.com' # Base URL to be scraped
fin = '?sort=bestflight_a' # Final part of URL to be scraped
df_list = [] # List of dataframes, one per each webpage scraped

# %%
"""
### Overcoming cookies request
"""

# %%
def click_cookies():
    """
    Pushes the first option in cookies consent request
    :return: None.
    """
    cookie_btn = driver.find_elements(By.XPATH, "//p[contains(@class, 'fC_s-statement')]")
    if len(cookie_btn) > 0:
        driver.find_element(By.XPATH, "//button[contains(@class, 'RxNS')]").click()
        driver.implicitly_wait(3)

# %%
"""
### Definition of web scraping functions
"""

# %%
def push_more_results():
    """
    Pushes the "Show more results" button if it exists.
    :return: None.
    """
    show_more_btn = driver.find_elements(By.XPATH, "//div[contains(@class, 'show-more-button')]")
    if len(show_more_btn) > 0:
        show_more_btn[0].click()
        driver.implicitly_wait(3)

# %%
def get_prices_results(carriers, dep_hour, arr_hour, duration, price):
    """
    Given the web page the driver is pointing to, collects all the information for each 
    flight in the page and returns it in a list of lists.
    :param carriers: list of carriers
    :param dep_hour: list of departure hours
    :param arr_hour: list of arrival hours
    :param duration: list of durations
    :param price: list of prices
    :return: updated lists containing all the information for each flight in the page.
    """
    hours_carriers = driver.find_elements(By.XPATH, "//div[@class='VY2U']") # Finds flight hours and carrier for each flight card in the webpage
    for elem in hours_carriers: # For each web element in the list gets their children, containing information, and adds it to their corresponding lists
        children = elem.find_elements(By.XPATH, ".//*") 
        carriers.append(children[len(children)-1].text)
        hours = children[0].text.split('–')
        dep_hour.append(hours[0])
        arr_hour.append(hours[1])
        
    duration_elem = driver.find_elements(By.XPATH, "//div[@class='xdW8']") # Repeats same thing than before but with flight duration
    for elem in duration_elem:
        dur = elem.find_elements(By.XPATH, ".//*")
        duration.append(dur[0].text)        
        
    price_elem = driver.find_elements(By.XPATH, "//div[@class='f8F1-price-text']") # Repeats same thing than before but with flight price
    for elem in price_elem:
        price.append(elem.text)
    return carriers, dep_hour, arr_hour, duration, price # Returns updated lists with new information

# %%
def load_data(carriers, dep_hour, arr_hour, duration, price):
    """
    With the driver pointing to the webpage with all flight availabilities, pushes 5 times "Show more results" button and,
    invoking get_prices_results function, returns updated lists with flights informations.
    :param carriers: list of carriers
    :param dep_hour: list of departure hours
    :param arr_hour: list of arrival hours
    :param duration: list of durations
    :param price: list of prices
    :return: updated lists containing all the information for each flight in the page.
    """
    for i in range(5):
        push_more_results()
    return get_prices_results(carriers, dep_hour, arr_hour, duration, price)

# %%
def format_col(data):
    """
    Given a time string in a 12-hour format, returns it in a 24-hour format 
    :param data: The time string
    :return: The 24-hour formatted time string
    """
    split = data.split()
    hours_min, period = data.split()
    hours, min = hours_min.split(':')
    if period.lower() == 'pm' and int(hours) != 12:
        hours = str(int(hours) + 12)
    
    if period.lower() == 'am' and int(hours) == 12:
        hours = '00'
    
    return f"{hours}:{min}"
    

# %%
def handle_df(df):
    """
    Given the dataframe scraped from the webpage, adds DayAfter column and modifies ArrTime and DepTime ones and returns it.
    :param df: the web scraped dataframe
    :return: the dataframe updated with modified columns
    """
    # Adds DayAfter column, True if the arrival date is the day after the departure, false otherwise
    # this is done looking at the '\n' character, representing the eventual day after arrival date
    df['DayAfter'] = df['ArrTime'].str.contains('\n') 
    
    # Removes the eventual '\n+1' character at the end of the ArrTime data
    df['ArrTime'] = df['ArrTime'].str.replace('\n+1', '')
    
    # Formats DepTime and ArrTime into 24-hours format
    df['DepTime'] = df['DepTime'].apply(format_col)
    df['ArrTime'] = df['ArrTime'].apply(format_col)
    return df

# %%
def get_webpage(dep_airport, arr_airport, dep_date):
    """
    Gets the webpage to scrape, invokes function to load data, handle dataframes and to append each df to the corresponding list
    :param dep_airport: Departure airport string
    :param arr_airport: Arrival airport string
    :param dep_date: Departure date string
    :return: None.
    """
    
    # Gets the correct url by joining all informations needed and waits to overcome cookies request and to stabilize the webpage
    url = f'{base}/flights/{dep_airport}-{arr_airport}/{dep_date}{fin}'
    driver.get(url)
    time.sleep(5)
    click_cookies()
    print(url)
    
    # Initializes data structures to be filled with data
    carriers = [] # list of flight carriers
    dep_hour = [] # list of flight departure hours
    arr_hour = [] # list of flight arrival hours
    price = [] # list of flight prices
    duration = [] # list of flight durations
    
    # Loads data from the webpage and updates data structures given
    carriers, dep_hour, arr_hour, duration, price = load_data(carriers, dep_hour, arr_hour, duration, price)
    
    # Creates a DataFrame with the information in the 5 lists defined and filled before and fills Day, DepAirport and ArrAirport
    # with information common to each row
    data = {'Carrier': carriers, 'DepTime': dep_hour, 'ArrTime': arr_hour, 'Price': price, 'Duration': duration}
    df = pd.DataFrame(data)
    df['Day'] = dep_date
    df['DepAirport'] = airports_dict[dep_airport]
    df['ArrAirport'] = airports_dict[arr_airport]
    
    # Handles the data frame and appends it to the dataframe list
    df = handle_df(df)
    df_list.append(df)


# %%
"""
### Invoking static resources functions
"""

# %%
# Fills airports_list with airports and dates_list with dates invoking functions defined above
airports_list = get_airports()
dates_list = get_dates()

# %%
"""
### Defining of main loop function
"""

# %%
def main_loop():
    """
    Handles the main loop function, with three nested loops. First for loops on the list of airports and 
    gets the departure airport, median one loops again on the same list and gets the arrival airport, Last one loops 
    on the dates list and gets the departure date. For each combination of these three params, invokes function handling 
    the whole retrieving algorithm.
    :return: None.
    """    
    # Due to Kayak.com anti-bot policy, after a certain number of consequent calls, CAPTCHA to be solved will appear instead
    # of the webpage. Therefore, we need to split the process in many steps (one run for each departure airport, for half of the arrival airports, 
    # for all dates given) in order to avoid this problem.
    for dep in airports_list:
    # dep = airports_list[0]
        for id2, arr in enumerate(airports_list):
            for id3, date in enumerate(dates_list):
                if dep == arr:
                    continue
                else:
                    print(dep, arr, date)
                    get_webpage(dep, arr, date)        
                    
                

# %%
"""
### Executing main loop function
"""

# %%
main_loop()

# %%
"""
### Creating final DataFrame
"""

# %%
# Final DataFrame is created joining all dataframes in df_list together
joined_df = pd.concat(df_list)

# %%
# Brief inspection of final DataFrame
joined_df.head()

# %%
"""
### Saving final DataFrame
"""

# %%
joined_df.to_csv('dublin.csv', index=False)