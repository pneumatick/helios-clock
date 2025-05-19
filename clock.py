import math
import requests
from datetime import datetime, timedelta

weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
greekdays = ["Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Sun"]
day_symbols = ["☾", "♂", "☿", "♃",  "♀", "♄", "☉"]
# Planet-hour table (starting from Monday)
planet_hours = ["Moon", "Saturn", "Jupiter", "Mars", "Sun", "Venus", "Mercury"] 
planet_symbols = ["☾", "♄", "♃", "♂", "☉", "♀", "☿"]

# Geolocation and time data (sample data for now)
lat = 41.695228
long = -71.453311
tz = "America/New_York"

# Get data from sunrise-sunset API for a given location
def get_api_data(lat, long, date, tz):
    # Set up URL
    url = f"https://api.sunrise-sunset.org/json?lat={lat}8&lng={long}&date={date}&tzid={tz}"

    # Get data from API
    return requests.get(url).json()

# Get a time delta from a time string given some format
def get_time_delta(time_str, dt_format):
    formatted_time = datetime.strptime(time_str, dt_format)
    time_delta = timedelta(hours=formatted_time.hour,
                           minutes=formatted_time.minute,
                           seconds=formatted_time.second)
    return time_delta

# Get today and tomorrow's data from API
today_res = get_api_data(lat, long, "today", tz) 
tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
tom_res = get_api_data(lat, long, tomorrow, tz)

# Get the length of the 12 hours of the day
length_format = "%H:%M:%S"
day_length = datetime.strptime(today_res["results"]["day_length"], length_format)
day_delta = timedelta(hours=day_length.hour,
                      minutes=day_length.minute,
                      seconds=day_length.second)
hour_length = day_delta.total_seconds() / 60 / 12
seconds_in_hour = round(math.modf(hour_length)[0] * 60, 2)
hour_delta = timedelta(minutes=hour_length)

# Get sunrise and sunset times
dt_format = "%H:%M:%S %p"
sunrise = today_res["results"]["sunrise"]
sunrise_delta = get_time_delta(sunrise, dt_format)
sunset = today_res["results"]["sunset"]
sunset_delta = get_time_delta(sunset, dt_format)

# Get tomorrow's sunrise time to calculate tonight's night hours
tom_sunrise = tom_res["results"]["sunrise"]
tom_sunrise_delta = get_time_delta(tom_sunrise, dt_format)


# Get day of week as int (Monday = 0, Sunday = 6)
dt_now = datetime.now()
day_of_week = dt_now.isoweekday() - 1
day_of_week_str = dt_now.strftime("%A")

# Create function to convert timedelta to 12-hour datetime format for ease
# of display
def delta_to_ampm(delta): 
    return (datetime.min + delta).strftime('%I:%M:%S %p')

# Print informaton
print(f"Today is {weekdays[day_of_week]}: Day of {greekdays[day_of_week]} {day_symbols[day_of_week]}\n")
print(f"Length of today's hours: {math.floor(hour_length)} minutes, {seconds_in_hour} seconds")
print(f"Sunrise: {sunrise}")
print(f"Sunset: {sunset}")
print("\nDay Hours\n")
for i in range(12):
    print("Hour {0:<5} {1:<1} {2:<8} : {3} - {4}".format(
          i + 1,
          planet_symbols[(day_of_week * 24 + i) % len(planet_symbols)],
          planet_hours[(day_of_week * 24 + i) % len(planet_hours)],
          delta_to_ampm(sunrise_delta + hour_delta * i),
          delta_to_ampm(sunrise_delta + hour_delta * (i + 1))))

print("\nNight Hours\n")
