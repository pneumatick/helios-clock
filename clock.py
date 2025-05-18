from datetime import datetime, timedelta
import requests

# Global coordinates
lat = 41.7042
long = -71.4558

# Get data from API
response = requests.get('https://api.sunrise-sunset.org/json?lat=41.695228&lng=-71.453311&date=today&tzid=America/New_York').json()

# Get the length of the 12 hours of the day
length_format = "%H:%M:%S"
day_length = datetime.strptime(response["results"]["day_length"], length_format)
day_delta = timedelta(hours=day_length.hour,
                      minutes=day_length.minute,
                      seconds=day_length.second)
hour_length = day_delta.total_seconds() / 60 / 12
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
dt_now = datetime.now()
day_of_week = dt_now.isoweekday() - 1
day_of_week_str = dt_now.strftime("%A")

# Set up planet-hour table (starting from Monday)
planet_hours = ["Moon", "Saturn", "Jupiter", "Mars", "Sun", "Venus", "Mercury"] 

# Print informaton
print(f"Today is {weekdays[day_of_week]}: Day of {greekdays[day_of_week]}")
print(f"Length of today's hours: {hour_length} minutes")
print(f"Sunrise: {formatted_sunrise.time()} AM")
print(f"Sunset: {formatted_sunset.time()} PM")
print("\nHour table\n")
for i in range(12):
    print("Hour {}: {} - {}, Hour of {}".format(
        i + 1,
        sunrise_delta + hour_delta * i,
        sunrise_delta + hour_delta * (i + 1),
        planet_hours[(day_of_week * 24 + i) % len(planet_hours)]))

