import requests

def get_melbourne_time():
    try:
        response = requests.get("https://timeapi.io/api/Time/current/zone?timeZone=Australia/Melbourne")
        if response.status_code == 200:
            data = response.json()
            melbourne_time = data.get("dateTime")
            if melbourne_time:
                # Extract the time part from the datetime string
                date_part, time_part = melbourne_time.split('T')
                time_str = time_part.split('.')[0]  # HH:MM:SS (ignore milliseconds if present)
                return time_str
            else:
                print("Time data not found in the response.")
                return None
        else:
            print("Failed to fetch Melbourne time. Status code:", response.status_code)
            return None
    except Exception as e:
        print("Error fetching Melbourne time:", e)
        return None

def get_melbourne_date():
    try:
        response = requests.get("https://timeapi.io/api/Time/current/zone?timeZone=Australia/Melbourne")
        if response.status_code == 200:
            data = response.json()
            melbourne_date = data.get("dateTime")
            if melbourne_date:
                # Extract the date part (yyyy-mm-dd) from the datetime string
                date_part = melbourne_date.split("T")[0]
                year, month, day = map(int, date_part.split("-"))
                return year, month, day
    except Exception as e:
        print('Error:', e)
    return None, None, None

# Fetch the date and store in variables
year, month, day = get_melbourne_date()

# Print the variables to verify
if year is not None:
    print("Year:", year)
    print("Month:", month)
    print("Day:", day)
else:
    print("Failed to fetch the date.")