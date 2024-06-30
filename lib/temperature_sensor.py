import machine
import dht

def get_temperature_and_humidity():
    temp_sensor = dht.DHT11(machine.Pin(27))
    temp_sensor.measure()
    temperature = temp_sensor.temperature()
    humidity = temp_sensor.humidity()
    return temperature, humidity