#Works with DHT11
#https://www.mouser.com/datasheet/2/758/DHT11-Technical-Data-Sheet-Translated-Version-1143054.pdf

#might be able to remove time later
import time
import RPi.GPIO as GPIO

class DHTSensor:
	def __init__(self, pin):
		self.pin = pin
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(self.pin, GPIO.OUT)
		GPIO.output(self.pin, GPIO.HIGH)
	def start_com(self):
		#Starting communication with DHT.
		GPIO.output(self.pin, GPIO.LOW) #Pull line low
		time.sleep(0.018) #Wait for DHT to accept signal
	def start_read(self):
		pulse_start_time_ns = None
		pulse_lengths = []
		
		print("Starting read")
		GPIO.setup(self.pin, GPIO.IN)

		while True:
			current_state = GPIO.input(self.pin)
			cur_time = time.perf_counter_ns()

			if current_state == GPIO.HIGH:
				if pulse_start_time_ns is None:
					pulse_start_time_ns = cur_time
			else:
				if pulse_start_time_ns is not None:
					pulse_length = cur_time - pulse_start_time_ns
					pulse_lengths.append(pulse_length)
					pulse_start_time_ns = None
			if pulse_start_time_ns is not None and (cur_time - pulse_start_time_ns) >= 100000:
				print( "Read done.")
				GPIO.setup(self.pin, GPIO.OUT)
				GPIO.output(self.pin, GPIO.HIGH)
				return pulse_lengths
	def process_stream(self , list):
		buffer = bytearray(5)
		for i, length in enumerate(list[1:]):
#			print(f"bit: {i + 1} and {length}")
			bit_value = 1 if length >= 30000 else 0

			#Calculate bit and byte position
			byte_index = i // 8
			bit_index = 7 - (i % 8)

			if bit_value == 1:
				buffer[byte_index] |= (1 << bit_index)
			else:
				buffer[byte_index] &= ~(1 << bit_index)

#		print(' '.join(str(byte) for byte in buffer))
		return buffer
	def read_sensor_data(self):
		self.start_com()
		pls_lng = self.start_read()
		proc_stream = self.process_stream(pls_lng)
		#Place holder error handling
		success = False
		error_message = ""

		#Placeholder variables initialized to 0 decimals as temp/humid  56.4F etc
		temp = 0.0
		humid = 0.0
		
		if not (sum(proc_stream[:4]) == proc_stream[4]):
			success = False
			error_message = "Data not read properly. Checksum Failure"
			#print(f"{proc_stream[0] + proc_stream[1] + proc_stream[2] + proc_stream[3]}={proc_stream[4]}")
		else:
			temp = proc_stream[2] + (proc_stream[3] / 10.0) #temp reading not sensitive enough for decimals but testing suggests adding it.
			humid = proc_stream[0]
			success = True
		print("Proc Stream:", ' '.join(f'0x{byte:02X}' for byte in proc_stream))
		print("Proc Stream:", ' '.join(str(byte) for byte in proc_stream))
		print(f"F: {temp * (9/5) + 32}")
		#Simulate Sensor data for testing before implementing sensor
		#time.sleep(2) #Simulate sensor response time. Read Datasheet
		#temp = 25.0 #Simulate temp reading
		#humid = 50.0 #Simulate Humid reading
		#success = True
	
		return success, temp, humid, error_message
