import utime
from machine import Pin
from time import sleep
from melbourne_time import get_melbourne_time, get_melbourne_date
from sunrise_sunset import get_sunrise_sunset
from temperature_sensor import get_temperature_and_humidity
import machine
from mqtt import MQTTClient
import ubinascii

AIO_SERVER = "io.adafruit.com"
AIO_PORT = 1883
AIO_USER = "hampushall"
AIO_KEY = "aio_gMNV42JVsjl1jaRqQlnR4Y26qVjd"
AIO_CLIENT_ID = ubinascii.hexlify(machine.unique_id())
AIO_DAYTIME_LED_FEED = "hampushall/feeds/daytimeled"
AIO_CURRENT_TIME_FEED = "hampushall/feeds/current-time"
AIO_DAYSUNTIL_FEED = "hampushall/feeds/daysuntil"
AIO_HUMIDITY_FEED = "hampushall/feeds/humidity"
AIO_TEMPERATURE_FEED = "hampushall/feeds/temperature"

def count_days():
    rtc = machine.RTC()
    rtc.datetime((2024, 6, 28, 0, 13, 38, 0, 0))  # (year, month, day, weekday, hour, minute, second, millisecond)
    current_time = rtc.datetime()
    current_year = current_time[0]
    current_month = current_time[1]
    current_day = current_time[2]

    target_year = 2024
    target_month = 12
    target_day = 12

    days_current = utime.mktime((current_year, current_month, current_day, 0, 0, 0, 0, 0)) // (24 * 3600)
    days_target = utime.mktime((target_year, target_month, target_day, 0, 0, 0, 0, 0)) // (24 * 3600)

    days_until_target = days_target - days_current
    print(current_time)
    return days_until_target

client = MQTTClient(AIO_CLIENT_ID, AIO_SERVER, AIO_PORT, AIO_USER, AIO_KEY)

def connect_to_adafruit():
    try:
        client.connect()
    except Exception as e:
        raise e

ledGreen = Pin(16, Pin.OUT)
ledRed = Pin(17, Pin.OUT)

last_sent_ticks = utime.ticks_ms()
SEND_INTERVAL = 60000  # 60 seconds
last_fetch_date = None

try:
    connect_to_adafruit()
    while True:
        client.check_msg()
        melbourne_time = get_melbourne_time()
        current_date = utime.localtime()[2]
        print(get_melbourne_date())

        if last_fetch_date != current_date:
            sunrise, sunset = get_sunrise_sunset()
            last_fetch_date = current_date

        if melbourne_time and sunrise and sunset:
            days_until_home = count_days()
            client.publish(topic=AIO_CURRENT_TIME_FEED, msg=str(melbourne_time))
            client.publish(topic=AIO_DAYSUNTIL_FEED, msg=str(days_until_home))
            print('Sunrise is: ', sunrise)
            print('Sunset is: ', sunset)
            print('Current time: ', melbourne_time)
            
            if sunrise <= melbourne_time <= sunset:
                ledGreen.on()
                ledRed.off()
                client.publish(topic=AIO_DAYTIME_LED_FEED, msg="1")
            else:
                ledGreen.off()
                ledRed.on()
                client.publish(topic=AIO_DAYTIME_LED_FEED, msg="2")

            temperature, humidity = get_temperature_and_humidity()
            client.publish(topic=AIO_HUMIDITY_FEED, msg=str(humidity))
            client.publish(topic=AIO_TEMPERATURE_FEED, msg=str(temperature))
        sleep(360)
finally:
    client.disconnect()
