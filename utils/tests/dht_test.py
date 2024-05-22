from ..sensors.dht11_interface import DHTSensor

def dht_test():
	#Instantiate DHTSensor object using pi GPIO 17 here
	sensor = DHTSensor(pin=17)

	#Read the sensor data
	success, temperature, humidity, error_message = sensor.read_sensor_data()

	#Display read data
	if success:
		#{:.if} placeholder string replaced with arg floating point number to one decimal
		print("Temperature: {.if}°C".format(temperature))
		print("Humidity: {:.if} %".format(humidity))
	else:
		print("Failed to read sensor data")
if __name__ == "__main__":
	dht_test()
