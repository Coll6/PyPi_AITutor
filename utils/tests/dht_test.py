import sys
import os
#import RPi.GPIO as GPIO
#print("Current sys.path:")
#for path in sys.path:
#	print(path)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
#print("Current sys.path2:")
#for path in sys.path:
#        print(path)
from utils.sensors.dht11_interface import DHTSensor

def dht_test():
	#Instantiate DHTSensor object using pi GPIO 17 here
	sensor = DHTSensor(pin=17)
	
	#Read the sensor data
	success, temperature, humidity, error_message = sensor.read_sensor_data()

	#Display read data
	if success:
		#{:.if} placeholder string replaced with arg floating point number to one decimal
		print("Temperature: {:.1f}°C".format(temperature))
		print("Humidity: {:.1f}%".format(humidity))
	else:
		print(f"{error_message}")
if __name__ == "__main__":
	dht_test()
