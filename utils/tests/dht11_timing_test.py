import RPi.GPIO as GPIO
import time

pin=17
pulse_start_time_ns = None
pulse_lengths = []

def inited():
	print("pin startup")
	GPIO.setmode(GPIO.BCM)
def start_com():
	GPIO.setup(pin, GPIO.OUT)
	GPIO.output(pin, GPIO.HIGH)
	print(f"Starting communication.{time.perf_counter_ns()}")
	GPIO.output(pin, GPIO.LOW)
	time.sleep(0.018) #Sleep for 18ms
def poll_for_pulses():
	global pulse_start_time_ns, pulse_lengths
	print(f"Starting Read.{time.perf_counter_ns()}")
	GPIO.setup(pin, GPIO.IN)

	while True:
		current_state = GPIO.input(pin)
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
			print("Read done.")
			break
if __name__ == "__main__":
	inited()
	start_com()
	poll_for_pulses()
	print("Pulse lengths (in microseconds?):")
	for i, length in enumerate(pulse_lengths):
		print(f"Pulse {i + 1}: {length / 1000} microseconds.")
	GPIO.cleanup()
