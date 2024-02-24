"""
Title: Automate the Boring Stuff, Chapter 16, Project 2
Purpose: Takes the location of the user as a command line argument and prints out the hourly weather forecase for the next
24 hours
Author: drstrangelove4
"""

from dotenv import load_dotenv
import requests
import sys
import os

# Load enviroment variables
load_dotenv()

# Set the API Key as an enviroment variable or just let API_KEY = '<your_api_key_here>'
API_KEY = os.environ["API_KEY"]
URL = "http://api.weatherapi.com/v1/forecast.json"


# -----------------------------------------------------------------------------------------------------------------------


def error_check(code, variable):
    """
    Raises an Exception if we encounter an error.
    """
    if code == 1:
        raise Exception(f"There was an error: {variable}")


# -----------------------------------------------------------------------------------------------------------------------


def print_data(weather_data):
    """
    This function takes weather data as an input, pulls relevant info for the user and displays it in the console.
    """

    print("Weather status for the next 24 hours:")
    print("-------------------------------------")
    time = 0
    if weather_data:

        # Loops over data and pulls out a English readable forecast from the large amount of data.
        for hour in weather_data["forecast"]["forecastday"][0]["hour"]:
            weather_condition = hour["condition"]["text"]
            if time != 0:
                print(f"In {time} hours: {weather_condition}")
            else:
                print(f"Now: {weather_condition}")

            time += 1

        # Return blank string and success code if the task was performed.
        return "", 0

    # Return a error message and code if no data is provided to the function.
    return "No data provided", 1


# -----------------------------------------------------------------------------------------------------------------------


def get_location():
    """
    Looks at the arguments passed to this program and builds a location input from the arguments. If there are no arguments
    then it returns what we will use as an error code and an error message, else it returns a string.
    """
    location_input = ""

    # If a argument has been provided to the script then build a location value from it.
    if len(sys.argv) > 1:
        for x in range(len(sys.argv)):
            if x != 0:
                location_input += sys.argv[x] + " "

        return location_input, 0

    return "No location given", 1


# -----------------------------------------------------------------------------------------------------------------------


def get_data(url, parameters):
    """
    Takes a string URL and dictionary of parameters as input and returns an status code and either json file/error message.
    """
    # Makes a request for data from the weather API provider. This will deal with errors using its inbuilt error handling
    # method instead of our own.
    response = requests.get(url=url, params=parameters)
    response.raise_for_status()

    return response.json()


# -----------------------------------------------------------------------------------------------------------------------


def main():

    # Take location from command line arguments and error checking.
    location_return, return_code = get_location()
    error_check(return_code, location_return)

    # Build parameters for API request:
    parameters = {
        "key": API_KEY,
        "q": location_return,
        "days": 1,
    }

    # Attempt to get data from API
    json_data = get_data(url=URL, parameters=parameters)

    # Display the data to the user in a readable way.
    print_data_return, return_code = print_data(json_data)
    error_check(return_code, print_data_return)


# -----------------------------------------------------------------------------------------------------------------------


if __name__ == "__main__":
    main()
