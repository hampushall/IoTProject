import requests

def add_hours_to_time(time_str, hours):
    try:
        date_part, time_part = time_str.split('T')
        time_str = time_part[:8]  # HH:MM:SS
        hours_int, minutes, seconds = map(int, time_str.split(':'))
        hours_int += hours
        if hours_int >= 24:
            hours_int -= 24
        time_str = '{:02d}:{:02d}:{:02d}'.format(hours_int, minutes, seconds)
        return time_str
    except Exception as e:
        print("Error in add_hours_to_time:", e)
        return None

def get_sunrise_sunset():
    try:
        response = requests.get("https://api.sunrise-sunset.org/json?lat=-37.8136&lng=144.9631&formatted=0")
        if response.status_code == 200:
            data = response.json()
            sunrise_utc = data['results']['sunrise']
            sunset_utc = data['results']['sunset']
            sunrise = add_hours_to_time(sunrise_utc, 10)
            sunset = add_hours_to_time(sunset_utc, 10)
            return sunrise, sunset
        else:
            print("Failed to fetch sunrise/sunset time. Status code:", response.status_code)
            return None, None
    except Exception as e:
        print("Error fetching sunrise/sunset time:", e)
        return None, None