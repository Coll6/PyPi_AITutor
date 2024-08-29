#Works with DHT11
#https://www.mouser.com/datasheet/2/758/DHT11-Technical-Data-Sheet-Translated-Version-1143054.pdf

#might be able to remove time later
import time
import RPi.GPIO as GPIO

class DHTSensor:
	def __init__(self, pin):
		self.pin = pin
		GPIO.setmode(GPIO.BCM)

	def read_sensor_data(self):
		#Some function or "method" to talk to the DHT
		#Starting communication.
#		GPIO.output(self.pin, GPIO.HIGH)
		GPIO.setup(self.pin, GPIO.OUT)
		GPIO.output(self.pin, GPIO.HIGH)

		GPIO.output(self.pin, GPIO.LOW)
		time.sleep(0.018)
		GPIO.output(self.pin, GPIO.HIGH)

		#Placeholder variables initialized to 0 decimals as temp/humid  56.4F etc
		temp = 0.0
		humid = 0.0

		#Place holder error handling
		success = False
		error_message = ""

		#Simulate Sensor data for testing before implementing sensor
		time.sleep(2) #Simulate sensor response time. Read Datasheet
		temp = 25.0 #Simulate temp reading
		humid = 50.0 #Simulate Humid reading
		success = True
	
		return success, temp, humid, error_message
