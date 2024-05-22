import RPi.GPIO as GPIO
import time

#GPIO setup
input_pin = 17 #Define pin to be read.
output_pin = 27 #Dine pin to be output

def setup_gpio():
	GPIO.setmode(GPIO.BCM) #Sets the pin labeling mode. 
	GPIO.setup(input_pin, GPIO.IN) #Sets the pin defined as input
	GPIO.setup(output_pin, GPIO.OUT) #Sets the pin defined as output

def test_gpio():
	#Loops the read and output 10 times _ is a placeholder variable
	for _ in range(10): 
		state = GPIO.input(input_pin)
		GPIO.output(output_pin, state)
		print(f"Input pin state: {state}")
		time.sleep(1) #Wait 1 second before the next read

def cleanup_gpio():
	GPIO.cleanup()

if __name__ == "__main__":
	try:
		setup_gpio()
		test_gpio()
	finally:
		cleanup_gpio()
