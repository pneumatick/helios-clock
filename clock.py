from datetime import datetime, timedelta
from math import floor, modf
import requests

# Geolocation and time data (sample data for now)
lat = 41.695228
long = -71.453311
date = "today"
tz = "America/New_York"

# Set up URL
url = f"https://api.sunrise-sunset.org/json?lat={lat}8&lng={long}&date={date}&tzid={tz}"

# Get data from API
response = requests.get(url).json()

# Get the length of the 12 hours of the day
length_format = "%H:%M:%S"
day_length = datetime.strptime(response["results"]["day_length"], length_format)
day_delta = timedelta(hours=day_length.hour,
                      minutes=day_length.minute,
                      seconds=day_length.second)
hour_length = day_delta.total_seconds() / 60 / 12
seconds_in_hour = round(modf(hour_length)[0] * 60, 2)
hour_delta = timedelta(minutes=hour_length)

# Get sunrise and sunset times
dt_format = "%H:%M:%S %p"
sunrise = response["results"]["sunrise"]
formatted_sunrise = datetime.strptime(sunrise, dt_format)
sunrise_delta = timedelta(hours=formatted_sunrise.hour,
                          minutes=formatted_sunrise.minute,
                          seconds=formatted_sunrise.second)

sunset = response["results"]["sunset"]
formatted_sunset = datetime.strptime(sunset, dt_format)
sunset_delta = timedelta(hours=formatted_sunset.hour,
                          minutes=formatted_sunset.minute,
                          seconds=formatted_sunset.second)

# Get day of week as int (Monday = 0, Sunday = 6)
weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
greekdays = ["Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Sun"]
day_symbols = ["☾", "♂", "☿", "♃",  "♀", "♄", "☉"]
dt_now = datetime.now()
day_of_week = dt_now.isoweekday() - 1
day_of_week_str = dt_now.strftime("%A")

# Set up planet-hour table (starting from Monday)
planet_hours = ["Moon", "Saturn", "Jupiter", "Mars", "Sun", "Venus", "Mercury"] 
planet_symbols = ["☾", "♄", "♃", "♂", "☉", "♀", "☿"]

# Create function to convert timedelta to 12-hour datetime format for ease
# of display
def delta_to_ampm(delta): 
    return (datetime.min + delta).strftime('%I:%M:%S %p')

# Print informaton
print(f"Today is {weekdays[day_of_week]}: Day of {greekdays[day_of_week]} {day_symbols[day_of_week]}\n")
print(f"Length of today's hours: {floor(hour_length)} minutes, {seconds_in_hour} seconds")
print(f"Sunrise: {formatted_sunrise.time()} AM")
print(f"Sunset: {formatted_sunset.time()} PM")
print()
for i in range(12):
    print("Hour {0:<5} {1:<1} {2:<8} : {3} - {4}".format(
          i + 1,
          planet_symbols[(day_of_week * 24 + i) % len(planet_symbols)],
          planet_hours[(day_of_week * 24 + i) % len(planet_hours)],
          delta_to_ampm(sunrise_delta + hour_delta * i),
          delta_to_ampm(sunrise_delta + hour_delta * (i + 1))))

