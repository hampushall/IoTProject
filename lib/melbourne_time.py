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
                print(melbourne_date)
    except Exception as e:
        print('Error', e)
        return None