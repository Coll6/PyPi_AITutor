import RPi.GPIO as GPIO
import time

pin=17
pulse_start_time_ns = None
pulse_lengths = []

def inited():
	print("pin startup")
	GPIO.setmode(GPIO.BCM)
def start_com():
	print("Starting communication.")
	GPIO.setup(pin, GPIO.OUT)
	GPIO.output(pin, GPIO.HIGH)
#	GPIO.add_event_detect(pin, GPIO.BOTH, callback=detected_edge)

	GPIO.output(pin, GPIO.LOW)
	time.sleep(0.018) #sleep 18ms
	GPIO.setup(pin,GPIO.IN)
	GPIO.add_event_detect(pin,GPIO.BOTH,callback=detected_edge)
def detected_edge(channel):
	global pulse_start_time_ns, pulse_lengths
	cur_time = time.time() * 1_000_000
	if GPIO.input(17) == GPIO.HIGH:
		if pulse_start_time_ns is None:
			print(f"low to high: {time.time()}")
			pulse_start_time_ns = cur_time
	else:
		#print("High to low")
		if pulse_start_time_ns is not None:
			print("High to low")
			pulse_length = cur_time - pulse_start_time_ns
			pulse_lengths.append(pulse_length)
			pulse_start_time_ns = None
#def read():
#	GPIO.setup(pin, GPIO.IN)
#	GPIO.add_event_detect(pin, GPIO.BOTH, callback=detected_edge)
if __name__ == "__main__":
	inited()
	start_com()
#	read()
	time.sleep(2)
	GPIO.remove_event_detect(pin)
	print("Finished read")
	for length in pulse_lengths:
		print(f"Pulse Length: {length:.2f} us")
	GPIO.cleanup()
